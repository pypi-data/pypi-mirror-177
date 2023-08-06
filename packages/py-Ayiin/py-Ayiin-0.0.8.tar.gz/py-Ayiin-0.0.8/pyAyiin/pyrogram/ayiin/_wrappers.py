import logging

from asyncio import sleep

from pyrogram.enums import MessageServiceType
from pyrogram.errors import MessageDeleteForbidden, MessageNotModified
from pyrogram.types import Message


LOGS = logging.getLogger(__name__)


class Wrappers(object):
    async def eor(self, message, text=None, **args):
        time = args.get("time", None)
        edit_time = args.get("edit_time", None)
        if "edit_time" in args:
            del args["edit_time"]
        if "time" in args:
            del args["time"]
        if "link_preview" not in args:
            args["link_preview"] = False
        args["reply_to"] = message.reply_to_message.id or message
        if message.outgoing and not isinstance(message, MessageServiceType()):
            if edit_time:
                await sleep(edit_time)
            if "file" in args and args["file"] and not message.media:
                await message.delete()
                ok = await message.client.send_message(message.chat.id, text, **args)
            else:
                try:
                    try:
                        del args["reply_to"]
                    except KeyError:
                        pass
                    ok = await message.edit(text, **args)
                except MessageNotModified:
                    ok = message
        else:
            ok = await message.client.send_message(message.chat.id, text, **args)
    
        if time:
            await sleep(time)
            return await ok.delete()
        return ok
    
    
    async def eod(self, message, text=None, **kwargs):
        kwargs["time"] = kwargs.get("time", 8)
        return await self.eor(message, text, **kwargs)
    
    
    async def _try_delete(self, message):
        try:
            return await message.delete()
        except (MessageDeleteForbidden):
            pass
        except BaseException as er:
            LOGS.error("Error while Deleting Message..")
            LOGS.exception(er)
    
    
    setattr(Message, "eor", eor)
    setattr(Message, "try_delete", _try_delete)
