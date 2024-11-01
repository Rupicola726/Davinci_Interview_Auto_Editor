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
for script_line in script_list:
    print(script_line)

sub_manager = SubManager()
sub_manager.subtitles, missing_subs, id_mismatch_subs = srt_parser.reorder_to_script(script_list)

for subtitle in sub_manager.subtitles:
    print(subtitle)
if not missing_subs:
    print("\n\033[32mNO MISSING SUBS!")
else:
    print("\n\033[31mMISSING SUBS:")
    for sub in missing_subs:
        print(sub)
if not id_mismatch_subs:
    print("\033[32mNO ID MISSMATCH!")
else:
    print("\033[31mID MISSMATCH:")
    for sub in id_mismatch_subs:
        print(sub)
print("\033[0m", end="")
