# SKILLS.md

## Purpose

This guide explains how to use the slim EML + SymPy edition of the MCP server.

It is designed for workflows where you want to:

- compile a standard mathematical expression into an explicit EML tree
- inspect how an expression is represented in EML (Exp-Minus-Log) form
- simplify, evaluate, and analyse that EML tree
- fit compact symbolic laws to data and convert the best candidate into EML
- compare the EML route with standard symbolic algebra through SymPy

## Active tool surface

The slim edition exposes the following tools:

- `eml_compile`
- `eml_eval`
- `eml_fit`
- `eml_simplify`
- `eml_stability_check`
- `sympy_eval`
- `sympy_simplify`

## When to use EML tools

Use the EML tools when you want the model to:

- rewrite a standard expression into EML (Exp-Minus-Log) form
- create an explicit EML tree from an infix mathematical expression using `eml_compile`
- inspect an intermediate symbolic representation before further analysis
- evaluate the EML form numerically at chosen bindings
- simplify and normalise the EML tree
- test numerical stability over a region
- fit a compact symbolic law to data and convert it into EML

### Typical EML workflow

1. `eml_compile` to create the EML tree from a standard expression
2. `eml_simplify` to reduce or normalise the tree
3. `eml_eval` to evaluate the EML expression numerically
4. `eml_stability_check` to inspect branch, overflow, and conditioning risks
5. `eml_fit` when working from data rather than from a known closed form

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

### Stability-aware fitting

1. `eml_fit`
2. `eml_stability_check`
3. `sympy_eval`

## Practical notes

- EML is useful when you want an explicit, inspectable symbolic form.
- Creating the EML tree is often the most informative first step, because it exposes the structure that later simplification and evaluation operate on.
- In this slim edition, tree creation is handled by `eml_compile`; there is no separate standalone tree tool.
- SymPy is useful when you want a conventional algebra baseline.
- The most informative behaviour often comes from using both together.
