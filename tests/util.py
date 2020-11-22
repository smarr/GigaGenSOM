def read_file(path, file_name):
    with open(str(path) + f"/{file_name}", "r") as output_file:
        return "".join(output_file.readlines())
