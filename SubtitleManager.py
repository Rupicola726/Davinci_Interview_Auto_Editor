import os
import win32ui
import win32con
import re
import pyperclip
import sys


# Subtitle class to store subtitle number, timecodes, and text
class Subtitle:
    def __init__(self, number, sub_id, start_time, end_time, start_tc, end_tc, text):
        self.id = sub_id
        self.number = number
        self.start_time = start_time
        self.end_time = end_time
        self.start_tc = start_tc
        self.end_tc = end_tc
        self.text = text

    def __repr__(self):
        return (f"Subtitle({self.number}, {self.id}, "
                f"{self.start_time}, {self.end_time}, "
                f"{self.start_tc}, {self.end_tc}, "
                f"{self.text})")

    def repr_text(self):
        return f"{self.id} -- {self.text}"


class SubManager:
    def __init__(self, frame_rate=23.976, timeline_start_tc='01:00:00:00'):
        self.subtitles = []
        self.frame_rate = frame_rate
        self.timeline_start_tc = timeline_start_tc
        self.stc_total_seconds, self.stc_frames = self._parse_start_timecode(timeline_start_tc)

    def _parse_start_timecode(self, timeline_start_tc):
        stc_hours, stc_minutes, stc_seconds, stc_frames = self.parse_time(timeline_start_tc, False)
        total_seconds = stc_hours * 3600 + stc_minutes * 60 + stc_seconds
        return total_seconds, stc_frames

    @staticmethod
    def parse_time(line, timecode=False):
        if timecode:
            hours, minutes, seconds_milliseconds = line.split(':')
            seconds, milliseconds = seconds_milliseconds.split(',')
            return int(hours), int(minutes), int(seconds), int(milliseconds)
        else:
            stc_hours, stc_minutes, stc_seconds, stc_frames = line.split(':')
            return int(stc_hours), int(stc_minutes), int(stc_seconds), int(stc_frames)

    def time2frames(self, time):
        hours, minutes, seconds, milliseconds = self.parse_time(time, True)
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        input_total_seconds = (total_seconds * (23.976 / 24) - self.stc_total_seconds)
        total_frames = int(round(input_total_seconds * self.frame_rate) - self.stc_frames)
        return total_frames

    @staticmethod
    def id_generator(n, text, start_fc, end_fc):
        tails = ''
        for character in text:
            if character.isalpha():
                tails += character
                break
        for character in text[::-1]:
            if character.isalpha():
                tails += character
                break
        if tails == '':
            tails = '~~'
        id = tails + str(n + len(text)) + '-' + str(start_fc) + 'X' + str(end_fc)
        return id

    def parse_srt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            subtitle_number = None
            start_time = None
            end_time = None
            subtitle_text = ''
            for line in file:
                line = line.strip()
                if line.isdigit():
                    if subtitle_number is not None:
                        sub_id = self.id_generator(subtitle_number, str(subtitle_text), start_fc, end_fc)
                        self.subtitles.append(
                            Subtitle(subtitle_number, sub_id, start_time, end_time, start_fc, end_fc, subtitle_text))
                    subtitle_number = int(line)
                    subtitle_text = ''
                elif '-->' in line:
                    times = line.split(' --> ')
                    start_time, end_time = times
                    start_fc = self.time2frames(start_time)
                    end_fc = self.time2frames(end_time)
                else:
                    if line:
                        clean_line = re.sub(r'<.*?>', '', line)
                        subtitle_text = str(clean_line)
            if subtitle_number is not None:
                sub_id = self.id_generator(subtitle_number, subtitle_text, start_fc, end_fc)
                self.subtitles.append(
                    Subtitle(subtitle_number, sub_id, start_time, end_time, start_fc, end_fc, subtitle_text))

    def reorder_to_script(self, ref_list):
        # Create a dictionary to quickly look up subtitles in sub_list by text
        sub_dict = {subtitle.id: subtitle for subtitle in self.subtitles}

        # Lists for reordering and tracking issues
        ordered_subtitles = []
        missing_subtitles = []
        wrong_subtitles = []

        # Reorder sub_list to match ref_list and track issues
        for ref_sub in ref_list:
            ref_text = ref_sub.text
            ref_id = ref_sub.id

            if ref_id in sub_dict:
                sub = sub_dict[ref_id]
                # Check if text matches ID
                if sub.text == ref_text:
                    ordered_subtitles.append(sub)  # Correct match
                else:
                    # ID mismatch, add to wrong subtitles
                    wrong_subtitles.append({"expected": ref_sub, "found": sub})
            else:
                # ID not found in sub_list, add to missing subtitles
                missing_subtitles.append(ref_sub)

        # Return ordered list and issue lists
        return ordered_subtitles, missing_subtitles, wrong_subtitles
