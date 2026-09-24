import ast
import operator
import os
import re
import requests


# ---------------- CALCULATOR ----------------

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left = _eval(node.left)
        right = _eval(node.right)
        return _OPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))

    raise ValueError("invalid expression")


def calculator(expression):
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_eval(tree.body))
    except Exception as error:
        return f"Calculator error: {error}. Use only numbers and + - * / ( )."


# ---------------- WEBPAGE READER ----------------

def read_webpage(url, max_chars=2000):
    try:
        if url.startswith(("http://", "https://")):
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html = response.text
        else:
            if not os.path.exists(url):
                raise FileNotFoundError(
                    f"'{url}' is not a URL and no such file exists."
                )

            with open(url, "r", encoding="utf-8") as file:
                html = file.read()

        # Remove script and style sections
        html = re.sub(
            r"<(script|style).*?>.*?</\1>",
            " ",
            html,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", " ", html)

        # Clean extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return "Read error: the page contained no readable text."

        # Limit output size
        return text[:max_chars]

    except Exception as error:
        return f"Read error: {error}"


# ---------------- TOOL REGISTRY ----------------

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "read_webpage": read_webpage,
}


# ---------------- OPENAI TOOL SCHEMAS ----------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression safely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression using numbers and + - * / ( )."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": "Read the text content of a webpage or local HTML file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "A webpage URL or local HTML file path."
                    }
                },
                "required": ["url"]
            }
        }
    }
]


# ---------------- BASIC TESTS ----------------

if __name__ == "__main__":

    print(calculator("12000 + 15000"))
    print(calculator("2 ** 10"))
    print(calculator("2 +"))

    print(read_webpage("notice.html"))
    print(read_webpage("no_such_file.html"))