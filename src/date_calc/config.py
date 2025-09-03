import locale
import sys
from typing import cast

_translate: dict[str, dict[str, dict[str, str]]] | None = None 

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

def translate_dict() -> dict[str, dict[str, str]]:
    """Configura a localização da aplicação.
    A ideia é utilizar a função 'locale.getlocale' para definir as configurações regionais.
    A função 'locale.getlocale' retorna a configuração regional atual e,
    a partir dela, podemos ajustar a aplicação conforme necessário.
    Este objeto lê um arquivo json, onde cada chave representa uma configuração
    e o valor é o valor a ser aplicado. Este objeto é utilizado na rederização do aplicativo.
    Suporte nativo aos idiomas pt_BR e en_US.
    """
    global _translate
    # ler arquivo json com as configurações em pt-br e en-us
    
    # avaliar qual configuração utilizar com base na localização
    locale_info = locale.getlocale()
    print(f"Locale info: {locale_info}")

    if locale_info is not None and all(isinstance(item, str) and item for item in locale_info):
        lang = locale_info[0]
    else:
        lang = "pt_BR"
        if lang not in ("pt_BR", "en_US"):
            lang = "en_US"

    if _translate is None:
        # ler arquivo json com as configurações em pt-br e en-us
        # avaliar qual configuração utilizar com base na localização
        # retornar as configurações
        _translate = {
            "pt_BR": {
                "main":{
                    "app_title": "Contador de Dias e Calculadora de Datas",
                    "tray_icon_tooltip": "Calculadora de Datas",
                    "btn_config_tooltip": "Janela de Configurações",
                    "btn_tray_tooltip": "Minimizar para a bandeja do sistema",
                    "btn_switch_tooltip": "Alternar tema entre modo claro e escuro",
                },
                "date_diff":{
                    "labelf": "Diferença de Datas",
                    "date_end_tooltip": "Selecione a data de término",
                    "difference_response": "Diferença:",
                    "business_response": "Dias Úteis:",
                    "btn_calc_tooltip": "Calcula o número de dias entre as datas selecionadas",
                    "btn_clean_tooltip": "Limpa os campos de respostas e reseta os campos de entrada de datas",
                    "label_info": "Permite calcular a quantidade de dias corridos e dias úteis entre as datas fornecidas",
                },
                "date_interval":{
                    "labelf": "Data com intervalo",
                    "entry_tooltip": "Digite um número, positivo ou negativo, de dias",
                    "btn_calc_tooltip": "Calcula a nova data",
                    "radio_consec": "Dias Corridos",
                    "radio_consec_tooltip": "Se marcado executa o cálculo para a nova data com dias corridos",
                    "radio_business": "Dias Úteis",
                    "radio_business_tooltip": "Se marcado executa o cáluclo para a nova data com dias úteis",
                    "label_info": "Permite calcular uma data a partir de um número de dias corridos ou dias úteis",
                    "result": "Resultado:",
                    "invalid": "Entrada Inválida",
                },
                "common":{
                    "date_start_tooltip": "Selecione a data de início",
                    "btn_calculate": "Calcular",
                    "btn_clear": "Limpar",
                    "days": "dias",
                },
            },
            "en_US": {
                "main":{
                    "app_title": "Day Counter and Date Calculator",
                    "tray_icon_tooltip": "Date Calculator",
                    "btn_config_tooltip": "Open configuration window",
                    "btn_tray_tooltip": "Minimize to tray system",
                    "btn_switch_tooltip": "Switch theme between light and dark mode",
                },
                "date_diff": {
                    "labelf": "Dates Difference",
                    "date_end_tooltip": "Select the end date",
                    "difference_response": "Difference:",
                    "business_response": "Business Days:",
                    "btn_calc_tooltip": "Calculates the number of days between selected dates",
                    "btn_clean_tooltip": "Clears the answer fields and resets the date input fields",
                    "label_info": "Allows you to calculate the number of calendar days and business days between the dates provided",
                },
                "date_interval":{
                    "labelf": "Date with Interval",
                    "entry_tooltip": "Enter a positive or negative number of days",
                    "btn_calc_tooltip": "Calculates the new date",
                    "radio_consec": "Consecutive Days",
                    "radio_consec_tooltip": "If checked, performs the calculation for the new date with calendar days",
                    "radio_business": "Business Days",
                    "radio_business_tooltip": "If checked, perform the calculation for the new date with working days",
                    "label_info": "Allows you to calculate a date from a number of calendar days or business days",
                    "result": "Result:",
                    "invalid": "Invalid input",
                },
                "common":{
                    "date_start_tooltip": "Select the start date",
                    "btn_calculate": "Calculate",
                    "btn_clear": "Reset",
                    "days": "days",
                },
            }
        }
    
    result = _translate[lang]
    
    # retornar as configurações
    t = cast(dict[str, dict[str, str]], result)
    return t