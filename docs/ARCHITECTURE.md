# Architecture

## Overview

The EML-MCP server is organised into six layers.

## 1. Expression core

The expression core defines:

- the `EMLExpr` tree structure
- literal and variable nodes
- the recursive `eml(x, y) = exp(x) - log(y)` representation

In practical mode, literal leaves may remain as ordinary numeric constants.
In pure mode, numeric constants are rewritten into EML constructions built from the distinguished constant `1`.

## 2. Compiler

The compiler takes ordinary infix maths, parses it through SymPy, then lowers the result into EML form.

Responsibilities:

- parse safe mathematical expressions
- convert standard functions into EML-compatible symbolic form
- support both practical compilation and pure-mode constant rewriting
- cache repeated compilation requests

Pure mode is intended for structural inspection and paper-style experimentation. It aims to eliminate ordinary numeric constant leaves by rewriting them into EML trees based on `1`.

## 3. Evaluator and simplifier

The evaluator executes the EML tree numerically.
The simplifier performs constant folding and canonical rebuilding.

Responsibilities:

- numerical evaluation with bindings
- trace-aware evaluation for stability checks
- expression simplification
- preservation of pure-mode structure when requested

In pure mode, simplification should avoid collapsing the tree back into ordinary numeric literals where that would defeat the purpose of the pure representation.

## 4. Fitting layer

The fitting layer performs heuristic symbolic regression over a compact set of candidate families.

Responsibilities:

- fit candidate families to `x/y` data
- rank by MSE and R²
- compile the best formula to EML
- optionally emit a pure-mode compiled form
- run a follow-up stability pass on the fitted form

## 5. SymPy bridge

The SymPy bridge provides a conventional symbolic algebra route.

Responsibilities:

- simplify standard symbolic expressions
- evaluate expressions numerically with bindings and precision
- act as a comparison baseline against the EML route

## 6. MCP transport and harness

The transport uses the official MCP Python SDK over stdio.
The same file also contains the regression harness and direct examples.

Responsibilities:

- expose `tools/list` and `tools/call`
- provide a subprocess-based regression test path
- keep the whole project as a single runnable file

## Why this slim split exists

The wider project grew to include constants, CLSPR, Cosmolog, units, overlap, and workflow layers.
This edition removes those layers so the symbolic EML and SymPy behaviour can be tested in isolation.

Pure mode extends this slim edition without reintroducing those wider domains. It adds a stricter EML-style constant representation while keeping the tool surface compact.
