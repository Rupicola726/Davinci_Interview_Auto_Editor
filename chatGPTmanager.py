import os
from win_os import WinOS


class ScriptLine:
    def __init__(self, script_line):
        self.script_line = script_line
        self.id, self.text = self.script_line.split(' -- ')
        tails_code, frame_codes = self.id.split('-')
        self.tails = tails_code[0:2]
        self.code = int(tails_code[2:])
        self.start_fc, self.end_fc = frame_codes.split('X')
        self.number = self.code - len(self.text)

    def __repr__(self):
        return (f"Line of script({self.number}, {self.id}, "
                f"{self.start_fc}, {self.end_fc}, "
                f"{self.text})")


class ChatManager:
    def __init__(self, prompt=None):
        self.script_list = []
        if prompt is None:
            with open(rf'{os.getcwd()}\prompt.txt') as prompt_path:
                prompt = prompt_path.read()
        self.prompt = prompt
        self.script = ""

    def export_to_chat(self, subtitles):
        self.script = f'\n{self.prompt}'
        for subtitle in subtitles:
            self.script += f'\n{subtitle.repr_text()}'
        self.script += f'\n"""'
        print(self.script)
        WinOS.clipboard_copy(self.script)

    def import_from_chat(self):
        with open(WinOS.select_file('.txt')) as file:
            file = file.read()
            file_list = (file[1:]).split('\n- ')
            # separate extraction of first line because it starts without \n
            self.script_list.append(ScriptLine(file_list[0][1:]))
        for line in file_list[1:]:
            self.script_list.append(
                ScriptLine(line))
        return self.script_list
