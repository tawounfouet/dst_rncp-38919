#!/usr/bin/env bash
#
# Supprime proprement le deploiement Kubernetes de ParcelPulse.
#
#   bash scripts/undeploy_k8s.sh
#
# Le PV est supprime explicitement : avec persistentVolumeReclaimPolicy: Retain,
# un PV supprime seul reste a l'etat "Released" et bloque la creation d'un
# nouveau PVC (statut Pending indefiniment).
#
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

NAMESPACE="${NAMESPACE:-parcelpulse}"

printf '\n\033[1m==> Suppression des objets namespaces\033[0m\n'
kubectl delete -f k8s/ --ignore-not-found

printf '\n\033[1m==> Suppression du namespace %s\033[0m\n' "$NAMESPACE"
kubectl delete namespace "$NAMESPACE" --ignore-not-found

printf '\n\033[1m==> Suppression du PersistentVolume (etat Released bloque les re-deploiements)\033[0m\n'
kubectl delete pv parcelpulse-pv --ignore-not-found

printf '\n\033[32mNettoyage termine.\033[0m\n'