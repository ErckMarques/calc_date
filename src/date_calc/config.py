import locale
import sys
from pathlib import Path
import logging

from dynaconf import Dynaconf, Validator, ValidationError
from date_calc.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

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

def _validate_path(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"The specified path does not exist: {path}")
    return path

def load_config() -> Dynaconf:
    ROOT_PATH = Path(__file__).parents[1].resolve()
    SETTINGS_PATH = ROOT_PATH.joinpath("settings.toml")
    
    logger.debug(f"Root path for configuration: {ROOT_PATH}")

    try:
        settings = Dynaconf(
            settings_files=[SETTINGS_PATH],
            envvar_prefix="DTC",
            environments=True,
            default_env='default',
            merge_enabled=True,
            validators=[
                Validator("DEFAULT_LOCALES_PATH", must_exist=True, cast=Path),
                Validator("ICON_PATH", must_exist=True, cast=Path),
                Validator("TIMEZONE", must_exist=True, is_type_of=str),
            ],
        )
        
        logger.info("✅ Configurações carregadas com sucesso")
        logger.debug(f"Ambiente: {settings.current_env}")
        
        return settings
        
    except ValidationError as e:
        logger.error(
            "❌ Validação de configuração falhou", 
            extra={
                'original_error': str(e.__cause__),
                'error_type': type(e.__cause__).__name__
            }
        )
        raise ConfigurationError(f"Configuração inválida: {e}") from e
        
    except Exception as e:
        logger.error(
            "❌ Erro inesperado ao carregar configurações",
            extra={
                'original_error': str(e.__cause__),
                'error_type': type(e.__cause__).__name__
            }
        )
        raise ConfigurationError(f"Falha ao carregar configurações: {e}") from e