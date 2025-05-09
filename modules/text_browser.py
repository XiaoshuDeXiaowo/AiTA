'''一个可以根据文本长度自动调整大小的 TextBrowser'''

# -- 以下内容来自 DeepSeek，并稍作修改 -- #

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QSizePolicy, QPlainTextEdit, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QTextOption
from qfluentwidgets import TextBrowser, isDarkTheme, PlainTextEdit
from qfluentwidgets.components.widgets.menu import TextEditMenu, LineEditMenu

class TextBrowser(TextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 允许访问链接
        self.setOpenLinks(True)
        self.setOpenExternalLinks(True)

        # 禁用滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 自动调整大小
        self.textChanged.connect(self.auto_resize)

    def auto_resize(self):
        # 计算理想宽度和高度
        doc = self.document()
        doc.adjustSize()  # 确保文档尺寸已更新

        ideal_width = doc.idealWidth()  # 获取理想宽度（无换行时的宽度）
        height = doc.size().height()    # 获取实际渲染高度

        # 考虑边距（可选）
        margin = self.contentsMargins()
        new_width = ideal_width + margin.left() + margin.right()
        new_height = height + margin.top() + margin.bottom()

        # 增加宽度，避免文字横向显示不全
        new_width += 50

        # 设置控件尺寸
        self.setFixedSize(int(new_width), int(new_height))

    def sizeHint(self):
        # 返回计算后的推荐尺寸
        return self.minimumSizeHint()

class QueLabel(QLineEdit):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        # 设置样式
        self.setStyleSheet(f'''
            QLineEdit{{
                font-size: 16px;
                line-height: 28px;
                color: {"#f8faff" if isDarkTheme() else "#262626"};
                padding: 8px 20px;
                white-space: pre-wrap;
                background-color: {"#414158" if isDarkTheme() else "#eff6ff"};
                border-radius: 14px;
                position: relative;
                border: none;
                font: 14px "Segoe UI", "Microsoft YaHei", "PingFang SC";
            }}
        ''')

        # 禁止用户修改
        self.setReadOnly(True)
        # 启用拖拽
        self.setDragEnabled(True)

        self.default_width = self.width()  # 保存初始宽度
        self.textChanged.connect(self.adjust_width)

    def adjust_width(self):
        text = self.text()
        fm = self.fontMetrics()
        # 计算文本宽度，添加10像素边距（可根据需要调整）
        text_width = fm.horizontalAdvance(text) + 50
        # 设置固定宽度，避免文本为空时过小
        # new_width = text_width if text else self.default_width                # 禁用，因为 self.default_width 的值太大了(640)
        new_width = text_width
        # self.setFixedWidth(max(new_width, self.default_width))                # 禁用，因为 self.default_width 的值太大了(640)
        self.setFixedWidth(new_width)

    def contextMenuEvent(self, e):
        menu = LineEditMenu(self)
        menu.exec_(e.globalPos())

class TextEdit(PlainTextEdit):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter) and event.modifiers() & Qt.ShiftModifier:
            # 阻止事件继续传播
            event.accept()
            self.insertPlainText('\n')
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # 阻止事件继续传播
            event.accept()
            if self.toPlainText().strip():
                self.window().Send.click()
        else:
            # 其他按键保持默认行为
            super().keyPressEvent(event)

if __name__ == '__main__':
    # 示例用法
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)

    text_browser = TextBrowser()
    text_browser.setPlainText("这是一段需要自适应大小的文本。当文本较长时，控件会自动调整宽度和高度。")

    layout.addWidget(text_browser)
    window.show()
    app.exec_()
