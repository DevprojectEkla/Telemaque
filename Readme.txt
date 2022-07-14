Telemaque v1.0 
(le projet d'origine est celui de Black Hat Python de J.Steiz
que j'ai essayé d'"améliorer" un peu en mettant notamment du multithreading pour les 
échanges server/client)

Logiciel libre de communication client server.

Telemaque permet notamment d'ouvrir l'invite de commande sur un server distant via un client.
Marche par défaut en local (paramètre ip = localhost pour le client port:1234).

bugs à corriger:

-l'affichage du prompt <hack#> n'est pas génial, il y a des sauts de ligne en trop parfois.

-Certaines commandes windows mettent du temps à être exécuter sur l'hôte distant,
 il faut patienter côté client pour ne pas risquer de faire planter le server ou le client.

en date du 04/01/2022: 

Toutes les commandes ont fonctionné (help, dir, cd, tasklist, taskkill etc.)
14/07/2022:
Ajout d'une version du fichier server_TLM en .pyw.
L'extension de fichier *.pyw permet de lancer un script en arrière plan sans afficher l'invite de commande.


