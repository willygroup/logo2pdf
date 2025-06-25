import gettext
import locale

from modules.paths import Paths

current_locale, _ = locale.getlocale()
if current_locale == "Italian_Italy":
    current_locale = "it_IT"
else:
    current_locale = "en_US"

locale_path = Paths.locales
dictionary = gettext.translation("logo2pdf", locale_path, [current_locale])
dictionary.install()
_ = dictionary.gettext
