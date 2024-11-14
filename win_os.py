import os
import win32ui
import win32con
import pyperclip


class WinOS:
    @staticmethod
    def select_file(file_extension):
        # Create a file filter using only the file extension
        file_filter = f"Files (*{file_extension})|*{file_extension}|All Files (*.*)|*.*|"
        dlg = win32ui.CreateFileDialog(1, None, None, win32con.OFN_FILEMUSTEXIST, file_filter)
        dlg.SetOFNInitialDir(rf'{os.getcwd()}\test_files')  # Set initial directory if you want
        dlg.DoModal()  # Display the file dialog
        file_path = dlg.GetPathName()  # Get the selected file path
        if file_path:
            print(f"\nSelected file: {file_path}")
            return file_path
        else:
            print('No file selected')
            return None

    @staticmethod
    def clipboard_copy(text):
        pyperclip.copy(text)
        print("\n\nCopied to clipboard!")

    @staticmethod
    def clipboard_paste():
        print("\n\nPasted from clipboard!")
        return pyperclip.paste()
