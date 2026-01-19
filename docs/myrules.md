# CLI Declarative Argument Architecture Protocol (Vibe Coding Edition v2.0)

## I. Core Principles

*   **Global Uniqueness:** All parameter names must be unique across the entire program. Parameter names can include hierarchical prefixes (e.g., `--org-summary`), as long as the full name is unique. Prefixes are considered part of the name, not a separate hierarchical identifier.
*   **Implicit Initialization:** Whenever a subordinate attribute is detected, the system must automatically activate its parent Entity and apply the default context.
*   **Read-Oriented Semantics:** Default configurations aim to provide maximum data coverage, reducing the need for explicit declarations.
*   **Collaboration First:** When new design requirements conflict with these rules, the AI should **proactively notify the user** to discuss whether to adjust the solution or revise the rules, rather than making a unilateral decision.

---

## II. Classification Codes (E-A-X-D)

We decompose parameter logic into four professional dimensions. Use these codes directly when instructing:

### **E (Entity): Logical Node**

*   **Definition:** A logical object container or functional namespace.
*   **Characteristics:** Does not necessarily appear directly as a CLI parameter, but serves as a unit for logical organization.
*   **Instruction Example:** `Define Entity E101: Network-Stack`

### **A (Attribute): Independent Attribute**

*   **Definition:** A globally unique leaf parameter that directly carries a value.
*   **Dependency:** Every **A** must and can only map to one **E**.
*   **Agile Logic:** Triggering `A` automatically derives the corresponding `E`.
*   **Instruction Example:** `Assign Attribute A201 (--port) to E101`

### **X (Exclusion): Mutually Exclusive Constraint**

*   **Definition:** Hard conflict rules between attributes or entities.
*   **Logic:** In a set `[A_i, A_j]`, only one member can exist.
*   **Instruction Example:** `Set Exclusion X301 on [A205, A208]`

### **D (Derivation): Derivation Rule**

*   **Definition:** The default state of a parent or associated entity when explicitly or implicitly initialized.
*   **Logic:** `If Condition(A) -> Then Set State(E)`.
*   **Instruction Example:** `Set Derivation D401: If any A of E102 exists, set E102.mode = "readonly"`

---

## III. Vibe Coding Instructions

When instructing AI to write code or add parameters, use the following standardized instruction format:

> **Instruction: [Operation Type] [ID]**
> *   **ADD E101:** Declare new Entity `Storage`.
> *   **BIND A501 (--path) TO E101:** Bind a unique attribute to an entity.
> *   **ASSERT X601 OVER [A501, A502]:** Declare two attributes as mutually exclusive.
> *   **ENABLE IMPLICIT-INIT FOR E101:** Enable agile mode for this entity, allowing attributes to reverse-derive the entity.

---

## IV. Internal Parsing Logic State Machine

1.  **Flattened Capture:** Capture all unique identifiers from `argv`.
2.  **Entity Mapping:** Retrieve the **A -> E** mapping table and mark all active entities.
3.  **X-Constraint Check:** Iterate through all **X** sets and check if active attributes violate exclusion logic.
4.  **Context Synthesis:** Trigger **D** rules to complete all parent context parameters that were not explicitly specified.
5.  **Object Tree Assembly:** Assemble flat parameters into a structured object (JSON/Object) and pass it to the business logic layer.

---

## V. Exception Standards

*   **Conflict Error:** "Invalid Argument Combination: [A_i] and [A_j] are mutually exclusive."
*   **Ambiguity Error:** (Triggered only when global uniqueness is violated) "Ambiguous Property: [A_n] matches multiple Entities."

