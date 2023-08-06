import json
import logging
from typing import Callable, Union

from websockets.client import connect, WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed

from .event import EventType
from .message import Message, PrivateMessage, MuteMessage
from .user import User
from .errors import (
    AccountTooYoung,
    Banned,
    DuplicateMessage,
    InvalidMessage,
    NeedLogin,
    NoPermission,
    NotFound,
    ProtocolError,
    SubMode,
    Throttled,
    TooManyConnections,
)

logger = logging.getLogger(__name__)


class DGGChat:
    uri = "wss://chat.destiny.gg/ws"
    origin = "https://www.destiny.gg"

    def __init__(self, auth_token=None, username: str = None):
        self.auth_token = auth_token
        self.username = username.lower() if isinstance(username, str) else None
        self.ws = WebSocketClientProtocol
        self._connected = False
        self._events = {}
        self._users = {}

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(username='{self.username}')"
            if self.username
            else f"{self.__class__.__name__}()"
        )

    @property
    def users(self) -> dict:
        return self._users.copy()

    async def send(self, msg: str):
        """Send a message to chat."""
        payload = {"data": msg}
        await self.ws.send(f"MSG {json.dumps(payload)}")

    async def send_privmsg(self, nick: str, msg: str):
        """Send private message to someone."""
        payload = {"nick": nick, "data": msg}
        await self.ws.send(f"PRIVMSG {json.dumps(payload)}")

    def event(self, event_name: str = None):
        """Decorator to run function when the specified event occurs."""

        def decorator(func: Callable):
            event = event_name or func.__name__
            if event not in self._events:
                self._events[event] = []
            self._events[event].append(func)
            return func

        return decorator

    async def run(self):
        headers = None
        if self.auth_token:
            headers = {"cookie": f"authtoken={self.auth_token}"}
        async for ws in connect(
            self.uri,
            origin=self.origin,
            extra_headers=headers,
            ping_timeout=None,
            logger=logging.getLogger("websocket"),
        ):
            self.ws = ws
            try:
                async for msg in ws:
                    await self._on_message(msg)
            except ConnectionClosed:
                logger.info(f"Websocket closed, restarting...")
                continue

    async def _on_message(self, message: str):
        event_type, data = message.split(maxsplit=1)
        data = json.loads(data)
        if event_type == EventType.MESSAGE:
            msg = Message(
                self,
                event_type,
                data["nick"],
                data["features"],
                data["timestamp"],
                data["data"],
            )
            await self.on_message(msg)
            if self.is_mentioned(msg):
                await self.on_mention(msg)
        elif event_type == EventType.PRIVMSG:
            msg = PrivateMessage(
                self,
                event_type,
                data["nick"],
                timestamp=data["timestamp"],
                data=data["data"],
                message_id=data["messageid"],
            )
            await self.on_privmsg(msg)
            if self.is_mentioned(msg):
                await self.on_mention(msg)
        elif event_type == EventType.BROADCAST:
            msg = Message(
                self, event_type, timestamp=data["timestamp"], data=data["data"]
            )
            await self.on_broadcast(msg)
        elif event_type == EventType.NAMES:
            await self.on_names(data["connectioncount"], data["users"])
        elif event_type in (EventType.JOIN, EventType.QUIT):
            msg = Message(
                self, event_type, data["nick"], data["features"], data["timestamp"]
            )
            if event_type == EventType.JOIN:
                await self.on_join(msg)
            else:
                await self.on_quit(msg)
        elif event_type == EventType.BAN:
            msg = Message(
                self,
                event_type,
                data["nick"],
                data["features"],
                data["timestamp"],
                data["data"],
            )
            await self.on_ban(msg)
        elif event_type == EventType.UNBAN:
            msg = Message(
                self,
                event_type,
                data["nick"],
                data["features"],
                data["timestamp"],
                data["data"],
            )
            await self.on_unban(msg)
        elif event_type == EventType.MUTE:
            msg = MuteMessage(
                self,
                event_type,
                data["nick"],
                data["features"],
                data["timestamp"],
                data["data"],
                data["duration"],
            )
            await self.on_mute(msg)
        elif event_type == EventType.UNMUTE:
            msg = Message(
                self,
                event_type,
                data["nick"],
                data["features"],
                data["timestamp"],
                data["data"],
            )
            await self.on_unmute(msg)
        elif event_type == EventType.REFRESH:
            msg = Message(
                self, event_type, data["nick"], data["features"], data["timestamp"]
            )
            await self.on_refresh(msg)
        elif event_type == EventType.PRIVMSGSENT:
            pass
        elif event_type == EventType.ERROR:
            err_dict = {
                "banned": Banned,
                "duplicate": DuplicateMessage,
                "invalidmsg": InvalidMessage,
                "needlogin": NeedLogin,
                "nopermission": NoPermission,
                "notfound": NotFound,
                "privmsgaccounttooyoung": AccountTooYoung,
                "protocolerror": ProtocolError,
                "submode": SubMode,
                "throttled": Throttled,
                "toomanyconnections": TooManyConnections,
            }
            if (desc := data["description"]) in err_dict:
                raise err_dict[desc]
            else:
                logger.error(event_type, data)
                raise Exception(desc)
        else:
            logger.warning(f"Unknown event type: {event_type} {data}")

    async def on_message(self, msg: Message):
        """Do stuff when a MSG is received."""
        for func in self._events.get("on_message", tuple()):
            await func(msg)

    def mention(self):
        """Decorator to run function on mentions. Shortcut for event('on_mention')."""
        return self.event("on_mention")

    def is_mentioned(self, msg: Union[Message, PrivateMessage]) -> bool:
        return (
            False if self.username is None else (self.username in msg.data.casefold())
        )

    async def on_mention(self, msg):
        """Do stuff when mentioned."""
        for func in self._events.get("on_mention", tuple()):
            await func(msg)

    async def on_names(self, connectioncount: int, users: list):
        """Do stuff when the NAMES message is received upon connecting to chat."""
        self._users = {
            user["nick"].lower(): User(user["nick"], user["features"]) for user in users
        }
        for func in self._events.get("on_names", tuple()):
            await func(connectioncount, users)

    async def on_privmsg(self, msg: PrivateMessage):
        """Do stuff when a PRIVMSG is received."""
        for func in self._events.get("on_privmsg", tuple()):
            await func(msg)

    async def on_broadcast(self, msg: Message):
        """Do stuff when a BROADCAST is received."""
        for func in self._events.get("on_broadcast", tuple()):
            await func(msg)

    async def on_join(self, msg: Message):
        """Do stuff when chatter joins."""
        self._users[msg.nick.lower()] = User(msg.nick, msg.features)
        for func in self._events.get("on_join", tuple()):
            await func(msg)

    async def on_quit(self, msg: Message):
        """Do stuff when chatter joins."""
        if msg.nick.lower() in self._users:
            del self._users[msg.nick.lower()]
        for func in self._events.get("on_quit", tuple()):
            await func(msg)

    async def on_ban(self, msg: Message):
        """Do stuff when a chatter is banned."""
        for func in self._events.get("on_ban", tuple()):
            await func(msg)

    async def on_unban(self, msg: Message):
        """Do stuff when a chatter is unbanned."""
        for func in self._events.get("on_unban", tuple()):
            await func(msg)

    async def on_mute(self, msg: MuteMessage):
        """Do stuff when a chatter is muted."""
        for func in self._events.get("on_mute", tuple()):
            await func(msg)

    async def on_unmute(self, msg: Message):
        """Do stuff when a chatter is unmuted."""
        for func in self._events.get("on_unmute", tuple()):
            await func(msg)

    async def on_refresh(self, msg: Message):
        """Do stuff when refreshed."""
        for func in self._events.get("on_refresh", tuple()):
            await func(msg)
