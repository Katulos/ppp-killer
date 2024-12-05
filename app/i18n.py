from __future__ import annotations

import os

from babel.support import Translations

from .config import settings
from .template import templates

TRANSLATIONS = {
    "en_US": Translations.load(
        os.path.join(settings.app.base_dir, "locales"),
        locales=["en_US"],
    ),
    "ru_RU": Translations.load(
        os.path.join(settings.app.base_dir, "locales"),
        locales=["ru_ru"],
    ),
}

translations = TRANSLATIONS.get("en_US")


def set_locale(locale: str):
    global translations
    translations = TRANSLATIONS.get(locale) or TRANSLATIONS.get("en_US")
    templates.env.install_gettext_translations(translations)
    translations.install(locale)


def _(msg: str):
    return translations.ugettext(msg)
