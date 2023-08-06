# py - Ayiin
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/pyAyiin >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/pyAyiin/blob/main/LICENSE/>.
#
# FROM py-Ayiin <https://github.com/AyiinXd/pyAyiin>
# t.me/AyiinXdSupport & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from io import BytesIO
from typing import Any

from .primitives.int import Int, Long
from .tl_object import TLObject


class FutureSalt(TLObject):
    ID = 0x0949D9DC

    __slots__ = ["valid_since", "valid_until", "salt"]

    QUALNAME = "FutureSalt"

    def __init__(self, valid_since: int, valid_until: int, salt: int):
        self.valid_since = valid_since
        self.valid_until = valid_until
        self.salt = salt

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "FutureSalt":
        valid_since = Int.read(data)
        valid_until = Int.read(data)
        salt = Long.read(data)

        return FutureSalt(valid_since, valid_until, salt)

    def write(self, *args: Any) -> bytes:
        b = BytesIO()

        b.write(Int(self.valid_since))
        b.write(Int(self.valid_until))
        b.write(Long(self.salt))

        return b.getvalue()
