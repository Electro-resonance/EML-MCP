# SKILLS.md

## Purpose

This guide explains how to use the slim EML + SymPy + family-tools edition of the MCP server.

It is designed for workflows where you want to:

- compile a standard mathematical expression into an explicit EML tree
- optionally compile into a stricter pure-mode EML tree for structural inspection
- inspect how an expression is represented in EML (Exp-Minus-Log) form
- simplify, evaluate, and analyse that EML tree
- fit compact symbolic laws to data and convert the best candidate into EML
- inspect generalized EML families from the follow-up paper
- compare the EML route with standard symbolic algebra through SymPy

## Active tool surface

The server exposes the following tools:

- `eml_compile`
- `eml_eval`
- `eml_fit`
- `eml_simplify`
- `eml_stability_check`
- `sympy_eval`
- `sympy_simplify`
- `eml_family_library`
- `eml_extract_group_structure`
- `eml_recover_core_family`
- `eml_generate_from_addition_formula`
- `eml_constant_free_scan`
- `eml_explore_family`

## Practical mode and pure mode

The EML tools support two styles of use:

- **practical mode** — the default mode for compact expressions and straightforward evaluation
- **pure mode** — an opt-in mode, requested with `pure: true`, for inspecting a stricter EML-style constant construction

In pure mode, numeric constants are rewritten into EML structures based on the distinguished constant `1`. This is useful when you want to inspect the structural form rather than just the shortest practical representation.

## When to use EML tools

Use the EML tools when you want the model to:

- rewrite a standard expression into EML (Exp-Minus-Log) form
- create an explicit EML tree from an infix mathematical expression using `eml_compile`
- create a pure-mode EML tree for stricter structural inspection
- inspect an intermediate symbolic representation before further analysis
- evaluate the EML form numerically at chosen bindings
- simplify and normalise the EML tree
- test numerical stability over a region
- fit a compact symbolic law to data and convert it into EML

### Typical EML workflow

1. `eml_compile` to create the EML tree from a standard expression
2. optionally rerun `eml_compile` with `pure: true` for structural inspection
3. `eml_simplify` to reduce or normalise the tree
4. `eml_eval` to evaluate the EML expression numerically
5. `eml_stability_check` to inspect branch, overflow, and conditioning risks
6. `eml_fit` when working from data rather than from a known closed form

## When to use family tools

Use the `eml_family_*` tools when you want to inspect the generalized operator perspective from the follow-up paper.

### Typical family workflow

1. `eml_family_library` to list the built-in families
2. `eml_extract_group_structure` to inspect the hidden abelian-group structure
3. `eml_recover_core_family` to see the six-step recovery chain
4. `eml_generate_from_addition_formula` to inspect what downstream operations the family yields
5. `eml_explore_family` when you want the whole picture in one call
6. `eml_constant_free_scan` when you want to inspect the open constant-free-generator question

## Built-in family names

- `original_eml`
- `cosine_arccos`
- `arccot_cot`
- `tanh_artanh`
- `elliptic_pair`
- `involutive_piecewise`

## When to use pure mode

Use pure mode when you want to:

- inspect how constants are represented using the distinguished constant `1`
- compare a practical tree with a stricter EML-style constant tree
- preserve a more paper-like EML structure during compilation and simplification
- analyse leaf structure using the returned `leaf_analysis`

Typical pure-mode example:
- compile `pi + e + 1/2` with `pure: true`
- inspect the returned `leaf_analysis`
- compare that result with the practical compile output

## When to use SymPy tools

Use the SymPy tools when you want:

- conventional symbolic simplification
- a second route to verify an identity
- direct numeric evaluation with controlled precision
- a baseline comparison against standard symbolic algebra

### Typical SymPy workflow

1. `sympy_simplify`
2. `sympy_eval`
3. compare the result with the EML path

## Example prompts for an LLM

### Create an EML tree

- Compile `sin(x)**2 + cos(x)**2` into an EML tree and show the result.
- Create the EML tree for `sqrt(a^2 + b^2)` and explain the major steps in the translation.
- Convert `exp(x) + log(x) + cos(x)` into EML form and describe the resulting tree structure.

### Create a pure-mode EML tree

- Compile `pi + e + 1/2` into a pure-mode EML tree and show the leaf analysis.
- Compare the practical and pure-mode EML trees for `pi + e + 1/2`.
- Compile a constant-heavy expression in pure mode and explain how the constants reduce to the distinguished constant `1`.

### Rewrite and simplify in EML

- Compile `sin(x)**2 + cos(x)**2` to EML and simplify it.
- Expand `sqrt(a^2 + b^2)` into EML, then simplify the resulting expression.
- Compile `sin(x) + log(x)` into EML and describe the main identities used.

### Numerical evaluation

- Evaluate `sqrt(a^2 + b^2)` through the EML route at `a=3`, `b=4`.
- Evaluate `sin(pi/6)^2 + cos(pi/6)^2` through the EML route.
- Evaluate `exp(x) + log(x)` at a chosen point and report the result.

### Numerical safety

- Compile `log(x)` and run a stability check over `x in [0, 1]`.
- Compare the behaviour of `exp(x)` and `log(x)` on a wide region.
- Run a stability check on `sin(x) + log(x)` over `x in [0.2, 2.0]`.

### Fitting

- Fit a linear law to these data and return the best EML form.
- Fit a compact law to the data, then simplify the best EML candidate and evaluate it at a new point.
- Fit a small dataset that resembles `log(x)` and compare the top candidate laws.


### Explore a generalized family

- List the built-in generalized EML families.
- Show the hidden group structure for `original_eml`.
- Recover the six-step family chain for `tanh_artanh`.
- Explain the addition formula and derived operations for `cosine_arccos`.
- Show the constant-free candidates from the follow-up paper.

### Cross-check with SymPy

- Simplify `sin(x)**2 + cos(x)**2` in both EML and SymPy.
- Evaluate `sqrt(a^2 + b^2)` using both routes and compare the results.
- Compile an expression to EML, then use SymPy to verify the same identity independently.

## Suggested comparison patterns

### Identity check

1. `eml_compile`
2. `eml_simplify`
3. `sympy_simplify`

### Numeric comparison

1. `eml_eval`
2. `sympy_eval`

### Pure-mode structural comparison

1. `eml_compile`
2. `eml_compile` with `pure: true`
3. inspect `leaf_analysis`
4. compare the two tree styles

### Stability-aware fitting

1. `eml_fit`
2. `eml_stability_check`
3. `sympy_eval`

### Generalized family inspection

1. `eml_family_library`
2. `eml_extract_group_structure`
3. `eml_recover_core_family`
4. `eml_generate_from_addition_formula`
5. optionally `eml_explore_family`

## Practical notes

- EML is useful when you want an explicit, inspectable symbolic form.
- Creating the EML tree is often the most informative first step, because it exposes the structure that later simplification and evaluation operate on.
- In this slim edition, tree creation is handled by `eml_compile`; there is no separate standalone tree tool.
- Pure mode is most useful for structural inspection, not for the shortest or fastest representation.
- The family tools are curated structural tools for built-in families, not arbitrary operator-proof checkers.
- SymPy is useful when you want a conventional algebra baseline.
- The most informative behaviour often comes from using all three layers together: practical EML, pure EML, and generalized family inspection.
