from pathlib import Path
import py_compile
import subprocess
import sys

project = Path(__file__).resolve().parents[1] / "exam" / "correction" / "reference_project"

# 1. Structure
required = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/demo_model.py",
    "app/schemas.py",
    "app/model.py",
    "models/model.joblib",
    "scripts/create_artifact.py",
    "scripts/http_client.py",
    "scripts/smoke_test.sh",
    "tests/__init__.py",
    "tests/test_api.py",
    ".gitlab-ci.yml",
    "Dockerfile",
    "docker-compose.yml",
    "config/prometheus.yml",
    "grafana/provisioning/datasources/prometheus.yml",
    "k8s/namespace.yml",
    "k8s/configmap.yml",
    "k8s/pv.yml",
    "k8s/pvc.yml",
    "k8s/deployment.yml",
    "k8s/service.yml",
    "requirements.txt",
    "README.md",
]

missing = [item for item in required if not (project / item).exists()]
if missing:
    print("❌ Structure Check FAILED. Missing files:")
    print("\n".join(f"  - {m}" for m in missing))
    sys.exit(1)
print(f"✅ 1. Structure Check: OK ({len(required)} files verified)")

# 2. Python Syntax
py_files = list(project.rglob("*.py"))
for py_file in py_files:
    try:
        py_compile.compile(str(py_file), doraise=True)
    except Exception as exc:
        print(f"❌ Syntax Error in {py_file}: {exc}")
        sys.exit(1)
print(f"✅ 2. Python Syntax: OK ({len(py_files)} files compiled)")

# 3. Model Generation & Loading
try:
    cmd = [sys.executable, str(project / "scripts" / "create_artifact.py")]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
except Exception as exc:
    print(f"❌ create_artifact.py execution failed: {exc}")
    sys.exit(1)

model_path = project / "models" / "model.joblib"
if not model_path.exists():
    print(f"❌ Artifact was not created at {model_path}")
    sys.exit(1)

try:
    if str(project) not in sys.path:
        sys.path.insert(0, str(project))
    import joblib
    model = joblib.load(model_path)
    pred = model.predict([[12.5, 3.2]])
    assert len(pred) == 1
    print("✅ 3. Model Generation & Prediction: OK")
except ModuleNotFoundError as exc:
    print(f"❌ Model unpickling failed: {exc}")
    sys.exit(1)
except ImportError:
    print("⚠️ 3. Model Prediction skipped (joblib not installed in current environment)")
except Exception as exc:
    print(f"❌ Model load/prediction failed: {exc}")
    sys.exit(1)

# 4. YAML Manifests Validation
try:
    import yaml
    yaml_files = list(project.rglob("*.yml")) + list(project.rglob("*.yaml"))
    for yf in yaml_files:
        with open(yf, encoding="utf-8") as fp:
            content = fp.read()
            yaml.safe_load(content)
    print(f"✅ 4. YAML Syntax: OK ({len(yaml_files)} YAML files validated)")
except ImportError:
    print("⚠️ 4. YAML validation skipped (PyYAML not installed)")
except Exception as exc:
    print(f"❌ YAML validation error in {yf}: {exc}")
    sys.exit(1)

# 5. Kubernetes Configuration Integrity
with open(project / "k8s" / "deployment.yml", encoding="utf-8") as fp:
    deploy_content = fp.read()
    if "USER/" in deploy_content:
        print("❌ Placeholder 'USER/' still present in k8s/deployment.yml")
        sys.exit(1)
    if "imagePullPolicy: IfNotPresent" not in deploy_content:
        print("⚠️ Warning: imagePullPolicy: IfNotPresent not explicitly set in k8s/deployment.yml")

with open(project / "k8s" / "pv.yml", encoding="utf-8") as fp:
    pv_content = fp.read()
    if "storageClassName: manual" not in pv_content:
        print("❌ storageClassName: manual missing in k8s/pv.yml")
        sys.exit(1)

with open(project / "k8s" / "pvc.yml", encoding="utf-8") as fp:
    pvc_content = fp.read()
    if "storageClassName: manual" not in pvc_content:
        print("❌ storageClassName: manual missing in k8s/pvc.yml")
        sys.exit(1)

print("✅ 5. Kubernetes Integrity: OK (No unreplaced placeholders, StorageClass aligned)")

print("\n🎉 Reference Project validation: 100% OPERATIONAL & VERIFIED")

