# Function Catalog

This document describes the active tool surface for the EML + SymPy + family-tools edition.
The examples below are deliberately small enough to understand quickly, but rich enough to show how an LLM or Python caller would actually use the tools.

## EML symbolic core

### `eml_eval`
Evaluate an EML expression or a normal infix expression after compiling it to EML.

Use: Use when the LLM already has an EML expression or wants to evaluate an infix expression through the EML route.

Arguments:
- `expr` (string) required
- `bindings` (object)
- `pure` (boolean)

Example call:
```json
{
  "name": "eml_eval",
  "arguments": {
    "expr": "eml(1, x)",
    "bindings": {
      "x": 2.0
    }
  }
}
```

Also useful for ordinary infix input:
```json
{
  "name": "eml_eval",
  "arguments": {
    "expr": "sqrt(a^2 + b^2)",
    "bindings": {
      "a": 5,
      "b": 12
    }
  }
}
```

Pure-mode example:
```json
{
  "name": "eml_eval",
  "arguments": {
    "expr": "pi + e + 1/2",
    "pure": true
  }
}
```

Related: `eml_compile`, `eml_simplify`, `eml_stability_check`, `sympy_eval`

### `eml_compile`
Compile a standard infix mathematical expression into an EML tree.

Use: Use when the LLM needs a normal expression translated into the EML basis before explanation, storage, or further evaluation.

Arguments:
- `target_expr` (string) required
- `simplify` (boolean)
- `pure` (boolean)

Example call:
```json
{
  "name": "eml_compile",
  "arguments": {
    "target_expr": "sin(x)+log(x)",
    "simplify": true
  }
}
```

Another semi-complex example:
```json
{
  "name": "eml_compile",
  "arguments": {
    "target_expr": "exp(x) + log(x) + cos(x)",
    "simplify": true
  }
}
```

Pure-mode constant example:
```json
{
  "name": "eml_compile",
  "arguments": {
    "target_expr": "pi + e + 1/2",
    "simplify": false,
    "pure": true
  }
}
```

Pure mode is intended for structural inspection. In this mode the compile result also reports leaf analysis so you can inspect whether the constant leaves reduce to the distinguished constant `1`.

Related: `eml_eval`, `eml_simplify`, `sympy_simplify`

### `eml_fit`
Fit a compact symbolic law to x/y data, compile the best result to EML, and return metrics.

Use: Use for symbolic-regression style fitting when the LLM has x/y data and wants a compact candidate law.

Arguments:
- `x_values` (array) required
- `y_values` (array) required
- `families` (array)
- `top_k` (integer)
- `pure` (boolean)

Example call:
```json
{
  "name": "eml_fit",
  "arguments": {
    "x_values": [
      0.5,
      1.0,
      2.0,
      4.0
    ],
    "y_values": [
      -0.6931471806,
      0.0,
      0.6931471806,
      1.3862943611
    ],
    "families": [
      "linear",
      "log_affine",
      "power_affine"
    ],
    "top_k": 3
  }
}
```

A simpler sanity-check dataset:
```json
{
  "name": "eml_fit",
  "arguments": {
    "x_values": [1, 2, 3, 4],
    "y_values": [2, 4, 6, 8],
    "families": ["linear"],
    "top_k": 1
  }
}
```

Pure-mode output can include an additional `best_formula_eml_pure` form for structural inspection.

Related: `eml_compile`, `eml_stability_check`, `sympy_eval`

### `eml_simplify`
Simplify an EML tree via constant folding and canonical rebuilding.

Use: Use when the LLM wants a cleaner canonical EML tree before comparing or explaining expressions.

Arguments:
- `expr` (string) required
- `pure` (boolean)

Example call:
```json
{
  "name": "eml_simplify",
  "arguments": {
    "expr": "eml(1, eml(eml(1, x), 1))"
  }
}
```

Infix input is also accepted and auto-compiled:
```json
{
  "name": "eml_simplify",
  "arguments": {
    "expr": "sin(x)**2 + cos(x)**2"
  }
}
```

Pure-mode example:
```json
{
  "name": "eml_simplify",
  "arguments": {
    "expr": "pi + e + 1/2",
    "pure": true
  }
}
```

In pure mode, simplification preserves the pure-style constant structure rather than collapsing the tree back to ordinary literals.

Related: `eml_compile`, `eml_eval`, `sympy_simplify`

### `eml_stability_check`
Sample an EML expression and flag branch-cut, overflow, near-zero log, and conditioning risks.

Use: Use before evaluating an EML expression broadly over a region, especially around logs, zeros, branches, or exponentials.

Arguments:
- `expr` (string) required
- `bindings` (object)
- `region` (object)
- `pure` (boolean)

Example call:
```json
{
  "name": "eml_stability_check",
  "arguments": {
    "expr": "sin(x)+log(x)",
    "region": {
      "x": {
        "min": 0.2,
        "max": 2.0
      }
    }
  }
}
```

A riskier example:
```json
{
  "name": "eml_stability_check",
  "arguments": {
    "expr": "log(x)",
    "region": {
      "x": {
        "min": 0.0,
        "max": 1.0
      }
    }
  }
}
```

Pure-mode example:
```json
{
  "name": "eml_stability_check",
  "arguments": {
    "expr": "pi + e + 1/2",
    "pure": true
  }
}
```

Related: `eml_eval`, `eml_compile`, `sympy_eval`

## Direct SymPy algebra and evaluation

### `sympy_eval`
Directly evaluate a SymPy expression with optional bindings and precision.

Use: Use when the LLM wants direct exact-algebra evaluation without routing through EML.

Arguments:
- `expr` (string) required
- `bindings` (object)
- `digits` (integer)

Example call:
```json
{
  "name": "sympy_eval",
  "arguments": {
    "expr": "sqrt(a^2 + b^2)",
    "bindings": {
      "a": 8,
      "b": 15
    },
    "digits": 30
  }
}
```

Identity-style example:
```json
{
  "name": "sympy_eval",
  "arguments": {
    "expr": "sin(pi/6)^2 + cos(pi/6)^2",
    "digits": 30
  }
}
```

Related: `sympy_simplify`, `eml_eval`

### `sympy_simplify`
Simplify an expression directly in SymPy and return plain-text and LaTeX forms.

Use: Use for exact algebraic cleanup or identity checking before deeper exploration.

Arguments:
- `expr` (string) required

Example call:
```json
{
  "name": "sympy_simplify",
  "arguments": {
    "expr": "sin(x)**2 + cos(x)**2"
  }
}
```

Another understandable but richer example:
```json
{
  "name": "sympy_simplify",
  "arguments": {
    "expr": "exp(log(x)) + sin(x)**2 + cos(x)**2"
  }
}
```

Related: `sympy_eval`, `eml_compile`, `eml_simplify`

## Generalized EML family tools

These tools are compact structural tools for built-in generalized families. They are based on curated family metadata, not arbitrary operator proof search.

### `eml_family_library`
List the built-in generalized EML families or inspect one family.

Arguments:
- `family` (string) optional

Returns:
- when omitted: a summary list of all built-in families
- when provided: the full metadata for the selected family

Example call:
```json
{
  "name": "eml_family_library",
  "arguments": {}
}
```

Example call for one family:
```json
{
  "name": "eml_family_library",
  "arguments": {
    "family": "original_eml"
  }
}
```

### `eml_extract_group_structure`
Expose the hidden abelian-group data behind a built-in generalized EML family.

Arguments:
- `family` (string) required

Returns:
- operator formula
- neutral element
- inverse map
- induced group law
- symbolic axiom flags

Example call:
```json
{
  "name": "eml_extract_group_structure",
  "arguments": {
    "family": "original_eml"
  }
}
```

### `eml_recover_core_family`
Return the six-step constructive recovery chain from the follow-up paper.

Arguments:
- `family` (string) required

Returns the sequence for recovering:
1. `f(x)`
2. `f(x) ⊟ y`
3. `g(x)`
4. `x ⊟ y`
5. the inverse map `ι(x)`
6. the induced group law `x ⊞ y`

Example call:
```json
{
  "name": "eml_recover_core_family",
  "arguments": {
    "family": "tanh_artanh"
  }
}
```

### `eml_generate_from_addition_formula`
Report the family-specific addition formula and what it can generate.

Arguments:
- `family` (string) required

This is useful for seeing what downstream operations a family yields. Some families reach multiplication and powers, while others stop at narrower composition laws.

Example call:
```json
{
  "name": "eml_generate_from_addition_formula",
  "arguments": {
    "family": "cosine_arccos"
  }
}
```

### `eml_constant_free_scan`
Summarise the open constant-free-generator question and curated candidates.

Arguments:
- none

Returns:
- the open-question marker
- constant-free candidates from the built-in family library
- notes on current limitations

Example call:
```json
{
  "name": "eml_constant_free_scan",
  "arguments": {}
}
```

### `eml_explore_family`
Convenience aggregation of family metadata, group structure, recovery chain, and addition-law consequences.

Arguments:
- `family` (string) required

Use this when you want the whole picture in one response rather than calling the other family tools separately.

Example call:
```json
{
  "name": "eml_explore_family",
  "arguments": {
    "family": "original_eml"
  }
}
```

## Built-in family names

- `original_eml`
- `cosine_arccos`
- `arccot_cot`
- `tanh_artanh`
- `elliptic_pair`
- `involutive_piecewise`

## Suggested patterns

### Identity check
- `eml_compile`
- `eml_simplify`
- `sympy_simplify`

### Numeric comparison
- `eml_eval`
- `sympy_eval`

### Structural inspection with pure mode
- `eml_compile` with `pure: true`
- inspect `leaf_analysis`
- `eml_simplify` with `pure: true`
- optionally compare the same expression against the practical mode output

### Practical-vs-pure comparison
- `eml_compile`
- `eml_compile` with `pure: true`
- inspect `leaf_analysis`

### Family inspection
- `eml_family_library`
- `eml_extract_group_structure`
- `eml_recover_core_family`
- `eml_generate_from_addition_formula`
- optionally `eml_explore_family`

### Constant-free investigation
- `eml_constant_free_scan`
- inspect `involutive_piecewise`
- compare limitations against `original_eml`

### Stability-aware fitting
- `eml_fit`
- `eml_stability_check`
- `sympy_eval`
