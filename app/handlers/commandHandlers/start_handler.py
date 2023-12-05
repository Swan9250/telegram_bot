#!/usr/bin/python3.11

from app.handlers.commandHandlers import action_base
from app.handlers.commandHandlers.actions import action_start


class StartHandler:

    def __init__(self, application):
        self.base_action = action_base.ActionBase()
        self.base_action.set_application(application)

    def actions(self):
        return {
            "start": action_start.ActionStart(self.base_action).run
        }
