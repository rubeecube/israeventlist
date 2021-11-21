dic = {
    "welcome text": "Bienvenue ...",
    "goodbye text": "Au revoir...",
    'retrieve phone': "nous avous besoin numero de tel...",
    "share contact": "Envoyer mon numero de telephone",
    'phone not retrieved, we try later': 'phone not retrieved, we try later',
    'retrieve location': "nous avous besoin localisation...",
    "share location": "Envoyer ma loc",
    'location not retrieved, we try later': 'loc not retrieved, we try later',
    'thanks phone': 'Merci dqvoir blqblq',
    'thanks location': 'Merci dqvoir blqblq',
    'thanks interests': 'Merci dqvoir blqblq',
}


def localize(key):
    if key in dic.keys():
        return dic.get(key)
    return key
