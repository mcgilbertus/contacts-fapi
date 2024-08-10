import logging

from fastapi import APIRouter, status, HTTPException

from domain.model.logging_levels import LoggingLevelsEnum

logging_router = APIRouter(prefix='/logging', tags=['Logging'])
logger = logging.getLogger(__name__)


@logging_router.get('/')
def get_loggers():
    loggers = [n for n in logger.manager.loggerDict.keys()]
    return {'loggers': loggers}


@logging_router.get('/{logger_name}')
def get_logger_config(logger_name: str):
    if not logger.manager.loggerDict.get(logger_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logger no encontrado")

    logger_info = logging.getLogger(logger_name)
    result = {
        'name': logger_name,
        'level': logging.getLevelName(logger_info.level),
        'handlers': [str(h) for h in logger_info.handlers],
        'propagate': logger_info.propagate
    }
    return result


@logging_router.put('/{logger_name}/level/{level}')
def set_logger_level(logger_name: str, level: LoggingLevelsEnum):
    if not logger.manager.loggerDict.get(logger_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logger no encontrado")
    the_logger = logging.getLogger(logger_name)
    the_logger.setLevel(level.value)
    return {'logger': logger_name, 'level': level}
