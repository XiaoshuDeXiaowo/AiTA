
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QShortcut

from qframelesswindow.titlebar import *
from qfluentwidgets import BodyLabel, HyperlinkLabel, SubtitleLabel, TitleLabel, FluentIcon, PopupTeachingTip, TeachingTipTailPosition, ToolTipFilter, ToolTipPosition
from qfluentwidgets.components.material.acrylic_flyout import AcrylicFlyoutViewBase

# 用于标题栏的可以显示系统菜单的图标控件
class IconLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

    def mousePressEvent(self, e):
        if sys.platform == "win32" and e.button() == Qt.LeftButton:
            from ctypes import windll
            import win32con
            systemMenu = windll.user32.GetSystemMenu(int(self.window().winId()), False)
            if self.window()._isResizeEnabled:
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
                if self.window().isMaximized():
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_ENABLED)
                else:
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)
            else:
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)

            command = windll.user32.TrackPopupMenuEx(
                systemMenu,
                win32con.TPM_LEFTALIGN | win32con.TPM_RETURNCMD,
                self.window().x(),
                self.window().y() + self.parent().height(),
                int(self.window().winId()),
                None
            )
            if command:
                windll.user32.PostMessageW(int(self.window().winId()), 0x0112, command, 0)
        super().mousePressEvent(e)

class InfoBtnFlyout(AcrylicFlyoutViewBase):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setupUi()

    def setupUi(self):
        self.setFixedSize(511, 166)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 511, 166))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.lay = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.lay.setContentsMargins(20, 20, 20, 20)
        self.lay.setObjectName("lay")
        self.title = TitleLabel(self.verticalLayoutWidget)
        self.title.setObjectName("title")
        self.lay.addWidget(self.title, 0, QtCore.Qt.AlignHCenter)
        self.subtitle = SubtitleLabel(self.verticalLayoutWidget)
        self.subtitle.setObjectName("subtitle")
        self.lay.addWidget(self.subtitle, 0, QtCore.Qt.AlignHCenter)
        self.bl = BodyLabel(self.verticalLayoutWidget)
        self.bl.setObjectName("bl")
        self.lay.addWidget(self.bl)
        self.lay2 = QtWidgets.QHBoxLayout()
        self.lay2.setObjectName("lay2")
        self.bl2 = BodyLabel(self.verticalLayoutWidget)
        self.bl2.setObjectName("bl2")
        self.lay2.addWidget(self.bl2)
        self.link = HyperlinkLabel(self.verticalLayoutWidget)
        self.link.setUrl(QtCore.QUrl("https://github.com/XiaoshuDeXiaowo/AiTA"))
        self.link.setObjectName("link")
        self.lay2.addWidget(self.link)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lay2.addItem(spacerItem)
        self.lay.addLayout(self.lay2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lay.addItem(spacerItem1)
        self.title.setText("人工智能旅行社客服")
        self.subtitle.setText("基于 DeepSeek-V3 | 版本：v0.1 Snapshot")
        self.bl.setText("目前仍处于测试阶段，功能可能不太稳定，遇到问题请理性反馈，谢谢！")
        self.bl2.setText("仓库链接：")
        self.link.setText("https://github.com/XiaoshuDeXiaowo/AiTA")

    def paintEvent(self, e):
        pass

class TitleBarBase(TitleBarBase):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        self.infoBtn = SvgTitleBarButton(FluentIcon.INFO.path(), parent = self)
        self.infoBtn.setFixedSize(32, 32)
        self.infoBtn.clicked.connect(self.onInfoBtnClicked)
        self.infoBtn.setToolTip("关于")
        self.infoBtn.setToolTipDuration(100000)
        self.infoBtn.installEventFilter(ToolTipFilter(self.infoBtn, 100, ToolTipPosition.TOP))
        self.minBtn.setToolTip("最小化")
        self.minBtn.setToolTipDuration(100000)
        self.minBtn.installEventFilter(ToolTipFilter(self.minBtn, 100, ToolTipPosition.TOP))
        self.closeBtn.setToolTip("关闭")
        self.closeBtn.setToolTipDuration(100000)
        self.closeBtn.installEventFilter(ToolTipFilter(self.closeBtn, 100, ToolTipPosition.TOP))

        # 激活系统菜单
        self.sysMenuShortcut = QShortcut(QKeySequence("Alt+Space"), self)
        self.sysMenuShortcut.activated.connect(self.showSystemMenu)

    def showSystemMenu(self):
        if sys.platform == "win32":
            # 触发系统菜单
            from ctypes import windll
            import win32con
            systemMenu = windll.user32.GetSystemMenu(int(self.window().winId()), False)
            if self.window()._isResizeEnabled:
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
                if self.window().isMaximized():
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_ENABLED)
                else:
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)
            else:
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)

            command = windll.user32.TrackPopupMenuEx(
                systemMenu,
                win32con.TPM_LEFTALIGN | win32con.TPM_RETURNCMD,
                self.window().x(),
                self.window().y() + self.height(),
                int(self.window().winId()),
                None
            )
            if command:
                windll.user32.PostMessageW(int(self.window().winId()), 0x0112, command, 0)

    # 添加的内容
    def onInfoBtnClicked(self):
        PopupTeachingTip.make(
            target=self.infoBtn,
            view=InfoBtnFlyout(),
            tailPosition=TeachingTipTailPosition.TOP,
            duration=-1,
            parent=self.window()
        )

    def mouseReleaseEvent(self, e):
        if sys.platform == "win32" and e.button() == Qt.RightButton:
            from ctypes import windll
            import win32con
            systemMenu = windll.user32.GetSystemMenu(int(self.window().winId()), False)
            if self.window()._isResizeEnabled:
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
                if self.window().isMaximized():
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_ENABLED)
                else:
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
                    windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)
            else:
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
                windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)

            command = windll.user32.TrackPopupMenuEx(
                systemMenu,
                win32con.TPM_LEFTALIGN | win32con.TPM_RETURNCMD,
                e.globalX(),
                e.globalY(),
                int(self.window().winId()),
                None
            )
            if command:
                windll.user32.PostMessageW(int(self.window().winId()), 0x0112, command, 0)
        super().mouseReleaseEvent(e)

    # def keyPressEvent(self, event):
    #     if (event.key() == Qt.Key_Space and event.modifiers() & Qt.AltModifier) and sys.platform == "win32":
    #         # 阻止事件继续传播
    #         event.accept()
    #         # 触发系统菜单
    #         from ctypes import windll
    #         import win32con
    #         systemMenu = windll.user32.GetSystemMenu(int(self.window().winId()), False)
    #         if self.window()._isResizeEnabled:
    #             windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
    #             if self.window().isMaximized():
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_ENABLED)
    #             else:
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_ENABLED)
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_ENABLED)
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_ENABLED)
    #                 windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)
    #         else:
    #             windll.user32.EnableMenuItem(systemMenu, win32con.SC_MAXIMIZE, win32con.MF_GRAYED)
    #             windll.user32.EnableMenuItem(systemMenu, win32con.SC_MOVE, win32con.MF_GRAYED)
    #             windll.user32.EnableMenuItem(systemMenu, win32con.SC_SIZE, win32con.MF_GRAYED)
    #             windll.user32.EnableMenuItem(systemMenu, win32con.SC_RESTORE, win32con.MF_GRAYED)
    #
    #         command = windll.user32.TrackPopupMenuEx(
    #             systemMenu,
    #             win32con.TPM_LEFTALIGN | win32con.TPM_RETURNCMD,
    #             self.window().x(),
    #             self.window().y() + self.height(),
    #             int(self.window().winId()),
    #             None
    #         )
    #         if command:
    #             windll.user32.PostMessageW(int(self.window().winId()), 0x0112, command, 0)
    #     else:
    #         super().keyPressEvent(event)

class TitleBar(TitleBarBase):
    """ Title bar with minimize, maximum and close button """

    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)


class StandardTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = IconLabel(self)                                                       # 可以显示系统菜单
        self.iconLabel.setFixedSize(20, 20)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft)
        self.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                padding: 0 4px
            }
        """)                                                                                   # 为标题栏添加字体
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        """ set the title of title bar

        Parameters
        ----------
        title: str
            the title of title bar
        """
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        """ set the icon of title bar

        Parameters
        ----------
        icon: QIcon | QPixmap | str
            the icon of title bar
        """
        self.iconLabel.setPixmap(QIcon(icon).pixmap(20, 20))


# -- 以下内容来自 qfluentwidgets.window.fluent_window -- #
from qfluentwidgets import FluentStyleSheet

# -- ...... -- #

class FluentTitleBar(TitleBar):
    """ Fluent title bar"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = IconLabel(self)                                                        # 可以显示系统菜单
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertWidget(0, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(1, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.infoBtn)                                               # 添加的内容
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))
# -- 以上内容来自 qfluentwidgets.window.fluent_window -- #
