from pathlib import Path
import py_compile

root = Path(__file__).resolve().parents[1]
failures = []

for path in root.rglob("*.py"):
    if "__pycache__" in path.parts:
        continue
    try:
        py_compile.compile(str(path), doraise=True)
    except Exception as exc:
        failures.append((path, exc))

if failures:
    for path, exc in failures:
        print(f"FAIL {path}: {exc}")
    raise SystemExit(1)

print("All Python files compile.")
