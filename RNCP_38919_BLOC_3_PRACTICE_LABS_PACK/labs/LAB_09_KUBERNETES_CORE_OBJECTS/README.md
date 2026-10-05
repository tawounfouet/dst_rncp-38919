# LAB 09 — Kubernetes

Créer les six objets annoncés dans le support :

```text
Namespace
ConfigMap
PersistentVolume
PersistentVolumeClaim
Deployment
Service
```

Valider :

```text
PVC Bound
Pod Running
Service présent
```

## Déploiement & Validation

1. Appliquer les manifests dans l'ordre logique :
   ```bash
   cd solution
   kubectl apply -f namespace.yml
   kubectl apply -f configmap.yml
   kubectl apply -f pv.yml
   kubectl apply -f pvc.yml
   kubectl apply -f deployment.yml
   kubectl apply -f service.yml
   ```
2. Vérifier l'état du cluster :
   ```bash
   kubectl get pv,pvc -n parcelpulse
   kubectl get pods -n parcelpulse
   kubectl get svc -n parcelpulse
   ```
3. Nettoyer les ressources :
   ```bash
   kubectl delete namespace parcelpulse
   kubectl delete pv parcelpulse-pv
   ```
