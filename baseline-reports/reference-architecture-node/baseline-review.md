# reference-architecture-node — baseline review

Review date: 2026-11-15
Review method: AI-assisted manual source review against the supplied R01–R10 definitions, combined with previously supplied local validation output. This is not an independent second-rater assessment.

## Decision

The adjusted source is suitable for the first in-memory tuning pilot under the documented R01–R10 scope. No confirmed baseline violations of those ten rules were found in the reviewed production source. No additional source fix is recommended before starting that pilot.

This is a baseline assessment, not a labelled dataset sample and not a certification of all Clean Architecture principles. It relies on the recorded local validation results described below; commands were not rerun during this document review. PostgreSQL runtime validation remains unavailable in the supplied evidence. Samples that change SQL, PostgreSQL mappings, or database-specific behavior need appropriate database validation before acceptance.

## Identity and evidence provenance

| Item | Value |
| --- | --- |
| Project | `reference-architecture-node` |
| Adjusted baseline SHA | `163c921c33e6eb396d8999df1d8336a41d1572c7` |
| Earlier baseline SHA, from project history supplied in conversation | `94703f25692f57aaac7c40e3f6951a04070c7ee5` |
| Source inspected | Uploaded `reference-architecture-node-baseline.zip` |
| Archive commit marker | ZIP comment matches the adjusted baseline SHA |
| Build/test evidence directory | `baseline-reports/reference-architecture-node/20261112T153326796908Z/` |
| Dependency evidence directory | `baseline-reports/reference-architecture-node/architecture-163c921/` |
| Definitions inspected | Uploaded `rules(1).yaml`, corresponding to `rules/rules.yaml` |
| Guide inspected | Uploaded `labelling-guide(1).md`, corresponding to `labelling-guide.md` |
| Licence found in source | MIT; retain the supplied copyright and licence notice |

The ZIP commit comment supports identification but is not independent verification against the remote Git object. All production TypeScript files under `src/`, all nine test files, the package manifest, TypeScript and coverage configuration, SQL schema, README architecture description, and licence were inspected. Line references below are relative to the exported source root at the adjusted baseline.

The baseline and configuration execution results below were supplied as terminal output by the dataset maintainer. The source archive does not contain the dataset-level JSON reports or tooling configuration. Their contents were not independently reloaded in this review; configuration scope is based on the configuration and script shown in the conversation, together with the maintainer's outputs.

Content fingerprints (SHA-256):

```text
reference-architecture-node-baseline.zip
f6c65a941d13161dbcbe2939f06d438b6fafb63b28c71b60160da6941f140cc6

rules(1).yaml
42618b86ede0238b41348d5e9a294cf14e49643afb047e5c2a3520bc17698f23

labelling-guide(1).md
217733eabdf68d9fac36f514efb5714076091afcbd7258de487a73c666ecf50e
```

The dataset commit identifying the supplied rule/guide versions was not provided. Before accepting sample records, record Git commit identifiers for the matching rule-set and guide versions as required by the guide; these content fingerprints supplement, rather than replace, those identifiers. Keep the project's existing tuning/test assignment unchanged.

## Architecture mapping

| Path | Responsibility and rule interpretation |
| --- | --- |
| `src/domain/**` | Domain entities, value objects, errors, title/description policy, and task transitions. |
| `src/application/use-cases/**` | Application orchestration: obtain domain objects through a repository port, invoke domain behavior, save results, return DTOs. |
| `src/application/ports/task-repository.ts` | Application-owned output port; its contract uses domain types and ordinary promises/arrays. |
| `src/application/dto/task-dto.ts` | Application-owned output representation and pure conversion. |
| `src/infrastructure/http/**` | Presentation/HTTP adapter: request parsing, routes, response/error formatting, and server setup. Although physically under infrastructure, it is presentation for R03, R04 and R09. Domain imports into this outer adapter area would also be outward dependencies for R01. |
| `src/infrastructure/persistence/**` | Concrete in-memory and PostgreSQL repository adapters. |
| `src/infrastructure/config/env.ts` | External environment parsing and technical configuration. |
| `src/infrastructure/config/container.ts` | External composition: selects repositories and injects them into use cases. |
| `src/main.ts` | External bootstrap: loads environment, wires server, starts listening. |
| `tests/**` | Test setup and assertions; constructing concrete adapters here does not make production use cases coupled to them. |

The mapping follows source responsibilities and the source README, lines 25–48. Composition is an allowed responsibility, not a blanket exemption for future business logic placed in these files.

## Dependency classifications

| Dependency or symbol | Classification for this review |
| --- | --- |
| `fastify`, `@fastify/swagger`, `@fastify/swagger-ui` and their framework types | Framework/HTTP integration dependencies prohibited in domain by R05. Currently confined to the outer HTTP adapter. |
| `pg`, including `Pool`, client/query APIs and database-specific types | Persistence dependency prohibited in domain/application by R06. Currently confined to `postgres-task-repository.ts`. Explicit imports from `@types/pg`, or re-exported PostgreSQL types, also need classification/resolution in future samples. |
| `TaskRow` in the PostgreSQL adapter | Adapter-owned database row shape. Kept private to infrastructure; converted to a domain object. |
| `TaskRepository` | Application-owned port, not a persistence-client API. Its name does not make it R06-prohibited. |
| `Task`, `TaskId`, `TaskStatus`, `TaskDTO` | Domain/application-owned types with no ORM or database-specific contract. |
| `zod` | General-purpose validation library, not automatically a prohibited web/DI framework. Current uses parse HTTP input and environment variables outside domain. Future framework-specific integrations require separate classification. |
| `node:crypto` / `randomUUID` | Platform UUID utility, not a web framework, persistence API, or constructed infrastructure adapter under these rules. Its domain use is explicitly acknowledged; this review does not claim the domain has no platform dependencies. |
| `Date`, `Map`, ordinary error classes | Language/runtime facilities; their construction alone is not R10 infrastructure construction. |

## R01–R10 review

“No violation found” below concerns this baseline under the supplied definitions. For later samples, review newly introduced relationships relative to this baseline and record every applicable rule.

| Rule | Finding | Source evidence and rationale |
| --- | --- | --- |
| R01 — domain → infrastructure | No violation found | Domain imports in `src/domain/task.ts:1–3`, `task-id.ts:1–2`, and `task-status.ts:1` resolve to domain files or `node:crypto`. `errors.ts` has no imports. No domain dependency resolves to a project infrastructure module. |
| R02 — domain → application | No violation found | The same complete domain import review finds no application target. Domain methods do not depend on application DTOs, ports, or use cases. |
| R03 — application → presentation | No violation found | All application imports resolve to domain or application-owned code. For example, `src/application/use-cases/create-task.ts:1–3` and `start-task.ts:1–4`. `TaskUseCases` is presentation-owned (`task-routes.ts:10–17`), but only outer composition/server code and tests reference it; application use cases do not. |
| R04 — presentation bypasses use cases | No violation found | `src/infrastructure/http/routes/task-routes.ts:23–75` delegates all six task operations to `useCases.*.execute`. No handler calls a repository, database client, or external-service adapter. The static health response in `server.ts:38–42` performs no task persistence operation. |
| R05 — domain framework coupling | No violation found | All four domain files contain plain TypeScript classes/types and domain imports, plus the classified UUID utility. No framework imports, framework decorators, framework base classes, or HTTP request/response types occur in domain. |
| R06 — inner persistence-specific types | No violation found | `src/application/ports/task-repository.ts:1–12` uses `Task`, `TaskId`, promises and arrays. Domain/application contain no `pg` or adapter row types. `Pool` and `TaskRow` stay in `src/infrastructure/persistence/postgres-task-repository.ts:1–23,46–78`. |
| R07 — use cases bypass inward-owned abstractions | No violation found | All six use cases receive the application-owned `TaskRepository` and use its declared operations. See `create-task.ts:10–16`, `get-task.ts:6–14`, `list-tasks.ts:4–9`, `start-task.ts:6–17`, `complete-task.ts:6–17`, and `delete-task.ts:5–14` under `src/application/use-cases/`. Both adapters implement this contract. |
| R08 — application executes external I/O directly | No violation found | Application operations call the repository port and perform domain/DTO transformations. No application-local filesystem, network, email, database-client, or broker calls were found. SQL execution is in the PostgreSQL adapter (`postgres-task-repository.ts:26–67`). |
| R09 — presentation owns business decisions | No violation found in adjusted source | HTTP schemas check strings and UUID syntax (`src/infrastructure/http/schemas.ts:3–10`). Routes delegate; `error-handler.ts:22–49` translates outcomes. Title/description policy is in `src/domain/task.ts:63–72`; transition policy is in `src/domain/task-status.ts:6–10,38–42`, invoked by domain methods and application use cases. |
| R10 — inner infrastructure construction | No violation found | Repository selection/construction occurs in external composition (`src/infrastructure/config/container.ts:22–34`); `new Pool` occurs in the PostgreSQL adapter (`postgres-task-repository.ts:22–24`). Inner construction is of domain objects, errors, and dates, not concrete infrastructure dependencies. |

## R09 baseline adjustment

The supplied project history records an adjustment from `94703f2…` to `163c921…`: HTTP length constraints were removed so that task title limits and description normalization are owned by the domain. The earlier source revision was not re-reviewed in this pass; the adjusted behavior was verified directly in the supplied source.

- Current HTTP input: required string title, optional string description, UUID parameter syntax.
- Domain title policy: trim, reject an empty result, reject more than 200 characters.
- Domain description policy: default to empty, trim, truncate to 2,000 characters.
- Behavior change recorded in the prior review: long descriptions now reach domain truncation rather than being rejected by the HTTP schema.
- Regression evidence in current source: `tests/integration/task-api.test.ts:148–162` checks blank/overlong titles return `InvalidTaskTitleError`; lines 164–194 check normalized output and subsequent retrieval of the truncated description through the in-memory API.

This is a project-specific ownership decision. The supplied R09 definition permits transport validation; it does not make every string-length check in every HTTP schema an architectural violation. Future labels must explain why a particular check implements business policy.

## Recorded execution evidence

| Check | Recorded outcome | Evidence location relative to project baseline-reports directory |
| --- | --- | --- |
| Baseline identity and clean working tree | SHA matches adjusted baseline; initial/final source status clean | `20261112T153326796908Z/baseline-sha.log`, `initial-git-status.log`, `final-git-status.log` |
| Environment | Node 22.23.5; npm 10.9.9 | Same run's `node-version.log` and `npm-version.log` |
| Lockfile installation | Exit 0; historical audit output reported 24 vulnerabilities (1 low, 12 moderate, 11 high) | Same run's `install.log`; this is not a current vulnerability assessment |
| Lint | Passed | Same run's `lint.log` |
| Type checking | Passed | Same run's `typecheck.log` |
| Tests and coverage | 9 files / 58 tests passed; 100% for measured statements, branches, functions and lines | Same run's `coverage.log` |
| Build | Passed | Same run's `build.log` |
| Dependency analysis | 27 modules and 68 dependencies cruised; zero configured violations | `architecture-163c921/dependencies.json`; count/result reported in terminal output |
| Configuration probes | Seven cases passed | `architecture-163c921/configuration-tests/results.json` and per-case reports |
| Architecture environment | dependency-cruiser 18.7.2; TypeScript installed alongside it using source project's installed version | `architecture-163c921/environment.txt`; use this file for the exact recorded compiler version |

The source install audit and the dataset-tooling install audit are different dependency sets. The tooling's reported zero vulnerabilities does not supersede the source project's recorded findings. Dependency updates would require a newly pinned baseline and revalidation; none were made during this review.

### Configuration verification and limits

The seven cases comprise one allowed domain import, five expected R01/R02/R03/R05/R06 findings, and one unresolved import. Reported results confirm that each probe was analysed, JSON parsing succeeded, and the detected rule-name set matched the expected set.

The JSON runs returned exit code 0 for both allowed and violating probes. The corrected script checks the JSON findings as well as command completion. A future validation gate must inspect the report; exit code 0 by itself must not mean architectural compliance. An unresolved import is a tool/analysis finding, not an extra R01–R10 label.

These are dependency-tool fixtures, not valid research samples. Their exported symbol names are not proven type-correct by dependency analysis; they were not build/test validated as feature patches. They must not be added as dataset rows.

The checks establish only the shown patterns: simple relative type re-exports, one Fastify dependency, one PostgreSQL dependency and a missing module. They do not establish full detection of aliases, chained barrels, every framework package, all persistence symbols, runtime imports, dynamic imports, require expressions or all possible ownership mappings. No alias mapping is configured in the supplied project `tsconfig.json`. Add targeted checks when future sample patterns need them.

R04 and R07–R10 rely on contextual source review. R05 and R06 automation uses bounded package lists, not exhaustive symbol classification. A zero-finding report is not sufficient by itself to accept a sample.

### Coverage and runtime limits

`vitest.config.ts:11–16` excludes `src/main.ts`, `src/infrastructure/config/container.ts`, `src/infrastructure/persistence/postgres-task-repository.ts`, and application port definitions from coverage. Therefore 100% is scoped coverage, not coverage of every production file.

`tests/integration/task-api.test.ts:13–22` wires an in-memory repository directly into use cases. The supplied tests provide no PostgreSQL integration run. README statements and the PostgreSQL adapter comment about real database validation are not execution evidence for this review.

Other acknowledged baseline behavior outside the ten-rule findings: `Task.restore` accepts stored title/description without reapplying creation normalization (`src/domain/task.ts:52–60`); in-memory storage retains `Task` object references (`in-memory-task-repository.ts:12–17`); list order differs between insertion-order memory storage and SQL's descending creation time. Do not assume adapter parity, persistence integrity, or ordering guarantees beyond the feature specification and tests.

## Pilot handoff

1. Commit this report at `baseline-reports/reference-architecture-node/baseline-review.md` alongside the existing evidence; retain earlier validation runs as history.
2. Update the dataset README's stale “automated architecture checks remain pending” statement to describe the completed configured checks and their limits.
3. Record matching Git rule-set and guide versions in sample metadata. Preserve the existing project split; do not send review findings or validation reports to the evaluated checker as context.
4. Start a small in-memory feature task from the adjusted SHA. A suitable candidate is exposing the existing domain `Task.rename` operation through an application use case and HTTP route, with explicit behavior and tests.
5. Apply each matched variant independently to the same baseline. Check all ten rules, functional equivalence, build/type checks, relevant tests, and dependency findings. Only then add reviewed sample records to `labels.csv`; record all overlapping rule IDs and keep unresolved cases outside evaluation.

No dataset samples were created or labelled by this baseline review. Independent reviewer decisions, agreement measures, and final sample acceptance remain separate activities under the labelling guide.
