def config_locale_app():
    """
    Uses the 'locale' library, native to Python,
    to configure the application for local date settings in Brazil.
    """
    
    import locale
    import sys

    if sys.platform.startswith('win'):
        # Configura para português do Brasil no Windows
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    else:
        # Configura para português do Brasil em outros sistemas
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')