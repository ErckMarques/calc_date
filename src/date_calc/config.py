import locale
import sys
from pathlib import Path
import logging

from dynaconf import Dynaconf, Validator, ValidationError

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
        logger.debug(f"SETTINGS path for configuration: {SETTINGS_PATH}, exists: {SETTINGS_PATH.exists()}")
        settings = Dynaconf(
            settings_files=[SETTINGS_PATH],
            
            # Prefixo para variáveis de ambiente
            envvar_prefix="DTC",
            
            # Suporte a múltiplos ambientes
            environments=True,
            default_env='default',
            
            # Mescla variáveis de ambiente com arquivos
            merge_enabled=True,

            # Validações para garantir que certas configurações estejam presentes
            validators=[
                Validator("DEFAULT_LOCALES_PATH", must_exist=True, cast=Path),
                Validator("ICON_PATH", must_exist=True, cast=Path),
                Validator("TIMEZONE", must_exist=True, is_type_of=str),
            ],
        )
    except ValidationError as e:
        logger.exception("Error loading configuration: %s", e)

    return settings 