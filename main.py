# import ctypes
import os
import shutil
import sys
import configparser

from PyQt5.QtCore import Qt, pyqtSignal
# from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFrame, QMenuBar, QListWidget, \
    QListWidgetItem, QWidget, QInputDialog
from PyQt5.QtGui import QFont, QIcon, QPixmap
# from PyQt5.QtWinExtras import QtWin
# from win32comext.shell import shellcon, shell
from sys import platform
import subprocess
import functions


supported_file_extensions = ['txt', 'png', 'jpg', 'pdf']

class MainWindow(QMainWindow):
    def __init__(self, config, width, height):
        super().__init__()
        self.setWindowTitle("Absolute Director")
        self.setGeometry(1000, 300, width, height)  # Initial window size: width, height

        # self.file_window.list.setStyleSheet(
        #     "QListWidget {"
        #     "color: black;"
        #     "font-size: 24px;"  # Hardcoded value for testing
        #     "font-family: Arial;"
        #     "}"
        #     "QListWidget::item:selected {"
        #     "background-color: blue;"
        #     "}"
        #     "QListWidget::item:hover {"
        #     "background-color: green;"
        #     "}"
        # )

        self.setStyleSheet(f"background-color: {config['background_color']};")
        # Adding a menu bar with a larger font and centered text
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setGeometry(0, 0, 1200, 75)  # x, y, width, height
        font = QFont(config['menu_bar_font_family'], int(config['menu_bar_font_size']))  # Font name and point size
        self.menu_bar.setFont(font)
        self.menu_bar.setStyleSheet("QMenuBar { background-color: " + config['menu_bar_color'] + "; color:" + config['menu_bar_font_color'] + "; }"
                                    "QMenuBar::item { padding: 20px 10px; }" "QMenuBar::item:selected { background-color: " + config['menu_bar_item_hover_bg'] + "; color: " + config['menu_bar_item_hover_fg'] +" ;}" "QMenuBar::item:hover {background-color: " + config['menu_bar_item_hover_bg'] + "; color: black;}")  # Adjust padding for vertical centering

        file_menu = self.menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        # Adding a button
        # self.button = QPushButton("Click me!", self)
        # self.button.setGeometry(350, 300, 100, 50)  # Adjusted y position to accommodate menu bar
        # self.button.clicked.connect(self.on_button_clicked)

        # Adding a vertical line as a divider
        self.divider = QFrame(self)
        self.divider.setFrameShape(QFrame.VLine)
        #self.divider.setFrameShadow(QFrame.Sunken)
        self.divider.setStyleSheet("QFrame { color: " + config['menu_bar_color'] +"; }")

        self.default_path = "d:\\chris\\test\\"


        self.file_window = FileWindow(0, width, height, config, self)
        self.file_window2 = FileWindow(width//2, width, height, config, self)

        self.file_window.display_directory_contents(self.default_path)
        self.file_window2.display_directory_contents(self.default_path)

        self.update_divider()
    # def on_button_clicked(self):
    #     QMessageBox.information(self, "Message", "You clicked the button!")
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_divider()
        self.menu_bar.setGeometry(0, 0, self.frameSize().width(), 75)  # Update menu bar width on resize
        self.file_window.resize()
        self.file_window2.resize()

    def update_divider(self):
        width = self.frameSize().width()
        height = self.frameSize().height()
        line_width = 10  # Set the thickness of the line
        self.divider.setGeometry(width // 2 - line_width // 2, 75, line_width, height - 75)  # Adjusted for menu bar height


    # def display_directory_contents(self, path):
    #     try:
    #         self.path = path
    #         self.file_window.list.clear()  # Clear existing entries
    #         files_and_folders = os.listdir(path)
    #         folders = []
    #         files = []
    #         for item in files_and_folders:
    #             full_path = os.path.join(path, item)
    #             if os.path.isdir(full_path):
    #                 folders.append(item)
    #             else:
    #                 files.append(item)
    #         folders.sort()
    #         files.sort()
    #
    #         for item in folders:
    #             icon = self.get_icon(os.path.join(path, item), True)
    #             list_item = QListWidgetItem(QIcon(icon), "[" + item + "]")
    #             self.file_window.list.addItem(list_item)
    #         for item in files:
    #             icon = self.get_icon(os.path.join(path, item), False)
    #             list_item = QListWidgetItem(QIcon(icon), item)
    #             self.file_window.list.addItem(list_item)
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to read directory contents: {str(e)}")
    #
    # def get_icon(self, path, is_folder):
    #     flags = shellcon.SHGFI_ICON | shellcon.SHGFI_SMALLICON
    #     if is_folder:
    #         flags |= shellcon.SHGFI_OPENICON
    #     info = shell.SHGetFileInfo(path, 0, flags)
    #     hicon = info[0]
    #     hbitmap = ctypes.windll.user32.CopyImage(hicon, 0, 0, 0, 0x00000001)  # 0x00000001 is the LR_COPYDELETEORG flag
    #     pixmap = QPixmap(QtWin.fromHBITMAP(hbitmap, QtWin.HBitmapNoAlpha))
    #     icon = QIcon(pixmap)
    #     return icon

    # def keyPressEvent(self, event):
    #     print(event.key())
    #     if event.key() == 16777220:
    #         print("enter")
    #         current_item = self.file_window.list.currentItem()
    #         if current_item and current_item.text().startswith('['):
    #             directory_name = current_item.text().strip('[]')
    #             print(self.path + '/' + directory_name)
    #             self.display_directory_contents(self.path + directory_name + '/')
    #             return
    #     if event.key() == 16777219:
    #         if len(self.path) > 3:
    #             parts = self.path.split('/')
    #             if parts[-1] == '':
    #                 parts = parts[:-2]
    #             else:
    #                 parts = parts[:-1]
    #
    #             new_path = '/'.join(parts) + '/'
    #
    #             self.display_directory_contents(new_path)
    def get_active_file_window(self):
        if self.file_window.list.hasFocus():
            return self.file_window
        elif self.file_window2.list.hasFocus():
            return self.file_window2
        return None
    def enter_pressed(self):
        print("active")
        current_file_window = self.get_active_file_window()
        if current_file_window is not None:
            current_item = current_file_window.list.currentItem()
            if current_item:
                item_text = current_item.text()
                if item_text.startswith('['):  # It's a directory
                    directory_name = item_text.strip('[]')
                    print(current_file_window.path + '\\' + directory_name)
                    current_file_window.display_directory_contents(current_file_window.path + directory_name + '\\')
                else:  # It's a file
                    file_path = os.path.join(current_file_window.path, item_text)
                    print("Opening file:", file_path)
                    if platform == "win32":
                        os.startfile(file_path)
                    else:
                        opener = "open" if platform == "darwin" else "xdg-open"
                        subprocess.call([opener, file_path])

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_Return:  # Enter key
            self.enter_pressed()
        elif event.key() == Qt.Key_Backspace:  # Backspace key
            current_file_window = self.get_active_file_window()
            if current_file_window is not None:
                if len(current_file_window.path) > 3:
                    parts = current_file_window.path.split('\\')
                    if parts[-1] == '':
                        parts = parts[:-2]
                    else:
                        parts = parts[:-1]

                    new_path = '\\'.join(parts) + '\\'
                    current_file_window.display_directory_contents(new_path)
        elif event.key() == Qt.Key_F3:  # F3 key
            current_file_window = self.get_active_file_window()
            if current_file_window is not None:
                current_item = current_file_window.list.currentItem()
                if current_item and not current_item.text().startswith('['):  # Ensure it's a file
                    file_path = os.path.join(current_file_window.path, current_item.text())
                    print("Opening file in Notepad++:", file_path)
                    #subprocess.call(["notepad++", file_path])
                    subprocess.run(f"\"C:\\Windows\\System32\\notepad.exe\" \"{file_path}\"")
        elif event.key() == Qt.Key_F4:  # F4 key
            current_file_window = self.get_active_file_window()
            if current_file_window is not None:
                current_item = current_file_window.list.currentItem()
                if current_item and not current_item.text().startswith('['):  # Ensure it's a file
                    file_path = os.path.join(current_file_window.path, current_item.text())
                    print("Opening file in Notepad++:", file_path)
                    #subprocess.call(["notepad++", file_path])
                    subprocess.run(f"\"C:\\Program Files\\Notepad++\\notepad++.exe\" \"{file_path}\"")
        elif event.key() == Qt.Key_F5:  # Check if F5 is pressed
            print("copying")
            active_file_window = self.get_active_file_window()
            target_file_window = self.file_window2 if active_file_window == self.file_window else self.file_window
            selected_items = active_file_window.list.selectedItems()
            if len(selected_items) < 1:
                selected_items = [active_file_window.list.currentItem()]
            for item in selected_items:
                source_path = os.path.join(active_file_window.path, item.text().strip('[]'))
                target_path = os.path.join(target_file_window.path, item.text().strip('[]'))
                if os.path.isdir(source_path):
                    if source_path != target_path:
                        #target_path = target_file_window.path
                        print(source_path)
                        print(target_path)
                        conflicts = functions.compare_2_directories(source_path + "\\", target_path)
                        print(conflicts)
                        self.copy(source_path, target_path, conflicts)
                    else:
                        files_and_folders = os.listdir(target_file_window.path)
                        while True:
                            new_location = self.copy_input(item.text())
                            print(new_location)
                            if new_location is not None:
                                contains_illegal_chars = any(char in new_location for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
                            else:
                                break
                            if new_location is not None and contains_illegal_chars is False and len(new_location) > 0 and new_location[-1] != ' ' and new_location[0] != ' ' and new_location not in files_and_folders:
                                new_path = os.path.join(target_file_window.path, new_location.strip('[]'))
                                if new_path != target_path:
                                    target_path = new_path
                                    conflicts = functions.compare_2_directories(source_path + "\\", target_path)
                                    self.copy(source_path, target_path, conflicts)
                                break
                            else:
                                QMessageBox.information(self, "Absolute Director", "Name can't already exist or contain / \\ : * ? \" < > | and cannot start or end with a space")
                else:
                    print("isfile")
                    if source_path != target_path:
                        data_in_target = os.listdir(target_file_window.path)
                        print(data_in_target)
                        if item.text() in data_in_target:
                            print(data_in_target)
                            overwrite = self.ask_user_choice(item.text())
                            if overwrite:
                                shutil.copy2(source_path, target_path)
                        else:
                            shutil.copy2(source_path, target_path)
                    else:
                        files_and_folders = os.listdir(target_file_window.path)
                        while True:
                            new_location = self.copy_input(item.text())
                            print(new_location)
                            if new_location is not None:
                                contains_illegal_chars = any(char in new_location for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
                            else:
                                break
                            if new_location is not None and contains_illegal_chars is False and len(new_location) > 0 and new_location[-1] != ' ' and new_location[0] != ' ' and new_location not in files_and_folders:
                                new_path = os.path.join(target_file_window.path, new_location.strip('[]'))
                                if new_path != target_path:
                                    target_path = new_path
                                    shutil.copy2(source_path, target_path)
                                break
                            else:
                                QMessageBox.information(self, "Absolute Director", "Name can't already exist or contain / \\ : * ? \" < > | and cannot start or end with a space")
            target_file_window.display_directory_contents(target_file_window.path)  # Refresh the target file window
            active_file_window.display_directory_contents(active_file_window.path)
        elif event.key() == Qt.Key_F6:  # Check if F6 is pressed
            print("moving")
            active_file_window = self.get_active_file_window()
            target_file_window = self.file_window2 if active_file_window == self.file_window else self.file_window
            selected_items = active_file_window.list.selectedItems()
            if len(selected_items) < 1:
                selected_items = [active_file_window.list.currentItem()]
            for item in selected_items:
                source_path = os.path.join(active_file_window.path, item.text().strip('[]'))
                target_path = os.path.join(target_file_window.path, item.text().strip('[]'))
                if os.path.isdir(source_path):
                    if source_path != target_path:
                        #target_path = target_file_window.path
                        print(source_path)
                        print(target_path)
                        conflicts = functions.compare_2_directories(source_path + "\\", target_path)
                        print(conflicts)
                        self.copy(source_path, target_path, conflicts)
                        shutil.rmtree(source_path)
                        #os.rmdir(source_path)
                    else:
                        files_and_folders = os.listdir(target_file_window.path)
                        while True:
                            new_location = self.move_input(item.text())
                            print(new_location)
                            if new_location is not None:
                                contains_illegal_chars = any(char in new_location for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
                            else:
                                break
                            if new_location is not None and contains_illegal_chars is False and len(new_location) > 0 and new_location[-1] != ' ' and new_location[0] != ' ' and new_location not in files_and_folders:
                                new_path = os.path.join(target_file_window.path, new_location.strip('[]'))
                                if new_path != target_path:
                                    target_path = new_path
                                    conflicts = functions.compare_2_directories(source_path + "\\", target_path)
                                    self.copy(source_path, target_path, conflicts)
                                    shutil.rmtree(source_path)
                                break
                            else:
                                QMessageBox.information(self, "Absolute Director", "Name can't already exist or contain / \\ : * ? \" < > | and cannot start or end with a space")
                else:
                    print("isfile")
                    if source_path != target_path:
                        data_in_target = os.listdir(target_file_window.path)
                        print(data_in_target)
                        if item.text() in data_in_target:
                            print(data_in_target)
                            overwrite = self.ask_user_choice(item.text())
                            if overwrite:
                                shutil.copy2(source_path, target_path)
                                os.remove(source_path)

                        else:
                            shutil.copy2(source_path, target_path)
                            os.remove(source_path)
                    else:
                        files_and_folders = os.listdir(target_file_window.path)
                        while True:
                            new_location = self.move_input(item.text())
                            print(type(new_location))
                            print(new_location is None)
                            if new_location is not None:
                                contains_illegal_chars = any(char in new_location for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
                            else:
                                break
                            if new_location is not None and contains_illegal_chars is False and len(new_location) > 0 and new_location[-1] != ' ' and new_location[0] != ' ' and new_location not in files_and_folders:
                                new_path = os.path.join(target_file_window.path, new_location.strip('[]'))
                                if new_path != target_path:
                                    target_path = new_path
                                    shutil.copy2(source_path, target_path)
                                    os.remove(source_path)
                                break
                            else:
                                QMessageBox.information(self, "Absolute Director", "Name can't already exist or contain / \\ : * ? \" < > | and cannot start or end with a space")
            target_file_window.display_directory_contents(target_file_window.path)  # Refresh the target file window
            active_file_window.display_directory_contents(active_file_window.path)

    def copy_input(self, file):
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("Absolute Director")
        input_dialog.setLabelText(f"Copy {file} as:")
        input_dialog.setStyleSheet(
            "QLineEdit { background-color: white; color: black; }"
            "QLabel { color: white; font-weight: bold; }"
            "QPushButton {color: white;}"
        )
        input_dialog.resize(500, 125)
        ok = input_dialog.exec_()
        text = input_dialog.textValue()
        if ok and text:
            return text
    def move_input(self, file):
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("Absolute Director")
        input_dialog.setLabelText(f"Rename {file} to:")
        input_dialog.setStyleSheet(
            "QLineEdit { background-color: white; color: black; }"
            "QLabel { color: white; font-weight: bold; }"
            "QPushButton {color: white;}"
        )
        input_dialog.resize(500, 125)
        ok = input_dialog.exec_()
        text = input_dialog.textValue()
        if ok and text:
            return text
    def ask_user_choice(self, file):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("File Conflict")
        msg_box.setText(f"{file} exists in target location")
        overwrite_button = msg_box.addButton("Overwrite", QMessageBox.YesRole)
        skip_button = msg_box.addButton("Skip", QMessageBox.NoRole)
        skip_all_button = msg_box.addButton("Skip All", QMessageBox.RejectRole)
        msg_box.exec_()

        if msg_box.clickedButton() == overwrite_button:
            return True
        elif msg_box.clickedButton() == skip_button:
            return False
        elif msg_box.clickedButton() == skip_all_button:
            return None

    def copy(self, source_path, target_path, conflicts, skip_all_conflicts=False):
        if skip_all_conflicts:
            return

        data_in_source = os.listdir(source_path)
        for item in data_in_source:
            source_item_path = os.path.join(source_path, item)
            target_item_path = os.path.join(target_path, item)
            print(f"Source: {source_item_path}")
            print(target_item_path)
            # Ensure the target directory exists
            target_dir = os.path.dirname(target_item_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            if os.path.isdir(source_item_path):
                self.copy(source_item_path, target_item_path, conflicts, skip_all_conflicts)
            else:
                if source_item_path in conflicts:
                    if not skip_all_conflicts:
                        user_choice = self.ask_user_choice(source_item_path)
                        if user_choice is None:  # User chose to skip all future conflicts
                            skip_all_conflicts = True
                        elif user_choice:  # User chose to overwrite the file
                            shutil.copy2(source_item_path, target_item_path)
                        # If user_choice is False, it means skip this file, so do nothing
                    # If skip_all_conflicts is True, do nothing
                else:
                    shutil.copy2(source_item_path, target_item_path)  # Copy file
    def move_folder(self, source_path, target_path, conflicts, skip_all_conflicts=False):
        if skip_all_conflicts:
            return

        data_in_source = os.listdir(source_path)
        for item in data_in_source:
            source_item_path = os.path.join(source_path, item)
            target_item_path = os.path.join(target_path, item)
            # print(f"Source: {source_item_path}")
            # print(target_item_path)
            # Ensure the target directory exists
            target_dir = os.path.dirname(target_item_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            if os.path.isdir(source_item_path):
                print(source_item_path)
                self.copy(source_item_path, target_item_path, conflicts, skip_all_conflicts)
                # shutil.rmtree(source_item_path)
                # os.rmdir(source_item_path)
            else:
                if source_item_path in conflicts:
                    if not skip_all_conflicts:
                        user_choice = self.ask_user_choice(source_item_path)
                        if user_choice is None:  # User chose to skip all future conflicts
                            skip_all_conflicts = True
                        elif user_choice:  # User chose to overwrite the file
                            shutil.copy2(source_item_path, target_item_path)
                            os.remove(source_item_path)
                        # If user_choice is False, it means skip this file, so do nothing
                    # If skip_all_conflicts is True, do nothing
                else:
                    shutil.copy2(source_item_path, target_item_path)  # Copy file
                    os.remove(source_item_path)

    # def copy(self, source_path, target_path, conflicts):
    #     print(source_path)
    #     data_in_source = os.listdir(source_path)
    #     for item in data_in_source:
    #         if os.path.isdir(item):
    #             source_item_path = os.path.join(source_path, item)
    #             target_item_path = os.path.join(target_path, item)
    #             self.copy(source_item_path, target_item_path, conflicts)
    #         else:
    #             source_item_path = os.path.join(source_path, item)
    #             print(source_item_path)
    #             if source_item_path in conflicts:
    #                 ## display window here ##
    #                 pass
    #             else:
    #                 shutil.copy2(source_path + item, target_path)  # Copy file
    def on_item_double_clicked(self, item):
        print("Item double-clicked:", item.text())
        self.enter_pressed()

class FileWindow(QWidget):
    tabPressed = pyqtSignal()
    def __init__(self, x, width, height, config, main_window):
        super().__init__()
        self.x = x
        self.main_window = main_window
        self.list = QListWidget(main_window)
        self.list.setGeometry(x, 75, width // 2, height - 100)
        self.list.setSelectionMode(QListWidget.MultiSelection)
        self.list.itemDoubleClicked.connect(main_window.on_item_double_clicked)
        # self.tabPressed = pyqtSignal()
        # self.tabPressed.connect(self.on_tab_pressed)
        self.list.setStyleSheet(
            "QListWidget {"
            f"color: {config['font_color']};"
            f"font-size: {int(config['font_size'])}px;"
            f"font-family: {config['font_family']};"
            "}"
            "QListWidget::item:selected {"
            f"background-color: {config['background_color']};"
            f"color: {config['selected_color']};"
            "}"
            "QListWidget::item:hover {"
            f"background-color: {config['hover_color']};"
            "}"
            "QScrollBar:vertical {"
            f"background: {config['selected_color']};"
            "border-radius: 15px;"  # Rounded corners
            "width: 10px;"  # Adjust width as needed
            "}"
            "QScrollBar::handle:vertical {"
            "background: " + config['selected_color'] + ";"  # Define handle_color in your config
            "min-height: 20px;"  # Adjust size as needed
            "}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {"
            "display: none;"  # Hides the buttons
            "}"
            "QScrollBar:horizontal { width: 0px; }"
        )
        self.list.update()

        self.path = main_window.default_path

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.tabPressed.emit()  # Emit the signal when Tab is pressed
            event.accept()
        else:
            super().keyPressEvent(event)
    def resize(self):
        width = self.main_window.frameSize().width()
        height = self.main_window.frameSize().height()
        if self.x != 0:
            self.x = width // 2
        self.list.setGeometry(self.x, 75, width // 2, height - 100)
    def display_directory_contents(self, path):
        try:
            self.path = path
            self.list.clear()  # Clear existing entries
            files_and_folders = os.listdir(path)
            folders = []
            files = []
            for item in files_and_folders:
                if os.path.isdir(path + item):
                    folders.append(item)
                else:
                    files.append(item)
            folders.sort()
            files.sort()
            folder_icon = QIcon("img\\folder.png")
            for item in folders:
                list_item = QListWidgetItem(folder_icon, "[" + item + "]")
                self.list.addItem(list_item)
            for item in files:
                file_icon = QIcon("img\\file.png")
                parts = item.split('.')
                if parts[-1] in supported_file_extensions:
                    file_icon = QIcon(f"img\\{parts[-1]}.png")
                list_item = QListWidgetItem(file_icon, item)
                self.list.addItem(list_item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read directory contents: {str(e)}")

    # def display_directory_contents(self, path):
    #     try:
    #         self.path = path
    #         self.list.clear()  # Clear existing entries
    #         files_and_folders = os.listdir(path)
    #         folders = []
    #         files = []
    #         for item in files_and_folders:
    #             item_path = os.path.join(path, item)
    #             if os.path.isdir(item_path):
    #                 total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
    #                                  for dirpath, dirnames, filenames in os.walk(item_path)
    #                                  for filename in filenames)
    #                 folders.append((item, total_size))
    #             else:
    #                 file_size = os.path.getsize(item_path)
    #                 files.append((item, file_size))
    #         folders.sort()
    #         files.sort()
    #         folder_icon = QIcon("img\\folder.png")
    #         for item, size in folders:
    #             size_str = self.format_size(size)
    #             list_item = QListWidgetItem(folder_icon, f"[{item}] ({size_str})")
    #             self.list.addItem(list_item)
    #         for item, size in files:
    #             file_icon = QIcon("img\\file.png")
    #             parts = item.split('.')
    #             if parts[-1] in supported_file_extensions:
    #                 file_icon = QIcon(f"img\\{parts[-1]}.png")
    #             size_str = self.format_size(size)
    #             list_item = QListWidgetItem(file_icon, f"{item} ({size_str})")
    #             self.list.addItem(list_item)
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to read directory contents: {str(e)}")
    #
    # def format_size(self, size):
    #     # Helper function to convert size to a more readable format
    #     for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
    #         if size < 1024.0:
    #             return f"{size:.2f} {unit}"
    #         size /= 1024.0
    #     return f"{size:.2f} YB"

def load_config():
    config = configparser.ConfigParser()
    config.read('theme.ini')
    theme_settings = config['Theme']
    return theme_settings

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    config = load_config()
    window = MainWindow(config, 2100, 1600)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()