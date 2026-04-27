# EML-MCP
MCP server for EML (Exp-Minus-Log) mathematical notation.

`eml_mcp_server.py` is a single-file MCP server focused on the symbolic EML and SymPy tool families.

## Why this project came to fruition

The EML methods paper inspired me to develop a new MCP server so that I could test out the EML methods.

## What is included

The server exposes seven MCP tools:

- `eml_compile`
- `eml_eval`
- `eml_simplify`
- `eml_stability_check`
- `eml_fit`
- `sympy_eval`
- `sympy_simplify`

## Practical mode and pure mode

The EML route now supports two compilation styles:

- **practical mode** — the default mode, designed for compact trees and efficient evaluation
- **pure mode** — an opt-in mode that rewrites numeric constants into EML trees built from the distinguished constant `1` and the `eml(...)` operator

Pure mode is intended for paper-style structural inspection and experimentation. Variables are still represented as variables, but numeric constants are rewritten into pure EML-style constant constructions.

The EML tools that support the `pure` flag are:

- `eml_compile`
- `eml_eval`
- `eml_simplify`
- `eml_stability_check`
- `eml_fit`

## Main files

- `eml_mcp_server.py` — single-file MCP server, direct examples, and test harness
- `docs/FUNCTION_CATALOG.md` — tool catalogue and argument overview
- `docs/ARCHITECTURE.md` — component-level design
- `docs/METHOD.md` — mathematical and computational approach
- `docs/TEST.md` — how to run the MCP tests and call the server from Python
- `SKILLS.md` — practical usage guide for humans and LLMs

## Run modes

```bash
python3 eml_mcp_server.py server
python3 eml_mcp_server.py test
python3 eml_mcp_server.py examples
python3 eml_mcp_server.py all
```

## Semi-complex but readable examples

### Example 1: identity through both routes

```text
sin(x)**2 + cos(x)**2
```

- compile it to EML with `eml_compile`
- simplify the resulting tree with `eml_simplify`
- confirm the same identity with `sympy_simplify`

### Example 2: inspect pure mode for constants

```text
pi + e + 1/2
```

Use `eml_compile` with `pure: true` to inspect how the constants are rewritten into an EML tree whose constant leaves reduce to the distinguished constant `1`.

### Example 3: evaluate a familiar geometric form

```text
sqrt(a^2 + b^2)
```

Use `eml_eval` and `sympy_eval` with bindings such as `a=5`, `b=12` to confirm that both routes give `13`.

### Example 4: inspect a mild branch-risk case

```text
sin(x) + log(x)
```

Use `eml_compile` followed by `eml_stability_check` over a region such as `x in [0.2, 2.0]` to see how the logarithm affects the numerical risk profile.

### Example 5: fit a compact law from data

Use `eml_fit` on a small and interpretable dataset, for example `y = log(x)` sampled at `x = [0.5, 1.0, 2.0, 4.0]`, and compare the best candidate families.

## Requirements

The script uses:

- Python 3.10+
- `numpy`
- `sympy`
- `scipy`
- `mcp` for `server` and `test` modes

## MCP transport

The server uses the official MCP Python SDK over stdio, which makes it easy to test from Python subprocesses and LLM tool wrappers.

## References

- Andrzej Odrzywołek, *All elementary functions from a single operator* (EML methods)  
  https://arxiv.org/html/2603.21852v2
