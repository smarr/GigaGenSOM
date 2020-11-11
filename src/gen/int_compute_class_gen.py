from random import Random

from som import object_system
from som.ast.basic import Literal, MsgSend, Return, Read
from som.clazz import Class
from som.method import Method


class IntegerComputationClassGenerator(object):
    """
    - generate k method, the based methods, with varying number of arguments
      that does basic arithmetics on integers
    - generate k-1 levels of methods, calling the methods of the previous layer,
      combining the results with varying basic arithmetics
    """

    def __init__(self, class_name, k):
        self._class_name = class_name
        self._k = k
        self._rand = Random(42)
        self._max_args = 4
        self._int_ops = ["+", "-", "*", "/", "%", "abs", "negated", "max:"]  #"rem:",
        self._unary_ops = ["abs", "negated"]

    def _generate_name_and_args(self, prefix, num_args):
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

    def _generate_base_method(self, index):
        num_args = self._rand.uniform(0, self._max_args)
        name, args = self._generate_name_and_args(f"base{index}", num_args)

        method = Method(name, args)

        remaining_args = args[:]
        self._rand.shuffle(remaining_args)
        expr_stack = []

        # produce expressions and consume the arguments
        while remaining_args:
            operation_i = self._rand.uniform(0, len(self._int_ops) - 1)
            op = self._int_ops[int(operation_i)]
            is_unary = op in self._unary_ops

            left = self._pick_operand(expr_stack, remaining_args)

            if is_unary:
                expr_stack.append(MsgSend(op, [left]))
            else:
                right = self._pick_operand(expr_stack, remaining_args)
                expr_stack.append(MsgSend(op, [left, right]))

        self._combine_expressions(expr_stack)

        method.add_statement(Return(expr_stack[0]))
        return method

    def _combine_expressions(self, expr_stack):
        while len(expr_stack) > 1:
            operation_i = self._rand.uniform(0, len(self._int_ops) - 1)
            op = self._int_ops[int(operation_i)]
            is_unary = op in self._unary_ops

            if not is_unary:
                expr = MsgSend(op, [expr_stack.pop(), expr_stack.pop()])
                expr_stack.append(expr)

    def _pick_operand(self, expr_stack, remaining_args):
        action = self._rand.uniform(0, 100)
        if action < 25 and expr_stack:
            return expr_stack.pop()
        elif action < 75 and remaining_args:
            if action > 65:
                return Read(remaining_args[-1])
            else:
                return Read(remaining_args.pop())
        else:
            return Literal(self._rand.randint(0, 10000))

    def _generate_method(self, target_methods, index):
        num_target_args = sum([t.get_num_arguments() for t in target_methods])
        num_args = self._rand.uniform(
            int(num_target_args / len(target_methods) / 2),
            int(num_target_args / len(target_methods)))
        name, args = self._generate_name_and_args(f"method{index}", num_args)

        method = Method(name, args)

        possible_args = []
        while len(possible_args) < num_target_args:
            args_arr = args[:]
            self._rand.shuffle(args_arr)
            possible_args += args_arr

        expr_stack = []

        self._construct_calls(expr_stack, method, possible_args, target_methods)
        return method

    def _construct_calls(self, expr_stack, method, possible_args, target_methods):
        for target in target_methods:
            call_args = [Read('self')]

            for _ in range(0, target.get_num_arguments()):
                call_args.append(self._pick_operand(expr_stack, possible_args))

            expr_stack.append(MsgSend(target.get_name(), call_args))
        self._combine_expressions(expr_stack)
        method.add_statement(Return(expr_stack[0]))

    def _generate_run_method(self, target_methods):
        method = Method("run")

        self._construct_calls([], method, [], target_methods)
        return method

    def serialize(self, target_directory):
        clazz = Class(self._class_name, object_system.Object, object_system.Empty)

        method_matrix = [[None] * self._k for _ in range(0, self._k)]

        for i in range(0, self._k):
            base_method = self._generate_base_method(i)
            method_matrix[0][i] = base_method
            clazz.add_method(base_method)

        method_i = 0
        for i in range(1, self._k):
            for j in range(0, self._k):
                method = self._generate_method(method_matrix[i - 1], method_i)
                clazz.add_method(method)
                method_matrix[i][j] = base_method
                method_i += 1

        clazz.add_method(self._generate_run_method(method_matrix[self._k - 1]))
        clazz.serialize(target_directory)
