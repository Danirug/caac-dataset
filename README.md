# CAAC dataset
This repository contains a labelled dataset of about 320 Git code changes drawn from open-source TypeScript projects that follow Clean Architecture. Each change implements a realistic feature task; compliant changes follow the project’s layering, while violating changes break exactly one rule from a ten-rule set adapted from the CA01–CA08 criteria of Gonzalez Bravo et al. (2026), such as a domain module importing infrastructure or business logic placed in a controller. Every sample compiles and passes the project’s tests, so the dataset captures code that works but breaks the intended architecture. Labels record the rule, file and line of each violation, whether the rule is visible from the diff alone or requires wider context, and whether the sample is a deliberately tricky compliant case. Samples are generated with an AI coding assistant from a different model family than the one used to evaluate them, validated by build, test and dependency-cruiser gates, and checked by a second rater using Cohen’s kappa. The dataset exists to answer one question: how much repository context does an LLM need to detect architectural violations in a code change accurately, and at what cost. It is the evaluation set for the Context-Aware Architecture Checker

## Decisions
- Checker model:         <name, context window>
- Generator model:       <name, different family from checker>
- Project token ceiling: <number>

## Projects
| name | upstream | fork | baseline SHA | tokens | split |
|------|----------|------|--------------|--------|-------|

## Layout
projects/         git submodules pinned at baseline SHA
samples/<project>/<task>/   correct.patch, broken-Rxx.patch
labels.csv        one row per violation; compliant samples have rule_id empty
rules/rules.yaml  canonical rule set R01-R10
baseline-reports/ build, test and dependency-cruiser output per project
scripts/          measure_tokens.py, check_baseline.sh, new_sample.sh, validate_labels.py
