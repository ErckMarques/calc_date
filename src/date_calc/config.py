import locale
import sys
from pathlib import Path

from dynaconf import Dynaconf, Validator

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
    ROOT_PATH = Path(__file__).parents[2].resolve()

    settings = Dynaconf(
        settings_files= ROOT_PATH.joinpath("settings.toml"),
        
        # Prefixo para variáveis de ambiente
        envvar_prefix="DATE_CALC",
        
        # Suporte a múltiplos ambientes
        environments=True,
        default_env='development',
        
        # Mescla variáveis de ambiente com arquivos
        merge_enabled=True,

        # Validações para garantir que certas configurações estejam presentes
        validators=[
            Validator("DEFAULT_LOCALES_PATH", must_exist=True, required=True, cast=Path),
        ],
    )

    return settings