# Labelling guide

Status — Initial guide for pilot validation.

This guide describes how to review architectural changes in the CAAC dataset. Use the version of `rules/rules.yaml` recorded for the sample. That file provides the operational definitions of R01–R10, adapted mainly from CA01–CA05 in González Bravo et al., Section 3.3, Tables 2–3. The procedures below are our dataset methodology.

## 1. What a sample is

A sample is one patch applied independently to a recorded baseline commit of a selected project. Review the baseline and the resulting project together. A patch alone may omit evidence needed to determine a dependency's destination or a component's responsibility.

Each sample belongs to a feature task. A matched compliant and violating pair implements the same intended feature from the same baseline, with comparable functional behavior. Apply each variant to the baseline independently. Match the variants through their task ID.

Use a documented architecture mapping to identify domain, application, presentation, infrastructure, and composition code. Establish roles from responsibilities and dependencies as well as directory structure. Record ambiguous assignments for resolution before accepting affected samples.

All variants of a task remain in the same split. Keep the project-level tuning and test assignments fixed. Develop prompts and revise this guide using tuning projects. Changes to the protocol after test evaluation require disclosure and a new evaluation plan.

## 2. Label schema

Separate the architectural label from validation and review status.

| Architectural label | Meaning | Rule IDs |
| --- | --- | --- |
| compliant | Review finds no introduced violation of R01–R10 and sufficient evidence supports the decision. | Empty set |
| violating | Review confirms at least one introduced violation. | All confirmed applicable IDs |
| unresolved | Evidence or a rule interpretation is insufficient for a final decision. | Preserve confirmed and suspected findings separately in review notes. |

Compliant refers to the defined rules and the reviewed change. It does not certify the entire repository against every Clean Architecture principle. Missing evidence does not justify a compliant label.

Track validation outcomes independently as pass, fail, or unavailable for patch application, build/type checking, relevant tests, and static analysis. Track review status as pending, accepted, or excluded. Only accepted samples with resolved architectural labels enter the evaluated dataset.

The record for each sample must identify the following information. These are required concepts to map to the existing `labels.csv` columns and linked review records when the CSV schema is finalized.

| Information | Purpose |
| --- | --- |
| Sample ID and task ID | Identify the patch and link matched variants. |
| Project, baseline SHA, patch path, and split | Reconstruct the input and preserve the split. |
| Rule-set version and guide version | Identify the definitions used for review. Use Git commit identifiers. |
| Architectural label and applicable rule IDs | Record the final decision and every confirmed violation. |
| Evidence and rationale | Record file paths, locations, symbols, and why each finding satisfies a rule. |
| Validation outcomes and logs | Support patch, build, test, and static-check results. |
| Reviewer decisions and resolution | Preserve independent judgments and the final outcome. |

Keep generator provenance and intended mutation labels for reproducibility. Hide intended labels and variant-revealing filenames from the independent reviewer and from evaluated checker inputs.

## 3. Decision procedure

1. Confirm the sample ID, baseline SHA, patch, split, rule-set version, and project architecture mapping.
2. Apply the patch to a clean checkout of its baseline. Stop acceptance if the patch fails to apply.
3. Inspect the diff and enough surrounding code to resolve imports, aliases, re-exports, contracts, callers, and relevant dependency wiring.
4. Assess every rule R01–R10. Treat the generator's intended violation as a hypothesis that requires verification.
5. For each finding, identify the changed code, source responsibility, target or operation, applicable rule, and relevant allowed cases. Compare baseline and patched code to establish that the violation was introduced.
6. Run the recorded build/type-check and relevant test commands. Compare failures with baseline results. Record unavailable checks explicitly. Resolve introduced failures before accepting the sample. Pre-existing or environment failures require a documented project-level decision applied consistently.
7. Run configured static checks. Compare new findings with the baseline and inspect each result. For violating samples, an expected architectural finding may cause the static checker to exit unsuccessfully. Interpret the report and distinguish findings from tool execution errors.
8. Assign the architectural label, record all applicable rule IDs, and determine acceptance eligibility. Unresolved samples stay outside final evaluation.

### Per-rule decisions

The examples below identify patterns. Apply the complete rule definition and check for other violations before accepting a sample.

| Rule | What to establish | Violating pattern | Compliant lookalike |
| --- | --- | --- | --- |
| R01 | Domain source depends on an infrastructure-owned module. | A domain service imports an infrastructure-owned repository interface. | It imports a domain-owned repository interface. |
| R02 | Domain source depends on application-owned code. | An entity imports an application use case or its DTO. | A use case imports the entity. |
| R03 | Application source depends on presentation-owned code. | A use case imports a controller-owned request DTO. | A controller converts the request into an application-owned input type. |
| R04 | A presentation handler performs an application operation through infrastructure while bypassing a use case. | A controller directly invokes a repository to save an order. | It calls an application service that coordinates saving the order. |
| R05 | Domain source depends on a prohibited framework package or symbol. | A domain class imports and uses NestJS's Injectable decorator. | External configuration registers a plain domain class. |
| R06 | Domain or application source references a persistence-specific type or API. | A use case exposes Prisma-generated query options. | It accepts an application-owned filter mapped by an adapter. |
| R07 | A use case depends on a concrete persistence implementation or an inappropriate repository contract. | Its constructor requires a concrete PostgreSQL repository. | It receives an inward-owned repository interface. |
| R08 | Application code directly executes external I/O. | A use case calls fetch to contact a payment provider. | It calls an inward-owned payment port implemented by an adapter. |
| R09 | Presentation code owns a business decision. | A controller calculates a loyalty discount. | It formats a discount calculated by the domain or application. |
| R10 | Domain or application code constructs concrete infrastructure. | A use case constructs a database client. | Composition code creates the adapter and injects its port. |

### Independent review and disagreements

A second reviewer independently labels a subset sampled across projects, rules, and compliant/violating cases. Record its selection procedure, size, and seed before review. Provide neutral sample identifiers, feature descriptions, the pinned code, architecture mappings, and the same rule-set and guide versions.

Preserve both reviewers' original judgments before discussion. Record disagreements about the architectural label and each applicable rule. Resolve them through joint evidence review, with a designated third reviewer or supervisor when needed. Record the reason for the final decision. Unresolved cases remain excluded.

Report agreement using the original independent labels. Report binary violation agreement separately from rule-level agreement. If using Cohen's kappa, calculate it for two reviewers before adjudication and report unresolved cases and denominators explicitly. Do not combine multiple rule labels into one arbitrary category.

## 4. Scope — only violations introduced by the change

The review target is the architectural effect of the patch relative to the baseline. Record existing issues in baseline reports without counting them as new sample findings.

A finding can involve unchanged code when the patch creates a new violating relationship, moves a component across a boundary, or adds a new use of an existing dependency. Explain how the patch caused the violation and cite the relevant changed and supporting locations.

Removing a violation does not create a positive violation label. A change that only removes violations can be compliant with respect to introduced violations, provided no other new rule is broken.

Use the same code versions and label definitions across checker strategies. Provide architectural mappings consistently where required by the protocol. Keep ground-truth labels, reviewer rationales, generator instructions, and validation reports outside checker input. A separate generator model family is a provenance choice and does not prove absence of model-training contamination.

## 5. Multi-violation samples

Record all confirmed rules, even when one code operation violates several rules. Multiple occurrences of the same rule count as one distinct rule ID, with each occurrence documented.

- A single-rule violating sample has exactly one distinct applicable rule ID.
- A multi-rule sample has two or more distinct applicable rule IDs.
- A compliant sample has no introduced violations under any of R01–R10.

Keep multi-rule samples outside the planned single-rule evaluation subset. Revise and revalidate them, or retain them in a separately identified exploratory subset with an explicit evaluation plan. Never remove valid labels simply to satisfy a sample quota.

R07 and R10 may overlap when a use case constructs a concrete repository. R06 and R08 may overlap when it invokes a database client directly. Other combinations are possible. Pilot generation must establish whether enough unambiguous single-rule samples can be produced for each rule. Revise the sampling target or definitions explicitly if needed, then relabel affected samples.

## 6. Tricky patterns and how to tell them apart

- **Type-only imports.** Count them as source dependencies where the rule includes them, even though TypeScript removes them at runtime.
- **Aliases and barrels.** Resolve imports to the defining module. A neutral-looking import path can re-export an infrastructure or framework symbol.
- **Injected dependencies.** Injection alone does not establish compliance. Check the declared contract, its owner, and implementation-specific usage.
- **Composition code.** Construction and wiring are permitted in documented composition code. A composition filename does not exempt business operations mixed into it.
- **Interfaces and abstract classes.** Judge ownership and coupling. A contract in infrastructure can still create an outward dependency.
- **Names and folder conventions.** A class named Entity, Repository, or Service is insufficient evidence of its architectural role.
- **Request validation.** Required fields and syntax checks can belong to presentation. Eligibility, pricing, and business state transitions require domain or application decisions.
- **Construction.** Creating a domain entity or value object is allowed. R10 concerns concrete infrastructure dependencies.
- **External libraries.** Use documented framework and persistence classifications. General-purpose utility libraries are not automatically prohibited.
- **Static-check results.** No findings do not establish compliance for context-dependent rules. A reported finding still requires verification against ownership, scope, and exceptions.
- **Missing tests.** Record test coverage and unavailable checks honestly. Build success and test success alone do not establish architectural compliance.

Review this guide during the tuning pilot. Version changes in Git and record which samples require relabelling. Freeze the reviewed guide and rule definitions before the held-out evaluation.
