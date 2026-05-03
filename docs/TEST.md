# TEST.md

## Purpose

This document explains how to run tests against the MCP server and how to call the same server from other Python code.

## Quick start

From the project directory:

```bash
python eml_mcp_server.py test
```

This launches the server as a subprocess, connects to it over stdio using the official MCP Python SDK, and runs the built-in regression suite.

## Other run modes

### Start the MCP server only

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
- `eml_compile` in pure mode on `pi + e + 1/2`
- pure-mode leaf analysis for the distinguished constant `1`
- `eml_simplify` on `sin(x)^2 + cos(x)^2`
- `eml_eval` on `sqrt(a^2 + b^2)`
- `eml_stability_check` on `log(x)` over a risky region
- `eml_fit` on a simple linear dataset
- `sympy_simplify` on a classic trigonometric identity
- `sympy_eval` on `sqrt(a^2 + b^2)`
- `eml_family_library` for presence of `original_eml`
- `eml_extract_group_structure` for the original EML family
- `eml_constant_free_scan` for constant-free candidate reporting


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

## Calling the MCP server from Python

The server uses the official MCP Python SDK over stdio. A second Python program can launch the server as a subprocess and communicate with it through an MCP client session.

### Minimal official SDK example

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    params = StdioServerParameters(
        command="python",
        args=["eml_mcp_server.py", "server"],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print(tools)

            result = await session.call_tool(
                "eml_eval",
                {
                    "expr": "sqrt(a^2 + b^2)",
                    "bindings": {"a": 3, "b": 4},
                },
            )
            print(result)

asyncio.run(main())
```

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    params = StdioServerParameters(
        command="python",
        args=["eml_mcp_server_v3.py", "server"],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(tools)

            result = await session.call_tool(
                "eml_explore_family",
                {"family": "original_eml"},
            )
            print(result)

asyncio.run(main())
```

### Pure-mode call example

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    params = StdioServerParameters(
        command="python",
        args=["eml_mcp_server.py", "server"],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "eml_compile",
                {
                    "target_expr": "pi + e + 1/2",
                    "simplify": False,
                    "pure": True,
                },
            )
            print(result)

asyncio.run(main())
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

pure_compiled = tool_eml_compile({
    "target_expr": "pi + e + 1/2",
    "simplify": False,
    "pure": True,
})
print(pure_compiled["leaf_analysis"])

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

### Family-tool example

```python
result = await session.call_tool(
    "eml_generate_from_addition_formula",
    {"family": "tanh_artanh"},
)
```

## Suggested external test patterns

### Python unit tests

Use `pytest` or `unittest` to check:

- that `eml_compile` returns a non-empty tree
- that pure-mode compile reports the expected leaf analysis
- that `eml_eval` and `sympy_eval` agree on simple benchmark expressions
- that `eml_stability_check` warns for `log(x)` near zero
- that `eml_fit` returns a high `r2` on known synthetic datasets
- that `eml_family_library` lists the expected families
- that `eml_explore_family` returns the expected structural keys

### Cross-route comparison tests

Useful benchmark expressions include:

- `sin(x)^2 + cos(x)^2`
- `sqrt(a^2 + b^2)`
- `exp(x) + log(x) + cos(x)`
- `sin(x) + log(x)`
- `pi + e + 1/2` in pure mode

## Future test ideas

- add more regression cases for inverse and hyperbolic functions
- add golden-file snapshots for pure-mode example outputs
- add tolerance-based comparison between EML and SymPy across parameter sweeps
- add CI automation so every commit runs the slim harness
- add more regression cases for family-tool outputs
- add golden-file snapshots for pure-mode outputs
- add CI automation so every commit runs the harness
