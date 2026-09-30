---
title: "Liora Learn"
source: "https://learn.datascientest.com/lesson/1739/5281"
author:
published:
created: 2026-09-28
description: "Liora learning platform"
tags:
  - "clippings"
---
## Bloc 3 RNCP 38919

DIFFICULTÉ

Difficile

TEMPS APPROXIMATIF

4h00

MACHINE LIÉE

Vous n'avez pas de machine pour cet exercice.  
En lancer une peut prendre un certain temps.

---

![](https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/logo_datascientest.png)

---

## Examen bloc 3 du titre RNCP Data Engineer

---

## Le passage d'examen

L'examen est minuté et dure **4 heures**. Vous serez surveillé par un système qui s'appelle Méréos, que vous pourrez installer en suivant le tutoriel sur les slides. L'utilisation de `Google Chrome` est obligatoire pour la bonne exécution du système de surveillance. En cliquant sur le bouton **Validate** présent en vas de la page, vous débloquerez dans la section **Mes Exams** la possibilité de passer l'examen.

Voici les slides qui'il est **OBLIGATOIRE** de consulter avant de commencer l'examen:

[CONSIGNE SURVEILLANCE ÉVALUATION](https://docs.google.com/presentation/d/15QDeOpGyCzaR7KWwo_a2gN6lzJ7wM2vmSCe97FCuFrg/edit?slide=id.g3be1143fc85_0_293#slide=id.g3be1143fc85_0_293)

Vous allez uploader directement votre archive sur la page du sujet de l'examen, tout en bas du sujet.

Attention: pour utiliser la machine virtuelle de Datascientest, il faudra utiliser celle présente sur ce notebook donc démarrez la avant de commencer l'examen. Il s'agit de la même machine que pour le Bloc 2 donc si elle n'est pas vide, pensez à tout supprimer (fichiers, dossiers, containers docker etc) pour repartir sur un environnement vierge.

## Les sujets abordés

Afin de vous préparer au mieux pour le passage de cet examen, voici les sujets qui seront abordés:

1. La lecture de notebooks Jupyter.
2. L'initialisation de variables d'environnement via la commande bash `export` et la modification du shell Bash de votre machine via le fichier `.bashrc`.
3. L'utilisation de variables d'environnement dans des scripts Python.
4. L'initilisation d'environnements virtuels pour des projets Python.
5. L'utilisation de Python et Bash pour envoyer des requêtes vers une URL.
6. La librairie `joblib` afin d'enregistrer des modèles de machine learning et autres objets liés à la data science.
7. La plateforme `GitLab` et plus précisemment:
- L'utilisation d'un `Repository`.
- La création d'un pipeline à l'aide du fichier `.gitlab-ci.yml`.
- La manipulation d'un `Runner` via la commande `gitlab-runner`.
8. Le logiciel `Docker` et plus précisemment:
- La création d'un `Dockerfile`.
- L'utilisation des `volumes`.
- La création d'un `docker-compose.yml` et la configuration de la section `services.depends_on`.
- L'utilisation des répertoires d'un compte hébergé par `DockerHub`.
9. Le framework `Pytest`.
10. Le framework `FastAPI` et la librairie `prometheus-fastapi-instrumentator`.
11. La définition de classe Python à l'aide de la classe `pydantic.BaseModel`.
12. L'utilisation de la commande Bash `curl`.
13. Le logiciel `Kubernetes` et plus précisemment:
- La gestion des `Namespaces`.
- La gestion des `PersistentVolumes`.
- La gestion des `PersistentVolumeClaims`.
- La gestion des `ConfigMaps`.
- La gestion des `Services`.
- La gestion des `Deployments`.
14. L'outil de monitoring `Promtheus` et plus précisemment:
- La librairie Python `prometheus-fastapi-instrumentator`.
- La configuration de `Prometheus` via le fichier `config/prometheus.yml`.
- Le langage `PromQL`.
15. L'outil de dashboarding `Grafana` et plus précisemment:
- La configuration d'une source de données via le fichier `datasources/<source_name>.yml`.
- La création d'un dashboard depuis l'UI de `Grafana`.

## Préparation de vos outils

### GitLab

Créez un compte et un répertoire privé nommé `dst_rncp38919_bloc_3`. Aidez-vous des consignes du notebook `GitLab DE - Prise en main`, plus précisemment la section `Création d'un projet`.

Créez une clé SSH sur votre machine virtuelle et ajoutez la clé publique générée à votre compte sur GitLab. Aidez-vous des consignes du notebook `GitLab DE - Exemple`, plus précisemment la section `1.1. Création du projet`.

Créez un `Runner` de type `shell` nommé `shell` depuis le navigateur, puis enregistrez celui-ci sur votre machine virtuelle. Aidez-vous des consignes du notebook `GitLab DE - Prise en main`, plus précisemment la section `Notre premier Runner`.

### DockerHub

Créez un compte via l'adresse https://hub.docker.com/ et le bouton `Sign up`.

Générez un token d'accès:

- Cliquez sur l'image de votre profile.
- Cliquez sur `Account settings`.
- Cliquez sur `Personal access tokens`.
- Cliquez sur `Generate new token`.
- Suivez ensuite les consignes pour connecter votre machine à votre compte `DockerHub`.

![Lesson done](https://learn.datascientest.com/assets/images/lesson-done.png)

### Cours terminé?

Progression dans le module: Examen RNCP 38919 - Bloc 3

---

<iframe src="https://app.hubspot.com/conversations-visitor/19831339/threads/utk/69b925f98dd743e2920d84fae52172c8?uuid=32ff9444617e4f788baae900169ff258&amp;mobile=false&amp;mobileSafari=false&amp;hideWelcomeMessage=false&amp;hstc=148549032.eb461542286f0320649d26ef0ca3e89c.1787324119735.1790542217279.1790547990806.31&amp;domain=learn.datascientest.com&amp;inApp53=false&amp;messagesUtk=69b925f98dd743e2920d84fae52172c8&amp;url=https%3A%2F%2Flearn.datascientest.com%2Flesson%2F1739%2F5281&amp;inline=false&amp;isFullscreen=false&amp;globalCookieOptOut=&amp;isFirstVisitorSession=false&amp;isAttachmentDisabled=false&amp;isInitialInputFocusDisabled=false&amp;enableWidgetCookieBanner=false&amp;isInCMS=false&amp;hideScrollToButton=true&amp;isIOSMobile=false&amp;hubspotUtk=eb461542286f0320649d26ef0ca3e89c" title="Widget de chat" allowfullscreen=""></iframe>