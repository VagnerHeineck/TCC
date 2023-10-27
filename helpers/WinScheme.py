import winreg


def get_color_scheme():
    # define a chave do registro que contém o esquema de cores do Windows
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"

    # abre a chave do registro
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)

    # obtém o valor da chave "AppsUseLightTheme"
    value = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
    # fecha a chave do registro
    winreg.CloseKey(key)

    return value
