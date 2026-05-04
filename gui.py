import sys
import random
import json
import winsound
import re
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import QSize
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QListWidgetItem
STYLE_SHEET = """
QWidget {
    background-color: #313338;
    color: #B5BAC1;
    font-family: 'Segoe UI', sans-serif;
}
QLabel {
    font-weight: bold;
    font-size: 12px;
}
QLabel#main_title {
    color: white;
    font-size: 28px;
    margin-bottom: 10px;
}
QLabel#captcha_label {
    color: #34E718;
    font-size: 18px;
    background-color: #1E1F22;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #34E718;
}
QLineEdit {
    background-color: #1E1F22;
    border: 1px solid #1E1F22;
    border-radius: 5px;
    padding: 10px;
    color: white;
}
QLineEdit:focus {
    border: 1px solid #5865F2;
}
QComboBox {
    background-color: #1E1F22;
    border-radius: 5px;
    padding: 8px;
    color: white;
}
QPushButton {
    background-color: #5865F2;
    color: white;
    border-radius: 6px;
    padding: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #4752C4;
}
QPushButton#link_btn {
    background-color: transparent;
    color: #00A8FC;
    text-align: left;
}
QTextEdit {
    background-color: #383A40;
    border: none;
    border-radius: 5px;
    padding: 10px;
    color: white;
    font-size: 14px;
}
QListWidget {
    background-color: #2B2D31;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 5px;
}
"""
class StartPage(QWidget):
    def __init__(self, go_login, go_register):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Eş Zamanlı Mesajlaşma")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_btn = QPushButton("Giriş Yap")
        login_btn.setFixedWidth(300)
        login_btn.clicked.connect(go_login)

        reg_btn = QPushButton("Bir Hesap Oluştur")
        reg_btn.setFixedWidth(300)
        reg_btn.setStyleSheet("background-color: #4E5058;")
        reg_btn.clicked.connect(go_register)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(reg_btn, alignment=Qt.AlignmentFlag.AlignCenter)

class RegisterPage(QWidget):
    def __init__(self, go_login, go_back, users, save_callback):
        super().__init__()
        self.go_login = go_login
        self.go_back = go_back
        self.users = users
        self.save_callback = save_callback
        self.captcha_result = 0
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(430)

        layout = QVBoxLayout(card)
        layout.setSpacing(12)

        title = QLabel("Bir hesap oluştur")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Kullanıcı adı")

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Şifre")
        self.passw.setEchoMode(QLineEdit.EchoMode.Password)

        dob_layout = QHBoxLayout()

        self.day = QComboBox()
        self.day.addItems([str(i) for i in range(1, 32)])

        self.month = QComboBox()
        self.month.addItems([
            "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
            "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
        ])

        self.year = QComboBox()
        self.year.addItems([str(i) for i in range(2024, 1950, -1)])

        dob_layout.addWidget(self.day)
        dob_layout.addWidget(self.month)
        dob_layout.addWidget(self.year)

        captcha_row = QHBoxLayout()

        self.captcha_text = QLabel()
        self.captcha_text.setObjectName("captcha_label")

        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("Cevap")
        self.captcha_input.setFixedWidth(100)

        captcha_row.addWidget(self.captcha_text)
        captcha_row.addWidget(self.captcha_input)

        reg_btn = QPushButton("Kayıt Ol")
        reg_btn.clicked.connect(self.register_action)

        back_link = QPushButton("← Geri Dön")
        back_link.setObjectName("link_btn")
        back_link.clicked.connect(self.go_back)

        layout.addWidget(title)
        layout.addWidget(QLabel("KULLANICI ADI *"))
        layout.addWidget(self.user)
        layout.addWidget(QLabel("ŞİFRE *"))
        layout.addWidget(self.passw)
        layout.addWidget(QLabel("DOĞUM TARİHİ *"))
        layout.addLayout(dob_layout)
        layout.addWidget(QLabel("MATEMATİKSEL CAPTCHA *"))
        layout.addLayout(captcha_row)
        layout.addWidget(reg_btn)
        layout.addWidget(back_link)

        main_layout.addWidget(card)
        self.generate_captcha()

    def generate_captcha(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        self.captcha_result = a + b
        self.captcha_text.setText(f"{a} + {b} = ?")

    def register_action(self):
        username = self.user.text().strip()
        password = self.passw.text().strip()
        answer = self.captcha_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
            return

        if username in self.users:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı zaten var.")
            return

        try:
            if int(answer) != self.captcha_result:
                QMessageBox.warning(self, "Hata", "CAPTCHA cevabı yanlış.")
                self.generate_captcha()
                self.captcha_input.clear()
                return
        except ValueError:
            QMessageBox.warning(self, "Hata", "CAPTCHA alanına sayı giriniz.")
            return

        self.users[username] = {
            "password": password,
            "friends": []
        }

        self.save_callback()
        QMessageBox.information(self, "Başarılı", "Hesap oluşturuldu. Giriş yapabilirsiniz.")
        self.go_login()

class LoginPage(QWidget):
    def __init__(self, open_chat, go_back, users):
        super().__init__()
        self.open_chat = open_chat
        self.go_back = go_back
        self.users = users
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(400)

        c_layout = QVBoxLayout(card)

        title = QLabel("Tekrar Hoş Geldin!")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Kullanıcı adı")

        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Şifre")
        self.pass_in.setEchoMode(QLineEdit.EchoMode.Password)

        btn = QPushButton("Giriş Yap")
        btn.clicked.connect(self.login_action)

        back = QPushButton("← Geri Dön")
        back.setObjectName("link_btn")
        back.clicked.connect(self.go_back)

        c_layout.addWidget(title)
        c_layout.addWidget(QLabel("KULLANICI ADI"))
        c_layout.addWidget(self.user_in)
        c_layout.addWidget(QLabel("ŞİFRE"))
        c_layout.addWidget(self.pass_in)
        c_layout.addWidget(btn)
        c_layout.addWidget(back)

        layout.addWidget(card)

    def login_action(self):
        username = self.user_in.text().strip()
        password = self.pass_in.text().strip()

        if username not in self.users:
            QMessageBox.warning(self, "Hata", "Böyle bir hesap bulunamadı.")
            return

        if self.users[username]["password"] != password:
            QMessageBox.warning(self, "Hata", "Şifre yanlış.")
            return

        self.open_chat(username)

class ChatPage(QWidget):
    def __init__(self, go_back, users, save_callback):
        super().__init__()
        self.go_back = go_back
        self.username = ""
        self.current_room = "genel"
        self.reply_to = None
        self.last_seen = {}
        self.chat_histories = {}
        self.unread_counts = {}
        self.all_app_users = users
        self.save_callback = save_callback
        self.init_ui()


    def init_ui(self):
        main = QHBoxLayout(self)

        self.rooms = QListWidget()
        self.rooms.addItems([
            "🌐 # genel",
            "📚 # ders",
            "💻 # proje",
            "🆘 # yardım"
        ])
        self.rooms.setFixedWidth(180)
        self.rooms.currentTextChanged.connect(self.change_room)

        center = QVBoxLayout()

        self.room_title = QLabel("# genel")
        self.room_title.setObjectName("main_title")
        self.header_avatar = QLabel()
        self.header_avatar.setFixedSize(28, 28)
        self.header_avatar.setPixmap(QPixmap("user.png").scaled(28, 28))
        self.header_avatar.setVisible(False)

        self.header_name = QLabel("# genel")
        self.header_name.setObjectName("main_title")

        self.header_widget = QWidget()
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        header_layout.addWidget(self.header_avatar)
        header_layout.addWidget(self.header_name)
        header_layout.addStretch()
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            color: #B5BAC1;
            font-size: 12px;
            margin-left: 5px;
        """)
        self.latency_label = QLabel("🟢 -- ms")
        self.latency_label.setStyleSheet("""
            color: #B5BAC1;
            font-size: 12px;
            margin-left: 5px;
        """)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.chat.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.chat.customContextMenuRequested.connect(self.show_message_menu)

        self.typing_label = QLabel("")
        self.typing_label.setStyleSheet("color: #B5BAC1; font-style: italic;")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Mesaj yaz...")
        self.input.returnPressed.connect(self.send)
        self.input.textChanged.connect(self.typing_packet)

        send = QPushButton("Gönder")
        send.setFixedWidth(90)
        send.clicked.connect(self.send)
        self.reply_container = QWidget()
        self.reply_container.setVisible(False)

        reply_layout = QHBoxLayout(self.reply_container)
        reply_layout.setContentsMargins(8, 4, 8, 4)

        self.reply_label = QLabel()
        self.reply_label.setStyleSheet("""
            color: white;
            font-size: 12px;
        """)

        self.cancel_reply_btn = QPushButton("✕")
        self.cancel_reply_btn.setFixedSize(24, 24)
        self.cancel_reply_btn.setStyleSheet("""
            background-color: transparent;
            color: white;
            border: none;
            font-size: 14px;
        """)
        self.cancel_reply_btn.clicked.connect(self.cancel_reply)

        reply_layout.addWidget(self.reply_label)
        reply_layout.addStretch()
        reply_layout.addWidget(self.cancel_reply_btn)

        self.reply_container.setStyleSheet("""
            background-color: #202c33;
            border-left: 4px solid #25D366;
            border-radius: 8px;
        """)
        self.spam_warning_label = QLabel("")
        self.spam_warning_label.setVisible(False)
        self.spam_warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spam_warning_label.setStyleSheet("""
            background-color: #3A1F24;
            color: #FF6B6B;
            padding: 7px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
        """)
        row = QHBoxLayout()
        row.addWidget(self.input)
        row.addWidget(send)

        center.addWidget(self.header_widget)
        center.addWidget(self.status_label)
        center.addWidget(self.latency_label)
        center.addWidget(self.chat)
        center.addWidget(self.typing_label)
        center.addWidget(self.reply_container)
        center.addWidget(self.spam_warning_label)
        center.addLayout(row)

        right = QVBoxLayout()

        title = QLabel("Kullanıcılar")

        self.users_list_widget = QListWidget()
        self.users_list_widget.setIconSize(QSize(40, 40))
        self.users_list_widget.itemClicked.connect(self.open_private_chat)
        self.users_list_widget.setFixedWidth(170)
        self.users_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.users_list_widget.customContextMenuRequested.connect(self.show_user_menu)

        add_friend_btn = QPushButton("+ Kişi Ekle")
        add_friend_btn.setStyleSheet("background-color: #248046; color: white;")
        add_friend_btn.clicked.connect(self.add_person_by_name)
        summary_btn = QPushButton("📊 Özet")
        summary_btn.clicked.connect(self.request_summary)

        exit_btn = QPushButton("Çıkış")
        exit_btn.setStyleSheet("background-color: #DA373C; color: white;")
        exit_btn.clicked.connect(self.logout)

        right.addWidget(title)
        right.addWidget(self.users_list_widget)
        right.addWidget(add_friend_btn)
        right.addWidget(summary_btn)
        right.addStretch()
        right.addWidget(exit_btn)

        main.addWidget(self.rooms)
        main.addLayout(center)
        main.addLayout(right)

    def change_room(self, room_name):
        if room_name:
            self.save_current_chat()

            clean_room = room_name.split("#")[-1].strip()

            self.current_room = clean_room
            self.header_avatar.setVisible(False)
            self.header_name.setText(room_name)
            self.status_label.setText("Grup sohbeti")
            self.load_chat(self.current_room)

            packet = {
                "type": "change_room",
                "user": self.username,
                "room": self.current_room
            }

            print("ROOM PACKET:", packet)

    def save_current_chat(self):
        self.chat_histories[self.current_room] = self.chat.toHtml()

    def load_chat(self, chat_key):
        self.chat.clear()
        if chat_key in self.chat_histories:
            self.chat.setHtml(self.chat_histories[chat_key])

    def open_private_chat(self, item):
        text = item.text()

        self.save_current_chat()

        if "(Sen)" in text:
            target = self.username
            self.current_room = "private:self"
            self.header_avatar.setVisible(True)
            self.header_avatar.setPixmap(QPixmap("user.png").scaled(28, 28))
            self.header_name.setText(f"{self.username} (Kendime)")
            self.status_label.setText("")
        else:

            target = text.split("(")[0].replace("○", "").replace("●", "").strip()


            if target in self.unread_counts:
                self.unread_counts[target] = 0
                self.update_users_list()

            self.current_room = f"private:{target}"
            self.header_avatar.setVisible(True)
            self.header_avatar.setPixmap(QPixmap("user.png").scaled(28, 28))
            self.header_name.setText(target)

            if target in self.last_seen:
                self.status_label.setText(f"son görülme: {self.last_seen[target]}")
            else:
                self.status_label.setText("çevrimiçi")

        self.load_chat(self.current_room)

        packet = {
            "type": "open_private_chat",
            "from": self.username,
            "to": target
        }

        print("PRIVATE CHAT PACKET:", packet)

    def update_users_list(self):
        self.users_list_widget.clear()

        if not self.username:
            return


        self.users_list_widget.setIconSize(QSize(28, 28))


        item = QListWidgetItem(f"{self.username} (Sen)")
        item.setIcon(QIcon("user.png"))
        self.users_list_widget.addItem(item)


        friends = self.all_app_users[self.username].get("friends", [])

        for friend in friends:
            count = self.unread_counts.get(friend, 0)
            text = f"{friend} ({count})" if count > 0 else friend

            item = QListWidgetItem(text)
            item.setIcon(QIcon("user.png"))
            self.users_list_widget.addItem(item)

    def add_person_by_name(self):
        name, ok = QInputDialog.getText(
            self,
            "Kişi Ekle",
            "Eklemek istediğiniz kullanıcı adı:"
        )

        if not ok:
            return

        name = name.strip()

        if not name:
            QMessageBox.warning(self, "Hata", "Lütfen bir kullanıcı adı giriniz.")
            return

        if name == self.username:
            QMessageBox.warning(self, "Hata", "Kendinizi ekleyemezsiniz.")
            return

        if name not in self.all_app_users:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı sistemde kayıtlı değil.")
            return

        friends = self.all_app_users[self.username].setdefault("friends", [])

        if name in friends:
            QMessageBox.warning(self, "Hata", "Bu kişi zaten listenizde var.")
            return

        friends.append(name)
        self.save_callback()
        self.update_users_list()

        packet = {
            "type": "add_friend",
            "from": self.username,
            "friend": name
        }

        print("ADD FRIEND PACKET:", packet)

        QMessageBox.information(self, "Tamam", f"{name} listenize eklendi.")

    def request_summary(self):
        packet = {
            "type": "request_summary",
            "user": self.username,
            "room": self.current_room
        }

        print("SUMMARY REQUEST PACKET:", packet)


    def toggle_emoji(self, text, emoji):
        emojis = ["👍", "❤️", "😂"]

        same_clicked = emoji in text

        clean_text = text
        for e in emojis:
            clean_text = clean_text.replace(f" {e}", "")

        if same_clicked:
            return clean_text
        else:
            return clean_text + f" {emoji}"

    def handle_summary_packet(self, packet):
        if packet["type"] == "summary":
            self.show_summary_result(packet["text"])

    def send(self):
        msg = self.input.text().strip()

        if not msg:
            return

        packet = {
            "type": "private_message" if self.current_room.startswith("private:") else "room_message",
            "from": self.username,
            "room": self.current_room,
            "text": msg,
            "seen": False
        }

        print("MESSAGE PACKET:", packet)
        try:
            winsound.Beep(250, 150)
        except Exception as e:
            print("Send sound error:", e)

        if self.reply_to:
            display_msg = f"""
            <div style='border-left:3px solid #ccc; padding-left:6px; margin-bottom:4px; font-size:12px; color:#555;'>
                {self.reply_to}
            </div>
            <div>{msg}</div>
            """
        else:
            display_msg = msg

        from datetime import datetime
        time_now = datetime.now().strftime("%H:%M")

        self.chat.append(f"""
        <div align="right" style="margin:12px 8px;">
            <span style="
                background-color:#25D366;
                color:white;
                padding:8px 12px;
                border-radius:12px;
                display:inline-block;
            ">
                <b>{self.username}:</b> {display_msg}
                <span style="font-size:10px; margin-left:8px; color:#FFFFFF;">
                    {time_now} ✔✔
                </span>
            </span>
        </div>
        """)

        self.input.clear()
        self.typing_label.setText("")
        self.cancel_reply()

    def show_summary_result(self, summary_text):
        QMessageBox.information(self, "Sohbet Özeti", summary_text)
    def show_user_menu(self, position):
        item = self.users_list_widget.itemAt(position)

        if not item:
            return

        text = item.text()

        if "(Sen)" in text:
            return

        friend = text.replace("○", "").strip()
        chat_key = f"private:{friend}"

        menu = QMenu(self)

        delete_chat_action = QAction("🗑 Sohbeti Sil", self)
        delete_user_action = QAction("❌ Kişiyi Sil", self)

        menu.addAction(delete_chat_action)
        menu.addAction(delete_user_action)

        action = menu.exec(self.users_list_widget.mapToGlobal(position))

        if action == delete_chat_action:
            confirm = QMessageBox.question(
                self,
                "Onay",
                f"{friend} ile olan sohbet silinsin mi?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                if chat_key in self.chat_histories:
                    del self.chat_histories[chat_key]

                if self.current_room == chat_key:
                    self.chat.clear()

                packet = {
                    "type": "delete_chat_local",
                    "from": self.username,
                    "with": friend
                }

                print("DELETE CHAT LOCAL PACKET:", packet)

        elif action == delete_user_action:
            confirm = QMessageBox.question(
                self,
                "Onay",
                f"{friend} kişi listenizden silinsin mi?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                friends = self.all_app_users[self.username].get("friends", [])

                if friend in friends:
                    friends.remove(friend)
                    self.save_callback()
                    self.update_users_list()

                    packet = {
                        "type": "remove_friend",
                        "from": self.username,
                        "friend": friend
                    }

                    print("REMOVE FRIEND PACKET:", packet)
    def cancel_reply(self):
        self.reply_to = None
        self.reply_label.setText("")
        self.reply_container.setVisible(False)

    def handle_spam_packet(self, packet):
        if packet.get("type") == "spam_warning":
            word = packet.get("word", "")
            self.show_spam_warning(word)

    def show_spam_warning(self, word):
        self.spam_warning_label.setText(f"⚠ '{word}' kelimesi engellendi!")
        self.spam_warning_label.setVisible(True)

        try:
            winsound.Beep(800, 200)
            winsound.Beep(1100, 200)
            winsound.Beep(800, 200)
            winsound.Beep(1100, 200)
            winsound.Beep(800, 200)
            winsound.Beep(1100, 200)
        except Exception as e:
            print("Sound error:", e)
            QApplication.beep()
        QTimer.singleShot(2500, lambda: self.spam_warning_label.setVisible(False))

    def show_message_menu(self, position):
        cursor = self.chat.cursorForPosition(position)
        cursor.select(cursor.SelectionType.LineUnderCursor)

        selected_text = cursor.selectedText()

        if not selected_text.strip():
            return

        menu = QMenu(self)

        like_action = QAction("👍 Beğen", self)
        heart_action = QAction("❤️ Kalp", self)
        laugh_action = QAction("😂 Gül", self)

        reply_action = QAction("↩ Cevapla", self)
        share_action = QAction("↪ İlet / Paylaş", self)

        delete_me_action = QAction("🗑 Sadece benden sil", self)
        delete_all_action = QAction("❌ Herkesten sil", self)

        menu.addAction(like_action)
        menu.addAction(heart_action)
        menu.addAction(laugh_action)

        menu.addSeparator()

        menu.addAction(reply_action)
        menu.addAction(share_action)

        menu.addSeparator()

        menu.addAction(delete_me_action)
        menu.addAction(delete_all_action)

        action = menu.exec(self.chat.viewport().mapToGlobal(position))

        clean_text = selected_text


        clean_text = clean_text.replace("✔✔", "").replace("✔", "")


        clean_text = re.sub(r"\d{1,2}:\d{2}", "", clean_text)


        for emoji in ["👍", "❤️", "😂"]:
            clean_text = clean_text.replace(f" {emoji}", "")

        clean_text = clean_text.strip()

        if action == like_action:
            new_text = self.toggle_emoji(selected_text, "👍")
            cursor.insertText(new_text)

        elif action == heart_action:
            new_text = self.toggle_emoji(selected_text, "❤️")
            cursor.insertText(new_text)

        elif action == laugh_action:
            new_text = self.toggle_emoji(selected_text, "😂")
            cursor.insertText(new_text)

        elif action == reply_action:
            self.reply_to = clean_text

            sender = clean_text.split(":")[0] if ":" in clean_text else "Kullanıcı"
            message = clean_text.split(":", 1)[1].strip() if ":" in clean_text else clean_text

            self.reply_label.setText(f"<b>{sender}</b><br>{message}")
            self.reply_container.setVisible(True)
            self.input.setFocus()

        elif action == share_action:
            targets = ["# genel", "# proje", "# ders", "# yardım"]

            for user in self.all_app_users.keys():
                if user != self.username:
                    targets.append(user)

            target, ok = QInputDialog.getItem(
                self,
                "İlet / Paylaş",
                "Nereye iletmek istiyorsunuz?",
                targets,
                0,
                False
            )

            if ok and target:
                packet = {
                    "type": "forward_message",
                    "from": self.username,
                    "to": target,
                    "text": clean_text
                }

                print("FORWARD MESSAGE PACKET:", packet)

                QMessageBox.information(self, "Tamam", f"Mesaj {target} ile paylaşıldı.")

        elif action == delete_me_action:
            cursor.removeSelectedText()

        elif action == delete_all_action:
            packet = {
                "type": "delete_message",
                "from": self.username,
                "text": clean_text
            }

            print("DELETE FOR ALL PACKET:", packet)

            cursor.removeSelectedText()

    def receive_message(self, packet):
        sender = packet.get("from", "unknown")
        text = packet.get("text", "")
        room = packet.get("room", self.current_room)
        from datetime import datetime
        time_now = datetime.now().strftime("%H:%M")

        if sender != self.username:
            if self.current_room != f"private:{sender}":
                self.unread_counts[sender] = self.unread_counts.get(sender, 0) + 1
            else:
                self.unread_counts[sender] = 0

            self.update_users_list()

        self.chat.append(f"""
        <div align="left" style="margin:12px 8px;">
            <span style="
                background-color:#4E5058;
                color:white;
                padding:8px 12px;
                border-radius:12px;
                display:inline-block;
            ">
                <b>{sender}:</b> {text}
                <span style="font-size:10px; margin-left:8px; color:#d3d3d3;">
                {time_now}
                </span>
            </span>
        </div>
        """)

        seen_packet = {
            "type": "seen",
            "from": self.username,
            "to": sender,
            "room": room
        }

        print("SEEN PACKET:", seen_packet)

    def seen(self):
        html = self.chat.toHtml()
        html = html.replace("color:white;", "color:#00B0F4;")
        self.chat.setHtml(html)

    def typing_packet(self):
        if not self.username:
            return

        packet = {
            "type": "typing",
            "from": self.username,
            "room": self.current_room,
            "typing": bool(self.input.text().strip())
        }

        print("TYPING PACKET:", packet)

    def show_typing_status(self, username):
        if self.current_room.startswith("private:"):
            self.status_label.setText("yazıyor...")
        else:
            self.status_label.setText(f"{username} yazıyor...")

    def hide_typing_status(self):
        if self.current_room.startswith("private:"):
            self.status_label.setText("çevrimiçi")
        else:
            self.status_label.setText("Grup sohbeti")

    def set_online_status(self, username):
        self.status_label.setText("çevrimiçi")

    def set_offline_status(self, username):
        now = datetime.now().strftime("%H:%M")
        self.last_seen[username] = now
        self.status_label.setText(f"son görülme: {now}")

    def update_latency(self, ms):
        if ms < 50:
            color = "🟢"
        elif ms < 120:
            color = "🟡"
        else:
            color = "🔴"

        self.latency_label.setText(f"{color} {ms} ms")

    def handle_status_packet(self, packet):
        if packet["type"] == "typing":
            sender = packet["from"]
            room = packet.get("room", "")


            if room != self.current_room:
                return

            if packet["typing"]:
                self.show_typing_status(sender)
            else:
                self.hide_typing_status()

        elif packet["type"] == "status":
            if packet["online"]:
                self.set_online_status(packet["user"])
            else:
                self.set_offline_status(packet["user"])
        elif packet["type"] == "summary":
                self.show_summary_result(packet["text"])

    def logout(self):
        packet = {
            "type": "logout",
            "user": self.username
        }

        print("LOGOUT PACKET:", packet)

        self.input.clear()
        self.chat.clear()
        self.typing_label.setText("")
        self.go_back()

    def set_username(self, username):
        self.username = username
        self.update_users_list()

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.db_file = "users_data.json"
        self.users = self.load_users()

        self.setStyleSheet(STYLE_SHEET)

        self.start = StartPage(self.show_login, self.show_register)
        self.login = LoginPage(self.open_chat, self.show_start, self.users)
        self.register = RegisterPage(self.show_login, self.show_start, self.users, self.save_users)
        self.chat = ChatPage(self.show_start, self.users, self.save_users)

        self.addWidget(self.start)
        self.addWidget(self.login)
        self.addWidget(self.register)
        self.addWidget(self.chat)

        self.setCurrentWidget(self.start)
        self.resize(900, 600)

    def load_users(self):
        try:
            with open(self.db_file, "r", encoding="utf-8") as file:
                data = json.load(file)

                fixed_data = {}

                for username, value in data.items():
                    if isinstance(value, str):
                        fixed_data[username] = {
                            "password": value,
                            "friends": []
                        }
                    else:
                        fixed_data[username] = value

                return fixed_data

        except FileNotFoundError:
            return {
                "admin": {
                    "password": "123",
                    "friends": []
                }
            }

    def save_users(self):
        with open(self.db_file, "w", encoding="utf-8") as file:
            json.dump(self.users, file, ensure_ascii=False, indent=4)

    def show_start(self):
        self.setCurrentWidget(self.start)

    def show_login(self):
        self.setCurrentWidget(self.login)

    def show_register(self):
        self.setCurrentWidget(self.register)

    def open_chat(self, username):
        self.chat.set_username(username)
        self.setCurrentWidget(self.chat)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())