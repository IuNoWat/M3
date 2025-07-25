# M3
Manip M3 de l'expo MAISON du Vaisseau

## Configuration de la Raspberry Pi

### Installation de la Pi
Rien de particulier à faire, télécharger la dernière version de Raspberry OS, puis copier le repository dans le bureau via git clone https://github.com/IuNoWat/M3.git

### Activer le lancement automatique via SystemD

- Copier le fichier .service dans le répertoire approprié : sudo cp M3.service /etc/systemd/system/M3.service
- Changer ses permissions : sudo chmod 644 /etc/systemd/system/M3.service
- Activer le système : sudo systemctl daemon-reload
- Activer le service : sudo systemctl enable M3.service
- Tester le service : sudo systemctl start M3.service

## Tutoriels
- Communication Raspi/Arduino : https://www.aranacorp.com/fr/communication-serie-entre-raspberry-pi-et-arduino/
- Utiliser RunningAverage.h : https://github.com/RobTillaart/RunningAverage
- Utiliser systemd : https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/

# Journal

## Infos Techniques


## 2025_07_02
Le tout fonctionne en théorie, mais plusieurs points sont à surveiller :
- On note encore quelques faux positifs dans les données arduino, mais je soupçonne les jumpers, qui sont un peu fatigués
- Par contre, je n'arrive pas à faire fonctionner systemd. J'ai une erreur que je n'ai pas en laissant le programme moi-même : "XDG_RUNTIME_DIR is invalid"
    De ce que je comprends, il essaye de lancer do_the_thing.py trop tôt, avant que les élèments graphiques utilisés par pygame soient initialisés.
- Autre soucis, il semblerais que l'Arduino ne soit pas accessible après un redémarrage. Mais ça, je pnse que c'est la faute de systemd, qui lance quand même le thread de arduino_serial et qui occupe la bande passante de l'arduino.
A voir...

## 2025_07_03
L'intégration est finie et tout fonctionne
- J'ai résolu l'erreur "XDG_RUNTIME_DIR is invalid" en spécifiant à la main cette variable dans M3.service, via la ligne Environment="XDG_RUNTIME_DIR=/run/user/1000"
    J'ai un message d'erreur, mais cela fonctionne, alors je reste comme ça
- L'Arduino n'a pas fait des siennes, j'en déduis que j'avais raison hier
- Je note toujours quelques faux positifs assez surprenant, je vais continuer à en chercher la cause.

## 2025_07_09
Pour ajouter le buzzer, j'ai dù installer pigpio, ce qui m'a obligé à crer un environnement virtuel qui se trouve ici : /home/vaisseau/Desktop/M3_env
Il faut y installer les dépendances suivantes :
- pip install pygame
- pip install pigpio
- pip install pyserial

## 2025_07_13
Il y a toujours un problème de connexion ssh. Via routeur, la connexion n'est pas très stable, en connexion ethernet directe, c'est encore pire, la pi se déconnecte toute seule quelques minutes après le branchement. plusieurs pistes doivent êtres explorées :
- Pour la connexion ethernet : https://raspberrypi.stackexchange.com/questions/147853/raspberry-pi-disconnects-from-ssh-intermittently
- Pour la connexion routeur : essayer la modif écrite ici : https://forums.raspberrypi.com/viewtopic.php?t=138631&start=100

## 2025_07_15
La connexion par routeur reste très stable, je crois que le problème est causé par la mise en veille de l'ordinateur
- L'implémentation de buzzer.py est fini, et un pilote est disponible dans Templates
- J'ai ajouté un timer de victoire
