"""Searchable, bounded language palette matching Voxcalibur's amber UI."""
import unicodedata
from PySide6.QtCore import Qt, QPoint, QRectF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem
from app.ui.key_picker import TriggerChoiceBox


def folded(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.casefold()) if not unicodedata.combining(c))


class LanguagePopup(QFrame):
    def __init__(self, owner):
        super().__init__(owner, Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.owner = owner
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(300)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(9)
        heading = QLabel("Langue de dictée")
        heading.setStyleSheet("background:transparent;border:0;color:#ffe3c4;font:600 11pt 'Segoe UI';")
        layout.addWidget(heading)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Rechercher une langue…")
        self.search.setAccessibleName("Rechercher une langue")
        self.search.setStyleSheet("QLineEdit{background:#21160f;color:#fff1e5;border:1px solid #765035;border-radius:9px;padding:9px;font:10pt 'Segoe UI';} QLineEdit:focus{border-color:#e5ad6b;}")
        layout.addWidget(self.search)
        self.list = QListWidget()
        self.list.setAccessibleName("Langues disponibles")
        self.list.setFixedHeight(260)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.setStyleSheet("QListWidget{background:transparent;color:#fff1e5;border:0;outline:0;font:10pt 'Segoe UI';} QListWidget::item{padding:8px 10px;border-radius:7px;margin:1px 0;} QListWidget::item:hover{background:#54331b;} QListWidget::item:selected{background:#57381f;color:#ffe3c4;font-weight:600;} QScrollBar:vertical{background:#15110e;width:6px;border:0;} QScrollBar::handle:vertical{background:#89603b;border-radius:3px;min-height:28px;} QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}")
        layout.addWidget(self.list)
        self.search.textChanged.connect(self.filter)
        self.search.returnPressed.connect(self.confirm)
        self.list.itemClicked.connect(self.choose)
        self.list.itemActivated.connect(self.choose)
        self.search.installEventFilter(self)
        self.list.installEventFilter(self)

    def filter(self, text):
        self.list.clear()
        for i in range(self.owner.count()):
            name = self.owner.itemText(i)
            if folded(text) in folded(name):
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, i)
                self.list.addItem(item)
                if i == self.owner.currentIndex():
                    self.list.setCurrentItem(item)
        if not self.list.currentItem() and self.list.count():
            self.list.setCurrentRow(0)

    def confirm(self):
        if self.list.currentItem():
            self.choose(self.list.currentItem())

    def choose(self, item):
        self.owner.setCurrentIndex(item.data(Qt.UserRole))
        self.owner.hidePopup()
        self.owner.setFocus(Qt.PopupFocusReason)

    def eventFilter(self, obj, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.owner.hidePopup()
                self.owner.setFocus(Qt.PopupFocusReason)
                return True
            if obj is self.search and event.key() in (Qt.Key_Down, Qt.Key_Up):
                delta = 1 if event.key() == Qt.Key_Down else -1
                self.list.setCurrentRow(max(0, min(self.list.count()-1, self.list.currentRow()+delta)))
                return True
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#21160f"))
        painter.setPen(QPen(QColor("#a77b4e"), 1))
        painter.drawRoundedRect(QRectF(self.rect()).adjusted(1,1,-1,-1), 14,14)


class LanguageChoiceBox(TriggerChoiceBox):
    def showPopup(self):
        if not self.count() or not self.isEnabled():
            return
        if self.popup is None:
            self.popup = LanguagePopup(self)
        self.popup.search.clear()
        self.popup.filter("")
        self.popup.adjustSize()
        area = self.screen().availableGeometry()
        origin = self.mapToGlobal(QPoint(0, self.height()+6))
        y = origin.y()
        if y + self.popup.height() > area.bottom()-4:
            y = self.mapToGlobal(QPoint(0, -self.popup.height()-6)).y()
        self.popup.move(max(area.left()+4,min(origin.x(),area.right()-self.popup.width()-4)), max(area.top()+4,y))
        self.popup.show()
        self.popup.search.setFocus(Qt.PopupFocusReason)
