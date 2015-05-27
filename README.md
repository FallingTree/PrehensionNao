## Suivi et préhension d'une balle par un robot NAO
----------------------------------------------------

Ce dossier contient un code source python permettant au robot de suivre une balle rouge du regard et de l'attrapper (même si cela ne fonctionne pas encore).

Le robot sera en position assise tout le long, ainsi, pour l'attrapage il faut que la balle soit à portée de ses bras.

Ce code à été réalisé dans le cadre d'un projet collectif à Grenoble INP - Phelma en fillière SICOM 2A.

Crédits :

Ammar Mian - Van-exaerde Cyprien - Lemmammer Imane

##### Utilisation :

Pour lancer le script, il faut l'envoyer dans la mémoire du robot par ssh et l'exécuter directement sur le robot. Par exemple :

```
scp -r PrehensionNao nao@adress_ip_du_robot:dossier_destination
ssh nao@adress_ip_du_robot:dossier_destination
python main.py
```
Le script gère trois états :

0. Attente d'ordre lors du lancement du programme.
0. Suivi de balle : le robot va suivre une balle rouge du regard grâce aux pixels rouges sur sa caméra.
0. Attrapage de balle : une fois que le robot suis la balle, il peux essayer de l'attraper

Les transitions entre les états se font par commande vocale. A tout moment, le robot peut reconnâitre les ordres suivants :

"On ne joue plus",
"Suis la balle",
"Attrape",
"Dis bonjour Naomie"

