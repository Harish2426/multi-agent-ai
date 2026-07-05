import ast
import operator


class CalculatorTool:
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(self, expression: str):
        tree = ast.parse(expression, mode="eval")
        return self._evaluate(tree.body)

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numbers are allowed.")
            return node.value

        if isinstance(node, ast.BinOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operator_function(left, right)

        if isinstance(node, ast.UnaryOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Unsupported operator.")

            return operator_function(
                self._evaluate(node.operand)
            )

        raise ValueError("Invalid mathematical expression.")


calculator_tool = CalculatorTool()