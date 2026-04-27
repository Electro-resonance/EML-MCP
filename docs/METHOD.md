# Method

## EML basis

The EML route is built around the operator:

`eml(x, y) = exp(x) - log(y)`

The server uses this basis as an explicit symbolic intermediate layer.

## Practical mode and pure mode

The EML compiler supports two modes:

- **practical mode** — the default mode, intended for efficient evaluation and compact trees
- **pure mode** — an opt-in mode intended for stricter EML-style structural inspection

In pure mode, numeric constants are rewritten into EML constructions based on the distinguished constant `1`. This makes the resulting tree closer to the spirit of the EML paper, even though variables remain as variables and the implementation still serves practical evaluation workflows.

## Compilation strategy

The compilation path is:

1. parse infix maths through SymPy
2. simplify the parsed expression
3. lower the result into a recursive EML tree
4. optionally simplify the EML tree further
5. in pure mode, rewrite numeric constants into pure-style EML constructions

## Evaluation strategy

Evaluation is performed recursively over the EML tree.

Outputs may be complex because logarithms and branch behaviour are handled using complex arithmetic.

The same evaluator is used for both practical and pure-mode trees.

## Simplification strategy

The simplifier normally performs constant folding over literal EML subtrees.

In pure mode, simplification should preserve the structural intent of the tree rather than collapsing the pure constant representation back into ordinary numeric leaves.

## Stability strategy

The stability check samples the expression over a requested region and inspects:

- near-zero log inputs
- negative-real log inputs
- large positive exponential inputs
- very large intermediate outputs
- evaluation failures
- wide output-range conditioning

This is not a formal proof of stability. It is a practical warning layer.

Pure mode can also be used with stability checking when you want to inspect whether a pure-style representation behaves differently or exposes different intermediate structure.

## Fitting strategy

The fitting tool performs heuristic symbolic regression over a small family library.

It ranks candidate laws by:

- mean squared error
- R²

The best candidate is then compiled into EML and checked for stability over the fitted domain.

When requested, fitting can also emit a pure-mode EML form of the best candidate for structural inspection.

## SymPy role

SymPy is used as the conventional symbolic algebra baseline.

It provides:

- direct symbolic simplification
- direct numeric evaluation
- a second route for comparison against EML behaviour

## Why combine EML and SymPy

Using both routes lets you inspect whether:

- the EML path preserves structure in a useful way
- the pure-mode EML path reveals a stricter constant construction
- the SymPy path confirms the conventional symbolic result
- the two routes agree numerically
- the EML form reveals stability or branch behaviour that might be hidden in a more compact form
