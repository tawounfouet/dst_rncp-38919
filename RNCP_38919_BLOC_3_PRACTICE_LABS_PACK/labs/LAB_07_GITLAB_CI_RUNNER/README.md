# LAB 07 — GitLab CI et Runner shell

## Préparation issue du support

- repository privé `dst_rncp38919_bloc_3` ;
- clé SSH sur la VM ;
- Runner de type `shell`, nommé `shell` ;
- enregistrement via `gitlab-runner`.

## Mission

Créer une pipeline :

```text
test
→ build
```

Diagnostiquer ensuite un job volontairement `pending` ou une commande `pytest` introuvable.
