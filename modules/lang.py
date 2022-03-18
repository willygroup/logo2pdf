import gettext
import locale
import os

current_locale, _ = locale.getlocale()
if current_locale == "Italian_Italy":
    current_locale = "it_IT"
locale_path = os.path.join("files", "locale")
dictionary = gettext.translation("logo2pdf", locale_path, [current_locale])
dictionary.install()
_ = dictionary.gettext
