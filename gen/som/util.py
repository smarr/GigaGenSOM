def combine_pattern_with_args(selector, args):
    result = ""
    name_parts = selector.split(":")
    for i in range(0, len(name_parts) - 1):
        if i > 0:
            result += " "
        result += f"{name_parts[i]}: {args[i]}"
    return result
