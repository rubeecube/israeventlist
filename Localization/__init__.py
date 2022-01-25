from Localization import fr
from Localization import en


def localize(key, lang):
    if lang == "fr":
        return fr.localize(key)
    # if lang == "en":
    #    return en.localize(key)
    return fr.localize(key)
