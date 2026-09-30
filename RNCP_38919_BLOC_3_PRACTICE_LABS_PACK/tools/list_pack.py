from pathlib import Path
root = Path(__file__).resolve().parents[1]
files = sorted(p for p in root.rglob("*") if p.is_file())
for p in files:
    print(p.relative_to(root))
print(f"\nTotal files: {len(files)}")
