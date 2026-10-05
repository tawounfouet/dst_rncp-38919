#!/usr/bin/env python3
"""Auto-correction de l'examen blanc Bloc 2 (barème du document 12, section 45).

Usage :
    python grade.py [workspace] [--with-db] [--json]

    workspace   dossier du rendu candidat (défaut : candidate_workspace)
    --with-db   vérifie l'ingestion idempotente contre la base MariaDB
    --json      sort le résultat en JSON

Le script fait des vérifications STATIQUES (fichiers/contenu) et
DYNAMIQUES (exécution du code candidat), pour un total de 100 points.
"""

from __future__ import annotations

import argparse
import json as jsonlib
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

CATEGORY_ORDER = [
    ("Exploration", 10),
    ("ETL", 15),
    ("Modèle relationnel", 10),
    ("Docker", 10),
    ("ORM", 15),
    ("Ingestion", 10),
    ("ML", 15),
    ("Tests", 10),
    ("Documentation", 5),
]


def run_py(code: str, cwd: Path, timeout: int = 120) -> tuple[int, str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(cwd),
            text=True,
            capture_output=True,
            env=env,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def glob_text(ws: Path, pattern: str) -> str:
    return "\n".join(read(p) for p in ws.glob(pattern))


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, float, float, str]] = []

    def add(self, category: str, label: str, earned: float, maximum: float, detail: str = "") -> None:
        self.rows.append((category, label, round(earned, 2), float(maximum), detail))

    def category_totals(self) -> dict[str, tuple[float, float]]:
        totals: dict[str, tuple[float, float]] = {c: (0.0, float(m)) for c, m in CATEGORY_ORDER}
        for cat, _label, earned, maximum, _d in self.rows:
            e, m = totals.get(cat, (0.0, 0.0))
            if (e, m) != (0.0, 0.0):
                totals[cat] = (e + earned, m)
        return totals

    def total(self) -> float:
        return round(sum(e for _c, _l, e, _m, _d in self.rows), 2)


def grade(ws: Path, with_db: bool) -> Report:
    r = Report()
    if not ws.is_dir():
        raise SystemExit(f"Workspace introuvable : {ws}")

    # ---------------- Exploration (10) ----------------
    nb_path = ws / "notebooks" / "01_exploration.ipynb"
    if nb_path.exists():
        r.add("Exploration", "notebook présent", 5, 5)
        try:
            nb = jsonlib.loads(nb_path.read_text(encoding="utf-8", errors="ignore"))
            cells = nb.get("cells", [])
            code_cells = [c for c in cells if c.get("cell_type") == "code"]
            executed = any(c.get("outputs") for c in code_cells)
        except Exception:
            code_cells, executed = [], False
        r.add("Exploration", "≥ 3 cellules de code", 3 if len(code_cells) >= 3 else 0, 3, f"{len(code_cells)} cellules")
        r.add("Exploration", "notebook exécuté (sorties)", 2 if executed else 0, 2)
    else:
        r.add("Exploration", "notebook présent", 0, 5, "notebooks/01_exploration.ipynb manquant")

    # ---------------- ETL (15) ----------------
    etl = ws / "src" / "etl.py"
    if not etl.exists():
        r.add("ETL", "src/etl.py présent", 0, 1, "manquant")
    else:
        r.add("ETL", "src/etl.py présent", 1, 1)

        common = (
            "import importlib.util, sys, pathlib\n"
            "spec = importlib.util.spec_from_file_location('cand_etl', 'src/etl.py')\n"
            "m = importlib.util.module_from_spec(spec); sys.modules['cand_etl'] = m\n"
            "spec.loader.exec_module(m)\n"
        )

        rc, out, err = run_py(common + (
            "try:\n"
            "    m.extract('__absent__.json'); print('NOERROR')\n"
            "except FileNotFoundError: print('OK')\n"
            "except Exception as e: print('OTHER:' + type(e).__name__)\n"
        ), ws)
        ok = "OK" in out and "NOERROR" not in out
        r.add("ETL", "extract lève FileNotFoundError", 3 if ok else 0, 3, out or err[:60])

        rc, out, err = run_py(common + (
            "import pandas as pd\n"
            "df = pd.read_json('data/raw/deliveries.json').drop(columns=['weather'])\n"
            "try:\n"
            "    m.validate_schema(df); print('NOERROR')\n"
            "except ValueError: print('OK')\n"
            "except Exception as e: print('OTHER:' + type(e).__name__)\n"
        ), ws)
        ok = "OK" in out and "NOERROR" not in out
        r.add("ETL", "validate_schema lève ValueError", 3 if ok else 0, 3, out or err[:60])

        rc, out, err = run_py(common + (
            "import pandas as pd, pathlib\n"
            "raw = m.extract('data/raw/deliveries.json')\n"
            "c = m.transform(raw)\n"
            "p = pathlib.Path('data/processed/_grade_check.csv'); m.save_processed(c, p)\n"
            "print('ROWS', len(c)); print('UNIQ', int(c['delivery_id'].is_unique))\n"
            "print('NULLS', int(c.isna().sum().sum())); print('SAVED', int(p.exists()))\n"
        ), ws)
        rows = uniq = nulls = saved = None
        m_ = re.search(r"ROWS (\d+)", out)
        if m_:
            rows = int(m_.group(1))
            uniq = int(re.search(r"UNIQ (\d+)", out).group(1))
            nulls = int(re.search(r"NULLS (\d+)", out).group(1))
            saved = int(re.search(r"SAVED (\d+)", out).group(1))
            (ws / "data" / "processed" / "_grade_check.csv").unlink(missing_ok=True)
        transform_ok = rows == 23 and uniq == 1 and nulls == 0
        r.add("ETL", "transform → 23 lignes, unique, 0 null", 5 if transform_ok else 0, 5,
              f"rows={rows}, unique={uniq}, nulls={nulls}" if rows is not None else (err[:60] or "échec"))
        r.add("ETL", "save_processed écrit le CSV", 3 if saved == 1 else 0, 3)

    # ---------------- Modèle relationnel (10) ----------------
    models = read(ws / "src" / "models.py")
    if models:
        has_classes = ("class Customer" in models) and ("class Delivery" in models)
        r.add("Modèle relationnel", "Customer + Delivery définis", 3 if has_classes else 0, 3)
        pk = models.count("primary_key=True")
        r.add("Modèle relationnel", "PK sur les deux entités", 3 if pk >= 2 else 0, 3, f"{pk} primary_key")
        fk = 'ForeignKey("customers.customer_id")' in models or "ForeignKey('customers.customer_id')" in models
        r.add("Modèle relationnel", "FK deliveries.customer_id", 2 if fk else 0, 2)
        rel = models.count("relationship(") >= 2 and "back_populates" in models
        r.add("Modèle relationnel", "relationship des deux côtés", 2 if rel else 0, 2)
    else:
        r.add("Modèle relationnel", "src/models.py présent", 0, 3, "manquant")

    # ---------------- Docker (10) ----------------
    compose = read(ws / "docker-compose.yml")
    if compose:
        r.add("Docker", "docker-compose.yml présent", 3, 3)
        r.add("Docker", "image MariaDB/MySQL", 3 if re.search(r"image:\s*(mariadb|mysql)", compose) else 0, 3)
        r.add("Docker", "volume persistant", 2 if ("volumes:" in compose and "/var/lib/mysql" in compose) else 0, 2)
        r.add("Docker", "variables via ${...}", 2 if "${" in compose else 0, 2)
    else:
        r.add("Docker", "docker-compose.yml présent", 0, 3, "manquant")

    # ---------------- ORM (15) ----------------
    database = read(ws / "src" / "database.py")
    config = read(ws / "src" / "config.py")
    r.add("ORM", "database.py : create_engine", 5 if "create_engine" in database else 0, 5)
    env_driven = ("getenv" in config) or ("DATABASE_URL" in database)
    r.add("ORM", "URL DB depuis l'environnement", 5 if env_driven else 0, 5)
    create_db = read(ws / "src" / "create_database.py")
    r.add("ORM", "create_database.py : create_all", 5 if "create_all" in create_db else 0, 5)

    # ---------------- Ingestion (10) ----------------
    ingest = read(ws / "src" / "ingest.py")
    if ingest:
        r.add("Ingestion", "src/ingest.py présent", 2, 2)
        refs = ("Customer" in ingest) and ("Delivery" in ingest)
        r.add("Ingestion", "ingère Customer et Delivery", 3 if refs else 0, 3)
        guard = bool(re.search(r"filter_by|\.filter\(|\.first\(\)|\.get\(|merge\(|isin\(|already|exists", ingest))
        if with_db:
            idem_ok, detail = check_ingestion_idempotent(ws)
            r.add("Ingestion", "idempotence vérifiée (base)", 5 if idem_ok else 0, 5, detail)
        else:
            r.add("Ingestion", "garde d'idempotence (statique)", 5 if guard else 0, 5,
                  "lance --with-db pour une vérification réelle")
    else:
        r.add("Ingestion", "src/ingest.py présent", 0, 2, "manquant")

    # ---------------- ML (15) ----------------
    train = read(ws / "src" / "train_model.py")
    if train:
        r.add("ML", "src/train_model.py présent", 2, 2)
        r.add("ML", "train_test_split", 3 if "train_test_split" in train else 0, 3)
        r.add("ML", "encodage catégories (OneHot/ColumnTransformer)",
              3 if ("OneHotEncoder" in train or "ColumnTransformer" in train) else 0, 3)
        r.add("ML", "joblib", 2 if "joblib" in train else 0, 2)
        model_path = ws / "models" / "model.joblib"
        if model_path.exists():
            rc, out, err = run_py(
                "import joblib; m = joblib.load('models/model.joblib'); "
                "print('OK' if hasattr(m, 'predict') else 'NOPREDICT')", ws)
            r.add("ML", "model.joblib chargeable et prédictif", 5 if out == "OK" else 0, 5, out or err[:60])
        else:
            r.add("ML", "model.joblib présent", 0, 5, "models/model.joblib manquant")
    else:
        r.add("ML", "src/train_model.py présent", 0, 2, "manquant")

    # ---------------- Tests (10) ----------------
    test_files = list((ws / "tests").glob("test_*.py")) if (ws / "tests").is_dir() else []
    tests_text = glob_text(ws, "tests/**/*.py")
    r.add("Tests", "fichiers de test présents", 2 if test_files else 0, 2, f"{len(test_files)} fichier(s)")
    if test_files:
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=str(ws), text=True, capture_output=True, timeout=300,
            )
            pytest_ok = proc.returncode == 0 and "passed" in proc.stdout
            tail = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[:60]
        except subprocess.TimeoutExpired:
            pytest_ok, tail = False, "timeout"
        r.add("Tests", "pytest passe", 4 if pytest_ok else 0, 4, tail)
    else:
        r.add("Tests", "pytest passe", 0, 4, "aucun test")
    r.add("Tests", "test conformité schéma", 2 if re.search(r"validate_schema|missing|schema", tests_text) else 0, 2)
    r.add("Tests", "test doublon", 2 if re.search(r"duplicate|doublon", tests_text, re.I) else 0, 2)

    # ---------------- Documentation (5) ----------------
    doc = read(ws / "ARCHITECTURE.md") or read(ws / "README.md")
    r.add("Documentation", "ARCHITECTURE.md / README.md", 2 if doc else 0, 2)
    r.add("Documentation", "mention impact écologique", 1 if re.search(r"[ée]colog|impact", doc, re.I) else 0, 1)
    r.add("Documentation", "mention limites", 1 if re.search(r"limite", doc, re.I) else 0, 1)
    r.add("Documentation", "schéma ASCII", 1 if re.search(r"▼|→|│", doc) else 0, 1)

    return r


def check_ingestion_idempotent(ws: Path) -> tuple[bool, str]:
    def run_ingest():
        try:
            p = subprocess.run([sys.executable, "-m", "src.ingest"], cwd=str(ws),
                               text=True, capture_output=True, timeout=180)
            return p.returncode == 0, (p.stderr or "").strip().splitlines()[:1]
        except subprocess.TimeoutExpired:
            return False, ["timeout"]

    counts_code = (
        "from src.database import Session\n"
        "from src.models import Customer, Delivery\n"
        "s = Session(); print(s.query(Customer).count(), s.query(Delivery).count()); s.close()\n"
    )

    ok1, e1 = run_ingest()
    rc, c1, err1 = run_py(counts_code, ws)
    ok2, e2 = run_ingest()
    rc, c2, err2 = run_py(counts_code, ws)

    if not (ok1 and ok2 and c1 and c2):
        return False, (e1 or e2 or err1 or err2 or ["ingestion indisponible"])[0][:70]
    return c1 == c2, f"counts1={c1} counts2={c2}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Auto-correction Examen Blanc Bloc 2")
    ap.add_argument("workspace", nargs="?", default="candidate_workspace")
    ap.add_argument("--with-db", action="store_true", help="vérifie l'ingestion contre la base")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    args = ap.parse_args()

    ws = Path(args.workspace)
    if not ws.is_absolute():
        ws = (HERE / ws).resolve()

    report = grade(ws, args.with_db)
    totals = report.category_totals()
    total = report.total()

    if args.json:
        print(jsonlib.dumps({
            "workspace": str(ws),
            "total": total,
            "categories": {c: {"earned": e, "max": m} for c, (e, m) in totals.items()},
            "checks": [
                {"category": c, "label": l, "earned": e, "max": m, "detail": d}
                for c, l, e, m, d in report.rows
            ],
        }, ensure_ascii=False, indent=2))
        return 0

    print("=" * 66)
    print(f" AUTO-CORRECTION — {ws.name}")
    print("=" * 66)
    current = None
    for cat, label, earned, maximum, detail in report.rows:
        if cat != current:
            e, m = totals[cat]
            print(f"\n[{cat}]")
            current = cat
        mark = "OK " if earned == maximum else ("~  " if earned > 0 else "KO ")
        suffix = f"  ({detail})" if detail else ""
        print(f"  {mark} {earned:>4.1f}/{maximum:<4.0f} {label}{suffix}")

    print("\n" + "-" * 66)
    print(" RÉCAPITULATIF")
    print("-" * 66)
    for cat, _m in CATEGORY_ORDER:
        e, m = totals[cat]
        bar = "█" * int(round(e)) if e else ""
        print(f"  {cat:<22} {e:>5.1f}/{m:<4.0f} {bar}")
    print("-" * 66)
    print(f"  {'TOTAL':<22} {total:>5.1f}/100")

    if total >= 90:
        verdict = "chaîne très maîtrisée"
    elif total >= 75:
        verdict = "bon niveau, quelques fragilités"
    elif total >= 60:
        verdict = "pipeline compris, automatismes à renforcer"
    else:
        verdict = "refaire le blanc après révision ciblée"
    print(f"\n  Verdict : {verdict}")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
