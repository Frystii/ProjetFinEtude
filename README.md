# Projet de fin d'études

Projet réalisé par Miguel PRADEL et Clément BILLARDON dans le cadre du projet de fin d'études de Master Informatique SIIA.

## Sur la VM

Le dossier `ros_packages` contient les packages ROS suivants, que nous avons implémentés pour diverses fonctionnalités et intégrations robotiques :

- **go_to_goal_package** : Permet d'envoyer le robot a une position sauvegardée précédemment.
- **save_position_package** : Permet de sauvegarder la position exacte du robot sur la carte qu'il a généré.
- **socket_package** : Permet la communication avec l'ordinateur sur lequel se trouve la VM pour la reconnaissance vocale.

## Sur le PC

Le fichier **vosk_socket.py** est un programme python permettant de communiquer via les sockets avec la VM. Il est utilisé pour la reconnaissance vocale.
