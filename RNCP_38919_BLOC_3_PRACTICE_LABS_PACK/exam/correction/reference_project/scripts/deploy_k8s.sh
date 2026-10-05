#!/usr/bin/env bash
#
# Deploie ParcelPulse sur un cluster Kubernetes local en une seule commande.
#
#   bash scripts/deploy_k8s.sh            # deploiement seul
#   bash scripts/deploy_k8s.sh --smoke    # deploiement + smoke test automatise
#
# Le script enchaine les etapes qui manquaient auparavant et qui sont la
# cause n°1 des echecs de deploiement :
#   1. verifier que le cluster est joignable (sinon : connection refused)
#   2. construire l'image Docker sous son nom de REGISTRE
#   3. la rendre visible du cluster : kind/minikube par chargement local,
#      MicroK8s/EKS/GKE par pull depuis le registre (Docker et containerd
#      n'ont PAS le meme magasin d'images)
#   4. appliquer le namespace AVANT les objets namespaces (ordre alphabetique)
#   5. attendre le rollout et afficher l'etat
#
# Variables d'environnement optionnelles :
#   IMAGE            image a utiliser (defaut : tawounfouet/parcelpulse-api:latest)
#   NAMESPACE        namespace cible (defaut : parcelpulse)
#   TIMEOUT          delai d'attente du rollout en secondes (defaut : 120)
#   RESTART          "false" pour ne pas redemarrer les pods (defaut : true)
#
# Options :
#   --smoke          ajoute un smoke test automatise (tunnel temporaire)
#   --registry-only  ne construit pas l'image localement (elle vient du registre)
#   --refresh        force imagePullPolicy: Always (re-tire un tag mutable)
#   --import-local   solution de repli hors-ligne : importe l'image dans containerd
#
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

IMAGE="${IMAGE:-tawounfouet/parcelpulse-api:latest}"
NAMESPACE="${NAMESPACE:-parcelpulse}"
TIMEOUT="${TIMEOUT:-120}"
RESTART="${RESTART:-true}"
SMOKE_TEST=false
REGISTRY_ONLY=false
REFRESH=false
IMPORT_LOCAL=false

for arg in "$@"; do
    case "$arg" in
        --smoke) SMOKE_TEST=true ;;
        --registry-only) REGISTRY_ONLY=true ;;
        --refresh) REFRESH=true ;;
        --import-local) IMPORT_LOCAL=true ;;
        -h | --help)
            sed -n '2,24p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            printf 'Option inconnue : %s\n' "$arg" >&2
            printf 'Options : --smoke | --registry-only | --refresh | --import-local | --help\n' >&2
            exit 2
            ;;
    esac
done

step() {
    printf '\n\033[1m==> %s\033[0m\n' "$1"
}

fail() {
    printf '\n\033[31m[ECHEC] %s\033[0m\n' "$1" >&2
    exit 1
}

# ---------------------------------------------------------------------------
step "1/5  Contexte Kubernetes et accessibilite du cluster"
CONTEXT="$(kubectl config current-context 2>/dev/null || true)"
printf 'Contexte actif : %s\n' "${CONTEXT:-<aucun>}"

if [ -z "$CONTEXT" ]; then
    fail "Aucun contexte Kubernetes. Creez un cluster : kind create cluster"
fi

if ! kubectl --request-timeout=10s cluster-info >/dev/null 2>&1; then
    cat >&2 <<EOF
Le cluster du contexte "${CONTEXT}" est injoignable (API server injoignable).

Erreur typique vue par les debutants :
    error validating "k8s/configmap.yml": failed to download openapi:
    Get "https://127.0.0.1:XXXXX/openapi/v2": dial tcp: connection refused

Cause : le contexte pointe vers un cluster arrete/supprime. Ce n'est PAS un
probleme de manifest. Demarrez un cluster local :
    kind create cluster                                  # kind
    minikube start --driver=docker                       # minikube
    k3d cluster create k3s-cluster                       # k3d
    # ou activez Kubernetes dans Docker Desktop
EOF
    exit 1
fi
printf 'Cluster joignable.\n'

# ---------------------------------------------------------------------------
step "2/5  Image Docker (${IMAGE})"
if [ "$REGISTRY_ONLY" = "true" ]; then
    printf 'Mode --registry-only : l image est prise telle quelle dans le registre.\n'
    docker manifest inspect "$IMAGE" >/dev/null 2>&1 \
        || printf 'Attention : %s est introuvable ou prive depuis cette machine.\n' "$IMAGE"
else
    docker build -t "$IMAGE" . || fail "Echec du build Docker"
fi

# ---------------------------------------------------------------------------
step "3/5  Mise a disposition de l'image dans le cluster"
#
# Point cle : Docker et containerd (le runtime Kubernetes) ont DEUX magasins
# d'images SEPARES. "docker build" sur la machine ne rend donc rien visible
# du cluster, et un manifest qui reference un nom local tombe en
# ErrImageNeverPull. Notre manifest utilise le nom de REGISTRE, ce qui
# laisse trois strategies :
case "$CONTEXT" in
    kind-*)
        if [ "$REGISTRY_ONLY" != "true" ]; then
            kind load docker-image "$IMAGE" \
                || fail "Echec du chargement de l'image dans le nœud kind"
            printf 'Image chargee dans le nœud kind (aucun pull necessaire).\n'
        fi
        ;;
    minikube)
        if [ "$REGISTRY_ONLY" != "true" ]; then
            minikube image load "$IMAGE" \
                || fail "Echec du chargement de l'image dans minikube"
            printf 'Image chargee dans minikube (aucun pull necessaire).\n'
        fi
        ;;
    *)
        # MicroK8s, EKS, GKE, k3d... : le cluster sait tirer l'image du registre.
        printf 'Cluster "%s" : l image sera tiree du registre par containerd.\n' "$CONTEXT"
        if [ "$IMPORT_LOCAL" = "true" ]; then
            printf '\033[33m--import-local : injection de l image dans containerd\033[0m\n'
            printf 'Cette methode rend le deploiement dependant de l etat local de la VM.\n'
            docker build -t "$IMAGE" . || fail "Echec du build Docker"
            TMP_TAR="$(mktemp -u /tmp/parcelpulse-image.XXXXXX.tar)"
            # shellcheck disable=SC2064
            trap "rm -f '${TMP_TAR}' 2>/dev/null || true" EXIT
            docker save "$IMAGE" -o "$TMP_TAR" || fail "Echec du docker save"
            sudo microk8s ctr images import "$TMP_TAR" \
                || fail "Echec de l'import dans containerd"
            rm -f "$TMP_TAR"
            trap - EXIT
            printf 'Image importee. Le pod demarrera avec imagePullPolicy: Never.\n'
            kubectl apply -f k8s/namespace.yml || fail "Echec de la creation du namespace"
            kubectl apply -f k8s/ || fail "Echec de l'application des manifests"
            kubectl set image "deployment/parcelpulse-api" \
                "api=${IMAGE}" -n "$NAMESPACE" >/dev/null
            kubectl set image "deployment/parcelpulse-api" \
                "init-model-artifact=${IMAGE}" -n "$NAMESPACE" >/dev/null
            kubectl patch "deployment/parcelpulse-api" -n "$NAMESPACE" --type=strategic \
                -p '{"spec":{"template":{"spec":{"containers":[{"name":"api","imagePullPolicy":"Never"}],"initContainers":[{"name":"init-model-artifact","imagePullPolicy":"Never"}]}}}}' \
                >/dev/null
            step "Deploiement applique (mode hors-ligne)"
        fi
        ;;
esac

# ---------------------------------------------------------------------------
step "4/5  Application des manifests"
# kubectl apply -f <dossier> traite les fichiers par ordre ALPHABETIQUE :
# configmap.yml et deployment.yml passent AVANT namespace.yml et echouent avec
#   Error from server (NotFound): namespaces "parcelpulse" not found
# On applique donc le namespace en premier, puis tout le dossier.
kubectl apply -f k8s/namespace.yml || fail "Echec de la creation du namespace"
kubectl apply -f k8s/ || fail "Echec de l'application des manifests"

# --refresh : avec IfNotPresent et un tag mutable (:latest), containerd garde
# l'image deja tiree et ne va PAS chercher la version nouvellement poussee.
# On force alors Always pour que le nœud re-tire effectivement l'image.
if [ "$REFRESH" = "true" ] && [ "$IMPORT_LOCAL" != "true" ]; then
    printf 'Mode --refresh : imagePullPolicy force a Always.\n'
    kubectl patch "deployment/parcelpulse-api" -n "$NAMESPACE" --type=strategic \
        -p '{"spec":{"template":{"spec":{"containers":[{"name":"api","imagePullPolicy":"Always"}],"initContainers":[{"name":"init-model-artifact","imagePullPolicy":"Always"}]}}}}' \
        >/dev/null
fi

# Avec imagePullPolicy: IfNotPresent et un tag mutable (:latest), un redéploiement
# ne redémarre pas les pods : ils tournent encore avec l'image précédente.
# rollout restart force la reprise des pods avec l'image fraîchement chargée.
if [ "${RESTART:-true}" = "true" ]; then
    printf 'Redémarrage des pods pour charger la nouvelle image...\n'
    kubectl rollout restart "deployment/parcelpulse-api" -n "$NAMESPACE"
fi

# ---------------------------------------------------------------------------
step "5/5  Attente du deploiement et etat du cluster"
kubectl rollout status "deployment/parcelpulse-api" \
    -n "$NAMESPACE" --timeout="${TIMEOUT}s" \
    || fail "Le deploiement n'est pas devenu Available en ${TIMEOUT}s (voir 'kubectl describe pod -n ${NAMESPACE}')"

kubectl get all,pvc -n "$NAMESPACE"

# ---------------------------------------------------------------------------
# Mode --smoke : tout valider en une seule commande.
#
# Un port-forward est un processus lié au POD qu'il cible : le rollout restart
# de l'etape 4 le coupe. C'est pour cela qu'il faut normalement le relancer
# dans un second terminal apres chaque deploiement. Ce mode ouvre un tunnel
# temporaire sur un port libre, enchaine le smoke test, puis le referme.
if [ "$SMOKE_TEST" = "true" ]; then
    step "Bonus  Smoke test automatise (tunnel temporaire)"

    PORT="${SMOKE_PORT:-8000}"
    if command -v python3 >/dev/null 2>&1; then
        PORT="$(
            python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
        )"
    fi
    printf 'Port local libre choisi : %s\n' "$PORT"

    kubectl port-forward "svc/parcelpulse-api-service" "${PORT}:8000" \
        -n "$NAMESPACE" >/tmp/parcelpulse-port-forward.log 2>&1 &
    PF_PID=$!
    # shellcheck disable=SC2064
    trap "kill ${PF_PID} 2>/dev/null || true" EXIT INT TERM

    READY=false
    for _ in $(seq 1 30); do
        if curl -fsS --max-time 2 "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
            READY=true
            break
        fi
        sleep 1
    done

    if [ "$READY" != "true" ]; then
        printf 'Le tunnel n a pas demarre :\n' >&2
        cat /tmp/parcelpulse-port-forward.log >&2
        exit 1
    fi

    if API_URL="http://127.0.0.1:${PORT}" bash scripts/smoke_test.sh; then
        SMOKE_STATUS=0
    else
        SMOKE_STATUS=$?
    fi

    kill "$PF_PID" 2>/dev/null || true
    wait "$PF_PID" 2>/dev/null || true
    rm -f /tmp/parcelpulse-port-forward.log
    trap - EXIT INT TERM

    if [ "$SMOKE_STATUS" -ne 0 ]; then
        fail "Le deploiement est en place mais le smoke test a echoue"
    fi
    printf '\n\033[32mDeploiement ET smoke test valides.\033[0m\n'
    exit 0
fi

cat <<EOF

\033[32mDeploiement termine.\033[0m Pour tester l'API :
    kubectl port-forward svc/parcelpulse-api-service 8000:8000 -n ${NAMESPACE}
    bash scripts/smoke_test.sh

Pour tout faire en une seule commande (le tunnel est gere automatiquement) :
    bash scripts/deploy_k8s.sh --smoke

Si un port-forward etait deja ouvert, il est coupe par le redemarrage des pods :
relancez-le.

Pour annuler : Ctrl+C puis
    bash scripts/undeploy_k8s.sh
EOF