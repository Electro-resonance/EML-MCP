# EML-MCP
MCP server for EML (Exp-Minus-Log) mathematical notation.

`eml_mcp_server.py` is a single-file, text-based MCP server focused only on the symbolic EML and SymPy tool families.

This slim edition removes the constants, CLSPR, Cosmolog, units, overlap, music, and workflow layers from the broader project so the repository is centred on one task: testing how LLMs use EML expansion and conventional symbolic algebra side by side.

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

## Main files

- `eml_mcp_server.py` — single-file text MCP server, direct examples, and test harness
- `docs/FUNCTION_CATALOG.md` — tool catalogue and argument overview
- `docs/ARCHITECTURE.md` — component-level design
- `docs/METHOD.md` — mathematical and computational approach
- `docs/TEST.md` — how to run the text-based MCP tests and call the server from Python
- `SKILLS.md` — practical usage guide for humans and LLMs

## Run modes

```bash
python eml_mcp_server.py server
python eml_mcp_server.py test
python eml_mcp_server.py examples
python eml_mcp_server.py all
```

## Semi-complex but readable examples

### Example 1: identity through both routes

```text
sin(x)**2 + cos(x)**2
```

- compile it to EML with `eml_compile`
- simplify the resulting tree with `eml_simplify`
- confirm the same identity with `sympy_simplify`

### Example 2: evaluate a familiar geometric form

```text
sqrt(a^2 + b^2)
```

Use `eml_eval` and `sympy_eval` with bindings such as `a=5`, `b=12` to confirm that both routes give `13`.

### Example 3: inspect a mild branch-risk case

```text
sin(x) + log(x)
```

Use `eml_compile` followed by `eml_stability_check` over a region such as `x in [0.2, 2.0]` to see how the logarithm affects the numerical risk profile.

### Example 4: fit a compact law from data

Use `eml_fit` on a small and interpretable dataset, for example `y = log(x)` sampled at `x = [0.5, 1.0, 2.0, 4.0]`, and compare the best candidate families.

## Requirements

The script uses:

- Python 3.10+
- `numpy`
- `sympy`
- `scipy`

## Text-based MCP transport

The server uses stdio with JSON-RPC messages framed by `Content-Length`, which makes it easy to test from shell scripts, Python subprocesses, and LLM tool wrappers without depending on a separate web server.

## References

- Andrzej Odrzywołek, *All elementary functions from a single operator* (EML methods)  
  https://arxiv.org/html/2603.21852v2
