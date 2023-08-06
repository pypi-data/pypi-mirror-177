# hito_mail: gestion des listes Zimbra et LISTSERV

Ce module contient des scripts pour créer et mettre à jour les listes Zimbra et LISTSERV associées au laboratoire
et à ses différentes entités (pole, département, service...), à partir des informations contenues dans Hito.

Pour tous les scripts indiqués ci-dessous, il y a une option `--help` qui permet de connaitre la liste des
options et paramètres du script.

## Installation

Le déploiement du module `hito_mail` nécessite le déploiement d'un environnement Python, de préférence distinct
de ce qui est délivré par l'OS car cela pose de gros problèmes avec les prérequis sur les versions
des dépendances. Les environnements recommandés sont [pyenv](https://github.com/pyenv/pyenv),
[poetry](https://python-poetry.org) ou [Anaconda](https://www.anaconda.com/products/individual).
Pour la création d'un environnement virtuel avec Conda, voir la
[documentation spécifique](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands).

Pour installer le module `hito_mail`, il faut utiliser les commandes suivantes :

```bash
pip install hito_mail
```

## hito2lists

Cette commande permet de produire les commandes pour créer et mettre à jour des listes Zimbra ou LISTSERV à partir de la base Hito
(base RH). L'information Hito doit être exportée dans un CSV (utf-8) avec au moins les 4 colonnes suivantes : nom,
prénom, email, service. Le service doit être au format `pole - equipe - service` (interprété comme 3 niveaux hiérarchiques)
si le paramètre de configuration `hito_team_format` est `True` ou doit être dans 3 colonnes différentes si
`hito_team_format` est `False`. 


`hito2lists` permet de gérer 2 types de liste :

- Les listes basées sur l'affectation des personnes dans Hito. Ce sont les listes générées par défaut. En plus de la
création des listes, il est possible de créer un fichier contenant la liste des listes créées, au format HTML, CSV ou
texte suivant l'extension (respectivement `.html`, `.csv` or something else).
- Une ou plusieurs listes avec l'ensemble du personnel présent dans Hito, indépendamment de son affectation. Ce sont
les listes générées lorsque l'option `--personnel` est spécifiée. Dans ce mode, le nom de la liste à générer peut être spécifié
avec l'option `--list-name` ou bien être définie dans le fichier de configuration (dans ce cas, on peut générer plusieurs listes).
Il est aussi possible de donner une liste de personne qui doivent être exclues de la liste du personnel, à travers un CSV
spécifique spécifié avec l'option `--exclude-list` (la seule colonne obligatoire est l'email).

L'option `--output` est requise sauf si l'option `--execute` est présente : c'est le fichier produit par `hito2lists` 
dans le format spécifié par `--format`. Le
format par défaut est `zimbra` pour les listes issues de Hito et `listserv` pour les listes de l'ensemble du personnel. Il
est aussi possible de générer une liste de participant Limesurvey avec le format `limesurvey`. 

L'option `--execute` est supportée avec les formats `zimbra` et `listserv`. Au lien de produire un fichier avec les commandes
à exécuter pour mettre les listes à jour, les commandes sont directement exécutées sur le serveur Zimbra (voir la section
`zimbra` du fichier de configuration) ou LISTSERV (voir la section `listserv` du fichier de configuration).

### Update et reset mode

Par défaut, `hito2lists` génére les commandes nécessaires pour mettre à jour les listes (listes associées aux équipes ou listes
de tout le personnel). Cela inclut :

- Ajouter les nouveaux membres dans les listes existantes ou les nouvelles listes
- Retirer les membres qui ne font plus partie d'une liste
- Supprimer les listes qui n'existent plus (pour celles associées aux équipes uniquement)

Par défaut, le ficher CSV doit se trouver dans un repository Git. Si on utilise l'option `--git-commit`, la version
précédente du CSV est récupéré dans le commit indiqué (par son ID/hash). En l'absence de cette option, si le fichier CSV
a été modifié depuis le dernier commit, la version précédente est récupérée dans le dernier commit. Si le fichier n'a
pas été modifié, la version précédente est recherchée dans l'historique Git (premier commit antérieur modificant le
fichier CSV). Il est aussi possible d'utiliser l'option `--previous` 
pour indiquer le fichier correspondant à une version antérieure du CSV au lieu d'utiliser Git. 

La mise à jour respecte les informations se trouvant éventuellement dans le fichier spécifié par `--additional-lists`, soit :

- Les personnes devant être ajoutées dans les listes bien que les informations Hito ne le spécifient pas
- Les personnes qui ont demandé à être retirées d'une liste auxquelles elles devraient appartenir d'après les informations
extraites de Hito

Pour cette raison, les personnes ajoutées via `--additional-lists` sont systématiquement réajoutées dans la mise à jour.

Le seul cas qui ne peut pas être géré par le script et demande une action manuelle est celui de personnes ayant demandé
à être retirées d'une liste puis demandant à y être réintégrées (suppression du opt-out du fichier spécifié par 
`--additional-lists`).

Pour regénérer le contenu des listes, il faut utiliser l'option `--reset-lists`. Dans ce cas, il
est possible de spécifier une ou des listes à regenérer avec l'option `--list-pattern`. La valeur
spécifié est interprétée comme une regex appliquée au nom des listes : celles qui ne correspondent
pas sont ignorées. Par exemple, `--list-pattern ing-` regénerera toutes les listes qui
commencent par `-ing-` (et ignorera donc `ingenierie`).

**Remarque: à casue de limitation dans l'interface d'administration Zimbra, l'option 
`--reset-lists` ne supprime pas les membres actuels de la liste avant d'ajouter les membres
issus de Hito ce qui peut laisser des membres qui devraient être supprimés. Pour faire un
reset complet, il faut utiliser `zmprov` pour supprimer les membres courants (sans détruire la
liste qui peut être membre d'autres listes) puis exécuter `hito2lists --reset-lists`. Pour supprimer
les membres d'une liste, utiliser une commande telle que:**

```bash
# Définir la variable listes avec les noms de liste appropriées
listes='ing-informatique ing-mecanique'
for liste in ${listes}; do l_email=${liste}@ijclab.in2p3.fr;  echo Removing members from ${l_email}; zmprov rdlm ${l_email} $(zmprov gdl ${l_email} |grep zimbraMailForwardingAddress |awk -F": " '{print $2 }'); done
```

### Ajout/retrait de personnes dans une liste

Le fichier spécifié par `--additional-lists` permet de définir des emails qui doivent être ajoutés ou supprimés des listes
issues de Hito. Il y a un paramètre spécifique pour ajouter/ou enlever une liste issue des groupes définies dans Hito 
(`--lists` et `--lists-optout`) et
pour ajouter/enlever une personne de la liste de l'ensemble du personnel (`--personnel-lists` et `--personnel-lists-optout`) 
afin de détecter plus facilement les erreurs de
configuration mais le fonctionnement est le même dans les deux cas. Les personnes ajoutées n'ont pas besoin d'être déclarées 
dans Hito. Les listes spécifiées pour les ajouts doivent exister. Le format du fichier spécifié par `--additional-lists` 
est :

```
"email1":
  lists:
    - list1
    - list2
  lists-optout:
    - list3
    - list 4
   personnel-lists-optout:
    - ijclab-forum-l

"email2":
  lists:
    - Anotherlist1
    - list2

"email3":
  personnel-lists:
    - ijclab-personnels-l
```

### Fichier de configuration

Le fichier de configuration par défaut est `hito2lists.cfg`. Un autre fichier peut être spécifié avec l'option `--config`.
Ce fichier peut contenir les paramètres suivants :

```
teams:
  aliases:
    fullname: alias
    fullname2: alias2

  reserved_names:
    - reserved1
    - reserved2

  short_names:
    long_team_name1: short_name
    long_team_name2: short_name2

  sublist_disabled:
    - team1
    - team2

# List the list to produce with all the persons in the input CSV
general_lists:
  format: listserv
  lists:
    - ijclab-personnels-l
    - ijclab-forum-l

# Nom des colonnes dans le fichier CSV produit à partir de Hito
csv_columns:
  hito_team_format: True
  names:
    name: "Nom"
    givenname: "Prénom"
    email: "email"
    service: "Équipe"

# Nom de la colonne email dans le fichier spécifié par --exclude-list
exclusion_list:
  columns:
    email: "E_MAIL"

# Paramaters to connect to Zimbra for updating the lists
zimbra:
  server: zimbra.dom.ain
  port: port_number
  user: zimbra_admin_user
  password: zimbra_admin_pwd (empty string if a SSH key is used)
  ssh_key_path: path to the SSK (private) key to use
  command: 'zimbra administration commmand'

listserv:
  smtp_relay: smtp.dom.ain
  # server is the management email for the LISTSERV service
  server: listserv@dom.ain
  # Subject of emails sent to LISTSERV (date/time will be appended) - Optional
  mail_subject: LISTSERV update from Hito
  # Email of the list owner to use to manage the lists (must be registered as a list owner on LISTSERV)
  admin_email: list-mgrs@dom.ain
  # List maangement password if any. Must be the same for all the lists managed by the script.
  admin_password: LISTERV_pwd
```

Les valeurs de `csv_columns` indiquées sont les valeurs typiques pour un export depuis Hito. Si le fichier est généré
autrement et contient 3 colonnes, il faut indiquer des valeurs telles que :

```
csv_columns:
  hito_team_format: False
  names:
    name: "NOM_USUEL"
    givenname: "PRENOM"
    email: "E_MAIL"
    pole: "POLE"
    equipe: "DEPARTEMENT"
    service: "SERVICE"(base)
```

Pour les paramètres relatifs au service Zimbra et LISTSERV, voir le fichier d'exemple de configuration fournit
avec le module.

## hito_export

`hito_export` permet de faire l'export des données de Hito sous la forme d'un fichier CSV compatible
avec `hito2lists` et `hito2nsip` puis de les exécuter pour mettre à jour respectivement les 
listes Zimbra et/ou LISTSERV et l'annuaire (NSIP). Cette commande
est conçue pour être mise dans un cron afin de faire une mise à jour régulière des listes construites à partir d'Hito.
Les principales fonctionnalités sont :

* Récupération des données Hito dans un fichier CSV faisant partie d'un repository Git. Si une version précédente du
fichier CSV existe avec des modifications non enregistrées dans Git, le script refuse de faire un nouvel export.
* Si le nouveau fichier CSV contient des modifications par rapport à la version précédente (détectées via Git), exécution
de `hito2lists --execute` pour mettre à jour les listes sur le serveur Zimbra et/ou LISTSERV à partir des modifications depuis la
version précédente du fichier CSV puis exécution de `hito2nsip --execute` pour mettre à jour l'annuaire
* Si la mise à jour se déroule sans erreur, commit de la nouvelle version du fichier CSV et éventuellement push
du commit sur un Git remote.
* Si la mise à jour produit une erreur, suppression de la nouvelle version du fichier CSV

```bash
usage: hito_export.py [-h] [--config CONFIG] [--no-push] [--verbose]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Configuration file (D: zimbra-lists\hito_export.cfg)
  --no-push        Git push of a new CSV disabled
  --verbose        Print debugging messsages
```

La principale option est `--config` qui spécifie le fichier de configuration à utiliser. If `--verbose` est présent, il est
passé à `hito2lists`. `--no-push` supprime le Git push après le commit de la nouvelle version du fichier CSV, même s'il
est activé dans le fichier de configuration : cette option ne doit normalement être utilisée que lors des tests pour 
simplifier l'effacement des actions qui ont eu lieu pendant les tests.

Cette commande est généralement exécutée en cron avec une entrée similaire à :

```
00 19 * * * root ( date --iso-8601=seconds; /path/to/anaconda/envs/hito2zimbra/bin/python /path/to/hito_export.py --verbose --config /path/to/hito_export.cfg) >> /var/log/hito_lists_update.log 2>&1
```

### Configuration file

`hito_export` **requiert** un fichier de configuration pour définir l'accès à la database Hito et les paramètres
à utiliser avec `hito2lists`. Par défaut le nom du fichier est `hito_export.cfg` et il doit se trouver soit dans
le répertoire contenant le fichier CSV, soit dans le répertoire où se trouve `hito_export.cfg`. Voir l'exemple
fourni dans le module pour plus de détails.

