# M3
Manip M3 de l'expo MAISON du Vaisseau

## Activer le lancement automatique via SystemD

Copier le fichier .service dans le répertoire approprié : sudo cp M3.service /etc/systemd/system/M3.service
Changer ses permissions : sudo chmod 644 /etc/systemd/system/M3.service
Activer le système : sudo systemctl daemon-reload
Activer le service : 

# Journal

## 2025_07_02
Le tout fonctionne en théorie, mais plusieurs points sont à surveiller :
- On note encore quelques faux positifs dans les données arduino, mais je soupçonne les jumpers, qui sont un peu fatigués
- Par contre, je n'arrive pas à faire fonctionner systemd. J'ai une erreur que je n'ai pas en laissant le programme moi-même : "XDG_RUNTIME_DIR is invalid"
    De ce que je comprends, il essaye de lancer do_the_thing.py trop tôt, avant que les élèments graphiques utilisés par pygame soient initialisés.
- Autre soucis, il semblerais que l'Arduino ne soit pas accessible après un redémarrage. Mais ça, je pnse que c'est la faute de systemd, qui lance quand même le thread de arduino_serial et qui occupe la bande passante de l'arduino.

A voir...