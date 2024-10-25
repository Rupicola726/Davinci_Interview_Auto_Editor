import win_os
from win_os import WinOS
from SubtitleManager import Subtitle, SubManager
from chatGPTmanager import ChatManager
import pyperclip
import os


file_path = WinOS.select_file('.srt')
srt_parser = SubManager()
srt_parser.parse_srt(file_path)
# print Subtitles list
for subtitle in srt_parser.subtitles:
    print(subtitle)

chat_manager = ChatManager()
chat_manager.export_to_chat(srt_parser.subtitles)
