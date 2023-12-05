import os.path as path
import app.base.logger as logging


class Path:
    ROOT_PATH = f"{path.expanduser('~')}/projects/telegram_bot/"
    APP_PATH = ROOT_PATH + 'app/'
    COMMON_PATH = ROOT_PATH + '.deployer/common/env/'
    PROD_PATH = ROOT_PATH + '.deployer/prod/env/'
    DEV_PATH = ROOT_PATH + '.deployer/dev/env/'
    BOT_FILENAME = 'bot.json'
    DB_FILENAME = 'mysql.json'
    PRIVILEGE_FILENAME = 'privilege.json'

    def __init__(self):
        self.effective_path = ''
        self.logger = logging.Logger(__name__, "ERROR").get_logger()

    def get_root_path(self):
        return self.ROOT_PATH

    def get_app_path(self):
        return self.APP_PATH

    def get_common_path(self):
        return self.COMMON_PATH

    def get_prod_path(self):
        return self.PROD_PATH

    def get_dev_path(self):
        return self.DEV_PATH

    def get_bot_path(self, deploy="PROD"):
        self.effective_path = self.DEV_PATH if deploy == "DEV" else self.PROD_PATH
        return self.get_path(self.BOT_FILENAME)

    def get_db_path(self, deploy="PROD"):
        self.effective_path = self.DEV_PATH if deploy == "DEV" else self.PROD_PATH
        return self.get_path(self.DB_FILENAME)

    def get_privilege_path(self):
        return self.get_path(self.PRIVILEGE_FILENAME)

    def get_path(self, file):
        if not path.isfile(self.effective_path + file):
            if not path.isfile(self.COMMON_PATH + file):
                self.logger.error("Не найден конфигурационный файл", exc_info=True)
            else:
                return self.COMMON_PATH + file
        else:
            return self.effective_path + file
