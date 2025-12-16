import pytest

from pathlib import Path
from zoneinfo import ZoneInfo
from dynaconf import Dynaconf, ValidationError, LazySettings
from date_calc import load_config

@pytest.fixture(scope="module", autouse=True)
def settings() -> LazySettings:
    return load_config() # type: ignore

def test_load_config(settings: LazySettings):
    
    assert settings is not None, "As configurações não foram devidamente carregadas."
    assert settings.current_env != "default", "O ambiente atual não é 'default'."
    assert isinstance(settings, LazySettings), "O objeto de configurações não é uma instância de LazySettings."
    assert settings.get("TIMEZONE") == ZoneInfo("America/Recife"), "A configuração TIMEZONE não está definida corretamente."
    assert isinstance(settings.get("DEFAULT_LOCALES_PATH"), Path), "A configuração DEFAULT_LOCALES_PATH não está definida corretamente."
    assert isinstance(settings.get("ICON_PATH"), Path), "A configuração ASSETS_PATH não está definida corretamente."

def test_development_env_vars(settings: LazySettings):
    # Testa se as variáveis de ambiente de desenvolvimento estão definidas corretamente
    with settings.using_env("development"):
        assert settings.get("DEBUG", default=True) is True, "A variável de ambiente DEBUG não está definida como True."
        assert settings.get("LOG_LEVEL") == "DEBUG", "A variável de ambiente LOG_LEVEL(=%s) não está definida como Debug.".format(settings.get("LOG_LEVEL"))