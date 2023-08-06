from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .telegram_bot import TelegramBot  # type: ignore


class CommandHandler(Protocol):
    def __call__(self, bot: TelegramBot, sender_id: int, argument: str | None):
        ...
