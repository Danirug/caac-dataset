import sys, pathlib, tiktoken
enc = tiktoken.get_encoding("o200k_base")
root = pathlib.Path(sys.argv[1])
skip = {"node_modules", "dist", "build", ".git", "coverage"}
total, files = 0, 0
for p in root.rglob("*.ts"):
    if any(s in p.parts for s in skip) or p.name.endswith((".spec.ts", ".test.ts", ".d.ts")):
        continue
    total += len(enc.encode(p.read_text(errors="ignore"))); files += 1
print(f"{root.name}: {files} files, {total:,} tokens")
