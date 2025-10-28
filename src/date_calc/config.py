import locale
import sys
import logging
import zoneinfo
import pytz
from pathlib import Path
from typing import Optional, cast

from dynaconf import Dynaconf, Validator, ValidationError, LazySettings
from date_calc.exceptions import ConfigurationError

logger = logging.getLogger(__name__); logger.setLevel(logging.DEBUG)

_CONFIG_INSTANCE: Optional[LazySettings] = None
_ROOT_PATH = Path(__file__).parents[1].resolve()
_SETTINGS_PATH = _ROOT_PATH.joinpath("settings.toml")

def config_locale_app():
    """Configura o locale para português do Brasil com fallback."""
    locales_to_try = []

    if sys.platform.startswith('win'):
        locales_to_try = ['Portuguese_Brazil.1252', 'pt_BR']
    else:
        locales_to_try = ['pt_BR.UTF-8', 'pt_BR.utf8', 'pt_BR']
    
    for loc in locales_to_try:
        try:
            locale.setlocale(locale.LC_ALL, loc)
            msg = "Locale configurado para: {}".format(loc)
            logger.info(msg)
            return
        except locale.Error:
            continue
    msg = "Não foi possível configurar locale específico, usando padrão do sistema {}".format(locale.getdefaultlocale())
    logger.warning(msg)

def _validate_path(path: Path) -> Path:
    """Validates whether the path exists, and consequently, whether it is also valid."""
    if not path.exists():
        raise FileNotFoundError(f"The specified path does not exist: {path}")
    return path

def _validate_timezone(tz: str) -> zoneinfo.ZoneInfo:
    """Validates whether the timezone string is valid."""
    try:
        msg = "Validating timezone: {}".format(tz)
        logger.debug(msg)
        return zoneinfo.ZoneInfo(tz)
    except zoneinfo.ZoneInfoNotFoundError as e:
        try:
            return zoneinfo.ZoneInfo(pytz.timezone(tz).zone)  # Tentativa de fallback com pytz
        
        except (ImportError, pytz.UnknownTimeZoneError):
            raise ValueError(f"Timezone inválido: {tz}") from e

def _create_dynaconf_instance() -> Dynaconf:
    """Create dynaconf instance"""
    msg = ("Carregando configurações de: %s", _SETTINGS_PATH)
    logger.debug(*msg)
    
    if not _SETTINGS_PATH.exists():
        msg = f"Arquivo não encontrado: {_SETTINGS_PATH}"
        raise FileNotFoundError(msg)
    
    return Dynaconf(
        settings_files=[_SETTINGS_PATH],
        envvar_prefix="DTC",
        environments=True,
        default_env='default',
        merge_enabled=True,
        validators=[
            Validator("DEFAULT_LOCALES_PATH", must_exist=True, cast=lambda v: _validate_path(Path(v))),
            Validator("ICON_PATH", must_exist=True, cast=lambda v: _validate_path(Path(v))),
            # Validator("TIMEZONE", must_exist=True, cast=lambda v: _validate_timezone(v)), # Fix this 
        ],
    )

def load_config() -> None:
    """Carrega configurações (singleton)."""
    global _CONFIG_INSTANCE
    
    if _CONFIG_INSTANCE is not None:
        return
    
    try:
        _CONFIG_INSTANCE = _create_dynaconf_instance()
        _CONFIG_INSTANCE.validators.validate() # type: ignore
        logger.info("✅ Configurações carregadas com sucesso")
        
    except ValidationError as e:
        logger.exception(
            "Validação de configuração falhou", 
            extra={
                'original_error': str(e.__cause__),
                'error_type': type(e.__cause__).__name__
            }
        )
        raise ConfigurationError(f"Configuração inválida: {e}") from e
    
    except zoneinfo.ZoneInfoNotFoundError as e:
        logger.exception(
            "Timezone inválida especificada",
            extra={
                'original_error': str(e.__cause__),
                'error_type': type(e.__cause__).__name__
            }
        )
        raise ConfigurationError(f"Timezone inválida especificada: {e}") from e
    
    except Exception as e:
        logger.exception(
            "Erro inesperado ao carregar configurações",
            extra={
                'original_error': str(e.__cause__),
                'error_type': type(e.__cause__).__name__
            }
        )
        raise ConfigurationError(f"Falha ao carregar configurações: {e}") from e

def get_settings() -> LazySettings:
    """Retorna instância das configurações."""
    if _CONFIG_INSTANCE is None:
        load_config()

    cast(LazySettings, _CONFIG_INSTANCE)  # Garantia para o type checker
    return _CONFIG_INSTANCE # type: ignore

def get_root_path() -> Path:
    """Getter seguro para o root path (se realmente necessário)."""
    return _ROOT_PATH

__all__ = ['get_settings', 'get_root_path', 'config_locale_app']