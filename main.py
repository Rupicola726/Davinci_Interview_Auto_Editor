import win_os
from win_os import WinOS
from SubtitleManager import Subtitle, SubManager
from chatGPTmanager import ChatManager
import pyperclip
import os


def properties_transfer(donor, acceptor):
    acceptor.subtitles = donor.subtitles
    acceptor.frame_rate = donor.frame_rate
    acceptor.timeline_start_tc = donor.timeline_start_tc
    acceptor.stc_total_seconds = donor.stc_total_seconds
    acceptor.stc_frames = donor.stc_frames


file_path = WinOS.select_file('.srt')
srt_parser = SubManager()
srt_parser.parse_srt(file_path)
# print Subtitles list
for subtitle in srt_parser.subtitles:
    print(subtitle)

chat_manager = ChatManager()
chat_manager.export_to_chat(srt_parser.subtitles)
# input('Press Enter to paste script from clipboard...')
script_list = chat_manager.import_from_chat()

sub_manager = SubManager()

properties_transfer(srt_parser, sub_manager)

