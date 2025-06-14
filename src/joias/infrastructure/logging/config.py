"""
Configuração de logging do sistema.

Este módulo configura o logging do sistema, definindo formatos,
handlers e níveis de log para diferentes ambientes.
"""
import logging
import logging.config
import os
from typing import Any, Dict


def get_logging_config() -> Dict[str, Any]:
    """
    Retorna a configuração de logging do sistema.

    A configuração varia de acordo com o ambiente (development,
    production, test) e inclui diferentes handlers e formatters.

    Returns:
        Dict[str, Any]: Configuração de logging
    """
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "app.log")

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": """
                    asctime: %(asctime)s
                    name: %(name)s
                    levelname: %(levelname)s
                    message: %(message)s
                """,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": log_file,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file"],
                "level": log_level,
            },
            "joias": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
            "sqlalchemy": {
                "handlers": ["console", "file"],
                "level": "WARNING",
                "propagate": False,
            },
            "alembic": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    # Em ambiente de teste, desabilita o log em arquivo
    if os.getenv("ENVIRONMENT") == "test":
        config["loggers"][""]["handlers"] = ["console"]
        config["loggers"]["joias"]["handlers"] = ["console"]
        config["loggers"]["sqlalchemy"]["handlers"] = ["console"]
        config["loggers"]["alembic"]["handlers"] = ["console"]
        config["loggers"]["uvicorn"]["handlers"] = ["console"]

    return config


def setup_logging() -> None:
    """
    Configura o logging do sistema.

    Esta função deve ser chamada no início da aplicação para
    configurar corretamente o logging.
    """
    config = get_logging_config()
    logging.config.dictConfig(config)

    # Cria o logger principal da aplicação
    logger = logging.getLogger("joias")
    logger.info("Logging configurado com sucesso")
