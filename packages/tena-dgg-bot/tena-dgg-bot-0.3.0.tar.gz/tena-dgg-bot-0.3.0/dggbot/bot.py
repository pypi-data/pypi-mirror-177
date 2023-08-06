import itertools
import logging
from typing import List, Tuple, Union, Callable

from .message import Message, PrivateMessage
from .chat import DGGChat

logger = logging.getLogger(__name__)


class DGGBot(DGGChat):
    def __init__(
        self,
        auth_token: str,
        username: str = None,
        owner: str = None,
        prefix="!",
    ):
        super().__init__(auth_token=auth_token, username=username)
        self._owner = owner.lower() if owner else None
        self.prefix = prefix
        self._commands = {}

    def command(
        self,
        aliases: Union[List[str], Tuple[str]] = tuple(),
        *args,
        whisper_only: bool = False,
        **kwargs,
    ):
        """
        Decorator to add commands to bot.
        :param aliases: aliases to call the function besides the function name
        :param whisper_only: Command will only run when through whispers/private messages.
        :return:
        """

        def decorator(func: Callable):
            if whisper_only:
                func = self.check(lambda msg: isinstance(msg, PrivateMessage))(func)
            for cmd_name in itertools.chain((func.__name__,), aliases):
                if cmd_name in self._commands:
                    raise Exception(f'Command name "{cmd_name}" already exists.')
                else:
                    self._commands[cmd_name] = func
            return func

        return decorator

    def is_command(self, msg: Message) -> bool:
        return msg.data.startswith(self.prefix)

    async def on_command(self, msg: Message):
        cmd = msg.data.split(" ")[0][1:]
        if cmd in self._commands:
            if hasattr(self._commands[cmd], "_perms"):
                perms = self._commands[cmd]._perms
                if any(not perm(msg) for perm in perms):
                    return
            logger.debug(f"Command {cmd} called by {msg.nick}")
            await self._commands[cmd](msg)

    def check(self, *check_funcs: Callable):
        """
        Decorator to restrict command-usage by using a check function(s).
        :param check_funcs: functions that check for some statement and returns a bool.
        :return:
        """

        def decorator(func: Callable):
            if not hasattr(func, "_perms"):
                func._perms = []
            func._perms.extend(check_funcs)
            return func

        return decorator

    def is_owner(self):
        """Decorator to make command only usable by the bot owner."""
        return self.check(lambda msg: msg.nick.lower() == self._owner)

    async def on_message(self, msg: Message):
        await super().on_message(msg)
        if self.is_command(msg):
            await self.on_command(msg)

    async def on_privmsg(self, msg: PrivateMessage):
        await super().on_privmsg(msg)
        if self.is_command(msg):
            await self.on_command(msg)
