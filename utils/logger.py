import configparser
import logging
import logging.handlers as handlers
import os

from utils.singleton_meta import SingletonMeta


class Logger(metaclass=SingletonMeta):
    def __init__(self, module_name, log_directory=None):
        config = configparser.ConfigParser()

        try:
            config.read("config.ini")
            environment = config.get("settings", "environment")

            if environment == "production":
                log_level = logging.ERROR
            else:
                log_level = logging.INFO
        except Exception:
            log_level = logging.INFO

        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(log_level)
        self._configure_logger(module_name, log_directory)

    def _configure_logger(self, module_name, log_directory):
        if not self.logger.hasHandlers():
            if not log_directory:
                log_directory = self._default_log_directory()

            file_path = os.path.join(log_directory, f"{module_name}.log")

            log_handler = handlers.TimedRotatingFileHandler(
                file_path, when="midnight", interval=1, backupCount=20
            )

            formatter = logging.Formatter(
                "%(asctime)s.%(msecs)03d %(process)d %(name)-15s %(levelname)-8s %(message)s",
                "%Y.%m.%d %H:%M:%S",
            )

            log_handler.setFormatter(formatter)

            self.logger.addHandler(log_handler)

    def _default_log_directory(self):
        arr_path = os.getcwd()
        log_directory_path = os.path.join(arr_path, "logs")

        if not os.path.exists(log_directory_path):
            os.makedirs(log_directory_path)

        return log_directory_path

    def log(self, level, comp_id, user_id, content):
        message = f"{comp_id}.{user_id} - {content}"
        if level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARN:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)

    def log_info(self, comp_id, user_id, content):
        self.log(logging.INFO, comp_id, user_id, content)

    def log_warning(self, comp_id, user_id, content):
        self.log(logging.WARNING, comp_id, user_id, content)

    def log_error(self, comp_id, user_id, content):
        self.log(logging.ERROR, comp_id, user_id, content)
