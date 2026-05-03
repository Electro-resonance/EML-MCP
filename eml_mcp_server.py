#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 27th April 2026
# License: MIT License
# Project: https://github.com/Electro-resonance/EML-MCP
# Description: MCP server for EML (Exp-Minus-Log) mathematical notation
# =============================================================================
"""
EML MCP Server (single-file, self-contained)
============================================

A minimal stdio MCP-style server exposing EML (exp-minus-log) tooling, plus a
built-in client harness that launches the server and exercises the tools.

Why this file exists:
- This is a complete runnable MCP server in one file.
- The execution environment here does not bundle the official `mcp` package,
  so this script uses the official `mcp` Python SDK for stdio
  transport in server and test modes.
- The tool surface is intentionally small in this slim edition:
    * eml_eval
    * eml_compile
    * eml_fit
    * eml_simplify
    * eml_stability_check
    * sympy_eval
    * sympy_simplify
    * eml_family_library
    * eml_extract_group_structure
    * eml_recover_core_family
    * eml_generate_from_addition_formula
    * eml_constant_free_scan
    * eml_explore_family

Usage
-----
Run the server:
    python eml_mcp_server.py server

Run the built-in test harness client:
    python eml_mcp_server.py test

Optional:
    python eml_mcp_server.py examples

Notes
-----
- This is a practical EML compiler/evaluator rather than a theorem-prover.
- For practicality, numeric literals are allowed as leaves in addition to the
  distinguished constant 1. The core EML identities still use the paper's
  operator eml(x, y) = exp(x) - log(y).
- Internal computation uses complex arithmetic to cope with log branch behavior.
- The symbolic regression tool is heuristic. It searches a library of compact
  candidate templates, fits parameters, compiles the best result to EML, and
  returns the ranking.
- A pure mode is available during compilation to rewrite numeric constants into
  trees constructed from the distinguished constant 1 and the EML operator.
  Variables remain as variable leaves.
"""

from __future__ import annotations

import argparse
import ast
import csv
import cmath
import hashlib
import io
import json
import logging
import math
import os
import queue
import random
import signal
import subprocess
import sys
import threading
import time
import traceback
from collections import OrderedDict
from dataclasses import dataclass
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import sympy as sp
from scipy.optimize import curve_fit


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("eml_mcp")

def _helper_namespace_prefix() -> str:
    ns = os.getenv("MCP_EXPOSED_NAMESPACE", "").strip()
    return f"{ns}__" if ns else ""

def _helper_exposed_name(name: str) -> str:
    prefix = _helper_namespace_prefix()
    return f"{prefix}{name}" if prefix else name

def _helper_strip_namespace(name: str) -> str:
    prefix = _helper_namespace_prefix()
    if prefix and name.startswith(prefix):
        return name[len(prefix):]
    return name

# -----------------------------------------------------------------------------
# Small cache layers
# -----------------------------------------------------------------------------

class TTLCache:
    """Simple LRU + TTL cache for JSON-serializable-ish objects."""

    def __init__(self, maxsize: int = 256, ttl_seconds: int = 600):
        self.maxsize = maxsize
        self.ttl_seconds = ttl_seconds
        self._data: OrderedDict[str, Tuple[float, Any]] = OrderedDict()
        self._lock = threading.Lock()

    def _purge(self) -> None:
        now = time.time()
        expired = [k for k, (t, _) in self._data.items() if now - t > self.ttl_seconds]
        for k in expired:
            self._data.pop(k, None)
        while len(self._data) > self.maxsize:
            self._data.popitem(last=False)

    def get(self, key: str) -> Any:
        with self._lock:
            self._purge()
            if key not in self._data:
                return None
            ts, value = self._data.pop(key)
            self._data[key] = (ts, value)
            return value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = (time.time(), value)
            self._purge()

    def clear(self) -> None:
        with self._lock:
            self._data.clear()


parse_cache = TTLCache(maxsize=512, ttl_seconds=3600)
compile_cache = TTLCache(maxsize=512, ttl_seconds=3600)
eval_cache = TTLCache(maxsize=1024, ttl_seconds=1800)
simplify_cache = TTLCache(maxsize=512, ttl_seconds=3600)
fit_cache = TTLCache(maxsize=128, ttl_seconds=1800)
resource_cache = TTLCache(maxsize=32, ttl_seconds=3600)
prompt_cache = TTLCache(maxsize=32, ttl_seconds=3600)
constants_tool_cache = TTLCache(maxsize=256, ttl_seconds=3600)
clspr_cache = TTLCache(maxsize=512, ttl_seconds=3600)
music_cache = TTLCache(maxsize=256, ttl_seconds=3600)
explore_cache = TTLCache(maxsize=256, ttl_seconds=1800)


# -----------------------------------------------------------------------------
# Utility helpers
# -----------------------------------------------------------------------------

def canonical_json(data: Any) -> str:
    """Serialise data deterministically so cache keys remain stable across runs."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_key(*parts: Any) -> str:
    """Build a repeatable cache key from heterogeneous Python values."""
    return sha256_text(canonical_json(parts))


def coerce_number(value: Any) -> complex:
    """Convert JSON-style numeric input into a complex value for evaluation.

    The evaluator consistently uses complex arithmetic so logs and roots can
    cross onto the principal complex branch without special-case plumbing."""
    if isinstance(value, complex):
        return value
    if isinstance(value, (int, float, np.integer, np.floating)):
        return complex(value)
    if isinstance(value, dict) and set(value.keys()) >= {"real", "imag"}:
        return complex(float(value["real"]), float(value["imag"]))
    if isinstance(value, str):
        text = value.strip().replace("i", "j")
        try:
            return complex(text)
        except Exception:
            return complex(float(text))
    raise TypeError(f"Cannot coerce {value!r} into a complex number")


def number_to_jsonable(value: complex, real_tol: float = 1e-12) -> Any:
    """Convert a Python complex value into a JSON-safe scalar or object."""
    if abs(value.imag) < real_tol:
        return float(value.real)
    return {"real": float(value.real), "imag": float(value.imag)}


def pretty_complex(value: complex, digits: int = 12) -> str:
    """Format real and complex values compactly for human-readable tool output."""
    if abs(value.imag) < 1e-12:
        return f"{value.real:.{digits}g}"
    return f"{value.real:.{digits}g}{value.imag:+.{digits}g}j"


def safe_float_array(values: Sequence[Any]) -> np.ndarray:
    """Normalise an arbitrary sequence into a dense NumPy float array."""
    return np.asarray([float(v) for v in values], dtype=float)


# -----------------------------------------------------------------------------
# EML expression tree
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class EMLExpr:
    """Immutable EML expression tree node used throughout the slim server."""
    op: str
    value: Any = None
    left: Optional["EMLExpr"] = None
    right: Optional["EMLExpr"] = None

    def to_prefix(self) -> str:
        if self.op == "lit":
            v = self.value
            if isinstance(v, complex):
                return pretty_complex(v)
            return repr(v)
        if self.op == "var":
            return str(self.value)
        return f"eml({self.left.to_prefix()}, {self.right.to_prefix()})"

    def to_dict(self) -> Dict[str, Any]:
        if self.op in {"lit", "var"}:
            val = self.value
            if isinstance(val, complex):
                val = number_to_jsonable(val)
            return {"op": self.op, "value": val}
        return {"op": "eml", "left": self.left.to_dict(), "right": self.right.to_dict()}

    def node_count(self) -> int:
        if self.op in {"lit", "var"}:
            return 1
        return 1 + self.left.node_count() + self.right.node_count()

    def depth(self) -> int:
        if self.op in {"lit", "var"}:
            return 0
        return 1 + max(self.left.depth(), self.right.depth())


def lit(value: Any) -> EMLExpr:
    """Create a literal EML node from a numeric value."""
    return EMLExpr("lit", complex(value))


def var(name: str) -> EMLExpr:
    """Create a variable EML node."""
    return EMLExpr("var", name)


def eml(left: EMLExpr, right: EMLExpr) -> EMLExpr:
    """Create a binary EML operator node."""
    return EMLExpr("eml", None, left, right)


ONE = lit(1)
ZERO = lit(0)
NEG_ONE = lit(-1)
I_UNIT = lit(1j)
PI = lit(math.pi)
E_CONST = lit(math.e)
TWO = lit(2)
HALF = lit(0.5)


# -----------------------------------------------------------------------------
# EML parser
# -----------------------------------------------------------------------------

ALLOWED_CONSTS: Dict[str, complex] = {
    "e": complex(math.e),
    "pi": complex(math.pi),
    "I": 1j,
    "j": 1j,
    "inf": complex(float("inf"), 0.0),
    "nan": complex(float("nan"), 0.0),
}


class SafeEMLParser(ast.NodeVisitor):
    """Restricted parser for already-EML-style text."""
    def visit(self, node: ast.AST) -> EMLExpr:
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor is None:
            raise ValueError(f"Unsupported AST node: {node.__class__.__name__}")
        return visitor(node)

    def visit_Expression(self, node: ast.Expression) -> EMLExpr:
        return self.visit(node.body)

    def visit_Name(self, node: ast.Name) -> EMLExpr:
        if node.id in ALLOWED_CONSTS:
            return lit(ALLOWED_CONSTS[node.id])
        return var(node.id)

    def visit_Constant(self, node: ast.Constant) -> EMLExpr:
        if isinstance(node.value, (int, float, complex)):
            return lit(node.value)
        raise ValueError(f"Unsupported literal: {node.value!r}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> EMLExpr:
        operand = self.visit(node.operand)
        if operand.op != "lit":
            raise ValueError("Unary +/- is only allowed on numeric literals in EML syntax")
        if isinstance(node.op, ast.USub):
            return lit(-operand.value)
        if isinstance(node.op, ast.UAdd):
            return lit(+operand.value)
        raise ValueError("Unsupported unary operator")

    def visit_BinOp(self, node: ast.BinOp) -> EMLExpr:
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left.op != "lit" or right.op != "lit":
            raise ValueError("Binary arithmetic in EML syntax is only allowed for numeric literals")
        if isinstance(node.op, ast.Add):
            return lit(left.value + right.value)
        if isinstance(node.op, ast.Sub):
            return lit(left.value - right.value)
        if isinstance(node.op, ast.Mult):
            return lit(left.value * right.value)
        if isinstance(node.op, ast.Div):
            return lit(left.value / right.value)
        if isinstance(node.op, ast.Pow):
            return lit(left.value ** right.value)
        raise ValueError("Unsupported binary operator in numeric literal")

    def visit_Call(self, node: ast.Call) -> EMLExpr:
        if not isinstance(node.func, ast.Name) or node.func.id != "eml":
            raise ValueError("Only eml(a, b) calls are allowed in EML syntax")
        if len(node.args) != 2:
            raise ValueError("eml() requires exactly two arguments")
        return eml(self.visit(node.args[0]), self.visit(node.args[1]))


@lru_cache(maxsize=512)
def parse_eml_expr(expr_text: str) -> EMLExpr:
    """Parse a literal EML string into an immutable expression tree."""
    parsed = parse_cache.get(expr_text)
    if parsed is not None:
        return parsed
    tree = ast.parse(expr_text, mode="eval")
    expr = SafeEMLParser().visit(tree)
    parse_cache.set(expr_text, expr)
    return expr


# -----------------------------------------------------------------------------
# Compiler from SymPy -> EML
# -----------------------------------------------------------------------------

x_sym = sp.Symbol("x")
y_sym = sp.Symbol("y")
z_sym = sp.Symbol("z")


class EMLCompiler:
    """Practical compiler from a useful SymPy subset to EML trees.

    In default mode the compiler keeps numeric literals and selected constants as
    direct leaves for practicality. In pure mode it rewrites those constants into
    trees built from the distinguished constant 1 and the EML operator, while
    variables remain variable leaves.
    """

    def __init__(self, pure_mode: bool = False) -> None:
        self.symbol_cache: Dict[str, EMLExpr] = {}
        self.pure_mode = pure_mode
        self._pure_constant_cache: Dict[str, EMLExpr] = {}

    def compile_text(self, expr_text: str, pure: Optional[bool] = None) -> EMLExpr:
        """Parse ordinary infix maths, simplify it with SymPy, then lower to EML."""
        use_pure = self.pure_mode if pure is None else bool(pure)
        key = stable_key("compile_text", expr_text, use_pure)
        cached = compile_cache.get(key)
        if cached is not None:
            return cached

        transformations = sp.parsing.sympy_parser.standard_transformations + (
            sp.parsing.sympy_parser.implicit_multiplication_application,
            sp.parsing.sympy_parser.convert_xor,
        )
        expr = sp.parsing.sympy_parser.parse_expr(
            expr_text,
            transformations=transformations,
            local_dict={'e': sp.E, 'E': sp.E, 'pi': sp.pi, 'π': sp.pi, 'I': sp.I},
            evaluate=True,
        )
        compiled = self.compile_sympy(sp.simplify(expr), pure=use_pure)
        compile_cache.set(key, compiled)
        return compiled

    def compile_sympy(self, expr: sp.Expr, pure: Optional[bool] = None) -> EMLExpr:
        """Lower a SymPy expression tree into either practical or pure EML."""
        use_pure = self.pure_mode if pure is None else bool(pure)
        if expr == sp.E:
            return self.e_const() if use_pure else E_CONST
        if expr == sp.pi:
            return self.pi_const() if use_pure else PI
        if expr == sp.I:
            return self.i_unit() if use_pure else I_UNIT
        if expr.is_Number:
            return self.number_literal(expr, pure=use_pure)
        if expr.is_Symbol:
            name = str(expr)
            if name not in self.symbol_cache:
                self.symbol_cache[name] = var(name)
            return self.symbol_cache[name]
        if isinstance(expr, sp.Add):
            args = [self.compile_sympy(a, pure=use_pure) for a in expr.args]
            out = args[0]
            for arg in args[1:]:
                out = self.add(out, arg)
            return out
        if isinstance(expr, sp.Mul):
            args = [self.compile_sympy(a, pure=use_pure) for a in expr.args]
            out = args[0]
            for arg in args[1:]:
                out = self.mul(out, arg)
            return out
        if isinstance(expr, sp.Pow):
            base, exponent = expr.args
            return self.pow(self.compile_sympy(base, pure=use_pure), self.compile_sympy(exponent, pure=use_pure))
        if expr.func == sp.exp:
            return self.exp(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.log:
            if len(expr.args) == 1:
                return self.log(self.compile_sympy(expr.args[0], pure=use_pure))
            return self.div(self.log(self.compile_sympy(expr.args[0], pure=use_pure)), self.log(self.compile_sympy(expr.args[1], pure=use_pure)))
        if expr.func == sp.sqrt:
            return self.sqrt(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.sin:
            return self.sin(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.cos:
            return self.cos(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.tan:
            return self.tan(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.asin:
            return self.asin(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.acos:
            return self.acos(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.atan:
            return self.atan(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.sinh:
            return self.sinh(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.cosh:
            return self.cosh(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.tanh:
            return self.tanh(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.asinh:
            return self.asinh(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.acosh:
            return self.acosh(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.atanh:
            return self.atanh(self.compile_sympy(expr.args[0], pure=use_pure))
        if expr.func == sp.Abs:
            return self.sqrt(self.mul(self.compile_sympy(expr.args[0], pure=use_pure), self.compile_sympy(expr.args[0], pure=use_pure)))
        if expr.func == sp.sign:
            raise ValueError("sign() is not supported by this practical EML compiler")
        raise ValueError(f"Unsupported SymPy expression/function: {expr.func} ({expr!s})")

    # --- Pure-mode constant construction ---

    def one(self) -> EMLExpr:
        return ONE

    def zero(self) -> EMLExpr:
        if not self.pure_mode:
            return ZERO
        if 'zero' not in self._pure_constant_cache:
            self._pure_constant_cache['zero'] = eml(self.one(), eml(eml(self.one(), self.one()), self.one()))
        return self._pure_constant_cache['zero']

    def neg_one(self) -> EMLExpr:
        if not self.pure_mode:
            return NEG_ONE
        if 'neg_one' not in self._pure_constant_cache:
            self._pure_constant_cache['neg_one'] = self.sub(self.zero(), self.one())
        return self._pure_constant_cache['neg_one']

    def two(self) -> EMLExpr:
        if not self.pure_mode:
            return TWO
        if 'two' not in self._pure_constant_cache:
            self._pure_constant_cache['two'] = self.add(self.one(), self.one())
        return self._pure_constant_cache['two']

    def half(self) -> EMLExpr:
        if not self.pure_mode:
            return HALF
        if 'half' not in self._pure_constant_cache:
            self._pure_constant_cache['half'] = self.div(self.one(), self.two())
        return self._pure_constant_cache['half']

    def i_unit(self) -> EMLExpr:
        if not self.pure_mode:
            return I_UNIT
        if 'i' not in self._pure_constant_cache:
            self._pure_constant_cache['i'] = self.sqrt(self.neg_one())
        return self._pure_constant_cache['i']

    def e_const(self) -> EMLExpr:
        if not self.pure_mode:
            return E_CONST
        if 'e' not in self._pure_constant_cache:
            self._pure_constant_cache['e'] = self.exp(self.one())
        return self._pure_constant_cache['e']

    def pi_const(self) -> EMLExpr:
        if not self.pure_mode:
            return PI
        if 'pi' not in self._pure_constant_cache:
            self._pure_constant_cache['pi'] = self.mul(self.from_integer(4), self.atan(self.one()))
        return self._pure_constant_cache['pi']

    def from_integer(self, n: int) -> EMLExpr:
        if not self.pure_mode:
            return lit(n)
        key = f'int:{n}'
        if key in self._pure_constant_cache:
            return self._pure_constant_cache[key]
        if n == 1:
            out = self.one()
        elif n == 0:
            out = self.zero()
        elif n < 0:
            out = self.sub(self.zero(), self.from_integer(-n))
        else:
            out = self.one()
            for _ in range(1, n):
                out = self.add(out, self.one())
        self._pure_constant_cache[key] = out
        return out

    def from_fraction(self, frac: Fraction) -> EMLExpr:
        if not self.pure_mode:
            return lit(frac.numerator / frac.denominator)
        frac = Fraction(frac.numerator, frac.denominator)
        key = f'frac:{frac.numerator}/{frac.denominator}'
        if key in self._pure_constant_cache:
            return self._pure_constant_cache[key]
        num = self.from_integer(frac.numerator)
        den = self.from_integer(frac.denominator)
        out = self.div(num, den)
        self._pure_constant_cache[key] = out
        return out

    def number_literal(self, expr: sp.Expr, pure: bool = False) -> EMLExpr:
        if not pure:
            return lit(complex(expr.evalf()))
        cval = complex(expr.evalf(50))
        if abs(cval.imag) < 1e-15:
            frac = Fraction(str(float(cval.real))).limit_denominator(1000000)
            return self.from_fraction(frac)
        real_part = self.number_literal(sp.Float(cval.real), pure=True)
        imag_part = self.number_literal(sp.Float(cval.imag), pure=True)
        return self.add(real_part, self.mul(imag_part, self.i_unit()))

    # --- Core EML primitives and helper algebra ---

    def exp(self, a: EMLExpr) -> EMLExpr:
        """Construct `exp(a)` in EML form."""
        return eml(a, self.one())

    def log(self, a: EMLExpr) -> EMLExpr:
        """Construct `log(a)` in EML form using the practical encoding used here."""
        if a.op == "lit" and abs(complex(a.value)) == 0:
            return lit(complex(float("-inf"), 0.0))
        return eml(self.one(), eml(eml(self.one(), a), self.one()))

    def sub(self, a: EMLExpr, b: EMLExpr) -> EMLExpr:
        """Construct `a - b` in EML form."""
        return eml(self.log(a), self.exp(b))

    def neg(self, a: EMLExpr) -> EMLExpr:
        """Construct `-a` in EML form."""
        return self.sub(self.zero(), a)

    def add(self, a: EMLExpr, b: EMLExpr) -> EMLExpr:
        """Construct `a + b` in EML form."""
        return self.sub(a, self.neg(b))

    def mul(self, a: EMLExpr, b: EMLExpr) -> EMLExpr:
        """Construct `a * b` in EML form."""
        return self.exp(self.add(self.log(a), self.log(b)))

    def div(self, a: EMLExpr, b: EMLExpr) -> EMLExpr:
        """Construct `a / b` in EML form."""
        return self.exp(self.sub(self.log(a), self.log(b)))

    def pow(self, a: EMLExpr, b: EMLExpr) -> EMLExpr:
        """Construct `a ** b` in EML form."""
        return self.exp(self.mul(b, self.log(a)))

    def sqrt(self, a: EMLExpr) -> EMLExpr:
        """Construct `sqrt(a)` in EML form."""
        return self.pow(a, self.half())

    def sin(self, a: EMLExpr) -> EMLExpr:
        """Construct `sin(a)` in EML form via exponential identities."""
        ia = self.mul(self.i_unit(), a)
        num = self.sub(self.exp(ia), self.exp(self.neg(ia)))
        den = self.mul(self.two(), self.i_unit())
        return self.div(num, den)

    def cos(self, a: EMLExpr) -> EMLExpr:
        """Construct `cos(a)` in EML form via exponential identities."""
        ia = self.mul(self.i_unit(), a)
        num = self.add(self.exp(ia), self.exp(self.neg(ia)))
        return self.div(num, self.two())

    def tan(self, a: EMLExpr) -> EMLExpr:
        """Construct `tan(a)` in EML form."""
        return self.div(self.sin(a), self.cos(a))

    def sinh(self, a: EMLExpr) -> EMLExpr:
        """Construct `sinh(a)` in EML form."""
        num = self.sub(self.exp(a), self.exp(self.neg(a)))
        return self.div(num, self.two())

    def cosh(self, a: EMLExpr) -> EMLExpr:
        """Construct `cosh(a)` in EML form."""
        num = self.add(self.exp(a), self.exp(self.neg(a)))
        return self.div(num, self.two())

    def tanh(self, a: EMLExpr) -> EMLExpr:
        """Construct `tanh(a)` in EML form."""
        return self.div(self.sinh(a), self.cosh(a))

    def asin(self, a: EMLExpr) -> EMLExpr:
        """Construct `asin(a)` in EML form."""
        inner = self.add(self.mul(self.i_unit(), a), self.sqrt(self.sub(self.one(), self.mul(a, a))))
        return self.mul(self.neg(self.i_unit()), self.log(inner))

    def acos(self, a: EMLExpr) -> EMLExpr:
        """Construct `acos(a)` in EML form."""
        inner = self.add(a, self.mul(self.i_unit(), self.sqrt(self.sub(self.one(), self.mul(a, a)))))
        return self.mul(self.neg(self.i_unit()), self.log(inner))

    def atan(self, a: EMLExpr) -> EMLExpr:
        """Construct `atan(a)` in EML form."""
        left = self.log(self.sub(self.one(), self.mul(self.i_unit(), a)))
        right = self.log(self.add(self.one(), self.mul(self.i_unit(), a)))
        diff = self.sub(left, right)
        return self.mul(self.div(self.i_unit(), self.two()), diff)

    def asinh(self, a: EMLExpr) -> EMLExpr:
        """Construct `asinh(a)` in EML form."""
        return self.log(self.add(a, self.sqrt(self.add(self.mul(a, a), self.one()))))

    def acosh(self, a: EMLExpr) -> EMLExpr:
        """Construct `acosh(a)` in EML form."""
        part = self.mul(self.sqrt(self.sub(a, self.one())), self.sqrt(self.add(a, self.one())))
        return self.log(self.add(a, part))

    def atanh(self, a: EMLExpr) -> EMLExpr:
        """Construct `atanh(a)` in EML form."""
        num = self.log(self.div(self.add(self.one(), a), self.sub(self.one(), a)))
        return self.mul(self.half(), num)


COMPILER = EMLCompiler(pure_mode=False)
PURE_COMPILER = EMLCompiler(pure_mode=True)



# -----------------------------------------------------------------------------
# Evaluation, simplification, tracing
# -----------------------------------------------------------------------------

def _eval_eml(expr: EMLExpr, bindings: Dict[str, complex], memo: Dict[EMLExpr, complex], trace: Optional[List[Dict[str, Any]]] = None) -> complex:
    """Recursively evaluate an EML tree, optionally capturing per-node trace data."""
    if expr in memo:
        return memo[expr]

    if expr.op == "lit":
        out = complex(expr.value)
    elif expr.op == "var":
        if expr.value not in bindings:
            raise KeyError(f"Missing binding for variable '{expr.value}'")
        out = bindings[expr.value]
    else:
        xval = _eval_eml(expr.left, bindings, memo, trace)
        yval = _eval_eml(expr.right, bindings, memo, trace)
        out = cmath.exp(xval) - cmath.log(yval)
        if trace is not None:
            trace.append(
                {
                    "x": number_to_jsonable(xval),
                    "y": number_to_jsonable(yval),
                    "out": number_to_jsonable(out),
                }
            )
    memo[expr] = out
    return out


def evaluate_expr(expr: EMLExpr, bindings: Dict[str, Any]) -> complex:
    """Evaluate an EML tree numerically using the supplied variable bindings."""
    key = stable_key("eval", expr.to_prefix(), bindings)
    cached = eval_cache.get(key)
    if cached is not None:
        return cached
    b = {k: coerce_number(v) for k, v in bindings.items()}
    value = _eval_eml(expr, b, memo={})
    eval_cache.set(key, value)
    return value


def evaluate_with_trace(expr: EMLExpr, bindings: Dict[str, Any]) -> Tuple[complex, List[Dict[str, Any]]]:
    """Evaluate an EML tree and return both the value and an execution trace."""
    b = {k: coerce_number(v) for k, v in bindings.items()}
    trace: List[Dict[str, Any]] = []
    value = _eval_eml(expr, b, memo={}, trace=trace)
    return value, trace


def simplify_expr(expr: EMLExpr) -> EMLExpr:
    """Simplify an EML tree by recursively constant-folding literal subtrees."""
    key = stable_key("simplify", expr.to_prefix())
    cached = simplify_cache.get(key)
    if cached is not None:
        return cached

    def rec(node: EMLExpr) -> EMLExpr:
        if node.op in {"lit", "var"}:
            return node
        left = rec(node.left)
        right = rec(node.right)
        if left.op == "lit" and right.op == "lit":
            try:
                return lit(cmath.exp(left.value) - cmath.log(right.value))
            except Exception:
                return eml(left, right)
        return eml(left, right)

    out = rec(expr)
    simplify_cache.set(key, out)
    return out


def expr_from_auto(text: str, pure: bool = False) -> Tuple[EMLExpr, str]:
    """Detect whether input is literal EML or infix maths and return both forms."""
    stripped = text.strip()
    if stripped.startswith("eml("):
        return parse_eml_expr(stripped), "eml"
    compiler = PURE_COMPILER if pure else COMPILER
    return compiler.compile_text(stripped), "infix"


def analyse_tree_leaves(expr: EMLExpr) -> Dict[str, Any]:
    """Summarise literal and variable leaves, useful for pure-mode inspection."""
    literals: List[complex] = []
    variables: List[str] = []

    def walk(node: EMLExpr) -> None:
        if node.op == "lit":
            literals.append(complex(node.value))
            return
        if node.op == "var":
            variables.append(str(node.value))
            return
        walk(node.left)
        walk(node.right)

    walk(expr)
    non_one_literals = [v for v in literals if abs(v - 1) > 1e-12]
    return {
        "literal_count": len(literals),
        "variable_count": len(variables),
        "variables": sorted(set(variables)),
        "non_one_literal_count": len(non_one_literals),
        "non_one_literals": [number_to_jsonable(v) for v in non_one_literals[:16]],
        "is_one_only_constant_tree": len(non_one_literals) == 0,
    }


# -----------------------------------------------------------------------------
# Stability analysis
# -----------------------------------------------------------------------------

def _sample_bindings(base_bindings: Dict[str, Any], region: Optional[Dict[str, Any]], n: int = 9) -> List[Dict[str, complex]]:
    """Generate sample points for numerical stability analysis."""
    if region:
        samples: List[Dict[str, complex]] = []
        for i in range(n):
            point: Dict[str, complex] = {}
            for name, spec in region.items():
                if isinstance(spec, dict) and "min" in spec and "max" in spec:
                    lo = float(spec["min"])
                    hi = float(spec["max"])
                    if n == 1:
                        val = lo
                    else:
                        val = lo + (hi - lo) * (i / max(n - 1, 1))
                    point[name] = complex(val)
                else:
                    point[name] = coerce_number(spec)
            samples.append(point)
        return samples

    base = {k: coerce_number(v) for k, v in base_bindings.items()}
    if not base:
        return [{}]

    samples = [base]
    eps = 1e-6
    for name, val in base.items():
        plus = dict(base)
        minus = dict(base)
        plus[name] = val + eps
        minus[name] = val - eps
        samples.extend([plus, minus])
    return samples


def stability_check(expr: EMLExpr, bindings: Optional[Dict[str, Any]] = None, region: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Probe an expression over a region and return practical numerical-risk warnings.

    This is deliberately heuristic rather than formal. It is intended to help an
    LLM or developer notice likely domain, branch, overflow, and conditioning
    issues before treating a numeric result as trustworthy."""
    samples = _sample_bindings(bindings or {}, region, n=11)
    warnings: List[str] = []
    outputs: List[complex] = []
    trace_summary = {
        "near_zero_log_inputs": 0,
        "negative_real_log_inputs": 0,
        "large_exp_real_parts": 0,
        "huge_intermediate_outputs": 0,
        "errors": 0,
    }

    for sample in samples:
        try:
            result, trace = evaluate_with_trace(expr, sample)
            outputs.append(result)
            for step in trace:
                x = coerce_number(step["x"])
                y = coerce_number(step["y"])
                out = coerce_number(step["out"])
                if abs(y) < 1e-8:
                    trace_summary["near_zero_log_inputs"] += 1
                if abs(y.imag) < 1e-12 and y.real <= 0:
                    trace_summary["negative_real_log_inputs"] += 1
                if x.real > 700:
                    trace_summary["large_exp_real_parts"] += 1
                if abs(out) > 1e12:
                    trace_summary["huge_intermediate_outputs"] += 1
        except Exception:
            trace_summary["errors"] += 1

    if trace_summary["near_zero_log_inputs"]:
        warnings.append("Some internal log() inputs approach zero; this can cause blow-up or discontinuities.")
    if trace_summary["negative_real_log_inputs"]:
        warnings.append("Some internal log() inputs cross the negative real axis; principal-branch behavior may introduce jumps.")
    if trace_summary["large_exp_real_parts"]:
        warnings.append("Some internal exp() inputs have large positive real parts; overflow risk is elevated.")
    if trace_summary["huge_intermediate_outputs"]:
        warnings.append("Some intermediate values are extremely large; numerical instability is likely.")
    if trace_summary["errors"]:
        warnings.append("Some samples raised evaluation errors; the expression may be ill-posed on part of the requested region.")

    cond_estimate = None
    if len(outputs) >= 3:
        mags = np.asarray([abs(v) for v in outputs], dtype=float)
        if np.all(np.isfinite(mags)) and mags.size:
            cond_estimate = float((mags.max() + 1e-12) / (mags.min() + 1e-12))
            if cond_estimate > 1e6:
                warnings.append("The sampled output range spans many orders of magnitude; conditioning looks poor.")

    return {
        "node_count": expr.node_count(),
        "depth": expr.depth(),
        "samples_checked": len(samples),
        "condition_proxy": cond_estimate,
        "trace_summary": trace_summary,
        "warnings": warnings,
    }


# -----------------------------------------------------------------------------
# Heuristic symbolic fitting layer
# -----------------------------------------------------------------------------

FIT_FAMILIES: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    "constant": ("c", ("c",)),
    "linear": ("a*x + b", ("a", "b")),
    "quadratic": ("a*x**2 + b*x + c", ("a", "b", "c")),
    "cubic": ("a*x**3 + b*x**2 + c*x + d", ("a", "b", "c", "d")),
    "exp_affine": ("a*exp(b*x) + c", ("a", "b", "c")),
    "log_affine": ("a*log(b*x + c) + d", ("a", "b", "c", "d")),
    "power_affine": ("a*(x**b) + c", ("a", "b", "c")),
    "sqrt_affine": ("a*sqrt(b*x + c) + d", ("a", "b", "c", "d")),
    "reciprocal_affine": ("a/(b*x + c) + d", ("a", "b", "c", "d")),
    "sin_affine": ("a*sin(b*x + c) + d", ("a", "b", "c", "d")),
    "cos_affine": ("a*cos(b*x + c) + d", ("a", "b", "c", "d")),
    "tanh_affine": ("a*tanh(b*x + c) + d", ("a", "b", "c", "d")),
}


@dataclass
class FitResult:
    family: str
    formula: str
    params: Dict[str, float]
    mse: float
    r2: float


def _initial_guess(param_names: Sequence[str], x: np.ndarray, y: np.ndarray) -> List[float]:
    """Generate pragmatic starting guesses for nonlinear curve fitting."""
    y_span = float(np.nanmax(y) - np.nanmin(y)) if y.size else 1.0
    y_mean = float(np.nanmean(y)) if y.size else 0.0
    x_span = float(np.nanmax(x) - np.nanmin(x)) if x.size else 1.0
    guesses = []
    for p in param_names:
        if p == "a":
            guesses.append(y_span if y_span > 1e-9 else 1.0)
        elif p == "b":
            guesses.append(1.0 / x_span if x_span > 1e-9 else 1.0)
        elif p == "c":
            guesses.append(max(y_mean, 0.5) if y_mean != 0 else 1.0)
        elif p == "d":
            guesses.append(y_mean)
        else:
            guesses.append(1.0)
    return guesses


def _fit_one_family(family: str, x: np.ndarray, y: np.ndarray) -> Optional[FitResult]:
    """Fit one candidate symbolic family and score its numerical quality."""
    formula, params = FIT_FAMILIES[family]
    x_symbol = sp.Symbol("x")
    param_symbols = [sp.Symbol(p) for p in params]
    expr = sp.parse_expr(formula, evaluate=True)
    fn = sp.lambdify((x_symbol, *param_symbols), expr, modules=["numpy"])

    p0 = _initial_guess(params, x, y)
    try:
        popt, _ = curve_fit(lambda xx, *pp: fn(xx, *pp), x, y, p0=p0, maxfev=20000)
        y_hat = np.asarray(fn(x, *popt), dtype=float)
        if not np.all(np.isfinite(y_hat)):
            return None
        mse = float(np.mean((y - y_hat) ** 2))
        ss_res = float(np.sum((y - y_hat) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2)) + 1e-12
        r2 = 1.0 - ss_res / ss_tot
        param_map = {name: float(value) for name, value in zip(params, popt)}
        pretty = formula
        for name, value in param_map.items():
            pretty = pretty.replace(name, f"({value:.8g})")
        return FitResult(family=family, formula=pretty, params=param_map, mse=mse, r2=r2)
    except Exception:
        return None


def eml_fit(x_values: Sequence[Any], y_values: Sequence[Any], families: Optional[Sequence[str]] = None, top_k: int = 5) -> Dict[str, Any]:
    """Fit multiple candidate families, rank them, and compile the best to EML."""
    key = stable_key("fit", list(x_values), list(y_values), list(families or []), top_k)
    cached = fit_cache.get(key)
    if cached is not None:
        return cached

    x = safe_float_array(x_values)
    y = safe_float_array(y_values)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size < 3:
        raise ValueError("x_values and y_values must be one-dimensional arrays of equal length >= 3")

    fams = list(families) if families else list(FIT_FAMILIES.keys())
    results: List[FitResult] = []
    for family in fams:
        if family not in FIT_FAMILIES:
            continue
        fit = _fit_one_family(family, x, y)
        if fit is not None and np.isfinite(fit.mse):
            results.append(fit)

    if not results:
        raise RuntimeError("No candidate families could be fit to the dataset")

    results.sort(key=lambda item: (item.mse, -item.r2))
    best = results[0]
    best_eml = COMPILER.compile_text(best.formula)
    payload = {
        "best_family": best.family,
        "best_formula": best.formula,
        "best_formula_eml": best_eml.to_prefix(),
        "best_metrics": {"mse": best.mse, "r2": best.r2},
        "top_candidates": [
            {
                "family": r.family,
                "formula": r.formula,
                "mse": r.mse,
                "r2": r.r2,
            }
            for r in results[:top_k]
        ],
    }
    fit_cache.set(key, payload)
    return payload


# -----------------------------------------------------------------------------
# Resources and prompts
# -----------------------------------------------------------------------------

def tool_eml_compile(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool wrapper for compiling ordinary maths into an EML tree."""
    expr_text = str(arguments["target_expr"])
    pure = bool(arguments.get("pure", False))
    compiler = PURE_COMPILER if pure else COMPILER
    expr = compiler.compile_text(expr_text)
    simplified = expr if pure and arguments.get("simplify", True) else (simplify_expr(expr) if arguments.get("simplify", True) else expr)
    return {
        "source_expression": expr_text,
        "eml_expression": expr.to_prefix(),
        "simplified_eml_expression": simplified.to_prefix(),
        "tree": expr.to_dict(),
        "node_count": expr.node_count(),
        "depth": expr.depth(),
        "pure_mode": pure,
        "leaf_analysis": analyse_tree_leaves(expr),
    }


def tool_eml_eval(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool wrapper for evaluating either EML or infix expressions."""
    expr_text = str(arguments["expr"])
    bindings = dict(arguments.get("bindings", {}))
    pure = bool(arguments.get("pure", False))
    expr, mode = expr_from_auto(expr_text, pure=pure)
    value = evaluate_expr(expr, bindings)
    return {
        "mode": mode,
        "expr": expr.to_prefix(),
        "bindings": {k: number_to_jsonable(coerce_number(v)) for k, v in bindings.items()},
        "value": number_to_jsonable(value),
        "value_pretty": pretty_complex(value),
        "pure_mode": pure,
    }


def tool_eml_simplify(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool wrapper for EML simplification and size/depth reporting."""
    expr_text = str(arguments["expr"])
    pure = bool(arguments.get("pure", False))
    expr, mode = expr_from_auto(expr_text, pure=pure)
    simplified = expr if pure else simplify_expr(expr)
    result = {
        "mode": mode,
        "original": expr.to_prefix(),
        "simplified": simplified.to_prefix(),
        "original_node_count": expr.node_count(),
        "simplified_node_count": simplified.node_count(),
        "original_depth": expr.depth(),
        "simplified_depth": simplified.depth(),
        "pure_mode": pure,
    }
    if pure:
        result["note"] = "Pure mode preserves 1-only constant construction, so literal constant folding is skipped."
    return result


def tool_eml_stability_check(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool wrapper for region-based numerical risk analysis."""
    expr_text = str(arguments["expr"])
    bindings = dict(arguments.get("bindings", {}))
    region = arguments.get("region")
    pure = bool(arguments.get("pure", False))
    expr, mode = expr_from_auto(expr_text, pure=pure)
    report = stability_check(expr, bindings=bindings, region=region)
    report["mode"] = mode
    report["expr"] = expr.to_prefix()
    report["pure_mode"] = pure
    return report


def tool_eml_fit(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool wrapper for symbolic-regression style fitting into EML."""
    x_values = arguments["x_values"]
    y_values = arguments["y_values"]
    families = arguments.get("families")
    top_k = int(arguments.get("top_k", 5))
    pure = bool(arguments.get("pure", False))
    result = eml_fit(x_values, y_values, families=families, top_k=top_k)
    if pure:
        pure_expr = PURE_COMPILER.compile_text(result["best_formula"])
        result["best_formula_eml_pure"] = pure_expr.to_prefix()
    best_expr = parse_eml_expr(result["best_formula_eml"])
    result["best_formula_stability"] = stability_check(best_expr, region={"x": {"min": float(min(x_values)), "max": float(max(x_values))}})
    return result




# -----------------------------------------------------------------------------
# Generalized EML family tools (concise family surface)
# -----------------------------------------------------------------------------

EML_FAMILY_LIBRARY: Dict[str, Dict[str, Any]] = {
    'original_eml': {
        'display_name': 'Original EML',
        'operator_formula': 'S(x, y) = exp(x) - ln(y)',
        'f_name': 'exp', 'g_name': 'ln',
        'neutral_element': '0', 'seed_constant': '1', 'seed_condition': 'ln(1)=0',
        'group_law': 'A ⊞ B = A + B', 'inverse_map': 'ι(A) = -A',
        'addition_formula': 'exp(x+y) = exp(x) exp(y)',
        'derived_operations': ['multiplication', 'division', 'powers', 'trigonometric families'],
        'recoverable_functions': ['exp', 'ln', 'subtraction', 'addition', 'multiplication', 'division', 'powers'],
        'requires_external_constant': True, 'constant_free_candidate': False,
        'notes': 'Canonical EML family from Odrzywołek, algebraically unpacked by Stachowiak.',
        'limitations': ['Branch cuts and inverse-cancellation caveats remain through the logarithm.'],
    },
    'cosine_arccos': {
        'display_name': 'Cosine / arccos family',
        'operator_formula': 'S(x, y) = cos(x) - arccos(y)',
        'f_name': 'cos', 'g_name': 'arccos',
        'neutral_element': '0', 'seed_constant': '1', 'seed_condition': 'arccos(1)=0',
        'group_law': 'A ⊞ B = A + B', 'inverse_map': 'ι(A) = -A',
        'addition_formula': 'cos(a+b) + cos(a-b) = 2 cos(a) cos(b)',
        'derived_operations': ['scaled multiplication F(x,y)=2xy', 'Chebyshev polynomials'],
        'recoverable_functions': ['cos', 'arccos', 'addition', 'subtraction', 'sin via phase shift', 'Chebyshev polynomials'],
        'requires_external_constant': True, 'constant_free_candidate': False,
        'notes': 'Good family for trigonometric DSL generation.',
        'limitations': ['Ordinary multiplication is not recovered without extra constants or operations.'],
    },
    'arccot_cot': {
        'display_name': 'arccot / cot family',
        'operator_formula': 'S(x, y) = arccot(x) - cot(y)',
        'f_name': 'arccot', 'g_name': 'cot',
        'neutral_element': '0', 'seed_constant': 'pi/2', 'seed_condition': 'cot(pi/2)=0',
        'group_law': 'A ⊞ B = A + B', 'inverse_map': 'ι(A) = -A',
        'addition_formula': 'tan(a+b) = (tan(a)+tan(b)) / (1 - tan(a) tan(b))',
        'derived_operations': ['fractional-linear composition F(x,y)=(x+y)/(1-xy)', 'reciprocal 1/x'],
        'recoverable_functions': ['arccot', 'cot', 'tan', 'reciprocal 1/x', 'addition', 'subtraction'],
        'requires_external_constant': True, 'constant_free_candidate': False,
        'notes': 'Illustrates a non-multiplicative addition law.',
        'limitations': ['The recovered addition law does not directly yield ordinary multiplication.'],
    },
    'tanh_artanh': {
        'display_name': 'tanh / artanh family',
        'operator_formula': 'S(x, y) = tanh(x) - artanh(y)',
        'f_name': 'tanh', 'g_name': 'artanh',
        'neutral_element': '0', 'seed_constant': '0', 'seed_condition': 'artanh(0)=0',
        'group_law': 'A ⊞ B = A + B', 'inverse_map': 'ι(A) = -A',
        'addition_formula': 'tanh(a+b) = (tanh(a)+tanh(b)) / (1 + tanh(a) tanh(b))',
        'derived_operations': ['relativistic velocity addition F(x,y)=(x+y)/(1+xy)'],
        'recoverable_functions': ['tanh', 'artanh', 'addition', 'subtraction', 'Lorentz-boost-style composition'],
        'requires_external_constant': True, 'constant_free_candidate': False,
        'notes': 'Compact language for Lorentz-boost-style composition.',
        'limitations': ['No direct route to ordinary multiplication in the recovered language.'],
    },
    'elliptic_pair': {
        'display_name': 'Weierstrass elliptic pair',
        'operator_formula': "S(z,t)=℘(z)-℘⁻¹(t), paired with R(z,t)=℘′(z)-(℘′)⁻¹(t)",
        'f_name': "℘ and ℘′", 'g_name': 'formal inverses',
        'neutral_element': '0', 'seed_constant': '∞', 'seed_condition': 'formal on a restricted subdomain',
        'group_law': 'Elliptic-curve point addition P1 ⊞ P2 = P3', 'inverse_map': 'Point inversion on the elliptic curve',
        'addition_formula': '℘(u+v) = Q(℘(u),℘(v),℘′(u),℘′(v)) with rational Q',
        'derived_operations': ['elliptic-curve group law using a paired-operator language'],
        'recoverable_functions': ['℘', '℘′', 'addition/subtraction on curve parameters', 'elliptic-curve point arithmetic'],
        'requires_external_constant': True, 'constant_free_candidate': False,
        'notes': 'Key multi-operator example from the follow-up paper.',
        'limitations': ['Requires two coordinated operators and restricted domains.'],
    },
    'involutive_piecewise': {
        'display_name': 'Involutive piecewise family',
        'operator_formula': 'S(x, y) = f(x) - f(y) with a piecewise involution f(f(x))=x',
        'f_name': 'piecewise involution', 'g_name': 'same as f',
        'neutral_element': '0', 'seed_constant': '0', 'seed_condition': 'f(0)=0',
        'group_law': 'A ⊞ B = A + B', 'inverse_map': 'ι(A) = -A',
        'addition_formula': 'f(x+y) yields a bilinear ts+t+s structure on (-1,0)',
        'derived_operations': ['restricted multiplication ts = f(f(s)+f(t)) - t - s on (-1,0)'],
        'recoverable_functions': ['f', 'addition', 'subtraction', 'restricted-domain multiplication'],
        'requires_external_constant': False, 'constant_free_candidate': True,
        'notes': 'Strongest constant-free candidate discussed in the note.',
        'limitations': ['Works only on a narrow domain and does not obviously recover division or universality.'],
    },
}


def _get_eml_family_spec(name: str) -> Dict[str, Any]:
    name = str(name).strip()
    if name not in EML_FAMILY_LIBRARY:
        raise KeyError(f'Unknown EML family: {name}')
    return json.loads(json.dumps(EML_FAMILY_LIBRARY[name]))


def tool_eml_family_library(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """List the built-in generalized EML families or inspect one family."""
    family = arguments.get('family')
    if family:
        spec = _get_eml_family_spec(str(family))
        spec['family'] = str(family)
        return spec
    return {
        'families': [
            {
                'family': name,
                'display_name': spec['display_name'],
                'operator_formula': spec['operator_formula'],
                'requires_external_constant': spec['requires_external_constant'],
                'constant_free_candidate': spec['constant_free_candidate'],
            }
            for name, spec in EML_FAMILY_LIBRARY.items()
        ],
        'notes': [
            'Curated family templates based on the algebraic-structure follow-up paper.',
            'These tools expose the family metadata and symbolic recovery roadmap rather than proving arbitrary user-defined operators.',
        ],
    }


def tool_eml_extract_group_structure(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Expose the hidden abelian-group data behind a built-in generalized EML family."""
    family = str(arguments['family'])
    spec = _get_eml_family_spec(family)
    return {
        'family': family,
        'display_name': spec['display_name'],
        'operator_formula': spec['operator_formula'],
        'neutral_element': spec['neutral_element'],
        'inverse_map': spec['inverse_map'],
        'group_law': spec['group_law'],
        'axioms': {'neutral_element': True, 'self_cancellation': True, 'anti_associativity': True},
        'notes': [
            'Reports the symbolic group data associated with the chosen built-in family.',
            'The follow-up paper shows that the subtraction-like M induces an abelian group through A ⊞ B := M(A, M(e, B)).',
        ],
        'limitations': spec['limitations'],
    }


def tool_eml_recover_core_family(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the six-step constructive recovery chain from the follow-up paper."""
    family = str(arguments['family'])
    spec = _get_eml_family_spec(family)
    f_name, g_name = spec['f_name'], spec['g_name']
    steps = [
        {'step': 1, 'name': 'recover_f', 'construction': 'S(x, c)', 'result': f'{f_name}(x)', 'note': f'Uses c={spec["seed_constant"]} with {spec["seed_condition"]}.'},
        {'step': 2, 'name': 'recover_f_minus_y', 'construction': f'S(x, {f_name}(y))', 'result': f'{f_name}(x) ⊟ y', 'note': 'Feeds an already recovered f(y) back into the second argument.'},
        {'step': 3, 'name': 'recover_inverse_g', 'construction': 'f2(z, S(z, x))', 'result': f'{g_name}(x)', 'note': 'Generic inverse-recovery step.'},
        {'step': 4, 'name': 'recover_subtraction_like_operation', 'construction': f'S({g_name}(x), {f_name}(y))', 'result': 'x ⊟ y', 'note': 'Makes the underlying subtraction-like operation explicit.'},
        {'step': 5, 'name': 'recover_inverse_map', 'construction': '(x ⊟ y) ⊟ x', 'result': spec['inverse_map'], 'note': 'Recovers the inverse map ι associated with the hidden group.'},
        {'step': 6, 'name': 'recover_group_law', 'construction': 'x ⊟ ι(y)', 'result': spec['group_law'], 'note': 'Recovers the induced abelian-group law.'},
    ]
    return {
        'family': family,
        'display_name': spec['display_name'],
        'seed_constant': spec['seed_constant'],
        'seed_condition': spec['seed_condition'],
        'steps': steps,
        'recoverable_functions': spec['recoverable_functions'],
        'notes': ['Symbolic roadmap for the built-in families rather than an arbitrary solver over user-defined operators.'],
    }


def tool_eml_generate_from_addition_formula(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Report the family-specific addition formula and what it can generate."""
    family = str(arguments['family'])
    spec = _get_eml_family_spec(family)
    return {
        'family': family,
        'display_name': spec['display_name'],
        'addition_formula': spec['addition_formula'],
        'derived_operations': spec['derived_operations'],
        'recoverable_functions': spec['recoverable_functions'],
        'limitations': spec['limitations'],
        'notes': ['Different families generate different downstream operations: original EML reaches multiplication and powers, while others stop at narrower compositions.'],
    }


def tool_eml_constant_free_scan(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Summarise constant-free candidates and the open constant-free question."""
    candidates = [
        {
            'family': name,
            'display_name': spec['display_name'],
            'operator_formula': spec['operator_formula'],
            'notes': spec['notes'],
            'limitations': spec['limitations'],
        }
        for name, spec in EML_FAMILY_LIBRARY.items() if spec.get('constant_free_candidate')
    ]
    return {
        'open_problem': True,
        'question': 'Is there a single constant-free universal generator with the simplicity of EML?',
        'constant_free_candidates': candidates,
        'notes': [
            'The follow-up paper leaves the constant-free universal generator question open.',
            'This tool reports curated candidates and limitations rather than claiming to solve that open problem.',
        ],
    }


def tool_eml_explore_family(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience aggregation of family metadata, group structure, recovery, and addition-law consequences."""
    family = str(arguments['family'])
    spec = _get_eml_family_spec(family)
    return {
        'family': family,
        'display_name': spec['display_name'],
        'operator_formula': spec['operator_formula'],
        'group_structure': tool_eml_extract_group_structure({'family': family}),
        'recovery_chain': tool_eml_recover_core_family({'family': family})['steps'],
        'addition_formula': spec['addition_formula'],
        'derived_operations': spec['derived_operations'],
        'recoverable_functions': spec['recoverable_functions'],
        'requires_external_constant': spec['requires_external_constant'],
        'constant_free_candidate': spec['constant_free_candidate'],
        'limitations': spec['limitations'],
        'notes': ['Convenience view for LLM/tool use; packages the core structural ideas into one response.'],
    }




# -----------------------------------------------------------------------------
# SymPy bridge (slim edition)
# -----------------------------------------------------------------------------

sympy_eval_cache = TTLCache(maxsize=256, ttl_seconds=1800)


def _sympy_local_dict() -> Dict[str, Any]:
    """Return the controlled local namespace used by the SymPy parser."""
    d: Dict[str, Any] = {
        'pi': sp.pi,
        'π': sp.pi,
        'e': sp.E,
        'E': sp.E,
        'tau': 2 * sp.pi,
        'I': sp.I,
        'oo': sp.oo,
        'sin': sp.sin,
        'cos': sp.cos,
        'tan': sp.tan,
        'asin': sp.asin,
        'acos': sp.acos,
        'atan': sp.atan,
        'sinh': sp.sinh,
        'cosh': sp.cosh,
        'tanh': sp.tanh,
        'exp': sp.exp,
        'log': sp.log,
        'ln': sp.log,
        'sqrt': sp.sqrt,
        'Abs': sp.Abs,
        'abs': sp.Abs,
        're': sp.re,
        'im': sp.im,
    }
    for name in list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        d[name] = sp.Symbol(name)
    for name in ['alpha', 'beta', 'gamma', 'delta', 'theta', 'phi', 'lam', 'lambda_']:
        d[name] = sp.Symbol(name)
    return d


def sympy_expr_from_text(expr_text: str, extra_locals: Optional[Dict[str, Any]] = None) -> sp.Expr:
    """Parse conventional maths text into a SymPy expression."""
    key = stable_key('sympy-expr', expr_text, extra_locals or {})
    cached = sympy_eval_cache.get(key)
    if cached is not None and isinstance(cached, sp.Expr):
        return cached
    transformations = sp.parsing.sympy_parser.standard_transformations + (
        sp.parsing.sympy_parser.implicit_multiplication_application,
        sp.parsing.sympy_parser.convert_xor,
    )
    local_dict = _sympy_local_dict()
    if extra_locals:
        local_dict.update(extra_locals)
    expr = sp.parsing.sympy_parser.parse_expr(
        str(expr_text),
        transformations=transformations,
        local_dict=local_dict,
        evaluate=True,
    )
    sympy_eval_cache.set(key, expr)
    return expr


def sympy_bindings_from_json(bindings: Dict[str, Any]) -> Dict[sp.Symbol, Any]:
    """Convert JSON-style bindings into a SymPy substitution dictionary."""
    out: Dict[sp.Symbol, Any] = {}
    for k, v in bindings.items():
        out[sp.Symbol(str(k))] = sp.sympify(v)
    return out


def sympy_numeric_to_complex(value: Any) -> complex:
    """Normalise a SymPy numeric result into Python complex form."""
    try:
        return complex(sp.N(value, 40))
    except Exception:
        return complex(complex(value))


def tool_sympy_eval(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool wrapper for direct SymPy numeric evaluation."""
    expr_text = str(arguments['expr'])
    bindings = dict(arguments.get('bindings', {}))
    digits = int(arguments.get('digits', 30))
    expr = sympy_expr_from_text(expr_text)
    if bindings:
        expr = expr.subs(sympy_bindings_from_json(bindings))
    value = sp.N(expr, digits)
    cval = sympy_numeric_to_complex(value)
    return {
        'expr': str(expr),
        'value': number_to_jsonable(cval),
        'value_pretty': pretty_complex(cval, digits=12),
        'digits': digits,
    }


def tool_sympy_simplify(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool wrapper for direct SymPy simplification and LaTeX output."""
    expr_text = str(arguments['expr'])
    expr = sympy_expr_from_text(expr_text)
    simplified = sp.simplify(expr)
    return {
        'original': str(expr),
        'simplified': str(simplified),
        'latex': sp.latex(simplified),
    }


# -----------------------------------------------------------------------------
# Active tool surface (EML + SymPy only)
# -----------------------------------------------------------------------------

TOOL_HANDLERS: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    'eml_compile': tool_eml_compile,
    'eml_eval': tool_eml_eval,
    'eml_simplify': tool_eml_simplify,
    'eml_stability_check': tool_eml_stability_check,
    'eml_fit': tool_eml_fit,
    'sympy_eval': tool_sympy_eval,
    'sympy_simplify': tool_sympy_simplify,
    'eml_family_library': tool_eml_family_library,
    'eml_extract_group_structure': tool_eml_extract_group_structure,
    'eml_recover_core_family': tool_eml_recover_core_family,
    'eml_generate_from_addition_formula': tool_eml_generate_from_addition_formula,
    'eml_constant_free_scan': tool_eml_constant_free_scan,
    'eml_explore_family': tool_eml_explore_family,
}

TOOL_DEFS: List[Dict[str, Any]] = [
    {
        'name': 'eml_compile',
        'description': 'Compile a standard infix mathematical expression into an EML tree.',
        'inputSchema': {
            'type': 'object',
            'properties': {'target_expr': {'type': 'string'}, 'simplify': {'type': 'boolean'}},
            'required': ['target_expr'],
        },
    },
    {
        'name': 'eml_eval',
        'description': 'Evaluate an EML expression or a normal infix expression after compiling it to EML.',
        'inputSchema': {
            'type': 'object',
            'properties': {'expr': {'type': 'string'}, 'bindings': {'type': 'object'}},
            'required': ['expr'],
        },
    },
    {
        'name': 'eml_simplify',
        'description': 'Simplify an EML tree via constant folding and canonical rebuilding.',
        'inputSchema': {
            'type': 'object',
            'properties': {'expr': {'type': 'string'}},
            'required': ['expr'],
        },
    },
    {
        'name': 'eml_stability_check',
        'description': 'Sample an EML expression and flag domain, branch-cut, overflow, and conditioning risks.',
        'inputSchema': {
            'type': 'object',
            'properties': {'expr': {'type': 'string'}, 'bindings': {'type': 'object'}, 'region': {'type': 'object'}},
            'required': ['expr'],
        },
    },
    {
        'name': 'eml_fit',
        'description': 'Fit a compact symbolic law to x/y data, compile the best result to EML, and return ranking metrics.',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'x_values': {'type': 'array', 'items': {'type': 'number'}},
                'y_values': {'type': 'array', 'items': {'type': 'number'}},
                'families': {'type': 'array', 'items': {'type': 'string'}},
                'top_k': {'type': 'integer'},
            },
            'required': ['x_values', 'y_values'],
        },
    },
    {
        'name': 'sympy_eval',
        'description': 'Directly evaluate a SymPy expression with optional bindings and precision.',
        'inputSchema': {
            'type': 'object',
            'properties': {'expr': {'type': 'string'}, 'bindings': {'type': 'object'}, 'digits': {'type': 'integer'}},
            'required': ['expr'],
        },
    },
    {
        'name': 'sympy_simplify',
        'description': 'Simplify an expression directly in SymPy and return plain-text and LaTeX forms.',
        'inputSchema': {
            'type': 'object',
            'properties': {'expr': {'type': 'string'}},
            'required': ['expr'],
        },
    },

    {
        'name': 'eml_family_library',
        'description': 'List the built-in generalized EML families or inspect one family.',
        'inputSchema': {
            'type': 'object',
            'properties': {'family': {'type': 'string'}},
            'required': [],
        },
    },
    {
        'name': 'eml_extract_group_structure',
        'description': 'Expose the hidden abelian-group data behind a built-in generalized EML family.',
        'inputSchema': {
            'type': 'object',
            'properties': {'family': {'type': 'string'}},
            'required': ['family'],
        },
    },
    {
        'name': 'eml_recover_core_family',
        'description': 'Return the six-step constructive recovery chain for a built-in generalized EML family.',
        'inputSchema': {
            'type': 'object',
            'properties': {'family': {'type': 'string'}},
            'required': ['family'],
        },
    },
    {
        'name': 'eml_generate_from_addition_formula',
        'description': 'Report the addition formula and derived operations for a built-in generalized EML family.',
        'inputSchema': {
            'type': 'object',
            'properties': {'family': {'type': 'string'}},
            'required': ['family'],
        },
    },
    {
        'name': 'eml_constant_free_scan',
        'description': 'Summarise constant-free candidate families and the open constant-free question.',
        'inputSchema': {
            'type': 'object',
            'properties': {},
            'required': [],
        },
    },
    {
        'name': 'eml_explore_family',
        'description': 'Convenience aggregation of family metadata, group structure, recovery, and addition-law consequences.',
        'inputSchema': {
            'type': 'object',
            'properties': {'family': {'type': 'string'}},
            'required': ['family'],
        },
    },
]


# -----------------------------------------------------------------------------
# Official MCP SDK transport (stdio)
# -----------------------------------------------------------------------------

def _require_official_mcp() -> Dict[str, Any]:
    """Import the official MCP SDK lazily so direct examples can still run without it.

    Server and test modes require the `mcp` package because the slim server now
    uses the official stdio transport and session lifecycle rather than the
    legacy hand-rolled framed JSON-RPC loop.
    """
    try:
        import mcp.server.stdio as mcp_server_stdio
        import mcp.types as mcp_types
        from mcp.client.session import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client
        from mcp.server.lowlevel import NotificationOptions, Server
        from mcp.server.models import InitializationOptions
    except Exception as exc:
        raise RuntimeError(
            "Official `mcp` package support is required for server/test modes in eml_mcp_server.py. "
            "Install the official MCP Python SDK in the target environment and rerun."
        ) from exc

    return {
        'mcp_server_stdio': mcp_server_stdio,
        'types': mcp_types,
        'ClientSession': ClientSession,
        'StdioServerParameters': StdioServerParameters,
        'stdio_client': stdio_client,
        'NotificationOptions': NotificationOptions,
        'Server': Server,
        'InitializationOptions': InitializationOptions,
    }


def _model_to_jsonable(value: Any) -> Any:
    """Convert Pydantic / MCP SDK model objects into plain JSON-safe Python data."""
    if hasattr(value, 'model_dump'):
        try:
            return value.model_dump(mode='json')
        except TypeError:
            return value.model_dump()
    if isinstance(value, dict):
        return {k: _model_to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_model_to_jsonable(v) for v in value]
    return value


class OfficialSDKHarnessClient:
    """Synchronous-looking adapter around an async official MCP ClientSession.

    The regression suite already expects a tiny client object with `.request()`
    and `.notify()` methods. This adapter keeps that calling style while routing
    everything through the official MCP SDK session.
    """

    def __init__(self, session: Any, loop: Any):
        self.session = session
        self.loop = loop

    async def _request_async(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params or {}

        if method == 'initialize':
            return _model_to_jsonable(await self.session.initialize())
        if method == 'tools/list':
            return _model_to_jsonable(await self.session.list_tools())
        if method == 'tools/call':
            return _model_to_jsonable(await self.session.call_tool(params['name'], params.get('arguments') or {}))
        if method == 'shutdown':
            return {}
        raise KeyError(f'Unknown method: {method}')

    def request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        import asyncio
        future = asyncio.run_coroutine_threadsafe(self._request_async(method, params or {}), self.loop)
        return future.result()

    def notify(self, method: str, params: Optional[Dict[str, Any]] = None) -> None:
        # Official MCP session initialization already completes the necessary
        # handshake, so the legacy initialized notification becomes a no-op.
        return None


def build_official_mcp_server() -> Any:
    """Create the slim official MCP SDK server exposing only EML + SymPy tools."""
    sdk = _require_official_mcp()
    mcp_types = sdk['types']
    Server = sdk['Server']

    server = Server('eml-mcp-server')

    @server.list_tools()  # type: ignore[no-untyped-call]
    async def list_tools() -> List[Any]:
        tools: List[Any] = []
        for item in TOOL_DEFS:
            exposed_name = _helper_exposed_name(item.get('name', ''))
            description = item.get('description', '') or ''
            input_schema = item.get('inputSchema') or {'type': 'object', 'properties': {}, 'required': []}
            tools.append(
                mcp_types.Tool(
                    name=exposed_name,
                    description=description,
                    inputSchema=input_schema,
                )
            )
        logger.info('Listed %d tools via official MCP SDK', len(tools))
        return tools

    @server.call_tool()  # type: ignore[no-untyped-call]
    async def call_tool(name: str, arguments: Dict[str, Any]) -> Any:
        internal_name = _helper_strip_namespace(name)
        if internal_name not in TOOL_HANDLERS:
            raise ValueError(f'Unknown tool: {name}')
        try:
            structured = TOOL_HANDLERS[internal_name](arguments or {})
            text = json.dumps(structured, indent=2, ensure_ascii=False, default=str)
            return mcp_types.CallToolResult(
                content=[mcp_types.TextContent(type='text', text=text)],
                structuredContent=structured,
                isError=False,
            )
        except Exception as exc:
            logger.exception('Tool call failed: %s', name)
            return mcp_types.CallToolResult(
                content=[mcp_types.TextContent(type='text', text=f'{type(exc).__name__}: {exc}')],
                structuredContent={'error': str(exc), 'tool': name},
                isError=True,
            )

    return server


async def run_stdio_server_async() -> None:
    """Run the slim server over the official MCP stdio transport."""
    sdk = _require_official_mcp()
    NotificationOptions = sdk['NotificationOptions']
    InitializationOptions = sdk['InitializationOptions']

    server = build_official_mcp_server()
    logger.info('EML MCP official SDK server starting on stdio')
    async with sdk['mcp_server_stdio'].stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name='eml-mcp-server',
                server_version='1.0.0',
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )



def _extract_structured_content(call_result: Dict[str, Any]) -> Dict[str, Any]:
    """Pull structuredContent out of whichever shape the SDK returns."""
    if isinstance(call_result, dict):
        if 'structuredContent' in call_result:
            return call_result['structuredContent']
        if 'result' in call_result and isinstance(call_result['result'], dict) and 'structuredContent' in call_result['result']:
            return call_result['result']['structuredContent']
    return call_result


def _assert_close(name: str, got: float, expected: float, tol: float = 1e-6) -> Dict[str, Any]:
    return {'name': name, 'pass': abs(got - expected) <= tol, 'details': {'got': got, 'expected': expected, 'tol': tol}}


def run_regression_suite(client: Any) -> Dict[str, Any]:
    """Run the built-in end-to-end regression suite against the live stdio server."""
    results: List[Dict[str, Any]] = []

    tools_resp = client.request('tools/list')
    tools = tools_resp['tools'] if isinstance(tools_resp, dict) and 'tools' in tools_resp else tools_resp
    names = {row['name'] for row in tools}
    expected = {_helper_exposed_name(name) for name in {'eml_compile', 'eml_eval', 'eml_simplify', 'eml_stability_check', 'eml_fit', 'sympy_eval', 'sympy_simplify', 'eml_family_library', 'eml_extract_group_structure', 'eml_recover_core_family', 'eml_generate_from_addition_formula', 'eml_constant_free_scan', 'eml_explore_family'}}
    results.append({'name': 'tools_list_expected_surface', 'pass': names == expected, 'details': {'names': sorted(names)}})

    compiled = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_compile'), 'arguments': {'target_expr': 'sin(x)**2 + cos(x)**2', 'simplify': False}}))
    results.append({'name': 'eml_compile_returns_tree', 'pass': 'eml_expression' in compiled and compiled['node_count'] > 0, 'details': compiled})

    pure_compiled = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_compile'), 'arguments': {'target_expr': 'pi + e + 1/2', 'simplify': False, 'pure': True}}))
    pure_leaf_analysis = pure_compiled.get('leaf_analysis', {})
    pure_pass = pure_compiled.get('pure_mode') is True and pure_leaf_analysis.get('is_one_only_constant_tree') is True
    results.append({'name': 'eml_compile_pure_mode_eliminates_named_constants', 'pass': pure_pass, 'details': pure_compiled})

    simplified = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_simplify'), 'arguments': {'expr': 'sin(x)**2 + cos(x)**2'}}))
    results.append({'name': 'eml_simplify_trig_identity', 'pass': simplified['simplified'] in {'1', '1.0'}, 'details': simplified})

    evaluated = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_eval'), 'arguments': {'expr': 'sqrt(a^2 + b^2)', 'bindings': {'a': 3, 'b': 4}}}))
    results.append(_assert_close('eml_eval_pythagorean', float(evaluated['value']), 5.0))

    stability = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_stability_check'), 'arguments': {'expr': 'log(x)', 'region': {'x': {'min': 0.0, 'max': 1.0}}}}))
    stability_pass = (
        any('log' in str(item).lower() or 'zero' in str(item).lower() or 'ill-posed' in str(item).lower() for item in stability.get('warnings', []))
        or stability.get('trace_summary', {}).get('near_zero_log_inputs', 0) > 0
        or stability.get('trace_summary', {}).get('errors', 0) > 0
    )
    results.append({'name': 'eml_stability_detects_log_risk', 'pass': stability_pass, 'details': stability})

    xs = np.array([1.0, 2.0, 3.0, 4.0])
    ys = 2.0 * xs
    fit = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_fit'), 'arguments': {'x_values': xs.tolist(), 'y_values': ys.tolist(), 'families': ['linear'], 'top_k': 1}}))
    fit_pass = (
        fit.get('best_family') == 'linear'
        and 'best_formula' in fit
        and float(fit.get('best_metrics', {}).get('r2', 0.0)) > 0.99
    )
    results.append({'name': 'eml_fit_linear_dataset', 'pass': fit_pass, 'details': fit})

    sym_s = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('sympy_simplify'), 'arguments': {'expr': 'sin(x)**2 + cos(x)**2'}}))
    results.append({'name': 'sympy_simplify_trig_identity', 'pass': sym_s['simplified'] == '1', 'details': sym_s})

    sym_e = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('sympy_eval'), 'arguments': {'expr': 'sqrt(a^2 + b^2)', 'bindings': {'a': 3, 'b': 4}, 'digits': 30}}))
    results.append(_assert_close('sympy_eval_pythagorean', float(sym_e['value']), 5.0))

    fams = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_family_library'), 'arguments': {}}))
    fam_pass = any(row.get('family') == 'original_eml' for row in fams.get('families', []))
    results.append({'name': 'eml_family_library_lists_original_eml', 'pass': fam_pass, 'details': fams})

    group = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_extract_group_structure'), 'arguments': {'family': 'original_eml'}}))
    group_pass = group.get('group_law') == 'A ⊞ B = A + B' and group.get('axioms', {}).get('neutral_element') is True
    results.append({'name': 'eml_extract_group_structure_original_eml', 'pass': group_pass, 'details': group})

    cfree = _extract_structured_content(client.request('tools/call', {'name': _helper_exposed_name('eml_constant_free_scan'), 'arguments': {}}))
    cfree_pass = cfree.get('open_problem') is True and len(cfree.get('constant_free_candidates', [])) >= 1
    results.append({'name': 'eml_constant_free_scan_reports_candidate', 'pass': cfree_pass, 'details': cfree})

    passed = sum(1 for row in results if row['pass'])
    return {'total_cases': len(results), 'passed_cases': passed, 'failed_cases': len(results) - passed, 'all_passed': passed == len(results), 'results': results}


async def _run_test_harness_async() -> int:
    """Launch a subprocess server and execute the regression suite through the official SDK."""
    import asyncio

    sdk = _require_official_mcp()
    server_file = Path(__file__).resolve()
    params = sdk['StdioServerParameters'](
        command=sys.executable,
        args=[str(server_file), 'server'],
        env={'PYTHONUNBUFFERED': '1', **dict(os.environ)},
        cwd=str(server_file.parent),
    )

    async with sdk['stdio_client'](params) as (read, write):
        async with sdk['ClientSession'](read, write) as session:
            logger.info('Official SDK test harness: initialize')
            init = _model_to_jsonable(await session.initialize())
            print('=== initialize ===')
            print(json.dumps(init, indent=2, ensure_ascii=False, default=str))

            print('\n=== tools/list ===')
            tools = _model_to_jsonable(await session.list_tools())
            print(json.dumps(tools, indent=2, ensure_ascii=False, default=str))

            adapter = OfficialSDKHarnessClient(session, asyncio.get_running_loop())

            print('\n=== regression suite ===')
            suite = await asyncio.to_thread(run_regression_suite, adapter)
            print(json.dumps(suite, indent=2, ensure_ascii=False, default=str))
            return 0 if suite['all_passed'] else 1


def run_test_harness() -> int:
    """Convenience sync wrapper around the async official-SDK harness."""
    import asyncio
    return asyncio.run(_run_test_harness_async())


def run_direct_examples() -> int:
    """Run several local examples without going through the RPC transport."""
    print('=== Example 1: compile a semi-complex expression ===')
    compiled = tool_eml_compile({'target_expr': 'exp(x) + log(x) + cos(x)', 'simplify': True})
    print(json.dumps(compiled, indent=2))

    print('\n=== Example 2: evaluate a Pythagorean form through EML ===')
    result = tool_eml_eval({'expr': 'sqrt(a^2 + b^2)', 'bindings': {'a': 5, 'b': 12}})
    print(json.dumps(result, indent=2))

    print('\n=== Example 3: run a stability scan around a logarithm ===')
    print(json.dumps(tool_eml_stability_check({'expr': 'sin(x) + log(x)', 'region': {'x': {'min': 0.2, 'max': 2.0}}}), indent=2))

    print('\n=== Example 4: fit a compact logarithmic-style law ===')
    x_vals = [0.5, 1.0, 2.0, 4.0]
    y_vals = [float(np.log(v)) for v in x_vals]
    print(json.dumps(tool_eml_fit({'x_values': x_vals, 'y_values': y_vals, 'families': ['linear', 'log_affine', 'power_affine'], 'top_k': 3}), indent=2))

    print('\n=== Example 5: compile in pure mode ===')
    pure_compiled = tool_eml_compile({'target_expr': 'pi + e + 1/2', 'simplify': False, 'pure': True})
    print(json.dumps(pure_compiled, indent=2))

    print('\n=== Example 6: cross-check an identity with SymPy ===')
    print(json.dumps(tool_sympy_simplify({'expr': 'sin(x)**2 + cos(x)**2'}), indent=2))

    print('\n=== Example 7: direct SymPy evaluation with bindings ===')
    print(json.dumps(tool_sympy_eval({'expr': 'sqrt(a^2 + b^2)', 'bindings': {'a': 8, 'b': 15}, 'digits': 30}), indent=2))

    print('\n=== Example 8: list built-in generalized EML families ===')
    print(json.dumps(tool_eml_family_library({}), indent=2))

    print('\n=== Example 9: explore the original EML family ===')
    print(json.dumps(tool_eml_explore_family({'family': 'original_eml'}), indent=2))

    print('\n=== Example 10: generate from the tanh/artanh addition formula ===')
    print(json.dumps(tool_eml_generate_from_addition_formula({'family': 'tanh_artanh'}), indent=2))

    print('\n=== Example 11: scan constant-free candidates ===')
    print(json.dumps(tool_eml_constant_free_scan({}), indent=2))
    return 0


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Command-line entry point for server, tests, and example execution."""
    parser = argparse.ArgumentParser(description='Slim EML + SymPy MCP server and harness (official MCP SDK transport)')
    parser.add_argument('mode', nargs='?', default='test', choices=['server', 'test', 'examples', 'all'], help='Run mode')
    args = parser.parse_args(argv)

    try:
        if args.mode == 'server':
            import asyncio
            asyncio.run(run_stdio_server_async())
            return 0
        if args.mode == 'examples':
            return run_direct_examples()
        if args.mode == 'all':
            rc1 = run_direct_examples()
            rc2 = run_test_harness()
            return 0 if rc1 == 0 and rc2 == 0 else 1
        return run_test_harness()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
