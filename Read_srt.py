import os
import win32ui
import win32con


def select_file():
    dlg = win32ui.CreateFileDialog(1)  # 1 indicates an Open File dialog
    dlg.SetOFNInitialDir('C:\\')       # Set initial directory if you want
    dlg.DoModal()                      # Display the file dialog
    file_path = dlg.GetPathName()       # Get the selected file path
    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected")
    return file_path


# Call the function to open the file dialog and select an .srt file
srt_file_path = select_file()
if srt_file_path and os.path.exists(srt_file_path):
    with open(srt_file_path, 'r') as srt_file:
        srt_content = srt_file.read()
        print("Subtitle Content:\n")
        print(srt_content)
else:
    print("No file selected or file does not exist.")
