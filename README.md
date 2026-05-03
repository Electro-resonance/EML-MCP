# EML-MCP
MCP server for EML (Exp-Minus-Log) mathematical notation.

`eml_mcp_server.py` is a single-file MCP server focused on symbolic EML, pure-mode EML, SymPy comparison, and a compact set of generalized EML family tools derived from the follow-up algebraic-structure paper.

## Why this project came to fruition

The EML methods paper inspired me to develop a new MCP server so that I could test out the EML methods.

The follow-up paper on the algebraic structure behind EML then motivated a second layer of tooling: compact MCP functions for exploring generalized EML families, their hidden abelian-group structure, their constructive recovery chain, and the open constant-free generator question.

## What is included

The server exposes thirteen MCP tools:

- `eml_compile`
- `eml_eval`
- `eml_simplify`
- `eml_stability_check`
- `eml_fit`
- `sympy_eval`
- `sympy_simplify`
- `eml_family_library`
- `eml_extract_group_structure`
- `eml_recover_core_family`
- `eml_generate_from_addition_formula`
- `eml_constant_free_scan`
- `eml_explore_family`

## Practical mode and pure mode

The EML route supports two compilation styles:

- **practical mode** — the default mode, designed for compact trees and efficient evaluation
- **pure mode** — an opt-in mode that rewrites numeric constants into EML trees built from the distinguished constant `1` and the `eml(...)` operator

Pure mode is intended for paper-style structural inspection and experimentation. Variables are still represented as variables, but numeric constants are rewritten into pure EML-style constant constructions.

The EML tools that support the `pure` flag are:

- `eml_compile`
- `eml_eval`
- `eml_simplify`
- `eml_stability_check`
- `eml_fit`

## Generalized EML family tools

The `eml_family_*` tools are curated structural tools based on the generalized operator view from the follow-up paper. They are intentionally concise and work with a built-in family library rather than attempting to prove arbitrary user-defined operators.

### Built-in families

- `original_eml`
- `cosine_arccos`
- `arccot_cot`
- `tanh_artanh`
- `elliptic_pair`
- `involutive_piecewise`

### What the family tools do

- `eml_family_library` — list the built-in family catalogue or inspect one family
- `eml_extract_group_structure` — expose the neutral element, inverse map, and induced abelian group law
- `eml_recover_core_family` — show the six-step constructive recovery chain
- `eml_generate_from_addition_formula` — report the family-specific addition formula and derived operations
- `eml_constant_free_scan` — summarise the open constant-free-generator question and curated candidates
- `eml_explore_family` — return an aggregated view of one family

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


### Example 5: inspect the built-in family library

Use `eml_family_library` to list the curated generalized EML families, then request one by name such as `original_eml` or `tanh_artanh`.

### Example 6: inspect one family structurally

Use `eml_explore_family` with a built-in family name to see:
- the operator formula
- the induced group structure
- the recovery chain
- the addition formula
- the derived operations

### Example 7: fit a compact law from data

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
- Tomasz Stachowiak, *Algebraic structure behind Odrzywołek’s EML operator*  
  https://arxiv.org/abs/2604.23893
