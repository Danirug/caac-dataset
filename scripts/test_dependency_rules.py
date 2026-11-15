import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    project = root / "projects" / "reference-architecture-node"
    checker = root / "node_modules" / ".bin" / "depcruise"
    config = root / "rules" / (
        "reference-architecture-node.dependency-cruiser.cjs"
    )
    output = root / "baseline-reports" / (
        "reference-architecture-node"
    ) / "architecture-163c921" / "configuration-tests"
    output.mkdir(parents=True, exist_ok=True)

    cases = [
        (
            "allowed-domain-import",
            "domain",
            "export type { Task } from './task';\n",
            set(),
        ),
        (
            "R01",
            "domain",
            "export type { InMemoryTaskRepository } from "
            "'../infrastructure/persistence/in-memory-task-repository';\n",
            {"R01-domain-no-infrastructure"},
        ),
        (
            "R02",
            "domain",
            "export type { CreateTask } from "
            "'../application/use-cases/create-task';\n",
            {"R02-domain-no-application"},
        ),
        (
            "R03",
            "application",
            "export type { TaskUseCases } from "
            "'../infrastructure/http/routes/task-routes';\n",
            {"R03-application-no-presentation"},
        ),
        (
            "R05",
            "domain",
            "export type { FastifyInstance } from 'fastify';\n",
            {"R05-domain-no-listed-frameworks"},
        ),
        (
            "R06",
            "application",
            "export type { Pool } from 'pg';\n",
            {"R06-inner-no-postgres-client"},
        ),
        (
            "unresolved-import",
            "domain",
            "export { missing } from './__missing_dependency_probe__';\n",
            {"unresolved-imports"},
        ),
    ]

    results = []

    with tempfile.TemporaryDirectory(prefix="caac-rule-check-") as directory:
        workspace = Path(directory)
        shutil.copytree(project / "src", workspace / "src")
        shutil.copy2(project / "tsconfig.json", workspace / "tsconfig.json")
        shutil.copy2(project / "package.json", workspace / "package.json")
        (workspace / "node_modules").symlink_to(
            project / "node_modules",
            target_is_directory=True,
        )

        for name, layer, code, expected in cases:
            probe = workspace / "src" / layer / "__caac_rule_probe__.ts"

            if probe.exists():
                raise RuntimeError(f"Probe filename already exists: {probe}")

            probe.write_text(code, encoding="utf-8")

            try:
                run = subprocess.run(
                    [
                        str(checker),
                        "--config", str(config),
                        "--output-type", "json",
                        "src",
                    ],
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                )
            finally:
                probe.unlink()

            (output / f"{name}.json").write_text(
                run.stdout, encoding="utf-8"
            )
            (output / f"{name}.stderr.txt").write_text(
                run.stderr, encoding="utf-8"
            )

            actual = set()
            analysed = False
            error = None

            try:
                report = json.loads(run.stdout)
                violations = report["summary"]["violations"]
                actual = {
                    finding["rule"]["name"]
                    for finding in violations
                }
                analysed = any(
                    module["source"].endswith("__caac_rule_probe__.ts")
                    for module in report["modules"]
                )
            except (ValueError, KeyError, TypeError) as exception:
                error = str(exception)

            # For these JSON reports, check violations in the report itself.
            expected_exit = 0
            passed = (
                error is None
                and analysed
                and actual == expected
                and run.returncode == expected_exit
            )

            results.append({
                "case": name,
                "probe_code": code,
                "expected_rules": sorted(expected),
                "actual_rules": sorted(actual),
                "probe_analysed": analysed,
                "exit_code": run.returncode,
                "parse_error": error,
                "passed": passed,
            })

            print(
                f"{name}: {'PASS' if passed else 'FAIL'} "
                f"(detected: {sorted(actual)})"
            )

    (output / "results.json").write_text(
        json.dumps(results, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"\nResults saved in {output}")
    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())