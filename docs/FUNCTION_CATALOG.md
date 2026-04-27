# Function Catalog

This document describes the active tool surface for the slim EML + SymPy edition.
The examples below are deliberately small enough to understand quickly, but rich enough to show how an LLM or Python caller would actually use the tools.

## EML symbolic core

### `eml_eval`
Evaluate an EML expression or a normal infix expression after compiling it to EML.

Use: Use when the LLM already has an EML expression or wants to evaluate an infix expression through the EML route.

Arguments:
- `expr` (string) required
- `bindings` (object)

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

Related: `eml_compile`, `eml_simplify`, `eml_stability_check`, `sympy_eval`

### `eml_compile`
Compile a standard infix mathematical expression into an EML tree.

Use: Use when the LLM needs a normal expression translated into the EML basis before explanation, storage, or further evaluation.

Arguments:
- `target_expr` (string) required
- `simplify` (boolean)

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

Related: `eml_eval`, `eml_simplify`, `sympy_simplify`

### `eml_fit`
Fit a compact symbolic law to x/y data, compile the best result to EML, and return metrics.

Use: Use for symbolic-regression style fitting when the LLM has x/y data and wants a compact candidate law.

Arguments:
- `x_values` (array) required
- `y_values` (array) required
- `families` (array)
- `top_k` (integer)

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

Related: `eml_compile`, `eml_stability_check`, `sympy_eval`

### `eml_simplify`
Simplify an EML tree via constant folding and canonical rebuilding.

Use: Use when the LLM wants a cleaner canonical EML tree before comparing or explaining expressions.

Arguments:
- `expr` (string) required

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

Related: `eml_compile`, `eml_eval`, `sympy_simplify`

### `eml_stability_check`
Sample an EML expression and flag branch-cut, overflow, near-zero log, and conditioning risks.

Use: Use before evaluating an EML expression broadly over a region, especially around logs, zeros, branches, or exponentials.

Arguments:
- `expr` (string) required
- `bindings` (object)
- `region` (object)

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

## Suggested comparison patterns

### Identity check
- `eml_compile`
- `eml_simplify`
- `sympy_simplify`

### Numeric comparison
- `eml_eval`
- `sympy_eval`

### Stability-aware fitting
- `eml_fit`
- `eml_stability_check`
- `sympy_eval`
