#!/usr/bin/python3.11

import argparse
import json
import path

import base.logger as logging

from app.base.bot.runner import Runner


class Init:
    PROD = "PROD"
    DEV = "DEV"
    REAL_RUN = "REAL RUN"
    DRY_RUN = "DRY RUN"

    def __init__(self):
        self.token = None
        self.env = None
        self.mode = None
        self.db_params = None
        self.bot_path = None
        self.db_path = None
        self.debug: bool = False
        self.path = path.Path()
        self.logger = logging.Logger(__name__, "DEBUG").get_logger()
        self.args = self.parse_args()
        if self.args.prod:
            self.env = self.PROD
            self.prod_init()
        else:
            self.env = self.DEV
            self.debug = True
            self.dev_init()

    def prod_init(self):
        self.bot_path = self.path.get_bot_path()
        self.db_path = self.path.get_db_path()
        with open(self.bot_path, 'r') as config:
            self.token = json.loads(config.read())['token']
        with open(self.db_path, 'r') as mysql_config:
            self.db_params = json.loads(mysql_config.read())
        if self.args.disable_dry_run:
            self.mode = self.REAL_RUN
            self.write_logs()
            Runner(self.token, self.db_params).run()
        else:
            self.mode = self.DRY_RUN
            self.write_logs(self.path.get_prod_path())

    def dev_init(self):
        self.bot_path = self.path.get_bot_path(self.DEV)
        self.db_path = self.path.get_db_path(self.DEV)
        with open(self.bot_path, 'r') as config:
            self.token = json.loads(config.read())['token']
        with open(self.db_path, 'r') as mysql_config:
            self.db_params = json.loads(mysql_config.read())
        if self.args.disable_dry_run:
            self.mode = self.REAL_RUN
            self.write_logs()
            Runner(self.token, self.db_params).run()
        else:
            self.mode = self.DRY_RUN
            self.write_logs(self.path.get_dev_path())

    @staticmethod
    def parse_args():
        parser_obj = argparse.ArgumentParser()
        group = parser_obj.add_mutually_exclusive_group(required=True)
        group.add_argument('--prod', action='store_true')
        group.add_argument('--dev', action='store_true')
        parser_obj.add_argument('-r', '--disable-dry-run', action='store_true', required=False, default=False)
        return parser_obj.parse_args()

    def write_logs(self, config_dir_path: str = ""):
        self.logger.info(f"{self.env} {self.mode}")
        if self.debug:
            self.logger.info(f"CONFIG_DIR_PATH      = {config_dir_path}")
            self.logger.info(f"BOT_CONFIG_FILE_PATH = {self.bot_path}")
            self.logger.info(f"DB_CONFIG_FILE_PATH  = {self.db_path}")
            self.logger.info(f"TOKEN                = {self.token}")
            self.logger.info(f"DB_PARAMS            = {self.db_params}")


if __name__ == '__main__':
    Init()
