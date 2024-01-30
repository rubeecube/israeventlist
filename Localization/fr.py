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
    "command commands": "Voir la liste des commandes.",
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

    'info to add': "Choisissez les champs à remplir",

    # MAASSER
    "MASR: welcome text": "Bonjour \nCe bot aide a comptabiliser les sorties et entrées d'argent pour remplir la"
                          " mitsvah du Maasser au mieux.\nPour ajouter un salaire, envoyez /salaire.\n"
                          "Pour enregistrer un don envoyez /don.\n"
                          "Pour afficher un résumé, envoyez /recap.\n"
                          "Pour changer le pourcentage du maasser, envoyez /maasser.\n"
                          "Pour changer la devise, envoyez /devise.\n"
                          "Les données sont enregistrées de façon securisées et protégées par un mot de passe.\n"
                          "Pour en savoir plus envoyez /details.\n"
                          "Pour contacter l'auteur encoyer /contact.",
    "MASR: details": "Chaque donnée est protegée via le mot de passe inséré à la premiere utilisation.\n"
                     "Les données ne sont dévoilées que lors de l'affichage.\n"
                     "Ni le robot, ni l'auteur ne sont capables de lire les données (Sauf le pourcentage de Maasser "
                     "pour des raisons techniques).\n"
                     "Pour les details techniques, envoyez /details2.",
    "MASR: details2": "A l'initialization, une paire de clé RSA 3072 est generée. la clé privée est chifrée grâce "
                      "au mot de passe inséré.\n"
                      "Dans la base de données figurent: la clé publique et la clé privée (chiffrée avec le mot de "
                      "passe)), et un tableau de données chiffrées.\n"
                      "A chaque insertion, une clé symetrique est générée, chiffrée grâce a la clé publique, "
                      "l'insertion (date, montant) est chifrée (avec AES GCM 128) et stockée en attente de"
                      " consolidation.\n"
                      "Lors de l'affichage, la clé privée est déchifrée et toutes les données en attente le sont aussi,"
                      " elles sont ensuite consolidées en un seul message, le tout est ensuite rechiffré.\n"
                      "J'en ai assez dit jusqu'à présent, pour plus: /contact :D.",
    'MASR: user not found': "Pour utiliser le service, merci de choisir un mot de passe. Il vous sera demandé a chaque "
                            "affichage. Attention, en case de perte nous ne serons pas en mesure de le retrouver."
                            "Vous perdrez alors toutes les données (Sauf les tableaux affichés).",
    'MASR: user found': 'Le compte à déjà été initialisé.',
    "MASR: command list": 'Liste des commandes',
    'MASR: date': "Date?\nFormats acceptés:  'Lundi, Demain, 07/06/2022...'",

    'MASR: retry': 'Rééssayez...',
    "MASR: amount--format": 'Montant en {}.\n'
                    'Pour insérer une autre devise, ajouter un symbole (EUR, €, USD, $, ILS, ₪).',
    'MASR: amount table--format': 'Montant ({})',
    'MASR: percentage': 'Pourcentage',
    "MASR: explain table": "Un montant négatif signale ce que vous devez encore verser ce mois-ci.",
    "MASR: added": 'Ajouté!',
    "MASR: password set": 'Enregistré!',
    "MASR: password?": "Veuillez inserer votre mot de passe",
    "MASR: invalid, bad password?": "Mot de passe érroné!",

    "MASR: command commands": "Afficher la liste des commandes",
    "MASR: command don": "Enregistrer un don",
    "MASR: command salaire": "Enregistrer un salaire",
    "MASR: command maasser": "Changer le pourcentage du Maasser",
    "MASR: command contact": "Contacter l'auteur",
    "MASR: command details": "Afficher les details",
    "MASR: command devise": "Changer la devise par défaut",
    "MASR: command recap": "Afficher un tableau récaputilatif",
    "MASR: command edit": "Supprimer une entrée",

    "MASR: choose edit": "Choisir la ligne à supprimer",
    "MASR: percentage ask": "Quel est le nouveau pourcentage à appliquer?",
    "MASR: changed": "Changé!",
    "MASR: removed": "Supprimé!",
    "MASR: error": "Erreur...",
    "MASR: comment": "Description",

    "MASR: currency ask": "Quel est la nouvelle devise à appliquer (EUR, ILS, USD)?",

    'Yesterday': 'Hier',
    'Today': "Aujourd'hui",
    'month': "Mois",

}


def localize(key):
    if key in dic.keys():
        return dic.get(key)
    return key
