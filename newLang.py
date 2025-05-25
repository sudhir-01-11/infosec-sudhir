import sys

class SimpleLangInterpreter:
    def execute_program(self, source_code):
        self.context = {}
        self.loop_context = {}
        instructions = [line for line in source_code.split("\n") if line.strip()]
        pointer = 0

        while pointer < len(instructions):
            line = instructions[pointer].strip()
            keyword = line.split(maxsplit=1)[0]

            match keyword:
                case "while":
                    condition = line[len("while "):]
                    if self.evaluate_expression(condition):
                        pointer += 1
                    else:
                        pointer = self.skip_block(instructions, pointer, "while", "end")

                case "end":
                    pointer = self.find_loop_start(instructions, pointer, "while", "end")

                case "if":
                    condition = line[len("if "):]
                    if self.evaluate_expression(condition):
                        pointer += 1
                    else:
                        pointer = self.skip_to_else_or_end(instructions, pointer)

                case "else":
                    pointer = self.skip_block(instructions, pointer, "if", "endif")

                case "endif":
                    pointer += 1

                case "for":
                    tokens = line.split()
                    if len(tokens) != 6 or tokens[2] != "=" or tokens[4] != "to":
                        print(f"Syntax error in 'for' loop: {line}")
                        pointer += 1
                        continue

                    var, start, end = tokens[1], int(tokens[3]), int(tokens[5])
                    self.context[var] = start
                    self.loop_context = {"iterator": var, "limit": end, "loop_start": pointer}
                    pointer += 1

                case "endfor":
                    var = self.loop_context["iterator"]
                    self.context[var] += 1
                    if self.context[var] <= self.loop_context["limit"]:
                        pointer = self.loop_context["loop_start"] + 1
                    else:
                        self.loop_context = {}
                        pointer += 1

                case "print":
                    print(line[len("print "):])
                    pointer += 1

                case _:
                    # Handle assignment like: x = y 2 +
                    if "=" in line:
                        name, expr = line.split("=", maxsplit=1)
                        self.context[name.strip()] = self.evaluate_expression(expr.strip())
                        pointer += 1
                    else:
                        print(f"Unknown instruction: {line}")
                        pointer += 1

        print(self.context)

    def evaluate_expression(self, expr):
        tokens = expr.split()
        stack = []

        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in self.context:
                stack.append(self.context[token])
            elif token in {"+", "-", "*", "/", ">", "<", ">=", "<=", "==", "!="}:
                b = stack.pop()
                a = stack.pop()
                result = {
                    "+": a + b,
                    "-": a - b,
                    "*": a * b,
                    "/": a // b,
                    ">": int(a > b),
                    "<": int(a < b),
                    ">=": int(a >= b),
                    "<=": int(a <= b),
                    "==": int(a == b),
                    "!=": int(a != b)
                }[token]
                stack.append(result)

        return stack[0] if stack else 0

    def skip_block(self, code_lines, index, start_kw, end_kw):
        level = 1
        index += 1
        while index < len(code_lines):
            head = code_lines[index].split(maxsplit=1)[0]
            if head == start_kw:
                level += 1
            elif head == end_kw:
                level -= 1
                if level == 0:
                    return index + 1
            index += 1
        return index

    def skip_to_else_or_end(self, code_lines, index):
        level = 1
        index += 1
        while index < len(code_lines):
            head = code_lines[index].split(maxsplit=1)[0]
            if head == "if":
                level += 1
            elif head == "endif":
                level -= 1
                if level == 0:
                    return index + 1
            elif head == "else" and level == 1:
                return index + 1
            index += 1
        return index

    def find_loop_start(self, code_lines, index, start_kw, end_kw):
        depth = 1
        index -= 1
        while index >= 0:
            head = code_lines[index].split(maxsplit=1)[0]
            if head == end_kw:
                depth += 1
            elif head == start_kw:
                depth -= 1
                if depth == 0:
                    return index
            index -= 1
        return index

# Entry point for file-based input
if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        script = f.read()
    interpreter = SimpleLangInterpreter()
    interpreter.execute_program(script)
