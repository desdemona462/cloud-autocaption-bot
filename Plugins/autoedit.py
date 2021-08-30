import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
from pyrogram import filters
from bot import autocaption
from config import Config
from database.database import *


# =
usercaption_position = Config.CAPTION_POSITION
caption_position = usercaption_position.lower()


@autocaption.on_message(filters.channel & (filters.document | filters.video | filters.audio ) & ~filters.edited, group=-1)
async def editing(bot, message):
      caption_text = await get_caption(Config.ADMIN_ID)
      try:
         caption_text = caption_text.caption
      except:
         caption_text = ""
         pass 
      if (message.document or message.video or message.audio): 
          if message.caption:                        
             file_caption = f"**{message.caption}**"
             file = media.file_name
             new_file = file.replace("-", " ").replace("@", " ").replace("_", " ").replace("avi", " ").replace(".mp4", " ").replace(".mkv", " ").replace(".pdf", " ").replace(".apk", " ").replace(".mp3", " ").replace(".zip", " ")
          else:
             file_caption = ""
             file = media.file_name
             new_file = file.replace("-", " ").replace("@", " ").replace("_", " ").replace("avi", " ").replace(".mp4", " ").replace(".mkv", " ").replace(".pdf", " ").replace(".apk", " ").replace(".mp3", " ").replace(".zip", " ")
                                                 
      try:
          if caption_position == "top":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = new_file + "\n\n" + caption_text + "\n" + file_caption,
                 parse_mode = "markdown"
             )
          elif caption_position == "bottom":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = new_file + "\n\n" + file_caption + "\n" + caption_text,
                 parse_mode = "markdown"
             )
          elif caption_position == "nil":
             await bot.edit_message_caption(
                 chat_id = message.chat.id,
                 message_id = message.message_id,
                 caption = new_file + "\n\n" + caption_text, 
                 parse_mode = "markdown"
             ) 
      except:
          pass
     
