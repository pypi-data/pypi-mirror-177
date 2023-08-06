#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import pyroxd
from pyroxd import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~pyroxd.types.InlineQueryResultCachedAudio`
    - :obj:`~pyroxd.types.InlineQueryResultCachedDocument`
    - :obj:`~pyroxd.types.InlineQueryResultCachedAnimation`
    - :obj:`~pyroxd.types.InlineQueryResultCachedPhoto`
    - :obj:`~pyroxd.types.InlineQueryResultCachedSticker`
    - :obj:`~pyroxd.types.InlineQueryResultCachedVideo`
    - :obj:`~pyroxd.types.InlineQueryResultCachedVoice`
    - :obj:`~pyroxd.types.InlineQueryResultArticle`
    - :obj:`~pyroxd.types.InlineQueryResultAudio`
    - :obj:`~pyroxd.types.InlineQueryResultContact`
    - :obj:`~pyroxd.types.InlineQueryResultDocument`
    - :obj:`~pyroxd.types.InlineQueryResultAnimation`
    - :obj:`~pyroxd.types.InlineQueryResultLocation`
    - :obj:`~pyroxd.types.InlineQueryResultPhoto`
    - :obj:`~pyroxd.types.InlineQueryResultVenue`
    - :obj:`~pyroxd.types.InlineQueryResultVideo`
    - :obj:`~pyroxd.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "pyroxd.Client"):
        pass
