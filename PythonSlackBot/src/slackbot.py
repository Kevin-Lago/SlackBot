import re
from threading import Event
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from src.commands import commands

from src.slackclient import SlackClient


class SlackBot:
    def __init__(self, app_token, bot_token):
        self._req = SocketModeRequest
        self.slack_client = SlackClient(
            app_token=app_token,
            bot_token=bot_token
        )
        self.event = Event()

    def stop(self):
        self.slack_client.disconnect()
        self.event.clear()
        listeneres = []

    def run(self):
        if not self.slack_client.socket_client.is_connected():
            self.slack_client.socket_client.connect()

        listeners = self.slack_client.socket_client.socket_mode_request_listeners
        if len(listeners) <= 1:
            listeners.append(self.listener)

        self.event.wait()

    def add_command(self, command_name, function):
        commands[
            re.compile(command_name)
        ] = function

    def listener(self, client, req):
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response=response)

        if req.type == 'slack_commands':
            try:
                command_name = req.payload['command']
                self.commands[re.compile(command_name)]()
            except KeyError:
                return
        elif req.type == 'events_api':
            try:
                event_type = req.payload['event']['type'] + req.payload['event']['subtype']
                self.events[re.compile(event_type)]()
            except KeyError:
                return
        else:
            print("thing")
