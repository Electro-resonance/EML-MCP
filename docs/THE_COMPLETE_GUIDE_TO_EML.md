# The Complete Guide to EML

## Exp-Minus-Log Mathematics, Pure Mode, Family Tools, Symbolic Trees, MCP Tooling, Discovery Engines, and Transformer Compilation

**Edition:** Working Draft  
**Date:** 2026-05-03  
**Format:** Markdown book manuscript  
**Scope:** EML theory, implementation, practical mode, pure mode, compact family tools, MCP servers, symbolic regression, transformer compilation, algebraic extensions, verification, and practical usage.  
**Important note:** This is a technical guide and synthesis based on public papers and repositories. It is not an independent proof of every theorem, not a formal code audit, and not an independently reproduced benchmark report.

---

## Dedication

For the builders who still believe that mathematics is not merely a list of operations, but a language waiting to be compressed into something more fundamental.

For the patient engineers who turn beautiful papers into working tools.

For the symbolic explorers who ask whether a single seed can grow a forest.

---

## Source Spine

| Source | Role |
|---|---|
| All elementary functions from a single operator | Primary constructive paper for EML |
| Algebraic structure behind Odrzywołek’s EML operator | Algebraic and generalisation follow-up |
| Electro-resonance/EML-MCP | Compact single-file EML/SymPy MCP server |
| angrysky56/eml-mcp | Expanded EML MCP research engine |
| angrysky56/eml-transformer | Compiled EML expression trees into transformer-shaped PyTorch machines |
| Model Context Protocol Specification | Protocol background for tools, resources, and prompts |

---

## What This Book Is

This book is a complete practical and conceptual guide to **EML**, the **Exp-Minus-Log** operator:

```text
EML(x, y) = exp(x) - ln(y)
```

The central idea is that this single binary operator, together with the distinguished constant `1`, can generate the usual repertoire of elementary functions found on a scientific calculator. This includes constants, arithmetic, exponentiation, logarithms, trigonometric and hyperbolic functions, and their compositions.

That idea is already remarkable. But EML becomes more interesting when it is implemented. It gives us:

- a uniform binary-tree grammar for elementary mathematics;
- a natural complexity measure, K, based on tree size;
- a searchable space for symbolic regression;
- a basis for MCP tools that AI agents can call;
- a compact route for formula catalogues and discovery engines;
- a way to compile symbolic function trees into transformer-shaped computation.

The aim of this book is to explain the complete stack, from intuition to implementation.

---

## How to Use This Book

Read **Part I** if you want intuition.

Read **Part II** if you want the mathematics.

Read **Part III** if you want implementation patterns.

Read **Part IV** if you want MCP integration.

Read **Part V** if you want symbolic regression and discovery.

Read **Part VI** if you want transformer compilation.

Read **Part VII** if you want verification, branch analysis, and scientific discipline.

Read **Part VIII** if you want roadmaps, exercises, and future research.

---

## One-Page Summary

EML is a binary operation:

```text
E(x, y) = exp(x) - ln(y)
```

With the constant `1`, it immediately gives:

```text
E(x, 1) = exp(x)
```

because:

```text
ln(1) = 0
```

The rest of the scientific-calculator world is recovered by repeated composition, using exponential/logarithmic identities, cancellation, complex arithmetic, and recursively constructed binary trees.

The grammar is tiny:

```text
S → 1 | x | E(S, S)
```

Every expression is a full binary tree whose internal nodes are all the same operator. That makes EML attractive for symbolic search, formula catalogues, AI tooling, and machine compilation.

The practical lesson is not that everyone should stop using `sin`, `cos`, `log`, or `sqrt`. The practical lesson is that underneath the diversity of elementary functions there may be a small generative language. EML gives that language a concrete operator, a computational interface, and a research programme.


---

# Part I — The Big Idea


---

# Chapter 1: The Two-Button Scientific Calculator

Imagine a scientific calculator with only two buttons.

One button is the constant:

```text
1
```

The other is a two-input operation:

```text
E(x, y) = exp(x) - ln(y)
```

At first, this looks absurd. How could such a calculator possibly replace addition, subtraction, multiplication, division, powers, square roots, logarithms, trigonometry, hyperbolic functions, constants such as `e`, `π`, and `i`, and all the usual combinations found in science and engineering?

Yet this is the claim at the centre of EML: the apparent diversity of elementary mathematics can be generated recursively from a single binary operator and a single constant. The operator is called **EML**, for **Exp-Minus-Log**.

The first tiny miracle is immediate:

```text
E(x, 1) = exp(x) - ln(1)
        = exp(x) - 0
        = exp(x)
```

So exponentiation is available as soon as we have the constant `1`. Once exponential structure is available, logarithmic and arithmetic structure can be built back through recursive constructions. Once complex exponentials are available, trigonometric functions can be recovered through Euler-style identities. Once arithmetic and transcendental operations are available, the scientific calculator begins to reappear.

The point is not that this is the fastest way to calculate. It is almost certainly not. The point is that the universe of elementary expressions can be represented through a radically simple grammar:

```text
S → 1 | x | E(S, S)
```

This grammar says: an expression is either the constant `1`, a variable such as `x`, or an EML node applied to two smaller expressions. That is all.

A conventional mathematical expression has many node types:

```text
+
-
*
/
sin
cos
tan
sqrt
log
exp
pow
...
```

An EML expression has one internal node type:

```text
E
```

This is a deep simplification. It does for elementary continuous mathematics something reminiscent of what NAND does for Boolean logic. NAND is not the only way to build digital circuits, and it is not always the most convenient gate. But it is a universal gate. EML plays an analogous role for elementary functions: a universal continuous operator, at least for the standard calculator basis described by Odrzywołek.

The metaphor of a two-button calculator is useful because it makes the philosophical compression vivid. But we should not misunderstand it. An actual EML calculator still needs a way to enter variables, compose trees, evaluate complex intermediate values, and choose branches of logarithms. It is not literally a pocket calculator with one operation key. It is a formal language.

That formal language becomes powerful when combined with software. A computer can generate EML trees, evaluate them, simplify them, compare them, search them, persist them in a database, and expose them as MCP tools. An AI system can then call those tools instead of pretending to do the symbolic work in prose.

The first lesson of EML is therefore simple:

**A full mathematical language may be hidden inside a tiny operator.**


---

# Chapter 2: What EML Is — and What It Is Not

EML is the binary operation:

```text
E(x, y) = exp(x) - ln(y)
```

It is not a new elementary function in the sense of being unrelated to known mathematics. It is made from two familiar functions and one familiar arithmetic operation. Its novelty lies in the way it combines them and in the claim that this single combination can generate the rest.

EML is best understood in five different ways.

## 1. EML as an operator

At the lowest level, EML is simply a function of two inputs. Given `x` and `y`, compute the exponential of `x`, subtract the logarithm of `y`, and return the result.

```python
def E(x, y):
    return exp(x) - log(y)
```

This view is computational.

## 2. EML as a gate

In digital logic, a gate takes inputs and produces an output. EML can be viewed as a continuous-valued gate. A circuit made only of EML gates can implement elementary functions.

This view is architectural.

## 3. EML as a grammar

The grammar:

```text
S → 1 | x | E(S, S)
```

generates a language of expressions. Each expression is a tree.

This view is symbolic.

## 4. EML as a search space

Because every internal node is the same, all formulas of a given size can be enumerated or searched more uniformly than formulas in a heterogeneous language.

This view is algorithmic.

## 5. EML as a bridge to AI tools

Because EML expressions can be represented as trees, stored in registries, verified numerically, exposed through MCP, and compiled into PyTorch modules, they form a bridge between symbolic mathematics and tool-using AI.

This view is agentic.

It is equally important to say what EML is not.

EML is not a replacement for NumPy, SymPy, Mathematica, SageMath, or ordinary calculators. Those systems are mature, optimised, broad, and deeply engineered. EML is a minimal generative basis and a research language.

EML is not automatically efficient. A simple conventional expression can become a large EML tree. Computing many nested exponentials and logarithms may be slower and less stable than using the original expression.

EML is not automatically proof. A tree that matches a reference function at several points is not necessarily a globally valid identity. Branch cuts, complex logarithms, singularities, and finite test sets all matter.

EML is not limited to pure philosophical beauty. It can be implemented and used. The compact EML-MCP server shows it can be exposed as seven practical MCP tools. The expanded eml-mcp package shows it can become a persistent research engine. The eml-transformer project shows EML trees can be compiled into transformer-shaped machines.

The balanced definition is this:

**EML is a minimal single-operator language for constructing and studying elementary functions, with practical value as a symbolic, searchable, verifiable, and AI-callable mathematical substrate.**


---

# Chapter 3: Why One Operator Matters

At first glance, one-operator universality may seem like mathematical minimalism for its own sake. Why should anyone care whether `sin`, `cos`, `log`, `sqrt`, and multiplication can be reconstructed from one exotic operation, when we already have direct implementations?

There are several reasons.

## 1. Minimal bases reveal hidden structure

When a large set of operations can be reduced to one primitive, we learn something about the structure of the domain. Boolean logic looked different after NAND and NOR were recognised as universal. Lambda calculus showed that computation can arise from abstraction and application. Cellular automata showed that simple local rules can produce complex global behaviour. EML suggests that the elementary functions may form a more compact generative family than the calculator menu implies.

## 2. Uniform grammars are easier to search

A symbolic-regression system using many primitives must decide which operation to place at each node. Should it use `+`, `*`, `sin`, `log`, `sqrt`, or `pow`? In EML, every internal node is the same. The search becomes a question of tree shape and wiring rather than operator selection. This does not make search easy, but it regularises the space.

## 3. Uniform trees have natural complexity

If every internal node has the same cost, the complexity of a formula can be measured by node count. This gives a useful metric, often called `K` in the EML context. A shorter EML tree is a shorter programme in the EML language.

## 4. Single-operation circuits are easier to compile

A circuit made of many operation types needs many functional units. A circuit made of one operation type needs one repeated unit. This is exactly why EML is attractive for the transformer-compilation experiment. Attention routes operands; the feed-forward layer applies EML; the residual stream stores intermediate values.

## 5. AI systems benefit from explicit tools

Large language models often answer mathematical questions by pattern matching. EML-MCP changes the relationship. The model can call a tool that compiles, evaluates, simplifies, or verifies an expression. The tool returns structured results. The model explains them. This is a healthier division of labour.

## 6. Minimal languages invite generalisation

Stachowiak’s algebraic note shows that EML is not merely a lucky accident. Behind it lie cancellation, identity, inverse functions, and group-like structure. Once those are identified, we can search for other operator families, perhaps tuned for stability, compactness, or specific domains.

The deeper reason one operator matters is that it creates a new kind of mathematical object: the **universal expression tree**. Instead of asking whether a formula can be written in familiar notation, we ask how it appears in the EML tree language. What is its depth? What is its K? Does it have shorter direct-search versions? Does it require complex intermediates? Is it branch-sensitive? Can it be compiled?

This transforms ordinary elementary functions into objects of comparative morphology. `sin`, `log`, `tan`, and multiplication are no longer just buttons. They are tree species in a single forest.

That forest is what this guide explores.


---

# Part II — The Mathematics of EML


---

# Chapter 4: The Operator, the Constant, and the Grammar

The EML operator is:

```text
E(x, y) = exp(x) - ln(y)
```

The distinguished constant is:

```text
1
```

The simplest grammar is:

```text
S → 1 | x | E(S, S)
```

For functions of more than one variable, we extend the terminals:

```text
S → 1 | x | y | z | ... | E(S, S)
```

This grammar generates full binary trees. Every internal node is `E`. Every leaf is a terminal.

For example:

```text
E(x, 1)
```

is a tree with one EML node and two leaves. It evaluates to:

```text
exp(x)
```

because `ln(1) = 0`.

A slightly larger tree:

```text
E(E(x, 1), 1)
```

evaluates to:

```text
exp(exp(x))
```

The uniformity is important. Every expression has a tree form. Every tree has a node count. Every tree can be traversed, stored, compared, mutated, and compiled.

A full binary tree has a relationship between leaves and total nodes:

```text
K = 2L - 1
```

where `L` is the number of leaves and `K` is the total node count. Since every internal node is the same operation, this node count becomes a meaningful complexity measure.

However, the grammar has a subtle distinction: **pure** versus **practical** terminals.

In pure mode, the only numeric constant is `1`. Other constants such as `0`, `e`, `π`, `i`, `1/2`, and `sqrt(2)` must be constructed.

In practical mode, an implementation may allow convenient constants directly. This is useful for efficient evaluation and demonstration, but it changes the complexity accounting.

For example, these are different kinds of expressions:

```text
Pure:
  π is constructed from EML and 1.

Practical:
  π appears as a leaf.
```

Both may be useful. They should not be confused.

An EML implementation should therefore report its basis:

```yaml
basis:
  mode: pure
  terminals:
    - 1
    - x
  hidden_constants: []
```

or:

```yaml
basis:
  mode: practical
  terminals:
    - 1
    - x
    - pi
    - e
    - i
  hidden_constants:
    - pi
    - e
    - i
```

The operator also demands a domain story. Because `ln(y)` is involved, `y` must be handled in a domain where the logarithm is meaningful. In practice, EML implementations use complex arithmetic, usually complex128. This allows expressions to pass through complex intermediate values even when the final result is real.

This means the grammar is syntactically simple but analytically rich. A tree is easy to draw. Its global behaviour may still require branch analysis, domain restrictions, and numerical stability checks.

The core grammar is therefore the seed. It is not the whole tree of knowledge, but it gives the tree somewhere to grow.


---

# Chapter 5: First Constructions: Exp, Zero, and the Opening Door

The first and most important construction is exponentiation:

```text
E(x, 1) = exp(x)
```

This works because:

```text
ln(1) = 0
```

So the constant `1` acts as the key that unlocks the exponential side of the operator.

From this, the constant `e` appears immediately:

```text
E(1, 1) = exp(1) - ln(1)
        = e - 0
        = e
```

This is already interesting. The constant `e` is not primitive. It is generated.

A next crucial target is zero. If we can construct zero, then cancellation and negation become possible. Odrzywołek’s paper gives constructive routes through the EML grammar. Stachowiak’s algebraic note explains why zero matters: it is the neutral element that allows the cancellation structure to unfold.

Informally, the path is:

```text
1 gives exp
exp and log structure give cancellation
cancellation gives zero
zero gives addition/subtraction structure
addition plus exp gives multiplication
```

The details of the exact pure trees can be long, and implementations often store them in a catalogue. The important conceptual point is that the early constructions are bootstrapping steps. Once enough seeds exist, later constructions become easier.

This suggests a useful way to think about EML development:

```text
Stage 0: E and 1
Stage 1: exp and e
Stage 2: zero and identity-like structures
Stage 3: log and negation
Stage 4: add and subtract
Stage 5: multiply and divide
Stage 6: powers and roots
Stage 7: trig and hyperbolic functions
Stage 8: composed elementary formulae
```

This staged view mirrors how an EML registry should be organised. Some formulas are foundational. Others are derived. Others are discovered. Others are practical shorthands.

A good formula catalogue should not merely list expressions. It should record dependency structure:

```yaml
formula: multiply
depends_on:
  - add
  - exp
  - ln
  - zero
derivation_type: constructed
verification: numeric_verified
```

This is not just documentation. Dependency tracking enables proof, simplification, and reproducibility. If a foundational formula is improved or corrected, dependent formulas can be rechecked.

The earliest EML constructions are also the place where branch choices begin to matter. The logarithm is multi-valued in the complex plane, and practical implementations use a principal branch. A construction that is valid under one convention may behave differently near a branch cut. This is why EML needs stability checking and domain metadata from the start.

The opening door is beautiful:

```text
E(x, 1) = exp(x)
```

But once the door opens, we enter a house with many rooms: algebra, complex analysis, symbolic computation, optimisation, and software engineering.


---

# Chapter 6: Arithmetic from EML

To recover a scientific calculator, EML must recover arithmetic: addition, subtraction, multiplication, division, negation, reciprocal, powers, and roots.

The broad strategy is to use the relationship between exponential and logarithmic structure.

The exponential converts addition into multiplication:

```text
exp(a + b) = exp(a) exp(b)
```

The logarithm converts multiplication into addition:

```text
ln(ab) = ln(a) + ln(b)
```

EML contains both `exp` and `ln` in a single operation. Once the system can extract or simulate enough of their behaviour, arithmetic becomes recoverable.

Stachowiak’s note emphasises cancellation. Subtraction carries a neutral element and a self-cancelling structure. In ordinary arithmetic:

```text
a - a = 0
a - 0 = a
```

These properties allow zero and additive inverses to be built. Once zero and inverse-like behaviour are available, addition and subtraction can be organised.

Multiplication comes through the exponential’s addition formula. If addition is available, then:

```text
a * b = exp(ln(a) + ln(b))
```

Division follows similarly:

```text
a / b = exp(ln(a) - ln(b))
```

Powers can be expressed as:

```text
a^b = exp(b ln(a))
```

Roots are powers:

```text
sqrt(a) = a^(1/2)
```

In conventional notation, these identities are familiar. In EML, they must be represented as trees of `E` nodes. That is where complexity appears. A simple-looking formula may require many EML nodes.

This is why EML implementations maintain registries. A registry stores known constructions so that a compiler can use them compositionally. Without a registry, every expression would require repeated rediscovery.

For example, a compiler translating:

```text
sqrt(a^2 + b^2)
```

needs constructions for:

```text
square
add
sqrt
```

Each of these may expand to an EML tree. Practical mode may allow these as catalogue entries. Pure mode expands them all the way down to EML and `1`.

Arithmetic recovery also illustrates the difference between **existence** and **optimality**. A compositional compiler can produce a valid tree for multiplication by using known identities. But a direct search might find a shorter EML tree for multiplication than the compiler’s path. Therefore, a formula catalogue should allow multiple entries:

```yaml
multiply:
  compiler_tree:
    K: 35
  direct_search_tree:
    K: 17
  preferred:
    reason: shorter and verified
```

This is one of the central research opportunities in EML: not merely proving that functions are constructible, but finding compact constructions.

Arithmetic is the spine of the calculator. Once EML can reconstruct it, the rest of elementary mathematics becomes reachable.


---

# Chapter 7: Trigonometry, Hyperbolic Functions, and Complex Intermediates

Trigonometric functions are where EML’s reliance on complex arithmetic becomes unavoidable.

The familiar bridge is Euler’s formula:

```text
exp(i x) = cos(x) + i sin(x)
```

From this, one can derive:

```text
sin(x) = (exp(i x) - exp(-i x)) / (2i)
cos(x) = (exp(i x) + exp(-i x)) / 2
```

Hyperbolic functions have analogous expressions:

```text
sinh(x) = (exp(x) - exp(-x)) / 2
cosh(x) = (exp(x) + exp(-x)) / 2
```

Since EML gives access to exponential structure and arithmetic structure, trigonometric and hyperbolic functions can be constructed. But the construction passes through complex values.

This matters for implementation.

A user may ask for:

```text
sin(0.5)
```

and expect a real number. Internally, an EML expression may compute with `i`, complex exponentials, and logarithms. The final imaginary residue should be close to zero, but numerical roundoff may leave a tiny imaginary part.

An implementation should therefore distinguish:

```text
mathematically real output
numerically complex output with tiny imaginary residue
genuinely complex output
```

A good evaluator might return:

```json
{
  "value": "0.479425538604203 + 0.0j",
  "real_projection": 0.479425538604203,
  "imaginary_residue": 2.1e-16,
  "safe_to_project_real": true
}
```

Branch cuts are the deeper issue. The complex logarithm is multi-valued:

```text
log(z) = ln|z| + i(arg(z) + 2πk)
```

Software libraries usually choose a principal branch. EML expressions using logarithms inherit that branch convention. A formula that behaves well in one region may jump near a branch cut.

Therefore, EML verification must include domain awareness. A trigonometric formula may pass at six standard test points and still require caution near branch boundaries.

The eml-transformer project reports a `tan` machine with 97 positions and 24 layers. This illustrates how trigonometric functions can be substantially more complex than `exp`. The catalog ranges from short primitives such as `exp` to deeper constructions such as `tan`.

The lesson is that trigonometry is not free. EML can reconstruct it, but the cost appears in tree size, complex intermediates, and branch sensitivity.

This does not weaken the EML thesis. It enriches it. EML reveals the hidden structural cost of familiar functions. The calculator button `tan` looks simple because centuries of mathematical engineering hide the machinery. In EML, the machinery becomes visible.


---

# Chapter 8: K Complexity and the Morphology of Formulae

EML gives a natural complexity measure: count the nodes in the expression tree.

If a full binary tree has `L` leaves, then total nodes are:

```text
K = 2L - 1
```

This is often referred to as K complexity in EML discussions. It is not formal Kolmogorov complexity, but it plays a similar practical role: it measures description length within the EML language.

K matters because EML has one internal node type. In conventional mathematics, counting complexity is awkward. Is `sin(x)` one operation or many? Is multiplication simpler than logarithm? Should `pi` cost one symbol or the cost of constructing it? EML makes one answer available: count the nodes of the pure tree.

However, K is only meaningful when the basis is specified.

A pure tree using only `1` and variables cannot be compared directly with a practical tree that treats `π`, `e`, or `i` as leaves. Therefore, a formula record should always include:

```yaml
basis:
  mode: pure
  allowed_constants:
    - 1
```

or:

```yaml
basis:
  mode: practical
  allowed_constants:
    - 1
    - e
    - pi
    - i
```

K also has different meanings depending on the source of the tree.

A compiler-derived tree may be valid but not shortest. A direct exhaustive search may find a shorter tree. A symbolic-regression result may find a candidate tree that matches data. A simplified tree may reduce K by applying identities. Each should be recorded.

For example:

```yaml
formula: tan
compiler_K: 143
simplified_K: 97
direct_search_K: unknown
verification: numeric_verified
```

K opens a new research field: the **morphology of elementary functions**.

Questions become possible:

- Which functions are short in EML?
- Which functions are unexpectedly long?
- Which functions simplify dramatically?
- Are there families with regular K growth?
- Does K correlate with numerical stability?
- Do direct-search optima have recognisable patterns?
- Can algebraic variants reduce K for certain domains?

The eml-transformer project makes K physically architectural. A formula with K positions becomes a compiled machine with corresponding sequence positions. A deeper tree requires more layers. This connects symbolic complexity to neural-like computational depth.

K should not be confused with runtime cost. One EML node contains an exponential and a logarithm. A short EML tree can still be slower than a conventional expression. K measures structural description length in the EML language, not CPU cycles.

K should also not be confused with human readability. A 97-node EML tree is explicit but difficult to read. A familiar expression such as `tan(x)` is far more human-readable. Therefore, a complete guide should distinguish:

```text
EML compactness
human readability
execution speed
numerical stability
proof simplicity
```

The best formula is not always the shortest formula. But the shortest verified pure EML tree is an important scientific object.


---

# Chapter 9: Pure Mode, Practical Mode, and Hidden Assumptions

Pure mode and practical mode are two ways of using EML.

**Pure mode** is faithful to the minimal basis. It uses only EML, the constant `1`, and variables. All other constants and operations must be constructed.

**Practical mode** allows convenient constants, catalogue functions, or shortcuts. It is useful for engineering.

Both modes are valid. Confusing them is not valid.

In the compact EML-MCP repository, pure mode is an opt-in compilation style that rewrites numeric constants into EML trees built from `1` and `eml(...)`. Practical mode is the default, designed for compact trees and efficient evaluation.

This distinction should become standard across all EML tooling.

Consider:

```text
pi + e + 1/2
```

In practical mode, this can be represented with leaves for `pi`, `e`, and `1/2`.

In pure mode, each of those constants must be constructed from EML and `1`. The pure expression may be much larger. That larger size is not a defect. It is the visible cost of not treating those constants as primitive.

Hidden assumptions matter because EML’s philosophical claim is about generative sufficiency. If an implementation quietly introduces `pi` as a primitive leaf, it may still compute correctly, but it is no longer demonstrating pure EML construction.

A robust compiler should therefore return metadata:

```json
{
  "mode": "pure",
  "expression": "pi + e + 1/2",
  "pure_tree_K": 231,
  "practical_tree_K": 9,
  "hidden_constants": [],
  "expanded_constants": ["pi", "e", "1/2"]
}
```

or:

```json
{
  "mode": "practical",
  "expression": "pi + e + 1/2",
  "tree_K": 9,
  "hidden_constants": ["pi", "e", "1/2"],
  "pure_equivalent_available": true
}
```

This distinction has parallels in computing. A universal Turing machine can simulate any computable process, but practical programming languages use libraries and machine instructions. A NAND-only circuit can build all Boolean logic, but real chips use many gates. Pure EML proves and explores the minimal basis. Practical EML makes the system usable.

The correct engineering principle is:

```text
Use practical mode for work.
Use pure mode for structural inspection.
Always label which mode was used.
```

Pure mode is especially important for research publications, complexity tables, and claims about minimality. Practical mode is appropriate for teaching examples, quick evaluations, MCP demonstrations, and AI-agent workflows where speed and clarity matter more than pure-basis accounting.

The best EML systems will let users move between the two modes, inspect the expansion cost, and choose the right representation for the task.


---

# Part III — The Papers and the Algebra


---

# Chapter 10: Odrzywołek’s Constructive Programme

Andrzej Odrzywołek’s paper, *All elementary functions from a single operator*, is the foundation of EML. It presents the EML operator as a constructive discovery rather than a purely abstract speculation.

The paper’s central claim is that:

```text
E(x, y) = exp(x) - ln(y)
```

together with the constant `1`, generates the standard repertoire of a scientific calculator.

The abstract states that this includes constants such as `e`, `π`, and `i`, arithmetic operations, exponentiation, transcendental functions, and algebraic functions. It also states that every such expression becomes a binary tree of identical nodes, and that this uniform structure enables gradient-based symbolic regression.

The paper has three major contributions.

## 1. A single continuous operator

The paper identifies EML as a continuous analogue to a Sheffer-like universal operator. It does not claim EML is Boolean NAND. It claims EML plays an analogous minimal-generative role for elementary continuous mathematics.

## 2. Constructive recovery

The paper does not merely assert universality. It gives constructive routes and a bootstrapped recovery process. The set of known functions grows as recovered functions become available for further constructions.

## 3. Symbolic regression

The paper explores EML trees as trainable circuits. A parameterised EML tree can be optimised using standard methods such as Adam. When the target function is elementary and shallow enough, the system may recover an exact closed-form expression.

The paper’s significance statement is bold: a two-button calculator, `1` and `eml`, suffices for what a full scientific calculator can do. This should be read carefully. It is a statement about representational sufficiency, not speed, convenience, or numerical robustness in every context.

The paper’s open questions are equally important. It mentions variants, including related operators and a ternary variant that may require no distinguished constant. It raises the possibility that EML is the “tip of an iceberg” rather than the unique final answer.

For software builders, the paper implies several requirements:

- represent expressions as binary trees;
- track K complexity;
- support pure EML expansion;
- use complex arithmetic;
- verify against reference functions;
- distinguish constructive compiler output from direct-search optimal trees;
- support symbolic-regression experiments;
- preserve failure cases and depth limits.

The most important practical lesson is that EML is a **research programme**, not just an operator. The operator is the seed. The programme includes catalogue construction, search, simplification, verification, symbolic regression, and architecture.

Odrzywołek’s paper gives the map. The repositories begin to build the roads.


---

# Chapter 11: Stachowiak’s Algebraic Lens

Tomasz Stachowiak’s note, *Algebraic structure behind Odrzywołek’s EML operator*, asks why EML works.

This is an important shift. Odrzywołek’s construction is partly search-driven and constructive. Stachowiak looks for the algebraic mechanism behind the construction.

The note identifies two key ingredients:

1. an abelian-group-like cancellation structure;
2. a functional inverse structure.

In ordinary EML:

```text
E(x, y) = exp(x) - ln(y)
```

the subtraction carries cancellation behaviour. The functions `exp` and `ln` are inverses. The constant `1` matters because:

```text
ln(1) = 0
```

This gives access to a neutral element and lets the construction begin.

Stachowiak’s framing suggests a broader template:

```text
S(x, y) = f(x) ⊖ g(y)
```

where `⊖` behaves like subtraction or a related cancellation operation, and `f` and `g` are paired by inverse-like relations.

The note shows that the relevant cancellation operation is connected to an abelian group. This means EML is not just an arbitrary combination of exp, minus, and log. It is an instance of a deeper pattern.

The exponential plays a double role. It is one part of the inverse pair, but it also converts addition into multiplication:

```text
exp(a + b) = exp(a) exp(b)
```

This is why, once additive structure is recovered, multiplicative structure becomes reachable.

Stachowiak also clarifies why the constant-free problem is hard. The constant `1` supplies the neutralising condition `ln(1)=0`. If a single binary operator requires a distinguished constant to unlock its structure, then eliminating that constant demands a different mechanism. A ternary operator may avoid the need, but that is no longer the same minimal binary setup.

For implementation, the algebraic lens suggests a new module: an **operator-family laboratory**.

Such a module could allow users to define candidate operators:

```yaml
name: EML
operator: exp(x) - log(y)
neutral_constant: 1
inverse_pair:
  f: exp
  g: log
cancellation:
  operation: subtraction
```

Then the system could test whether basic recovery steps are possible.

This would generalise EML-MCP from a tool for one operator into a platform for studying minimal generative operators. That should be done carefully. The verified EML core should remain stable. Algebraic-family exploration should be marked experimental.

Stachowiak’s note therefore turns EML from a discovery into a field: **the study of single-operator languages generated by cancellation and inverse structure**.


---

# Chapter 12: Variants: EDL, Ternary Operators, and the Constant-Free Dream

Once EML exists, a natural question appears: is it unique?

The answer is almost certainly no. Odrzywołek’s paper already suggests related operators and variants. Stachowiak’s note gives algebraic reasons to expect families of such constructions.

One obvious direction is to replace subtraction-like structure with division-like structure. If EML is Exp-Minus-Log, then an EDL-style operator might use division rather than subtraction:

```text
EDL(x, y) = exp(x) / ln(y)
```

This is not necessarily the exact best variant, but it illustrates the family idea: combine an inverse-function pair with a cancellation-like operation.

The central design questions for any variant are:

- What is the neutral element?
- What constant is needed to unlock it?
- Can the component functions be extracted?
- Can addition and multiplication be recovered?
- Does the operator handle branches better or worse than EML?
- Are tree complexities shorter for important functions?
- Does symbolic regression become easier or harder?
- Is the operator numerically stable?

A variant is not automatically better because it is novel. It should be evaluated against EML on a common benchmark.

The constant-free dream is more ambitious. EML uses the constant `1`. Can a binary operator generate elementary functions without any distinguished constant?

This is difficult because the constant plays a bootstrapping role. In EML, `1` gives `ln(1)=0`, and this opens the path to `exp`. Without a constant, the operator must contain a way to produce a neutral or fixed element internally.

A ternary operator may avoid the need for a distinguished constant, because it has more input structure. But then the minimality changes. A ternary single operator is not the same as a binary single operator plus constant. It may be elegant, but it should be compared fairly.

A complete EML guide should therefore define several levels of minimality:

```text
Level 1: one binary operator + one distinguished constant
Level 2: one binary operator, no constant
Level 3: one ternary operator, no constant
Level 4: one unary generator, no constant
```

The strongest open question may be whether a unary generator exists that can produce the elementary-function universe through iteration, composition, or parameterisation. That would be an even more radical compression.

For now, EML’s virtue is that it is concrete and implemented. Variants are research frontiers.

A future EML-MCP family module should support:

```text
define operator
test neutralisation
recover exp/log analogues
recover arithmetic
measure K
compare stability
run symbolic regression
produce report
```

The guiding principle should be:

**Explore variants boldly, but keep the verified EML core intact.**


---

# Part IV — Implementing EML


---

# Chapter 13: The Core Data Structures

A serious EML implementation needs a few core data structures.

The simplest is the EML node:

```python
@dataclass
class ENode:
    left: Expr
    right: Expr
```

Terminals might be:

```python
@dataclass
class ConstOne:
    pass

@dataclass
class Variable:
    name: str
```

A more practical implementation will include practical constants, catalogue references, metadata, and cached signatures.

A minimal expression type might be:

```python
Expr = ConstOne | Variable | PracticalConstant | ENode
```

Evaluation is recursive:

```python
def eval_expr(expr, env):
    if expr is ConstOne:
        return 1
    if expr is Variable:
        return env[expr.name]
    if expr is PracticalConstant:
        return expr.value
    if expr is ENode:
        a = eval_expr(expr.left, env)
        b = eval_expr(expr.right, env)
        return exp(a) - log(b)
```

This recursive evaluator is conceptually clean but may be inefficient for large shared subtrees. A compiler may instead convert the tree into RPN or a DAG.

RPN, reverse Polish notation, is useful because it gives a linear programme:

```text
x 1 E
```

means:

```text
E(x, 1)
```

The eml-transformer project uses RPN strings from the EML catalogue. RPN is ideal for stack-based parsing, catalogue entries, and compiler pipelines.

A formula record should include:

```yaml
name: sin
tree: ...
rpn: ...
K: ...
depth: ...
basis: pure
verification: ...
dependencies: ...
```

The expanded eml-mcp package has modules corresponding to these needs:

- `primitives.py` for the basic operation;
- `trees.py` for expression trees;
- `registry.py` for known formulas;
- `compiler.py` for translating familiar syntax;
- `simplifier.py` for reducing trees;
- `database.py` for persistence;
- `similarity.py` for comparing tree structures;
- `discovery.py` and `regression.py` for search;
- `server.py` for MCP exposure.

This is the right modular structure. Each part has a different responsibility.

The most important design rule is to avoid mixing symbolic identity, numerical evaluation, and storage concerns too early. A tree should be representable without knowing how it will be verified. A verifier should work on trees without knowing whether they came from a compiler or a discovery run. A database should store provenance rather than assuming all formulas are equal.

A good architecture is layered:

```text
math primitive
    ↓
tree representation
    ↓
evaluation
    ↓
compiler
    ↓
simplifier
    ↓
verification
    ↓
registry/database
    ↓
discovery/regression
    ↓
MCP tools
```

This layering makes it possible to test each part independently.

The implementation should also preserve exact symbolic structure even when numerical evaluation is performed. If a user only receives a floating-point answer, the value of EML is lost. The system should return the tree, K, mode, verification, and warnings.

EML is not just a calculator. It is a tree language. The data structures should honour that.


---

# Chapter 14: Building a Minimal Evaluator

A minimal EML evaluator can be built in a few lines, but a good evaluator needs discipline.

The mathematical function is:

```python
def eml(x, y):
    return np.exp(x) - np.log(y)
```

Because complex intermediates matter, use complex arithmetic:

```python
def eml(x, y):
    x = np.asarray(x, dtype=np.complex128)
    y = np.asarray(y, dtype=np.complex128)
    return np.exp(x) - np.log(y)
```

A tree evaluator then recursively computes leaves and nodes.

Example:

```python
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class One:
    pass

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class E:
    left: object
    right: object

def eval_eml(expr, env):
    if isinstance(expr, One):
        return np.complex128(1.0)
    if isinstance(expr, Var):
        return np.complex128(env[expr.name])
    if isinstance(expr, E):
        a = eval_eml(expr.left, env)
        b = eval_eml(expr.right, env)
        return np.exp(a) - np.log(b)
    raise TypeError(expr)
```

Now:

```python
x = Var("x")
expr = E(x, One())
eval_eml(expr, {"x": 0.5})
```

returns `exp(0.5)`.

This tiny evaluator is enough to demonstrate the principle. But it is not enough for a robust EML system. It lacks:

- parsing;
- RPN conversion;
- practical constants;
- vectorisation;
- error handling;
- branch diagnostics;
- overflow protection;
- simplification;
- verification;
- metadata;
- database persistence.

Still, the minimal evaluator is useful. Every larger implementation should be able to reduce conceptually to this:

```text
evaluate leaves
evaluate left subtree
evaluate right subtree
apply exp(left) - log(right)
```

Testing should begin here.

Suggested tests:

```python
assert close(eval(E(Var("x"), One()), {"x": 0.5}), np.exp(0.5))
assert close(eval(E(One(), One()), {}), np.e)
```

Once practical constants are allowed:

```python
@dataclass(frozen=True)
class Const:
    value: complex
    name: str = ""
```

the evaluator becomes more convenient but less pure.

A robust evaluator should return structured output rather than raw values:

```json
{
  "value": "1.6487212707001282+0j",
  "real": 1.6487212707001282,
  "imag_abs": 0.0,
  "warnings": [],
  "dtype": "complex128"
}
```

This is especially important when called through MCP. An LLM client needs context, not just a number.

A minimal evaluator is the seed. The complete system grows from it.


---

# Chapter 15: Registries, Formula Catalogues, and Persistence

An EML system without a registry must rediscover everything.

A registry stores known formula constructions. It lets a compiler translate familiar expressions into EML trees by reusing known components.

For example, if the registry knows:

```text
exp
ln
add
multiply
sin
cos
```

then a compiler can expand:

```text
sin(x)**2 + cos(x)**2
```

compositionally. Without a registry, it would need to derive everything from first principles each time.

A formula catalogue should include more than the tree.

A good record contains:

```yaml
id: formula_sin_v1
name: sin
rpn: ...
tree: ...
mode: pure
K: 41
depth: 10
dependencies:
  - exp
  - multiply
  - subtract
  - i
verification:
  status: numeric_verified
  tolerance: 1e-12
  max_error: 3.2e-14
domain:
  input: real
  internal: complex128
  branch_sensitive: true
provenance:
  method: constructed
  source: Odrzywołek-style identity
```

The expanded eml-mcp package includes a database layer and a formula catalogue. Its directory includes `database.py`, `registry.py`, and related modules. This is the correct direction because EML research is cumulative.

Persistence enables:

- formula reuse;
- discovery history;
- simplification records;
- verification status;
- symbolic-regression results;
- failure logs;
- benchmark reports;
- cross-project import/export.

The database should not treat every formula as equal. A seed formula, a discovered candidate, and a formally proved identity are different objects.

Recommended status levels:

```text
seed
constructed
compiler_generated
direct_search_found
symbolic_regression_candidate
numeric_verified
symbolic_verified
formally_proved
deprecated
invalidated
```

A database should also store failure. Failed symbolic-regression runs are useful. They tell us where the search space is hard, which depths fail, and which targets need warm starts.

The catalogue should be exportable. A future transformer compiler may load catalogue entries read-only. A paper may need to include a reproducible formula table. A user may want to inspect the database without running the MCP server.

Suggested export formats:

```text
catalogue.json
catalogue.csv
catalogue.md
catalogue.sqlite
```

The catalogue is the memory of the EML system. Without memory, EML is a clever operator. With memory, it becomes a growing mathematical organism.


---

# Chapter 16: Simplification and Canonicalisation

EML trees can grow quickly. Simplification is therefore not optional.

A compiler may generate a valid but bloated tree. A search process may discover a tree with redundant substructure. A pure-mode expansion of constants may produce repeated constructions. Without simplification, the catalogue becomes large, repetitive, and hard to compare.

Simplification can operate at several levels.

## 1. Local identity rules

If a subtree matches a known pattern, rewrite it.

Example:

```text
E(x, 1) → exp(x)
```

In pure EML, the right-hand side may be represented by a catalogue reference rather than leaving the EML language.

## 2. Constant folding

If a subtree contains only constants, evaluate it and replace it with a known constant or a canonical construction.

## 3. Structural sharing

If the same subtree appears multiple times, store it once as a DAG internally.

## 4. Behavioural equivalence

If two trees have the same signature across standard test points, mark them as candidates for equivalence.

## 5. Symbolic normalisation

If SymPy or another symbolic system can prove two expressions equivalent under assumptions, choose a canonical form.

Canonicalisation is harder than simplification. It asks for a unique or preferred representation among many equivalent trees. Full canonicalisation for EML may be difficult because elementary-function equivalence is hard, and complex branches complicate matters.

Therefore, practical EML systems should use layered normalisation:

```text
syntactic normalisation
local rewrite simplification
constant folding
signature comparison
symbolic proof attempt
human review
```

The expanded eml-mcp package includes a simplifier module. That is essential. Its results should always be recorded with before/after complexity:

```yaml
simplification:
  original_K: 189
  simplified_K: 97
  rules_applied:
    - constant_fold
    - known_identity
    - duplicate_subtree
  verification_after: passed
```

Simplification should never silently change semantics. Every simplification should be verified. If a simplifier uses finite numerical signatures, the result should say so.

One of the most valuable research tasks is finding shorter EML forms. A direct-search result may beat a compositional compiler. A simplifier may reduce a discovered tree. A human may find an identity that collapses a large expression. All of these should feed back into the registry.

The ultimate goal is not merely to make trees smaller. It is to find the natural morphology of functions in the EML language.

A formula is not fully known when it is constructed. It is better known when it is simplified, verified, compared, and placed in the catalogue.


---

# Part V — EML as MCP


---

# Chapter 17: Why EML Wants MCP

The Model Context Protocol gives AI systems a standard way to call external tools, access resources, and use prompts. EML is exactly the sort of capability that benefits from this boundary.

A language model can talk about EML. It can even write plausible EML expressions. But without a tool, it cannot reliably evaluate, simplify, verify, or search them. MCP changes that. It turns EML operations into named functions with structured inputs and outputs.

A practical single-file EML-MCP server can expose tools such as:

```text
eml_compile
eml_eval
eml_simplify
eml_stability_check
eml_fit
sympy_eval
sympy_simplify
eml_family_library
eml_extract_group_structure
eml_recover_core_family
eml_generate_from_addition_formula
eml_constant_free_scan
eml_explore_family
```

This is the current compact Electro-resonance model built around `eml_mcp_server.py`. It remains intentionally small and understandable, but it now covers three layers at once:

- the core EML symbolic tools;
- the SymPy comparison tools;
- the compact generalized-family tools derived from the Stachowiak follow-up paper.

A larger EML-MCP server can expose:

```text
eml_evaluate
eml_explain
eml_list_formulas
eml_tree_info
eml_compile
eml_verify
eml_master_tree
eml_symbolic_regression
eml_discover
eml_discover_start
eml_discover_status
eml_discover_result
eml_discover_cancel
eml_discover_list
eml_simplify
eml_similarity
```

This is the expanded research-lab model.

MCP matters because it enforces operational clarity. Instead of an AI saying:

> “This expression probably simplifies to 1.”

it can call:

```text
sympy_simplify("sin(x)**2 + cos(x)**2")
```

and:

```text
eml_compile("sin(x)**2 + cos(x)**2", pure=true)
eml_simplify(...)
eml_verify(...)
```

Then it can report what happened.

A good MCP result should include:

```json
{
  "operation": "eml_verify",
  "passed": true,
  "tolerance": 1e-12,
  "test_points": [...],
  "max_error": 2.3e-14,
  "warnings": ["numeric verification only; no formal proof attempted"]
}
```

This is much better than a fluent but ungrounded answer.

MCP also allows separation of roles:

```text
LLM:
  understands the user
  chooses tools
  explains results

EML-MCP:
  compiles
  evaluates
  verifies
  searches
  stores
```

This separation is central to trustworthy AI mathematics.

The protocol layer should be honest about side effects. Some tools are read-only. Some evaluate expressions. Some write to a database. Some launch long-running jobs. The tool descriptions should say so.

For example:

```yaml
eml_discover_start:
  side_effects:
    writes_job_state: true
    writes_database: optional
    long_running: true
    network: false
    requires_confirmation: if runtime > 30 minutes
```

EML wants MCP because EML is not just a notation. It is a set of operations. MCP makes those operations visible and callable.


---

# Chapter 18: The Compact EML-MCP Server

The compact `Electro-resonance/EML-MCP` repository is still centred on a single-file MCP server, and that server is still always called `eml_mcp_server.py`. The current compact surface now spans **thirteen tools**, not seven:

```text
eml_compile
eml_eval
eml_simplify
eml_stability_check
eml_fit
sympy_eval
sympy_simplify
eml_family_library
eml_extract_group_structure
eml_recover_core_family
eml_generate_from_addition_formula
eml_constant_free_scan
eml_explore_family
```

This is still an excellent first surface, because it remains compact while covering three complementary use-cases.

### 1. Core symbolic EML route

`eml_compile` turns a conventional expression into an EML representation.

`eml_eval` evaluates an expression with bindings.

`eml_simplify` attempts to simplify the EML tree or expression.

`eml_stability_check` evaluates numerical risk over a region, useful for branch-sensitive expressions such as `sin(x) + log(x)`.

`eml_fit` tries small fitting tasks, such as recovering or approximating `log(x)` from sampled data.

### 2. Conventional symbolic comparison route

`sympy_eval` and `sympy_simplify` provide reference routes through conventional symbolic tooling.

### 3. Generalized-family structural route

The newer family tools expose the compact algebraic layer inspired by Stachowiak’s follow-up paper:

- `eml_family_library` lists or inspects the built-in generalized operator families;
- `eml_extract_group_structure` exposes the hidden abelian-group-style structure;
- `eml_recover_core_family` returns the six-step constructive recovery chain;
- `eml_generate_from_addition_formula` shows what a family’s addition law can generate;
- `eml_constant_free_scan` summarizes the curated constant-free candidates and the still-open constant-free question;
- `eml_explore_family` packages the whole family picture into one tool result.

The server still supports **practical mode** and **pure mode**. Practical mode is the default, optimised for compactness and efficient evaluation. Pure mode rewrites numeric constants into EML trees built from `1` and `eml(...)`. The same filename, `eml_mcp_server.py`, is used regardless of whether the caller is using the practical or pure route.

The original README examples remain well chosen:

```text
sin(x)^2 + cos(x)^2
pi + e + 1/2
sqrt(a^2 + b^2)
sin(x) + log(x)
y = log(x) data fitting
```

They still demonstrate identity, constants, geometry, branch risk, and fitting. But the newer compact server now also supports a second layer of example workflows:

```text
inspect the built-in family library
extract the group structure for original_eml
recover the tanh/artanh family chain
generate consequences from the cosine/arccos addition law
scan curated constant-free candidates
explore a whole family in one call
```

These additions do not turn the compact server into the full discovery engine. They keep it compact while making it much more expressive as a teaching, inspection, and LLM-tooling interface.

The compact server should still remain compact. Its role is to teach, test, and demonstrate. The right design discipline is now:

- keep the executable tool entry point as `eml_mcp_server.py`;
- keep pure mode available for structural inspection;
- keep the family tools curated rather than pretending to solve arbitrary operator-proof search;
- link outward to the larger research engine for long-running discovery and database-heavy work.

The compact server is therefore still the right first contact for a new user. It now says:

```text
Here is EML.
Here is how to compile it.
Here is how to evaluate it.
Here is how to compare it with SymPy.
Here is how to inspect pure mode.
Here is how to inspect generalized EML families.
```

That is exactly what a first MCP should do.


---

# Chapter 19: The Expanded EML-MCP Research Engine

The expanded `angrysky56/eml-mcp` package is the research engine.

The public directory contains modules such as:

```text
attention.py
compiler.py
database.py
discovery.py
jobs.py
primitives.py
registry.py
regression.py
server.py
similarity.py
simplifier.py
transformer.py
trees.py
```

This is not a toy layout. It represents a full EML laboratory.

The core idea is that formulas should be treated as persistent research objects. A formula is not just a string. It has a tree, RPN form, K complexity, dependencies, verification status, derivation history, and possible symbolic-regression provenance.

The expanded package supports:

- evaluation;
- explanation;
- formula listing;
- tree information;
- compilation;
- verification;
- master-tree generation;
- symbolic regression;
- discovery;
- asynchronous job management;
- simplification;
- similarity comparison;
- server exposure.

This creates a workflow:

```text
compile → inspect → simplify → verify → persist → compare → discover → regress → catalogue
```

The `database.py` layer is crucial. Without persistence, formula discovery is ephemeral. With persistence, the EML system becomes cumulative.

The `jobs.py` layer is also important. Discovery and symbolic regression can take time. An MCP client should not block indefinitely. It should start a job, poll status, cancel if needed, and retrieve results.

The `similarity.py` layer points toward formula morphology. Two formulas may behave the same but have different tree shapes. Two trees may look similar but differ numerically. Similarity tools help organise the catalogue.

The `regression.py` layer connects EML to data-driven discovery. A master tree can be trained to fit data and potentially snap to exact symbolic choices.

The `transformer.py` and `attention.py` modules hint at the bridge to compiled neural-like computation, also explored separately in `eml-transformer`.

The expanded package should be documented as a research engine with different trust levels. Some tools are stable. Some are experimental. Some write state. Some launch long jobs. The documentation should say which is which.

Recommended tool categories:

```text
Core:
  evaluate, compile, explain

Catalogue:
  list, inspect, export

Verification:
  numeric, symbolic, domain

Discovery:
  start, status, result, cancel

Regression:
  master_tree, train, snap, validate

Similarity:
  tree_distance, signature_compare

Administration:
  database_info, export, backup
```

The expanded package is where EML becomes a living system.


---

# Chapter 20: Designing Good EML MCP Tools

Good MCP tools are not merely functions exposed over a protocol. They are contracts between an AI client, a user, and an implementation.

An EML MCP tool should have:

- a clear name;
- a clear purpose;
- typed inputs;
- structured outputs;
- warnings;
- side-effect metadata;
- examples;
- failure modes.

Consider `eml_compile`.

A poor output would be:

```json
{
  "result": "some tree"
}
```

A good output would be:

```json
{
  "tool": "eml_compile",
  "input_expression": "sin(x)**2 + cos(x)**2",
  "mode": "pure",
  "tree": "...",
  "rpn": "...",
  "K": 183,
  "depth": 22,
  "hidden_constants": [],
  "warnings": [
    "pure expansion may be large",
    "numeric verification not performed"
  ]
}
```

Consider `eml_verify`.

A good output should include:

```json
{
  "passed": true,
  "reference": "sympy/numpy",
  "tolerance": 1e-12,
  "max_error": 4.1e-14,
  "test_points": ["sqrt(2)", "phi", "pi/7"],
  "domain": "real inputs; complex internal arithmetic",
  "proof_status": "numeric_only",
  "warnings": []
}
```

The output should help the LLM explain honestly. It should not force the LLM to infer hidden details.

Tool descriptions should tell the model when to use the tool. For example:

```text
Use eml_stability_check when an expression contains log, reciprocal, division, powers, or complex-sensitive compositions, or when the user asks about numerical reliability.
```

Some tools need budgets:

```json
{
  "max_iterations": 10000,
  "max_depth": 4,
  "timeout_seconds": 60,
  "seed": 1234
}
```

Long-running tools should be asynchronous. They should return job IDs.

Tools that write to a database should say so:

```yaml
side_effects:
  writes_database: true
  creates_job: false
  modifies_formula_status: true
```

EML MCP tools should also preserve uncertainty. A tool should not return “identity proven” unless proof was attempted and succeeded. It should distinguish:

```text
candidate
numeric match
symbolically simplified
formally proved
```

The aim is not to make the AI sound impressive. The aim is to make mathematical work inspectable.

A good EML MCP server turns the assistant into a careful laboratory technician: curious, capable, and honest.


---

# Part VI — Discovery and Symbolic Regression


---

# Chapter 21: Searching the EML Forest

The space of EML trees is enormous.

At depth 0, there are leaves. At depth 1, there are EML nodes over leaves. At depth 2, each child may itself be a subtree. The number of full binary tree shapes grows according to Catalan structures. When variables and constants are assigned to leaves, the space grows further.

This is the EML forest.

A direct exhaustive search can find short trees for simple functions, but it becomes expensive quickly. Therefore, practical discovery needs strategies:

- bounded depth search;
- evolutionary mutation;
- random generation with pruning;
- signature caching;
- tree similarity filtering;
- known-catalogue expansion;
- gradient-based symbolic regression;
- warm starts;
- simplification after generation;
- verification at every step.

A discovery engine should define its target:

```yaml
target:
  name: "log(x)"
  samples:
    x: [0.5, 1.0, 2.0, 4.0]
    y: [...]
  reference_expression: "log(x)"
  tolerance: 1e-12
```

Then it should search within a budget:

```yaml
budget:
  max_depth: 4
  max_iterations: 100000
  timeout_seconds: 300
  seed: 42
```

A result should not merely say “found”. It should report the process:

```yaml
result:
  status: found
  candidate_tree: ...
  K: 31
  max_error: 8.2e-14
  iterations: 17422
  simplification:
    before_K: 45
    after_K: 31
  verification:
    train: passed
    validation: passed
    domain_sampling: partial
```

Failed searches should be stored too:

```yaml
status: failed
best_candidate_K: 63
best_error: 0.0042
failure_mode: plateau
recommendation: increase_depth or use warm_start
```

This is scientifically valuable. It tells us about the shape of the search space.

The expanded eml-mcp package includes discovery and asynchronous job tools. This is the right design. Search should not freeze an AI client. A model should start a job, poll status, and retrieve results.

Discovery also needs novelty control. If a candidate is equivalent to a known formula, the system should detect it. Tree similarity and signature comparison help.

The most important rule is:

**Do not confuse discovery with proof.**

A discovered candidate is a hypothesis. It becomes stronger after numerical verification. Stronger still after symbolic verification. Strongest after formal proof.

The EML forest is rich. A good explorer carries a map, a compass, and a notebook.


---

# Chapter 22: Symbolic Regression with EML Trees

Symbolic regression tries to recover a formula from data.

Given samples:

```text
x: 0.5, 1.0, 2.0, 4.0
y: log(x)
```

a symbolic-regression system tries to infer:

```text
y = log(x)
```

Traditional symbolic regression searches over many operations. EML symbolic regression searches over a uniform EML tree.

Odrzywołek’s paper describes parameterised EML trees as trainable circuits. The idea is to create a master tree whose inputs are weighted combinations of constants, variables, or earlier subresults. Then optimise the weights using a method such as Adam. If the target is elementary and the tree depth is sufficient, the weights may converge near exact choices and snap to a closed-form expression.

The expanded eml-mcp package includes symbolic-regression tooling using PyTorch and complex128 arithmetic. The reported pattern is realistic: shallow depths are tractable; deeper blind recovery is harder; warm starts help.

A robust symbolic-regression pipeline should look like this:

```text
prepare data
normalise domain
build master tree
train continuous weights
snap candidate weights
construct symbolic tree
simplify
verify on train points
verify on validation points
verify over domain samples
record status
```

The output should classify the result:

```text
exact_recovery
candidate_identity
approximate_fit
failed_search
invalid_due_to_branch
invalid_due_to_overflow
```

This classification prevents overclaiming.

Why is EML attractive for symbolic regression?

Because the grammar is complete and regular. Every elementary formula expressible in the EML basis lives somewhere in the same tree universe. There is no need to decide whether to include `sin`, `cos`, `log`, or `sqrt` as primitive operations. They are all generated from the same operation.

But regularity does not remove difficulty. The search space still explodes. The loss landscape can be difficult. Exponentials can overflow. Complex branches can cause discontinuities. Finite data can be misleading.

Therefore, EML symbolic regression should always include:

- train/validation splits;
- out-of-domain tests;
- branch warnings;
- multiple seeds;
- failure reporting;
- comparison with conventional symbolic-regression baselines;
- K complexity reporting.

A successful symbolic-regression result is beautiful because it turns data into structure. But the structure must earn trust.

The correct posture is:

```text
fit boldly
snap carefully
verify ruthlessly
claim modestly
```


---

# Chapter 23: AI Agents as Mathematical Lab Assistants

EML becomes especially powerful when used by AI agents.

A language model is good at understanding user intent, explaining concepts, and orchestrating workflows. It is not inherently reliable at exact symbolic computation. EML tools can fill that gap.

A user might ask:

> Can you express `sin(log(x))` in EML and verify it?

An agent should not invent the tree in prose. It should call tools:

```text
eml_compile("sin(log(x))", mode="practical")
eml_verify(...)
eml_tree_info(...)
```

Then it should explain:

```text
I compiled the expression using the EML catalogue.
The resulting tree has K=...
It was verified numerically against NumPy at tolerance...
No formal proof was attempted.
```

This is a better model of mathematical assistance.

The agent can also use EML for discovery:

```text
User: Here are data points. Can you infer a formula?
Agent:
  1. checks the data;
  2. runs eml_fit or symbolic regression;
  3. retrieves candidates;
  4. verifies against held-out points;
  5. explains uncertainty.
```

A good mathematical agent must resist hype. It should not say “I discovered a law” when it has only found a candidate fit. It should say:

```text
This candidate matches your supplied points and passes additional numerical checks over this interval. It is not yet a proven identity.
```

EML tools also make agent memory useful. A formula discovered today can be stored and reused tomorrow. The agent can ask:

```text
eml_list_formulas()
eml_similarity(candidate)
eml_get_formula("tan")
```

This turns the agent into a collaborator with a mathematical notebook.

A future AI research assistant might combine:

- EML-MCP for formula work;
- SymPy for symbolic reference;
- NumPy for numerical checks;
- PyTorch for symbolic regression;
- eml-transformer for compiled execution;
- a proof assistant for formal verification.

The agent’s role is orchestration and explanation. The tools do the grounded work.

This is the healthiest future for LLM mathematics: not larger models pretending harder, but models connected to inspectable mathematical instruments.


---

# Part VII — Compiling EML into Transformers


---

# Chapter 24: The EML Transformer Idea

The `eml-transformer` project asks a fascinating question:

Can an EML expression tree be compiled into a transformer-shaped machine?

The answer, at least for the Layer 1 catalogue described in the README, is yes.

The idea is that a transformer has a native structure:

```text
residual stream
attention routing
pointwise feed-forward computation
layered depth
```

An EML tree also has a structure:

```text
leaves
internal EML nodes
operand dependencies
tree depth
```

The compiler maps one to the other.

The README describes:

```text
sequence length = number of RPN tokens
layers          = tree depth + 1
attention       = analytic index-select routing
FFN             = EML(a,b)
parameters      = analytically set buffers
```

This is not a trained neural network in the usual sense. The weights are constructed analytically. Attention is not learned; it routes operands from known positions. The feed-forward operation applies EML.

The result is a transformer whose forward pass computes the function.

This matters because ordinary language models often compute elementary math statistically. They predict the answer-shaped tokens. They may succeed on common examples and fail unpredictably on uncommon ones. A compiled EML machine does not guess. It executes a fixed programme.

The README reports 27 compiled primitives verifying to within `1e-12` of NumPy reference, with examples ranging from `exp` to `tan`. It also explicitly says the system is not a production inference accelerator. A 24-layer machine for `tan` is not faster than NumPy. The point is architecture, not speed.

This is a crucial distinction. The EML transformer is valuable because it shows that transformer-shaped substrates can host exact, inspectable computation.

The architecture suggests a future hybrid system:

```text
LLM understands task
    ↓
LLM proposes formula or calls EML compiler
    ↓
EML tree is verified
    ↓
Tree is compiled into EMLMachine
    ↓
Machine becomes callable primitive
```

Layer 2, described as in progress, would learn to generate programme strings. That would turn the system into a verifier-guided programme generator. The learned part proposes. The compiled part executes. The verifier accepts or rejects.

This is a powerful pattern for AI alignment in mathematical domains:

```text
generation under verification
```

The EML transformer should not be described as replacing LLMs. It should be described as giving LLMs a reliable mathematical organ.

A language model thinks in tokens. EML gives it trees. The transformer compiler gives those trees a body.


---

# Chapter 25: RPN, Residual Streams, and Analytic Routing

Reverse Polish notation, or RPN, is central to the EML transformer workflow.

In RPN, operands come before operators:

```text
x 1 E
```

means:

```text
E(x, 1)
```

A more complex expression can be read by pushing operands onto a stack and applying operators when they appear.

RPN is ideal for compilation because each token has a position. The compiler can assign every intermediate result to a position in the residual stream.

Consider:

```text
x 1 E
```

Positions:

```text
0: x
1: 1
2: E(position 0, position 1)
```

The machine needs to route positions 0 and 1 into the EML operation at position 2. In a transformer-like architecture, attention can perform this routing.

For a larger RPN expression, each EML node depends on two earlier positions. The compiled attention pattern is therefore a dependency graph. It is not learned. It is calculated from the tree.

The feed-forward layer applies:

```text
E(a, b) = exp(a) - ln(b)
```

The residual stream stores intermediate values.

Layer depth corresponds to dependency depth. If a node depends on results that are themselves computed in earlier layers, the compiler schedules the computation across layers.

This is why the README says:

```text
layers = tree depth + 1
```

The compiled machine is a fixed-schedule programme.

This connects EML to hardware thinking. A mathematical expression becomes a circuit. The circuit becomes a scheduled machine. The machine can be run.

It also connects to interpretability. Since the routing is analytic, one can inspect which positions feed which node. Since the operation is fixed, one can inspect what every layer does. This is very different from a trained transformer whose attention patterns and MLP activations must be interpreted after the fact.

A compiled EML transformer should export a trace:

```yaml
tokens:
  - position: 0
    type: variable
    name: x
  - position: 1
    type: constant
    value: 1
  - position: 2
    type: eml_node
    left: 0
    right: 1
layers:
  - computes: [2]
verification:
  max_error: ...
```

For large trees, this trace becomes a circuit diagram.

The transformer idea is therefore not merely a novelty. It gives EML trees an executable architecture that resembles the native shape of modern LLMs, while remaining inspectable and exact by construction.


---

# Chapter 26: What EML Transformer Compilation Is Not

The EML transformer project is exciting precisely because it states what it is not.

It is not a production inference accelerator. NumPy will compute `tan(x)` far faster than a 24-layer transformer-style machine. If the goal is fast numerical evaluation, use NumPy.

It is not a general-purpose symbolic mathematics system. It does not perform integration, solve arbitrary equations, handle special functions, or replace SymPy.

It is not a trained LLM that has somehow learned all mathematics. The Layer 1 machines are analytically constructed.

It is not evidence that arbitrary transformer models internally compute elementary functions exactly. It is evidence that a transformer-shaped architecture can be constructed to compute them.

These limitations are not weaknesses. They clarify the research contribution.

The contribution is:

```text
A symbolic EML programme can be compiled into a transformer-like residual-stream machine whose forward pass executes the programme.
```

This has several implications.

First, it shows that transformer-like architectures can host exact computations when the computation is compiled rather than learned.

Second, it gives a possible way to attach reliable mathematical primitives to learned agents.

Third, it provides an interpretability contrast. A compiled machine is transparent because the routing and operations are known.

Fourth, it creates a route for programme generation. A learned model could emit RPN. A compiler could build a machine. A verifier could test it.

The practical use case is not:

```text
Replace NumPy with EML transformer.
```

The practical use case is:

```text
Give an AI agent a verified callable mathematical primitive represented in the same broad architectural family as transformer computation.
```

This distinction matters for communication. Overclaiming would damage the project. The truthful claim is already strong.

A future version might integrate into an LLM toolchain as follows:

```text
1. User asks for mathematical modelling.
2. LLM proposes candidate closed form.
3. EML-MCP compiles and verifies tree.
4. EML transformer compiles callable module.
5. Agent uses module repeatedly in a larger workflow.
```

In that context, speed may be less important than trust, provenance, and inspectability.

The EML transformer is not a faster calculator. It is a proof-of-concept for **compiled cognition**: exact symbolic structure embedded in a neural-style substrate.


---

# Part VIII — Verification, Safety, and Scientific Discipline


---

# Chapter 27: Verification Levels

EML needs strong verification discipline.

A candidate formula can have several levels of support.

## Level 0: untested candidate

The formula has been generated but not checked.

```yaml
status: candidate
claim_allowed: no
```

## Level 1: sample fit

The formula matches a training dataset.

```yaml
status: sample_fit
claim_allowed: approximate only
```

## Level 2: numerical verification

The formula matches a reference function at independent test points within a tolerance.

```yaml
status: numeric_verified
tolerance: 1e-12
```

## Level 3: domain sampling

The formula matches over a sampled domain, including edge cases and random points.

```yaml
status: domain_sample_verified
domain: [0.2, 2.0]
```

## Level 4: symbolic verification

A symbolic system such as SymPy simplifies the difference to zero under assumptions.

```yaml
status: symbolic_verified
assumptions: x > 0
```

## Level 5: formal proof

A proof assistant verifies the identity under explicit assumptions.

```yaml
status: formally_proved
system: Rocq/Coq or Lean
```

Most current EML work will sit between Levels 1 and 3. That is acceptable, as long as claims are labelled.

The dangerous phrase is:

```text
This proves...
```

unless proof has actually been performed.

A better phrase is:

```text
This candidate passed numerical verification against the reference over the chosen test set.
```

Verification should always include:

- reference function;
- dtype;
- test points;
- tolerance;
- max error;
- domain assumptions;
- branch warnings;
- proof status;
- implementation version.

A verification object:

```yaml
verification:
  reference: numpy.sin
  dtype: complex128
  test_points:
    - sqrt2
    - phi
    - pi/7
  tolerance: 1e-12
  max_abs_error: 2.4e-14
  passed: true
  proof_status: not_attempted
  warnings:
    - finite numerical verification only
```

This is the standard that EML-MCP tools should return.

Verification is not bureaucracy. It is the bridge from beautiful symbolic possibility to trustworthy computation.


---

# Chapter 28: Branch Cuts, Singularities, and Numerical Stability

EML uses logarithms. Logarithms bring branch cuts.

In the complex plane, logarithm is multi-valued. Practical numerical libraries choose a principal branch. EML expressions inherit this choice. When a tree crosses a branch boundary, values can jump.

This is why branch analysis is essential.

Expressions involving:

```text
log
division
reciprocal
powers
trigonometric constructions
complex constants
```

should trigger stability checks.

A stability check might sample a region and report:

```yaml
domain:
  x_min: 0.2
  x_max: 2.0
samples: 1000
issues:
  branch_jumps: 0
  overflow: 0
  near_singularities: 1
  imaginary_residue_max: 3e-16
risk: low
```

For a riskier expression:

```yaml
issues:
  branch_jumps: 4
  overflow: 12
  near_singularities: 3
risk: high
recommendation: restrict domain or use alternate formula
```

Numerical overflow is another problem. Repeated exponentials can grow extremely fast. A symbolic-regression engine may encounter NaNs or infinities. If the implementation clamps values, that must be reported.

Singularities must be explicit. For example:

```text
log(x) undefined at x <= 0 over reals
1/x singular at x = 0
tan(x) singular at pi/2 + k*pi
```

An EML tree that represents these functions inherits these singularities, possibly with additional internal branch structure.

A complete formula record should include:

```yaml
domain:
  external_domain: real
  valid_interval: "(0, infinity)"
  singularities:
    - x = 0
  branch_sensitive: true
  principal_log: true
```

An AI agent using EML must not hide these details. If the user asks for a formula over all real numbers and the expression is only verified for positive x, the final answer must say so.

Branch analysis is the difference between toy symbolic manipulation and serious numerical science.


---

# Chapter 29: Reproducibility and Benchmarks

The EML stack should become reproducible from a clean checkout.

A serious benchmark suite should include:

## 1. Core operator tests

Check:

```text
E(x,1) = exp(x)
E(1,1) = e
```

and foundational constructions.

## 2. Formula catalogue verification

For each catalogue entry:

```text
name
RPN
K
depth
reference
test points
max error
status
```

## 3. Pure/practical comparisons

For selected expressions, compare pure and practical K.

## 4. Simplification tests

Record before/after K and verify that simplification preserves behaviour.

## 5. Symbolic-regression tests

Run fixed-depth recovery tasks with fixed seeds and report distributions, not only successes.

## 6. Discovery tests

Search for known functions under fixed budgets and record success/failure.

## 7. Transformer compilation tests

Compile and verify every RPN catalogue entry.

## 8. Negative tests

Include wrong formulas, invalid RPN, branch traps, overflow traps, and cancelled jobs.

A benchmark report should be generated automatically:

```bash
uv sync --extra dev
uv run pytest
uv run python scripts/reproduce_eml_benchmarks.py
uv run python -m eml_transformer.compiler.verify --show-all
```

The output should include:

```text
benchmark_report.md
catalogue_verification.csv
symbolic_regression_results.csv
transformer_verification.csv
branch_risk_report.json
```

This would transform EML from an exciting prototype ecosystem into a credible research platform.

The most important benchmark principle is that failures are part of the science. A failed depth-4 symbolic-regression run teaches us about the search landscape. A branch failure teaches us about domains. A transformer compilation failure teaches us about catalogue assumptions.

Reproducibility is not the opposite of creativity. It is what lets creativity survive.


---

# Part IX — Practice, Exercises, and Roadmap


---

# Chapter 30: Worked Examples for Learners

This chapter gives learner-level exercises.

## Exercise 1: The first EML expression

Show that:

```text
E(x, 1) = exp(x)
```

Solution:

```text
E(x, 1) = exp(x) - ln(1)
        = exp(x) - 0
        = exp(x)
```

## Exercise 2: Generate e

Show that:

```text
E(1, 1) = e
```

Solution:

```text
E(1, 1) = exp(1) - ln(1)
        = e
```

## Exercise 3: Build a tree

Draw the tree for:

```text
E(E(x, 1), 1)
```

Tree:

```text
      E
     / \
    E   1
   / \
  x   1
```

Evaluate:

```text
E(E(x,1),1) = exp(exp(x))
```

## Exercise 4: Count K

The tree above has:

```text
leaves: x, 1, 1 = 3
internal E nodes = 2
K = 5
```

## Exercise 5: Practical vs pure

Take:

```text
pi + e
```

In practical mode, `pi` and `e` may be leaves.

In pure mode, both must be constructed. Ask:

```text
How much does K increase?
```

## Exercise 6: Verify an identity

Use an EML-MCP server to compile:

```text
sin(x)^2 + cos(x)^2
```

Then compare with SymPy simplification.

Expected mathematical result:

```text
1
```

Expected EML lesson:

```text
The conventional identity is simple, but the pure EML tree may be large.
```

## Exercise 7: Fit a small dataset

Given:

```text
x = [0.5, 1.0, 2.0, 4.0]
y = log(x)
```

Run a fitting or symbolic-regression tool. Ask:

- Does it recover log?
- What K is reported?
- Was the result verified outside the training points?
- Is it pure or practical?

## Exercise 8: Inspect branch risk

Evaluate:

```text
sin(x) + log(x)
```

over:

```text
x in [0.2, 2.0]
```

Then try:

```text
x in [-2.0, 2.0]
```

Observe how real logarithm issues and complex branches appear.

## Exercise 9: Compile to transformer

Using `eml-transformer`, compile:

```text
x sin
```

Then verify against NumPy for several inputs.

Ask:

- How many positions?
- How many layers?
- What is the maximum error?
- Is this faster than NumPy?
- Why is it still interesting?

Exercises like these turn EML from a claim into experience.


---

# Chapter 31: A Roadmap for the Complete EML Stack

The complete EML stack should develop in phases.

## Phase 1: Stabilise the core

- Minimal evaluator.
- Pure/practical compiler.
- Formula records.
- K complexity.
- Basic verification.
- Compact MCP server.

## Phase 2: Build the catalogue

- Store known formulas.
- Record dependencies.
- Add verification metadata.
- Export catalogue to JSON/CSV/Markdown.
- Add simplification rules.

## Phase 3: Improve verification

- Standard test-point suite.
- Random domain sampling.
- Branch-risk reports.
- SymPy proof attempts.
- Optional formal proof bridge.

## Phase 4: Discovery engine

- Direct search.
- Evolutionary search.
- Background jobs.
- Similarity checks.
- Failure logging.

## Phase 5: Symbolic regression

- Master trees.
- PyTorch optimisation.
- Snapping weights.
- Validation tests.
- Benchmark distributions.

## Phase 6: Transformer compilation

- RPN compiler.
- Residual-stream machine.
- Analytic routing.
- Full verification table.
- Exportable modules.

## Phase 7: Algebraic family exploration

- Operator-family definitions.
- Stachowiak-style axioms.
- EDL and variants.
- Constant-free search.
- Stability comparison.

## Phase 8: AI-agent workflows

- MCP profiles.
- Tool safety metadata.
- Formula notebook.
- Explanation templates.
- Reproducible reports.

## Phase 9: Publication

- Technical paper.
- Benchmark release.
- Tutorial notebooks.
- Public formula catalogue.
- MCP server documentation.
- Transformer compilation report.

The strategic principle is:

```text
Make the core boringly reproducible before making the frontier wildly imaginative.
```

The frontier matters. But the foundation must be strong enough to carry it.


---

# Chapter 32: Final Synthesis: The Seed and the Forest

EML begins as one line:

```text
E(x, y) = exp(x) - ln(y)
```

From that line grows a forest.

The first branch is mathematical: a single binary operator and the constant `1` generate elementary functions.

The second branch is symbolic: every expression becomes a binary tree of identical nodes.

The third branch is computational: trees can be evaluated, simplified, verified, and searched.

The fourth branch is architectural: formula trees can be compiled into transformer-shaped machines.

The fifth branch is agentic: MCP exposes the tools to AI systems.

The sixth branch is algebraic: EML belongs to a broader family of cancellation-and-inverse constructions.

The seventh branch is scientific: every discovery demands verification, metadata, reproducibility, and humility.

The beauty of EML is not that it makes mathematics trivial. It does not. The beauty is that it makes a hidden simplicity visible.

A scientific calculator looks like a cabinet of many tools. EML suggests that beneath the cabinet is a seed.

That seed is not enough by itself. It needs soil: implementation. It needs memory: a catalogue. It needs discipline: verification. It needs exploration: discovery. It needs bridges: MCP. It needs embodiment: transformer compilation. It needs critique: algebra and benchmarks.

The complete guide to EML is therefore not merely a guide to an operator. It is a guide to a way of thinking:

```text
Find the primitive.
Grow the tree.
Measure the form.
Verify the claim.
Expose the tool.
Let the agent use it.
Record the discovery.
Return to the seed.
```

The forest is only beginning.


---

# Appendix A: Glossary

**EML** — Exp-Minus-Log, the operator `E(x,y)=exp(x)-ln(y)`.

**Pure mode** — EML representation using only the EML operator, the constant `1`, and variables.

**Practical mode** — EML representation that may use convenient constants or catalogue shortcuts.

**K complexity** — Node-count complexity of an EML tree.

**RPN** — Reverse Polish notation, a stack-friendly linear representation of expression trees.

**MCP** — Model Context Protocol, a protocol for exposing tools, resources, and prompts to AI clients.

**Symbolic regression** — Inferring symbolic formulae from data.

**Branch cut** — A discontinuity introduced by choosing a principal branch of a multi-valued complex function such as logarithm.

**Catalogue** — A stored collection of known EML formulae, metadata, verification results, and derivations.

**Analytic routing** — In the EML transformer context, deterministic attention patterns that route operands rather than learned attention.

---

# Appendix B: Suggested Formula Record

```yaml
formula:
  id: string
  name: string
  conventional_expression: string
  eml_tree: string
  rpn: string
  basis:
    mode: pure | practical | mixed
    terminals: []
    hidden_constants: []
  complexity:
    K: integer
    depth: integer
    leaf_count: integer
  provenance:
    method: seed | constructed | direct_search | symbolic_regression | imported
    source: string
    date: string
    seed: integer | null
  verification:
    status: candidate | numeric_verified | symbolic_verified | formally_proved
    reference: string
    tolerance: float
    max_error: float
    test_points: []
  domain:
    external_domain: real | complex | restricted
    internal_arithmetic: complex128
    branch_sensitive: boolean
    singularities: []
  notes: string
```

---

# Appendix C: Suggested MCP Tool Catalogue

```yaml
eml_compile:
  purpose: Compile a conventional expression into EML.
  side_effects: none

eml_eval:
  purpose: Evaluate an EML or conventional expression.
  side_effects: none

eml_simplify:
  purpose: Reduce an EML tree using rewrite rules and catalogue identities.
  side_effects: optional database write if saving result

eml_verify:
  purpose: Compare an EML tree against a reference function.
  side_effects: optional verification record

eml_stability_check:
  purpose: Inspect branch, overflow, singularity, and residue risks.
  side_effects: none

eml_discover_start:
  purpose: Launch bounded formula discovery.
  side_effects: creates job and may write results

eml_symbolic_regression:
  purpose: Fit a parameterised EML tree to data.
  side_effects: may create regression result records

eml_similarity:
  purpose: Compare EML trees structurally and behaviourally.
  side_effects: none

eml_transformer_compile:
  purpose: Compile RPN EML expression into transformer-shaped module.
  side_effects: optional export
```

---

# Appendix D: Minimal Python Sketch

```python
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class One:
    pass

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class E:
    left: object
    right: object

def eml(a, b):
    return np.exp(np.asarray(a, dtype=np.complex128)) - np.log(np.asarray(b, dtype=np.complex128))

def evaluate(expr, env):
    if isinstance(expr, One):
        return np.complex128(1.0)
    if isinstance(expr, Var):
        return np.complex128(env[expr.name])
    if isinstance(expr, E):
        return eml(evaluate(expr.left, env), evaluate(expr.right, env))
    raise TypeError(expr)

x = Var("x")
exp_x = E(x, One())
print(evaluate(exp_x, {"x": 0.5}))
```

---

# Appendix E: Benchmark Checklist

- Core operator tests.
- Pure/practical mode comparison.
- Catalogue verification.
- Simplification before/after K.
- Branch and domain tests.
- Symbolic-regression success and failure distributions.
- Discovery search reproducibility.
- Transformer compilation verification.
- Negative tests for invalid formulas.
- Exported benchmark report.

---

# Appendix F: Source Notes

- **All elementary functions from a single operator** — https://arxiv.org/html/2603.21852v2  
  arXiv:2603.21852v2, 04 Apr 2026. Presents EML(x,y)=exp(x)-ln(y), constant 1, binary trees, scientific-calculator basis, and symbolic-regression experiments.
- **Algebraic structure behind Odrzywołek’s EML operator** — https://arxiv.org/html/2604.23893  
  arXiv:2604.23893v1, 26 Apr 2026. Frames EML through abelian-group-like cancellation and functional inverse structure.
- **Electro-resonance/EML-MCP** — https://github.com/Electro-resonance/EML-MCP  
  README lists seven MCP tools and pure/practical compilation modes.
- **angrysky56/eml-mcp** — https://github.com/angrysky56/eml-mcp/tree/main/src/eml_mcp  
  Directory contains primitives, trees, registry, database, compiler, simplifier, discovery, jobs, regression, server, similarity, transformer, and attention modules.
- **angrysky56/eml-transformer** — https://github.com/angrysky56/eml-transformer  
  README says Layer 1 compiles 27 elementary functions, verifies to 1e-12 against NumPy, and is not a production inference accelerator.
- **Model Context Protocol Specification** — https://modelcontextprotocol.io/specification/  
  Used as the protocol framing for EML-MCP tool interfaces.

---

# Appendix G: Suggested Further Work

1. Build a public EML formula atlas.
2. Add proof-assistant bridges for selected core identities.
3. Create an EML benchmark leaderboard.
4. Implement operator-family exploration from Stachowiak’s algebraic template.
5. Integrate EML-MCP with local LLM agents.
6. Create educational notebooks for school/university-level demonstrations.
7. Add visual tree rendering and interactive simplification.
8. Package EML transformer machines as inspectable mathematical modules.
9. Develop domain-specific EML variants for signal processing and physics.
10. Publish a reproducibility paper for the complete stack.

