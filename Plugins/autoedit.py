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

# ---size and duration--- started        
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def get_readable_file_size(size_in_bytes):
    if size_in_bytes == 0:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
# ---size and duration--- ended
  
@autocaption.on_message(filters.channel & (filters.document | filters.video | filters.audio ) & ~filters.edited, group=-1)
async def editing(bot, message):
      caption_text = await get_caption(Config.ADMIN_ID)
      try:
         caption_text = caption_text.caption
      except:
         caption_text = ""
         pass 
      if (message.document or message.video or message.audio): 
          media = message.audio or message.video or message.document or message.animation
	  	    if message.video:
            New_duration = f"\n**File Duration:** `{convert(media.duration)}`\n"
          elif message.caption:                        
             file_caption = f"**{message.caption}**"
          else:
             file_caption = ""
          file = media.file_name
          new_file = file.replace("-", " ").replace("@", " ").replace("_", " ").replace("avi", " ").replace(".mp4", " ").replace(".mkv", " ").replace(".pdf", " ").replace(".apk", " ").replace(".mp3", " ").replace(".zip", " ")
          New_name = "**File Name:** " + new_file
          New_size = f"**File Size:** `{get_readable_file_size(media.file_size)}`\n\n"
      try:
          if caption_position == "top":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = New_name + "\n\n" + caption_text + "\n" + file_caption,
                 parse_mode = "markdown"
             )
          elif caption_position == "bottom":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = New_name + "\n\n" + file_caption + "\n" + caption_text,
                 parse_mode = "markdown"
             )
          elif caption_position == "nil":
             await bot.edit_message_caption(
                 chat_id = message.chat.id,
                 message_id = message.message_id,
                 caption = New_name + New_duration + New_size + caption_text, 
                 parse_mode = "markdown"
             )
          elif caption_position == "nil" and message.document:
		         await bot.edit_message_caption(
                 chat_id = message.chat.id,
                 message_id = message.message_id,
                 caption = New_name + New_size + caption_text, 
                 parse_mode = "markdown"
             )
                
      except:
          pass
     
