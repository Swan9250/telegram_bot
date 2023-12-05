#!/usr/bin/python3.11

from app.handlers.commandHandlers import action_base
from app.handlers.commandHandlers.actions import action_hello


class HelloHandler:

    def __init__(self, base_action: action_base.ActionBase):
        self.base_action = base_action

    def actions(self):
        return {
            "hello": action_hello.ActionHello(self.base_action).run,
        }
