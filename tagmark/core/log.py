import logging
import logging.config
import os
from enum import Enum
from typing import Mapping

import structlog


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class LogHandler(Enum):
    CONSOLE = "console"
    FILE = "file"


default_logging_config: dict = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        LogHandler.CONSOLE.value: {
            "class": "logging.StreamHandler",
            "level": LogLevel.INFO.value,
            "stream": "ext://sys.stdout",
        },
        LogHandler.FILE.value: {
            "backupCount": 32,
            "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
            "filename": "/tmp/tagmark/log/tagmark.log",
            "level": LogLevel.INFO.value,
            "maxBytes": 1024 * 1024 * 512,  # 1024 * 1024 * 512 Bytes = 512 MB
        },
    },
    "loggers": {
        "tagmark": {
            "handlers": [
                LogHandler.CONSOLE.value,
                LogHandler.FILE.value,
            ],
            "level": LogLevel.INFO.value,
            "propagate": 0,
        },
    },
}

processors_mapping: Mapping[str, list[structlog.types.Processor]] = {
    "general": [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ],
    "level_debug": [
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.PROCESS,
                structlog.processors.CallsiteParameter.PROCESS_NAME,
                structlog.processors.CallsiteParameter.THREAD,
                structlog.processors.CallsiteParameter.THREAD_NAME,
            }
        ),
    ],
    "level_others": [
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.PROCESS,
                structlog.processors.CallsiteParameter.PROCESS_NAME,
            }
        ),
    ],
    "json": [
        structlog.processors.JSONRenderer(sort_keys=True, ensure_ascii=False),
    ],
}


def load_file_handler_settings(file_handler_settings: dict = {}):
    default_logging_config["handlers"]["file"].update(file_handler_settings)


def get_level_logger(
    name: str,
    level: LogLevel = LogLevel.DEBUG,
    handlers: list[LogHandler] = [
        LogHandler.CONSOLE,
    ],
):
    _logging_config: dict = default_logging_config.copy()

    for _handler in handlers:
        if _handler.value not in _logging_config["handlers"].keys():
            raise ValueError(f"Invalid handler name: {_handler.value}")
        _logging_config["handlers"][_handler.value]["level"] = level.value

    for _hanlder_value in _logging_config["handlers"].copy().keys():
        if _hanlder_value not in [_.value for _ in handlers]:
            _logging_config["handlers"].pop(_hanlder_value)

    _logging_config["loggers"][name.split(".")[0]]["handlers"] = [
        _.value for _ in handlers
    ]
    _logging_config["loggers"][name.split(".")[0]]["level"] = level.value

    if LogHandler.FILE in handlers:
        os.makedirs(
            os.path.dirname(_logging_config["handlers"]["file"]["filename"]),
            exist_ok=True,
        )

    processors: list[structlog.types.Processor] = (
        processors_mapping["general"]
        + processors_mapping[
            "level_{}".format("debug" if level.value.lower() == "debug" else "others")
        ]
        + processors_mapping["json"]
    )

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.config.dictConfig(config=_logging_config)
    return structlog.get_logger(name)


if __name__ == "__main__":
    logger = get_level_logger(name="tagmark.test", level=LogLevel.DEBUG)
    logger.warning(x=1)
    logger = logger.bind(scope="main")
    logger.debug(xxx="debug")

    try:
        a = 1 / 0
    except Exception as e:
        logger.error(x="عربي/عربى", msg=e, exc_info=True, a={"x": 1, "y": "zzz"})
