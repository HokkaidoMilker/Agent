import logging
import os
import pathlib
from datetime import datetime
from utils.path_tool import get_abs_path

#日志路径
log_path=get_abs_path("log")
#创建文件夹
os.makedirs(log_path,exist_ok=True)

#日志的格式配置
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


def get_logger(
        logger_name=None,
        level=logging.INFO,
        log_file_name=None,
        file_level=logging.INFO,
)->logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    #避免重复
    if logger.handlers:
        return logger
    #控制台hander
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    #文件handler
    if not log_file_name:
        log_file_name=  os.path.join(log_path,f"{logger_name}_{datetime.now().strftime('%y%m%d')}.log")
    file_handler = logging.FileHandler(log_file_name,encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger

logger = get_logger()
if __name__ == '__main__':
    logger.info("hello world")
    logger.debug("调试日志")
    logger.warning("警告日志")


