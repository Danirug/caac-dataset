from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    dataset_root = Path(__file__).resolve().parent.parent
    project = dataset_root / "projects" / "reference-architecture-node"

    if not (project / "package.json").is_file():
        print(f"Project package.json not found in {project}")
        return 1

    for tool in ("node", "npm", "git"):
        if shutil.which(tool) is None:
            print(f"Required command is unavailable: {tool}")
            return 1

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    logs = (
        dataset_root
        / "baseline-reports"
        / "reference-architecture-node"
        / timestamp
    )
    logs.mkdir(parents=True, exist_ok=False)

    print(f"Project: {project}")
    print(f"Logs: {logs}", flush=True)

    def run(name, command):
        """Run a command and display and save its output."""
        print(f"\nRunning {name}...", flush=True)

        log_path = logs / f"{name}.log"

        with log_path.open("w", encoding="utf-8") as log:
            log.write(f"Command: {' '.join(command)}\n")
            log.write(f"Working directory: {project}\n\n")
            log.flush()

            with subprocess.Popen(
                command,
                cwd=project,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            ) as process:
                for line in process.stdout:
                    print(line, end="", flush=True)
                    log.write(line)
                    log.flush()

                exit_code = process.wait()

            log.write(f"\nExit code: {exit_code}\n")

        print(f"{name}: exit code {exit_code}", flush=True)
        return exit_code

    environment_checks = [
        ("node-version", ["node", "--version"]),
        ("npm-version", ["npm", "--version"]),
        ("baseline-sha", ["git", "rev-parse", "HEAD"]),
        ("initial-git-status", ["git", "status", "--short"]),
    ]

    for name, command in environment_checks:
        if run(name, command) != 0:
            print(f"\nStopped because {name} failed.")
            print(f"Logs saved in {logs}")
            return 1

    # Record the current project state before installing dependencies.
    # A baseline run requires a clean tracked and untracked working tree.
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=project,
        capture_output=True,
        text=True,
        check=True,
    )

    if status.stdout.strip():
        print("\nThe project has local changes. Review them before running.")
        print(status.stdout)
        print(f"Logs saved in {logs}")
        return 1

    if run("install", ["npm", "ci"]) != 0:
        print("\nDependency installation failed. Checks were not run.")
        print(f"Logs saved in {logs}")
        return 1

    results = {}

    # Coverage runs the test suite and checks the coverage thresholds.
    for name in ("lint", "typecheck", "coverage", "build"):
        results[name] = run(name, ["npm", "run", name])

    status_exit_code = run(
        "final-git-status",
        ["git", "status", "--short"],
    )

    summary_lines = ["BASELINE CHECK SUMMARY"]

    for name, exit_code in results.items():
        outcome = "PASS" if exit_code == 0 else "FAIL"
        summary_lines.append(f"{name}: {outcome}")

    summary_lines.append(f"Logs saved in {logs}")
    summary = "\n".join(summary_lines)

    (logs / "summary.txt").write_text(
        summary + "\n",
        encoding="utf-8",
    )

    print(f"\n{summary}", flush=True)

    failed = any(code != 0 for code in results.values())
    return 1 if failed or status_exit_code != 0 else 0


if __name__ == "__main__":
    sys.exit(main())