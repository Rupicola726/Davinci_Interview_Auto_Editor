import os
import win32ui
import win32con
import re
import pyperclip
import sys


# Subtitle class to store subtitle number, timecodes, and text
class Subtitle:
    def __init__(self, number, start_time, end_time, start_tc, end_tc, text):
        self.number = number
        self.start_time = start_time
        self.end_time = end_time
        self.start_tc = start_tc
        self.end_tc = end_tc
        self.text = text

    def __repr__(self):
        return (f"Subtitle({self.number}, {self.start_time}, {self.end_time},"
                f"  {self.start_tc}, {self.end_tc}, {self.text})")

    def repr_text(self):
        return f"{self.number}) {self.text}"


def select_file(file_extension):
    # Create a file filter using only the file extension
    file_filter = f"Files (*{file_extension})|*{file_extension}|All Files (*.*)|*.*|"
    dlg = win32ui.CreateFileDialog(1, None, None, win32con.OFN_FILEMUSTEXIST, file_filter)
    dlg.SetOFNInitialDir(rf'{os.getcwd()}\test_files')  # Set initial directory if you want
    dlg.DoModal()  # Display the file dialog
    file_path = dlg.GetPathName()  # Get the selected file path
    if file_path:
        print(f"Selected file: {file_path}")
    else:
        sys.exit('No file selected')

    return file_path


def parse_line(line, timecode=False):
    # Split the timecode into hours, minutes, seconds, and milliseconds for subtitle
    if timecode:
        hours, minutes, seconds_milliseconds = line.split(':')
        seconds, milliseconds = seconds_milliseconds.split(',')

        # Convert everything to integers
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        milliseconds = int(milliseconds)

        return hours, minutes, seconds, milliseconds

    else:   # Split the timecode into hours, minutes, seconds, and frames for timeline start timecode
        stc_hours, stc_minutes, stc_seconds, stc_frames = line.split(':')

        # Convert everything to integers
        stc_hours = int(stc_hours)
        stc_minutes = int(stc_minutes)
        stc_seconds = int(stc_seconds)
        stc_frames = int(stc_frames)

        return stc_hours, stc_minutes, stc_seconds, stc_frames


def time2frames(time, stc_total_seconds, stc_frames, frame_rate): # Transform TC of subtitle to FC

    # Get integers from line
    hours, minutes , seconds, milliseconds = parse_line(time, True)

    # Calculate number of seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0

    # calculate number of seconds with StartTC
    input_total_seconds = (total_seconds * (23.976 / 24) - stc_total_seconds)

    # Calculate the total frames based on the frame rate
    total_frames = int(round(input_total_seconds * frame_rate) - stc_frames)

    return total_frames


def parse_srt(file_path, stc_total_seconds, stc_frames, frame_rate):
    with open(file_path, 'r', encoding='utf-8') as file:
        subtitles = []
        subtitle_number = None
        start_time = None
        end_time = None
        start_fc = None
        end_fc = None
        subtitle_text = []

        for line in file:
            line = line.strip()

            # If it's a digit, it's the subtitle number
            if line.isdigit():
                if subtitle_number is not None:
                    # Append previous subtitle before moving to the next
                    subtitles.append(Subtitle(subtitle_number, start_time, end_time, start_fc,
                                              end_fc, " ".join(subtitle_text)))
                subtitle_number = int(line)
                subtitle_text = []  # Reset for the next subtitle

            # If it contains '-->', it's the timecode line
            elif '-->' in line:
                times = line.split(' --> ')
                start_time = times[0]
                end_time = times[1]
                start_fc = time2frames(start_time, stc_total_seconds, stc_frames, frame_rate)
                end_fc = time2frames(end_time, stc_total_seconds, stc_frames, frame_rate)

            # Otherwise, it's part of the subtitle text
            else:
                if line:
                    clean_line = re.sub(r'<.*?>', '', line)  # Clean up HTML tags
                    subtitle_text.append(clean_line)

            # Append the last subtitle after the loop finishes
        if subtitle_number is not None:
            subtitles.append(Subtitle(subtitle_number, start_time, end_time,
                                      start_fc, end_fc, " ".join(subtitle_text)))

        return subtitles


def output_to_chat(subtitles,prompt=None):
    output_Chat_GPT = f'\n{prompt}'
    for subtitle in subtitles:
        output_Chat_GPT += f'\n{subtitle.repr_text()}'
    print(output_Chat_GPT)
    pyperclip.copy(output_Chat_GPT)
    print("\n\nParsed text copied to clipboard!")


timeline_start_tc = None
frame_rate = None
with open(rf'{os.getcwd()}\prompt.txt') as prompt_path:
    prompt = prompt_path.read()
# Set default settings if they're not specified
if timeline_start_tc is None:
    timeline_start_tc = '01:00:00:00'
if frame_rate is None:
    frame_rate = 23.976
stc_hours, stc_minutes, stc_seconds, stc_frames = parse_line(timeline_start_tc, False)
stc_total_seconds = stc_hours * 3600 + stc_minutes * 60 + stc_seconds

# Call the function to open the file dialog and select an .srt file
srt_file_path = select_file('.srt')
if srt_file_path and os.path.exists(srt_file_path):
    with open(srt_file_path, 'r') as srt_file:
        srt_content = srt_file.read()
        print("Subtitle Content:\n")
        print(srt_content)
else:
    print("No file selected or file does not exist.")

subtitles = parse_srt(srt_file_path, stc_total_seconds, stc_frames, frame_rate)
for subtitle in subtitles:
    print(subtitle)

output_to_chat(subtitles,prompt)
