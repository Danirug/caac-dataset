# CAAC dataset
Labelled TypeScript code changes with Clean Architecture violations.

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
