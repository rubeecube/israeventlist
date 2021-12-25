from Globals import *

dic = {
    "welcome text": "Bienvenue sur Israël Event List (IsraEL) en cliquant sur ce lien vous avez ouvert la porte à la "
                    "liste de l’ensemble des activités sur Tel Aviv ! Du Petit dej casher aux spectacles en passant par"
                    " les cours et les diners organises, excursions, soirées ... Vous n’avez qu’à sélectionner vos"
                    " centres d'intérêt et vous recevrez les notifications, c'est simple, c’est gratuit, c'est génial."
                    " Vous pouvez retrouver la liste des commandes à tout moment en envoyant /commands ."
                    " Le service peut être arrété en envoyant /stop",
    "goodbye text": "Nous sommes heureux de vous compter parmi nous, n’hésitez pas à nous remonter vos remarques pour"
                    " que nous puissions nous améliorer en utilisant la commande /contact. Pour recommencer utilisez "
                    "la commande /start",
    'retrieve phone': "Afin d'améliorer la qualité du service, nous avons besoin de votre numéro de téléphone. "
                      "Vous pourrez le renseigner plus tard.",
    "share contact": "Envoyer mon numéro de téléphone.",
    'phone not retrieved, we try later': "Le téléphone n'a pas pu être récupéré, nous réessaierons plus tard",
    'retrieve location': "Afin d'améliorer la qualité du service, nous avons besoin de votre localisation. "
                      "Vous pourrez le renseigner plus tard.",
    "share location": "Envoyer ma localisation",
    'location not retrieved, we try later': "La localisation n'a pas pu être récupérée, nous réessaierons plus tard",
    'thanks phone': "Merci d'avoir partagé votre numéro de téléphone.",
    'thanks location': "Merci d'avoir partagé votre localisation.",
    'thanks interests': "Merci d'avoir partagé vos centres d'interêts.",
    'retrieve interests': "Choisissez un ou plusieurs centre d'interêt.",
    'finish': "J'ai terminé %s" % Globals.EMOJI_THUMBS_UP,
    "contact us": "Vous pouvez envoyer vos suggestions directement à tout moment.",
    "command list": "Veuillez choisir:",

    "command interests": "Choisir ou éditer mes interêts.",
    "command phone": "Partager mon numéro de téléphone.",
    "command location": "Partager ma localisation.",
    "command commands": "Voir la liste des commmandes.",
    "command contact": "Contactez nous.",
    "command stop": "Arrêter le service.",
    "command search": "Recherche.",

    "exit menu": "Sortir du menu",
    "inform commands": "Vous pouvez retrouver la liste des commandes à tout moment en envoyant /commands",
    'search category': "Recherche selon:",

    'poi for search': "Choisir le point d'interêt:",
    'inerest for search': "Choisir le centre d'interêt:",
    'no event found for poi, showing all': "Pas d'événement trouvé pour ce point d'interêt,"
                                           " voici les résultats pour une recherche plus large",
    'shpwing events': "Voici les résultats:",

    # Admin
    "welcome admin": "Bonjour, bienvenue sur la partie admin de @IsraEventList_bot, pour voir la liste des commandes, "
                     "envoyez /commands",
    "command_admin add": "Ajouter une entrée.",
    "command_admin commands": "Voir la liste des commandes.",
    "command_admin list": "Veuillez choisir:",
    "admin add category": "Choisir la catégorie:",
    'saved': "Enregistré.",

    'name of poi': "Nom du POI?",
    'name of event': "Nom de l'événement?",

    'desc of poi': "Description du POI?",
    'desc of event': "Description de l'événement?",

    'location of poi': "Localisation GPS du POI?",
    'address of poi': "Adresse du POI?",

    'interest for add': "Choisir le centre d'interêt:",
    'poi for add': "Choisir le point d'interêt:",

    'poi': "Emplacement",
    'interest': "Catégorie d'interêt",
    'event': "Evénement",

    "no parent interest": "Interêt principal (Pas de parent)",
    'name of interest': "Nom du centre d'interêt?",

    'date': "Date?",
    'date format': "Formats acceptés:  'Lundi, Demain, 07/06...'",

    'hour': "Heure?",
    'hour format': "Formats acceptés:  '10h, 10:30; 10h30'",

    'retry': "Reessayez",

    'info to add': "Choisissez les champs à remplir"
}


def localize(key):
    if key in dic.keys():
        return dic.get(key)
    return key
