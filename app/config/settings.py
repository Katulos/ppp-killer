from __future__ import annotations

import logging
import pathlib
import sys
from typing import List, Tuple, Type, Union

from pydantic import Field, ValidationError
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

config = BASE_DIR / "config.yaml"

if config.is_file():
    logger.info("Using config file: %s", config)
else:
    logger.critical("Can't find config file: %s", config)
    logger.critical("The application is shutting down")
    sys.exit(1)


class AbstractSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
        yaml_file=config,
        yaml_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


class AppConfig(AbstractSettings):
    base_dir: Union[pathlib.PosixPath, pathlib.WindowsPath] = Field(
        default=BASE_DIR,
    )

    debug: bool = Field(default=False)

    secret: str

    static_dir: Union[pathlib.PosixPath, pathlib.WindowsPath] = Field(
        default=BASE_DIR / "static",
    )

    templates_dir: Union[pathlib.PosixPath, pathlib.WindowsPath] = Field(
        default=BASE_DIR / "templates",
    )

    admin_password: str

    allowed_hosts: List[str] = Field(default=["127.0.0.1"])


class DbConfig(AbstractSettings):
    database_url: str = Field(
        default=f"sqlite:///{BASE_DIR}/data/db.sqlite3",
    )


class Settings(AbstractSettings):
    try:
        app: AppConfig = AppConfig()
        db: DbConfig = DbConfig()
    except ValidationError as e:
        logger.critical(e)
        sys.exit(0)
    except ValueError as e:
        logger.critical("Configuration file validation error: %s", e)
        sys.exit(0)


settings = Settings()
