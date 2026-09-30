from pathlib import Path
import py_compile
import sys

root = Path(__file__).resolve().parents[1]
errors = []
count = 0
for path in root.rglob("*.py"):
    count += 1
    try:
        py_compile.compile(str(path), doraise=True)
    except Exception as exc:
        errors.append((path, exc))

print(f"Python files checked: {count}")
if errors:
    for path, exc in errors:
        print(f"ERROR {path}: {exc}")
    sys.exit(1)
print("Python syntax: OK")
