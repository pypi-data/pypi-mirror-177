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

import logging
import sys
import time

from pyAyiin.xd import GenSession
from pyAyiin.methods import *
from pyAyiin.pyrogram import AyiinMethods
from pyAyiin.pyrogram.ayiin import eod, eor
from pyAyiin.telethon.ayiin import *


__copyright__ = "Copyright (C) 2022-present AyiinXd <https://github.com/AyiinXd>"
__license__ = "GNU General Public License v3.0 (GPL-3.0)"
__version__ = "0.0.9"


adB = AyiinDB()

DEVS = [1905050903, 1965424892]


class PyrogramXd(AyiinMethods, GenSession, Methods):
    pass


class TelethonXd(AyiinMethod, GenSession, Methods):
    pass


suc_msg = (f"""
========================×========================
              Credit Py-Ayiin {__version__}
========================×========================
"""
)

fail_msg = (f"""
========================×========================
      Commit Yang Bener Bego Biar Gak Error
              Credit Py-Ayiin {__version__}
========================×========================
"""
)

run_as_module = False

if sys.argv[0] == "-m":
    run_as_module = True

    print("\n\n" + __copyright__ + "\n" + __license__)
    print(suc_msg)
else:
    print("\n\n" + __copyright__ + "\n" + __license__)
    print(fail_msg)
