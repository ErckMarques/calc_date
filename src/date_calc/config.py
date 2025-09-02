import locale
import sys
from typing import cast

_translate: dict[str, dict[str, str]] | None = None

def config_locale_app():
    """
    Uses the 'locale' library, native to Python,
    to configure the application for local date settings in Brazil.
    """
    if sys.platform.startswith('win'):
        # Configura para português do Brasil no Windows
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    else:
        # Configura para português do Brasil em outros sistemas
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def translate() -> dict[str, str]:
    """Configura a localização da aplicação.
    A ideia é utilizar a função 'locale.getlocale' para definir as configurações regionais.
    A função 'locale.getlocale' retorna a configuração regional atual e,
    a partir dela, podemos ajustar a aplicação conforme necessário.
    Este objeto lê um arquivo json, onde cada chave representa uma configuração
    e o valor é o valor a ser aplicado. Este objeto é utilizado na rederização do aplicativo.
    Suporte nativo aos idiomas pt-br e en-us.
    """
    global _translate
    # ler arquivo json com as configurações em pt-br e en-us
    
    # avaliar qual configuração utilizar com base na localização
    locale_info = locale.getlocale()
    print(f"Locale info: {locale_info}")
    lang = locale_info[0]

    if _translate is None:
        # ler arquivo json com as configurações em pt-br e en-us
        # avaliar qual configuração utilizar com base na localização
        # retornar as configurações
        _translate = {
            "pt_BR": {
                "main_app_title": "Contador de Dias e Calculadora de Datas",
                "tray_icon_tooltip": "Calculadora de Datas",
                "btn_config_tooltip": "Janela de Configurações",
                "btn_tray_tooltip": "Minimizar para a bandeja do sistema",
                "btn_switch_tooltip": "Alternar tema entre modo claro e escuro",
                "date_diff_labelf": "Diferença de Datas",
                "date_start_tooltip": "Selecione a data de início",
                "date_end_tooltip": "Selecione a data de término",
                "btn_calculate": "Calcular",
                "btn_clear": "Limpar"
            },
            "en_US": {
                "main_app_title": "Day Counter and Date Calculator",
                "tray_icon_tooltip": "Date Calculator",
                "btn_config_tooltip": "Open configuration window",
                "btn_tray_tooltip": "Minimize to tray system",
                "btn_switch_tooltip": "Switch theme between light and dark mode",
                "date_diff_labelf": "Dates Difference",
                "date_start_tooltip": "Select the start date",
                "date_end_tooltip": "Select the end date",
                "btn_calculate": "Calculate",
                "btn_clear": "Reset"
            }
        }
    
    # retornar as configurações
    t = cast(dict[str, str], _translate[lang])
    return t