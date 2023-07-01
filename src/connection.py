import getpass
import locale
import socketio
from src.models.player import Player
import repository
from src.config import config

# Création d'une instance de Socket.IO
sio = socketio.Client()

# Définition des événements à gérer
@sio.event
def connect():
    print('Connecté au serveur')
    username = getpass.getuser()
    language, encoding = locale.getlocale()

    try:
        sio.emit('whoiam', {
            'roomName': config["online"]["roomName"],
            'playerName': config["online"]["playerName"],
            'username': username,
            'language': language
        })
    except socketio.exceptions.BadNamespaceError:
        pass

@sio.event
def disconnect():
    print('Déconnecté du serveur')

@sio.event
def receive_data(data):
    # Variable pour stocker le joueur trouvé ou créé
    joueur_trouve = None

    # Vérifier si l'ID existe dans la liste de joueurs
    for player in repository.players:
        if player.id == data["id"]:
            joueur_trouve = player
            break

    # Créer un nouveau joueur si l'ID n'a pas été trouvé
    if joueur_trouve is None:
        nouveau_joueur = Player(data["id"], data["playerName"], 0, 0)
        repository.players.append(nouveau_joueur)
        joueur_trouve = nouveau_joueur

    if data.get("health", None) is not None:
        joueur_trouve.health = data["health"]
    if data.get("stamina", None) is not None:
        joueur_trouve.stamina = data["stamina"]
    if data.get("shieldUsed", None) is not None:
        joueur_trouve.last_shield_date = data["shieldUsed"]
    if data.get("dead", None) is not None:
        joueur_trouve.last_death_date = data["dead"]

    repository.overlay_window.update()

@sio.event
def leave(player_id):
    for player in repository.players:
        if player.id == player_id:
            repository.players.remove(player)
            repository.overlay_window.update()
            break


sio.connect('http://home.nwe.li:1613')