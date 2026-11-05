# CAAC dataset
This repository contains a labelled dataset of about 320 Git code changes drawn from open-source TypeScript projects that follow Clean Architecture. Each change implements a realistic feature task; compliant changes follow the project’s layering, while violating changes break exactly one rule from a ten-rule set adapted from the CA01–CA08 criteria of Gonzalez Bravo et al. (2026), such as a domain module importing infrastructure or business logic placed in a controller. Every sample compiles and passes the project’s tests, so the dataset captures code that works but breaks the intended architecture. Labels record the rule, file and line of each violation, whether the rule is visible from the diff alone or requires wider context, and whether the sample is a deliberately tricky compliant case. Samples are generated with an AI coding assistant from a different model family than the one used to evaluate them, validated by build, test and dependency-cruiser gates, and checked by a second rater using Cohen’s kappa. The dataset exists to answer one question: how much repository context does an LLM need to detect architectural violations in a code change accurately, and at what cost. It is the evaluation set for the Context-Aware Architecture Checker

## Decisions
- Checker model:         Google Gemini Flash via the Gemini API free tier (exact model id: <copy from AI Studio>, 1M context)
- Generator model:       OpenAI model via GitHub Copilot (Student Developer Pack); exact model id: <from Copilot settings>
- Project token ceiling: 100,000 tokens (src/**/*.ts excluding tests), measured with scripts/measure_tokens.py
- Dataset target:        500 validated samples; ~600 generated to allow for rejections
- Budget:                $0 planned (free tiers); $20 reserve for paid Flash-Lite if daily quota is insufficient
- Repeats:               3 repeats at temperature 0 on a 50-sample subset; single run on the remaining samples

## Projects

| name | upstream | fork | baseline SHA | tokens | split |
|------|----------|------|--------------|--------|-------|
| typescript-clean-architecture | [pvarentsov/typescript-clean-architecture](https://github.com/pvarentsov/typescript-clean-architecture) | [Danirug/…](https://github.com/Danirug/typescript-clean-architecture) | `5c29c39e402c67105ca66ec4dd2a4cf84b285e39` | 40,458 | test |
| domain-driven-hexagon | [Sairyss/domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon) | [Danirug/…](https://github.com/Danirug/domain-driven-hexagon) | `5c2d15a7e2d69e83dfddf28468ee9f30e02c30de` | 20,949 | tuning |
| typescript-microservice-template | [onlythompson/typescript-microservice-template](https://github.com/onlythompson/typescript-microservice-template) | [Danirug/…](https://github.com/Danirug/typescript-microservice-template) | `869eccad6fafdc7989986b26e8898c03b4e1b695` | 15,445 | test |
| nestjs-clean-boilerplate | [Gi-jutsu/nestjs-clean-boilerplate](https://github.com/Gi-jutsu/nestjs-clean-boilerplate) | [Danirug/…](https://github.com/Danirug/nestjs-clean-boilerplate) | `7ed518ea0a7f52b2d6aab79e1806c092806bb0e0` | 10,129 | test |
| reference-architecture-node | [eriksonwilliam/reference-architecture-node](https://github.com/eriksonwilliam/reference-architecture-node) | [Danirug/…](https://github.com/Danirug/reference-architecture-node) | `94703f25692f57aaac7c40e3f6951a04070c7ee5` | 5,260 | tuning |
| nestjs-clean-architecture-boilerplate | [toyo12312/nestjs-clean-architecture-boilerplate](https://github.com/toyo12312/nestjs-clean-architecture-boilerplate) | [Danirug/…](https://github.com/Danirug/nestjs-clean-architecture-boilerplate) | `eb1ae324c13faca5538a21ae97112e222159949a` | 3,866 | test |

All licences MIT. Tokens measured with `scripts/measure_tokens.py` on `src/**/*.ts` excluding tests. Ceiling: 100,000 tokens.
## Layout
projects/         git submodules pinned at baseline SHA
samples/<project>/<task>/   correct.patch, broken-Rxx.patch
labels.csv        one row per violation; compliant samples have rule_id empty
rules/rules.yaml  canonical rule set R01-R10
baseline-reports/ build, test and dependency-cruiser output per project
scripts/          measure_tokens.py, check_baseline.sh, new_sample.sh, validate_labels.py
