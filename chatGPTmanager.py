import os
from win_os import WinOS


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
        print(self.script)
        WinOS.clipboard_copy(self.script)

    def import_from_chat(self):
        with open(WinOS.select_file('.txt')) as file:
            script = file.read()
            self.script_list = (script[1:]).split('\n-')
            return self.script_list
