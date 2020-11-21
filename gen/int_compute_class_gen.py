from random import Random

from som import object_system
from som.ast.basic import Literal, MsgSend, Return, Read, Write
from som.clazz import Class
from som.method import Method


def generate_method_name_and_args(prefix, num_args):
    args = []
    name = prefix
    if num_args == 0:
        return name, args

    name += ":"
    num_args -= 1
    args.append("a")

    next_arg_i = 98  # magic number of lower-case b in ASCII

    while num_args > 0:
        name += chr(next_arg_i) + ":"
        args.append(chr(next_arg_i))
        num_args -= 1
        next_arg_i += 1

    return name, args


class IntegerComputationClassGenerator:  # pylint: disable=too-many-instance-attributes
    """
    - generate k method, the based methods, with varying number of arguments
      that does basic arithmetics on integers
    - generate k-1 levels of methods, calling the methods of the previous layer,
      combining the results with varying basic arithmetics
    """

    def __init__(self, class_name, call_stack_height, num_of_base_methods):
        self._class_name = class_name
        self._call_stack_height = call_stack_height
        self._num_of_base_methods = num_of_base_methods
        self._rand = Random(42)
        self._max_args = 4
        self._int_ops = [
            "+",
            "-",
            "*",
            "/",
            "%",
            "abs",
            "negated",
            "min:",
            "rem:",
            "as32BitSignedValue",
            "hashcode",
        ]  # "as32BitUnsignedValue",
        self._div_ops = ["/", "%", "rem:"]
        self._unary_ops = [
            "abs",
            "negated",
            "as32BitSignedValue",
            "hashcode",
        ]  # "as32BitUnsignedValue",

    def _generate_base_method(self, clazz, index):
        num_args = self._rand.uniform(0, self._max_args)
        name, args = generate_method_name_and_args(f"base{index}", num_args)

        method = Method(name, clazz, args)

        remaining_args = args[:]
        self._rand.shuffle(remaining_args)
        expr_stack = []

        # produce expressions and consume the arguments
        while remaining_args:
            is_unary, operation = self._determine_operation()

            left = self._pick_operand("", expr_stack, remaining_args)

            if is_unary:
                expr_stack.append(MsgSend(operation, [left]))
            else:
                right = self._pick_operand(operation, expr_stack, remaining_args)
                expr_stack.append(MsgSend(operation, [left, right]))

        self._combine_expressions(method, expr_stack)
        return method

    def _determine_operation(self, no_div=False):
        operation_i = self._rand.uniform(0, len(self._int_ops) - 1)
        operation = self._int_ops[int(operation_i)]

        if no_div:
            while operation in self._div_ops:
                operation_i = self._rand.uniform(0, len(self._int_ops) - 1)
                operation = self._int_ops[int(operation_i)]

        is_unary = operation in self._unary_ops
        return is_unary, operation

    def _combine_expressions(self, method, expr_stack):
        local = method.get_unused_local()
        write = Write(local, Literal(self._rand.randint(1, 10)))
        method.add_statement(write)

        while len(expr_stack) > 0:
            is_unary, operation = self._determine_operation(True)

            operands = [Read(local)]

            if not is_unary:
                operands.append(
                    self._add_constant_for_div_op(operation, expr_stack.pop())
                )

            expr = MsgSend(operation, operands)
            write = Write(local, expr)
            method.add_statement(write)

        method.add_statement(Return(Read(local)))

    def _add_constant_for_div_op(self, operation, expr):
        """
        This trick is borrowed from Gergö Barany's ldrgen
        Liveness-Driven Random Program Generation
        https://arxiv.org/abs/1709.04421
        """
        if operation in self._div_ops:
            return MsgSend("-", [expr, Literal(self._rand.randint(31, 63))])
        return expr

    def _pick_operand(self, operation, expr_stack, remaining_args):
        if operation in self._div_ops:
            use_expr_probability = 0
            use_arg_probability = 0
            consume_arg_probability = 0
            use_literal_probability = 100
        else:
            use_expr_probability = 25
            use_arg_probability = 10
            consume_arg_probability = 40
            use_literal_probability = 25
        assert (
            use_arg_probability
            + use_expr_probability
            + consume_arg_probability
            + use_literal_probability
        ) == 100

        action = self._rand.uniform(0, 100)
        if action < use_expr_probability and expr_stack:
            return self._add_constant_for_div_op(operation, expr_stack.pop())
        action -= use_expr_probability
        if action < use_arg_probability and remaining_args:
            return self._add_constant_for_div_op(operation, Read(remaining_args[-1]))
        action -= use_arg_probability
        if action < consume_arg_probability and remaining_args:
            return self._add_constant_for_div_op(operation, Read(remaining_args.pop()))
        action -= consume_arg_probability

        # we can't assert that action >= 0, because we may not have args to use
        assert action <= use_literal_probability

        return Literal(self._rand.randint(0, 1000))

    def _generate_method(self, clazz, target_methods, index):
        num_targets = self._rand.randint(1, 3)

        targets = [target_methods.pop()]
        while len(targets) < num_targets and target_methods:
            targets.append(
                target_methods[self._rand.randint(0, len(target_methods) - 1)]
            )

        num_target_args = sum([t.get_num_arguments() for t in targets])
        num_args = self._rand.uniform(
            int(num_target_args / len(targets) / 2),
            int(num_target_args / len(targets)),
        )
        name, args = generate_method_name_and_args(f"method{index}", num_args)

        method = Method(name, clazz, args)

        possible_args = []
        while len(possible_args) < num_target_args:
            args_arr = args[:]
            self._rand.shuffle(args_arr)
            possible_args += args_arr

        expr_stack = []

        self._construct_calls(expr_stack, possible_args, targets)
        self._combine_expressions(method, expr_stack)
        return method

    def _construct_calls(self, expr_stack, possible_args, target_methods):
        for target in target_methods:
            call_args = [Read("self")]

            for _ in range(0, target.get_num_arguments()):
                call_args.append(
                    self._pick_operand(target.get_name(), expr_stack, possible_args)
                )

            expr_stack.append(MsgSend(target.get_name(), call_args))

    def _generate_run_method(self, clazz, target_methods):
        method = Method("run", clazz)

        expr_stack = []
        self._construct_calls(expr_stack, [], target_methods)

        self._combine_expressions(method, expr_stack)
        clazz.add_method(method)
        return method

    def serialize(self, target_directory):
        clazz = Class(self._class_name, object_system.Object, object_system.Empty)

        method_matrix = [
            [None] * self._num_of_base_methods
            for _ in range(0, self._call_stack_height)
        ]

        for i in range(0, self._num_of_base_methods):
            base_method = self._generate_base_method(clazz, i)
            method_matrix[0][i] = base_method
            clazz.add_method(base_method)

        method_i = 0
        for i in range(1, self._call_stack_height):
            target_methods = method_matrix[i - 1][:]
            self._rand.shuffle(target_methods)
            for j in range(0, self._num_of_base_methods):
                method = self._generate_method(clazz, target_methods, method_i)
                clazz.add_method(method)
                method_matrix[i][j] = method
                method_i += 1

        self._generate_run_method(clazz, method_matrix[self._call_stack_height - 1])
        clazz.serialize(target_directory)
