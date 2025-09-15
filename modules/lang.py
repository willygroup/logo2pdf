import gettext
import locale

from modules.paths import Paths

CURRENT_LOCALE, _ = locale.getlocale()
if CURRENT_LOCALE == "Italian_Italy":
    CURRENT_LOCALE = "it_IT"
else:
    CURRENT_LOCALE = "en_US"

locale_path = Paths.locales
dictionary = gettext.translation("logo2pdf", locale_path, [CURRENT_LOCALE])
dictionary.install()
_ = dictionary.gettext
