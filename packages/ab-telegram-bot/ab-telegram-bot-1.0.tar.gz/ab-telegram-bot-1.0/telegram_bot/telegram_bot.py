import logging
from functools import cached_property

import requests
from pydantic.error_wrappers import ValidationError

from .command_handler import CommandHandler
from .models import Message, Update


class TelegramBot:
    TIMEOUT: int = 120
    token: str
    command_handler: dict[str, tuple[CommandHandler, str | None]]
    last_update_id: int

    def __init__(self, token: str, last_update_id: int = None):
        self.token = token
        self.command_handler = {}
        self.last_update_id = last_update_id  # type: ignore
        self.logger = logging.getLogger(__name__)

    @cached_property
    def base_url(self):
        return f'https://api.telegram.org/bot{self.token}'

    def register_command_handler(
        self, command: str, handler: CommandHandler, description: str = None
    ) -> None:
        self.logger.info('Registered handler for %s command', command)
        self.command_handler[command] = handler, description

    def start_server(self) -> None:
        self.logger.info('Telegram bot is starting')
        self._update_telegram_commands()
        while True:
            try:
                message = self._get_next_message()
                self._process_message(message)
            except Exception as generic_exception:
                self.logger.warning(
                    'Unknown exception occurred', exc_info=generic_exception
                )
            except KeyboardInterrupt:
                self.logger.warning('Keyboard interrupt. Closing server')
                break

    def send_message(self, text: str, chat_id: int) -> None:
        self.logger.info('Sending message %s to chat: %i', text, chat_id)
        response = requests.post(
            f'{self.base_url}/sendMessage',
            data={'chat_id': chat_id, 'text': text, 'parse_mode': 'html'},
        )
        if not response.ok:
            self.logger.warning(
                'Could not send message to chat: %i. '
                'Returned not successful status code: %i',
                chat_id,
                response.status_code,
            )

    def _retrieve_last_update_id(self) -> int | None:
        self.logger.info('Requested last update id')
        response = requests.post(f'{self.base_url}/getUpdates?offset=-1')
        response_json = response.json()
        json_result_ = response_json['result']
        result_ = json_result_[0]
        last_update_id_str = result_['update_id']
        self.logger.info('Last update id: %s', last_update_id_str)
        return int(last_update_id_str)



    def _get_get_updates_url(self):
        if self.last_update_id is None:
            return (
                f'{self.base_url}/getUpdates'
                f'?timeout={self.TIMEOUT}'
                f'&allowed_updates=["message"]'
            )
        return (
            f'{self.base_url}/getUpdates'
            f'?offset={self.last_update_id + 1}'
            f'&limit=1'
            f'&timeout={self.TIMEOUT}'
            f'&allowed_updates=["message"]'
        )

    def _get_next_message(self) -> Message:
        while True:
            try:
                get_updates_url = self._get_get_updates_url()
                self.logger.info(
                    'Start long polling with url: %s', get_updates_url
                )
                response = requests.post(get_updates_url, timeout=self.TIMEOUT)
                try:
                    result = response.json()['result']
                    if not len(result):
                        self.logger.info(
                            'No messages received. ' 'Start polling again'
                        )
                        continue

                    update_json = result[0]
                    self.logger.info('Returned last update: %s', update_json)
                    update = Update(**update_json)
                    self.last_update_id = update.update_id
                    return update.message
                except ValidationError as validation_error:
                    self.logger.warning(
                        'Telegram api returned invalid json',
                        exc_info=validation_error,
                    )
                    continue

            except requests.exceptions.Timeout:
                self.logger.info('Long polling timeout exceed. Start again')

    def _process_message(self, message: Message) -> None:
        try:
            command, args = message.text.split(maxsplit=1)
        except ValueError:
            command, args = message.text, None

        if not command.startswith('/'):
            return

        command = command.lstrip('/')
        self.logger.info(
            'User %i invoke command "%s" with args: "%s"',
            message.from_user.id,
            command,
            args,
        )
        try:
            handler, _ = self.command_handler[command]
        except KeyError as key_error:
            self.logger.warning(
                'Could not find handler for %s command',
                command,
                exc_info=key_error,
            )
            return
        handler(self, message.from_user.id, args)

    def _update_telegram_commands(self):
        commands_descriptions = [
            {'command': command, 'description': description or ''}
            for command, (_, description) in self.command_handler.items()
        ]
        try:
            requests.post(
                f'{self.base_url}/setMyCommands',
                json={
                    'commands': commands_descriptions,
                },
            )
        except requests.exceptions.RequestException as request_exception:
            self.logger.warning(
                'Could not update bot commands on server',
                exc_info=request_exception,
            )

