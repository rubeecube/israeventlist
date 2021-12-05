dic = {
    "welcome text": "Bienvenue sur Israël Event List (IsraEL) en cliquant sur ce lien vous avez ouvert la porte à la "
                    "liste de l’ensemble des activités sur Tel Aviv ! Du Petit dej casher aux spectacles en passant par"
                    " les cours et les diners organises, excursions, soirées ... Vous n’avez qu’à sélectionner vos"
                    " centres d'intérêt et vous recevrez les notifications, c'est simple, c’est gratuit, c'est génial.",
    "goodbye text": "Nous sommes heureux de vous compter parmi nous, n’hésitez pas à nous remonter vos remarques pour"
                    " que nous puissions nous améliorer.",
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
}


def localize(key):
    if key in dic.keys():
        return dic.get(key)
    return key
