from http.client import IncompleteRead

from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.errors import SlackApiError
from asyncio import sleep


class SlackClient:
    def __init__(self, app_token, bot_token, connect=True):
        self.app_token = app_token
        self.bot_token = bot_token
        self.socket_client = self.socket_connect()

    def socket_connect(self):
        return SocketModeClient(
            app_token=self.app_token,
            web_client=WebClient(
                self.bot_token
            )
        )

    def send_message(self, channel, text=None, blocks=None, attachments=None, thread_ts=None, mrkdwn=None):
        try:
            self.socket_client.web_client.chat_postMessage(
                channel=channel, text=text,
                blocks=blocks, attachments=attachments,
                thread_ts=thread_ts, mrkdwn=mrkdwn
            )
        except SlackApiError as error:
            if error.response.data['error'] == 'ratelimited':
                sleep(5)
                self.send_message(channel=channel, text=text, blocks=blocks, attachments=attachments, thread_ts=thread_ts)
            else:
                return

    def upload_file(self, channels, content=None, file=None, filename=None, filetype=None, initial_comment=None, thread_ts=None, title=None):
        try:
            self.socket_client.web_client.files_upload(
                channels=channels,
                content=content,
                file=file,
                filename=filename,
                filetype=filetype,
                initial_comment=initial_comment,
                thread_ts=thread_ts,
                title=title,

            )
        except Exception as e:
            print(e)

    def add_reaction(self, emoji, channel, ts):
        try:
            self.socket_client.web_client.reactions_add(
                name=emoji,
                channel=channel,
                timestamp=ts
            )
        except SlackApiError as error:
            if error.response.data['error'] == 'ratelimited':
                sleep(5)
                self.add_reaction(emoji=emoji, channel=channel, ts=ts)
            if error.response.data['error'] == 'already_reacted':
                return
            else:
                return

    def remove_reaction(self, emoji, channel, ts):
        try:
            self.socket_client.web_client.reactions_remove(
                name=emoji,
                channel=channel,
                timestamp=ts
            )
        except SlackApiError as error:
            if error.response.data['error'] == 'ratelimited':
                sleep(5)
                self.remove_reaction(emoji=emoji, channel=channel, ts=ts)
            elif error.response.data['error'] == 'no_reaction':
                return
            else:
                return

    def get_replies(self, channel, ts):
        result = self.socket_client.web_client.conversations_replies(channel=channel, ts=ts)

    def get_messages(self, channel, time_start, time_end, limit=None, slack_messages=None, cursor=None):
        if slack_messages is None:
            slack_messages = []
        try:
            result = self.socket_client.web_client.conversations_history(
                channel=channel,
                oldest=time_start, latest=time_end,
                limit=limit if limit else 1000,
                cursor=cursor
            )

            has_more = result.data['has_more']

            for message in result.data['messages']:
                # slack_message = SlackMessage().build_slack_message_from_dictionary(message)
                slack_messages.append(message)

            if has_more:
                cursor = result.data['response_metadata']['next_cursor']
                self.get_messages(
                    channel=channel, time_start=time_start, time_end=time_end,
                    limit=limit, slack_messages=slack_messages, cursor=cursor
                )

            return slack_messages
        except IncompleteRead as e:
            return
        except Exception as e:
            return

    def delete_message(self, channel, ts):
        try:
            self.socket_client.web_client.chat_delete(channel=channel, ts=ts)
        except SlackApiError as error:
            if error.response.data['error'] == 'ratelimited':
                sleep(2)
                self.delete_message(channel=channel, ts=ts)
            elif error.response.data['error'] == 'cant_delete_message':
                return
            else:
                return
