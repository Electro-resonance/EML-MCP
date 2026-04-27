# TEST.md

## Purpose

This document explains how to run tests against the text-based MCP server and how to call the same server from other Python code.

## Quick start

From the project directory:

```bash
python eml_mcp_server.py test
```

This launches the server as a subprocess, connects to it over stdio using framed JSON-RPC messages, and runs the built-in regression suite.

## Other run modes

### Start the text MCP server only

```bash
python eml_mcp_server.py server
```

### Run the direct local examples only

```bash
python eml_mcp_server.py examples
```

### Run both examples and the regression suite

```bash
python eml_mcp_server.py all
```

## What the built-in test suite checks

The regression suite currently checks:

- the exposed tool surface from `tools/list`
- `eml_compile` on a classic trigonometric identity
- `eml_simplify` on `sin(x)^2 + cos(x)^2`
- `eml_eval` on `sqrt(a^2 + b^2)`
- `eml_stability_check` on `log(x)` over a risky region
- `eml_fit` on a simple linear dataset
- `sympy_simplify` on a classic trigonometric identity
- `sympy_eval` on `sqrt(a^2 + b^2)`

## What success looks like

A successful run ends with a JSON report showing:

- `all_passed: true`
- `failed_cases: 0`

## Capturing output

### Save stdout and stderr separately

```bash
python eml_mcp_server.py test > test_output.txt 2> test_error.txt
```

### Save everything together

```bash
python eml_mcp_server.py test > test_full_output.txt 2>&1
```

## Calling the text MCP server from Python

The text-based transport uses stdio plus `Content-Length` framing. A second Python program can therefore launch the server as a subprocess and talk JSON-RPC to it.

### Minimal subprocess example

```python
import json
import subprocess


def write_framed(stream, payload):
    body = json.dumps(payload).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    stream.write(header)
    stream.write(body)
    stream.flush()


def read_framed(stream):
    headers = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, value = line.decode("ascii").split(":", 1)
        headers[key.strip().lower()] = value.strip()
    length = int(headers["content-length"])
    return json.loads(stream.read(length).decode("utf-8"))


proc = subprocess.Popen(
    ["python", "eml_mcp_server.py", "server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

write_framed(proc.stdin, {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {"clientInfo": {"name": "demo-client", "version": "1.0"}},
})
print(read_framed(proc.stdout))

write_framed(proc.stdin, {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "eml_eval",
        "arguments": {
            "expr": "sqrt(a^2 + b^2)",
            "bindings": {"a": 3, "b": 4},
        },
    },
})
print(read_framed(proc.stdout))
```

## Calling the underlying Python functions directly

If you do not need the MCP transport, another Python module can import the file and call the tool wrappers directly.

```python
from eml_mcp_server import tool_eml_compile, tool_eml_eval, tool_sympy_simplify

compiled = tool_eml_compile({
    "target_expr": "sin(x)**2 + cos(x)**2",
    "simplify": True,
})
print(compiled["simplified_eml_expression"])

value = tool_eml_eval({
    "expr": "sqrt(a^2 + b^2)",
    "bindings": {"a": 5, "b": 12},
})
print(value["value_pretty"])

sym = tool_sympy_simplify({
    "expr": "sin(x)**2 + cos(x)**2",
})
print(sym["simplified"])
```

## Suggested external test patterns

### Python unit tests

Use `pytest` or `unittest` to check:

- that `eml_compile` returns a non-empty tree
- that `eml_eval` and `sympy_eval` agree on simple benchmark expressions
- that `eml_stability_check` warns for `log(x)` near zero
- that `eml_fit` returns a high `r2` on known synthetic datasets

### Cross-route comparison tests

Useful benchmark expressions include:

- `sin(x)^2 + cos(x)^2`
- `sqrt(a^2 + b^2)`
- `exp(x) + log(x) + cos(x)`
- `sin(x) + log(x)`

## Future test ideas

- add more regression cases for inverse and hyperbolic functions
- add golden-file snapshots for example outputs
- add tolerance-based comparison between EML and SymPy across parameter sweeps
- add CI automation so every commit runs the slim harness
