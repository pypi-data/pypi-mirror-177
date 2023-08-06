import dataclasses


@dataclasses.dataclass
class Message:
    chat: "DGGChat"
    type: str
    nick: str = None
    features: list = None
    timestamp: int = None
    data: str = None

    async def reply(self, content):
        await self.chat.send(content)


@dataclasses.dataclass
class PrivateMessage(Message):
    message_id: str = None

    async def reply(self, content):
        await self.chat.send_privmsg(self.nick, content)


@dataclasses.dataclass
class MuteMessage(Message):
    duration: int = None
