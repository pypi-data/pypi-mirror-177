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
from typing import cast

from .bytes import Bytes


class String(Bytes):
    @classmethod
    def read(cls, data: BytesIO, *args) -> str:  # type: ignore
        return cast(bytes, super(String, String).read(data)).decode(errors="replace")

    def __new__(cls, value: str) -> bytes:  # type: ignore
        return super().__new__(cls, value.encode())
