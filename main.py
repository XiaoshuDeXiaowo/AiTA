
__all__ = ['Main']

# -- 常量：开始 -- #
VERSION_CODE = 0
VERSION_NUMBER = 'v0.1'
VERSION_TYPE = 'Snapshot'
VERSION = f'{VERSION_NUMBER} {VERSION_TYPE}'
# -- 常量：结束 -- #

# -- 全局变量：开始 -- #
questions = []                      # type: List[Question]
answers = []                        # type: List[Answer]
all = []                            # type: List[QWidget]
hlays = []                          # type: List[QHBoxLayout]
# -- 全局变量：结束 -- #

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from qfluentwidgets import  *
from qfluentwidgets import PlainTextEdit as TextEdit
from qfluentwidgets.components.widgets.menu import *
from qfluentwidgets.components.material.acrylic_tool_tip import AcrylicToolTipFilter
from qfluentwidgets.components.material.acrylic_flyout import AcrylicFlyout
from qframelesswindow import *
from qframelesswindow.utils import getSystemAccentColor
from markdown_it import MarkdownIt
# 导入插件
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.wordcount import wordcount_plugin

from modules.frameless_window import FramelessWindow
from modules.title_bar import *
from modules.text_browser import *
from modules.markdown_viewer import MarkdownViewer
from resource import resource_rc

import qfluentwidgets

from openai import OpenAI
# 在下面填入你的 DeepSeek API Key
client = OpenAI(api_key="", base_url="https://api.deepseek.com")

# class Worker(QtCore.QObject):
#     finished = QtCore.pyqtSignal(str)
#
#     def __init__(self, messages):
#         super().__init__()
#         self.messages = messages
#
#     def run(self):
#         try:
#             user_message_history = []  # type: List[str]
#             assistant_message_history = []  # type: List[str]
#             for i in questions:
#                 user_message_history.append(i.text())
#             for i in answers:
#                 assistant_message_history.append(i.text())
#             messages = [{"role": "system",
#                          "content": "你是一个旅行社AI助手，帮助用户规划优化路线并估算旅行费用。"}]  # type: List[dict]
#             for i, j in zip(user_message_history, assistant_message_history):
#                 messages.extend([{"role": "user", "content": i}, {"role": "assistant", "content": j}])
#             # self.finished.emit('client.chat.completions.create(\n    model="deepseek-chat",\n    messages={messages},\n    stream=False\n)')
#             response = client.chat.completions.create(
#                 model="deepseek-chat",
#                 messages=self.messages,
#                 stream=False
#             )
#             self.finished.emit(response.choices[0].message.content)
#         except Exception as e:
#             self.finished.emit(f"请求失败: {str(e)}")

def sendToAi():
    user_message_history = []                        # type: List[str]
    assistant_message_history = []                  # type: List[str]
    for i in questions:
        user_message_history.append(i.text())
    for i in answers:
        assistant_message_history.append(i.text())
    messages = [{"role": "system", "content": "你是一个旅行社AI助手，帮助用户规划优化路线并估算旅行费用。"}] # type: List[dict]
    for i, j in zip(user_message_history, assistant_message_history):
        messages.extend([{"role": "user", "content": i},{"role": "assistant", "content": j}])
    # return f'client.chat.completions.create(\n    model="deepseek-chat",\n    messages={messages},\n    stream=False\n)'
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages[:-1],
        stream=False
    )
    return response.choices[0].message.content

class Question(QWidget):
    def __init__(self, parent, queText = ''):
        super().__init__(parent = parent)

        # 用于 QWidget 内的布局
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # 用户的提问
        self.que = QueLabel()
        self.que.setText(queText)
        self.layout.addWidget(self.que)

        # 外部调用的方法
        self.text = self.que.text
        self.setText = self.que.setText

        # 将此控件加入到问题列表
        global questions
        questions += [self]

        # 将此控件加入到对话列表
        global all
        all += [self]

class Answer(QWidget):
    def __init__(self, parent = None, respondText = ''):
        super().__init__(parent = parent)

        # 用于 QWidget 内的布局
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # AI 的头像
        self.head = PixmapLabel(self)
        self.head.setPixmap(QtGui.QPixmap(":/app/img/icon_white.png" if isDarkTheme() else ':/app/img/icon_black.png'))
        self.head.setFixedSize(30, 30)
        self.head.setObjectName("head")
        self.layout.addWidget(self.head, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # AI 的回复
        self.respond = MarkdownViewer(self)
        self.respond.setMarkdown(respondText)
        self.layout.addWidget(self.respond, 0, QtCore.Qt.AlignLeft)

        # 弹簧控件，防止 self.respond 偏移
        self.spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout.addSpacerItem(self.spacer)

        # 外部调用的方法
        self.setMarkdown = self.respond.setMarkdown
        self.toMarkdown = self.respond.toMarkdown
        self.text = self.toMarkdown

        # 将此控件加入到答案列表
        global answers
        answers += [self]

        # 将此控件加入到对话列表
        global all
        all += [self]

class Main(FramelessWindow):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.__initWindow()
        self.__initWidgets()

        # 启用高 dpi 支持
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        self.titleBar.raise_()

    def __initWindow(self):
        self.setTitleBar(FluentTitleBar(self))
        self.titleBar.setFixedHeight(32)
        self.titleBar.hBoxLayout.insertSpacing(0, 15)
        self.titleBar.hBoxLayout.insertSpacing(2, 2)

        # 设置窗口最小宽度
        self.setMinimumWidth(623)

        # 窗口背景自适应主题
        if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            color = QColor(25, 33, 42) if isDarkTheme(
            ) else QColor(240, 244, 249)
            self.setStyleSheet(f"Main{{background: {color.name()}}}")

        self.titleBar.titleLabel.setStyleSheet(f"""
            QLabel{{
                color: {"white" if isDarkTheme() else "black"};
                background: transparent;
                font: 13px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                padding: 0 4px;
            }}
        """)
        self.setWindowTitle('人工智能旅行社客服 %s' % VERSION)
        self.setWindowIcon(QIcon(':/app/img/icon_white.png' if isDarkTheme() else ':/app/img/icon_black'))
        setThemeColor(getSystemAccentColor())
        self.resize(990, 680)

    def __initWidgets(self):
        # -- 以下内容来自 PyUIC，并稍作修改 -- #
        self.laywidget = QtWidgets.QWidget(self)
        self.laywidget.setGeometry(QtCore.QRect(0, 0, 991, 681))
        self.laywidget.setObjectName("laywidget")

        # 主要的 Layout
        self.lay = QtWidgets.QVBoxLayout(self.laywidget)
        self.lay.setContentsMargins(20, 32, 20, 20)
        self.lay.setObjectName("lay")

        # 滚动区域，用于展示对话记录
        self.scroll = ScrollArea(self.laywidget)
        self.scroll.setStyleSheet("QScrollArea{background: transparent; border: none}")
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")

        # 用于放置滚动区域内控件的 QWidget
        self.scrollwidget = QtWidgets.QWidget()
        self.scrollwidget.setGeometry(QtCore.QRect(0, 0, 951, 429))
        self.scrollwidget.setStyleSheet("QWidget{background: transparent}")
        self.scrollwidget.setObjectName("scrollwidget")

        # 滚动区域内的 Layout
        self.scrlaywidget = QtWidgets.QWidget(self.scrollwidget)
        self.scrlaywidget.setGeometry(QtCore.QRect(0, 0, 951, 421))
        self.scrlaywidget.setObjectName("scrlaywidget")

        self.scrlay = QtWidgets.QVBoxLayout(self.scrlaywidget)
        self.scrlay.setContentsMargins(32, 0, 32, 0)
        self.scrlay.setObjectName("scrlay")

        # 测试用，发布时禁用
        # self.hlay1 = QtWidgets.QHBoxLayout()
        # self.hlay1.setObjectName("hlay1")
        #
        # self.quelabel1 = Question(self.scrlaywidget)
        # self.quelabel1.setText('Question Text......')
        # self.hlay1.addWidget(self.quelabel1, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #
        # self.scrlay.addLayout(self.hlay1)

        self.hlay2 = QtWidgets.QHBoxLayout()
        global hlays
        hlays += [self.hlay2]
        self.hlay2.setObjectName("hlay2")

        # 初始回复
        respond1text = ('你好！欢迎使用旅行规划助手~ 😊 我可以帮您：\n\n1. 规划国内外旅行路线\n2. 估算交通/住宿/景点费用\n3. 推荐特色美食'
        '和必玩项目\n4. 优化行程时间安排\n\n您有具体的旅行需求吗？比如：\n✨ 想去哪个城市/国家？\n📅 计划出行时间和天数？\n👨👩👧👦 同行人'
        '数和类型（家庭/情侣/个人等）？\n💵 大致的预算范围？\n\n告诉我更多细节，我会为您定制专属方案哦~ ✈️')
        self.respond1 = Answer(self.scrlaywidget, respond1text)
        self.hlay2.addWidget(self.respond1)

        # spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.hlay2.addItem(spacerItem)

        self.scrlay.addLayout(self.hlay2)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scrlay.addItem(spacerItem1)

        self.scroll.setWidget(self.scrollwidget)
        self.lay.addWidget(self.scroll)

        # 发送区域
        self.sendlay = QtWidgets.QHBoxLayout()
        self.sendlay.setObjectName("sendlay")

        # 切换主题按钮
        self.toggleTheme = qfluentwidgets.ToolButton(self.laywidget)
        self.toggleTheme.setObjectName("toggleTheme")
        self.toggleTheme.setToolTip("切换主题")                                 # 设置工具提示
        self.toggleTheme.setToolTipDuration(100000)                           # 设置显示工具提示几毫秒
        self.toggleTheme.installEventFilter(AcrylicToolTipFilter(self.toggleTheme, 100, ToolTipPosition.BOTTOM))
        self.toggleTheme.setIcon(qfluentwidgets.FluentIcon.CONSTRACT)
        self.sendlay.addWidget(self.toggleTheme, 0, QtCore.Qt.AlignBottom)

        # 输入框
        self.Input = TextEdit(self.laywidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Input.sizePolicy().hasHeightForWidth())
        self.Input.setSizePolicy(sizePolicy)
        self.Input.setObjectName("Input")
        self.sendlay.addWidget(self.Input)

        # 发送键
        self.Send = qfluentwidgets.PrimaryToolButton(self.laywidget)
        self.Send.setObjectName("Send")
        self.Send.setIcon(qfluentwidgets.FluentIcon.UP)
        self.Send.setToolTip("发送")                                    # 设置工具提示
        self.Send.setToolTipDuration(100000)                           # 设置显示工具提示几毫秒
        self.Send.installEventFilter(AcrylicToolTipFilter(self.Send, 100, ToolTipPosition.BOTTOM))
        self.sendlay.addWidget(self.Send, 0, QtCore.Qt.AlignBottom)

        self.lay.addLayout(self.sendlay)
        # -- 以上内容来自 PyUIC，并稍作修改 -- #

        # 绑定操作
        self.Send.clicked.connect(self.onSend)
        self.toggleTheme.clicked.connect(self.onToggleThemeClicked)

        # 初始化时记录滚动区域底部位置
        self.scroll.verticalScrollBar().rangeChanged.connect(
            lambda: self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            )
        )

        self.scrollwidget.setLayout(self.scrlay)
        self.setLayout(self.lay)

    def onSend(self):
        if self.Input.toPlainText().strip():                        # 如果用户输入了文本
            global hlays, questions, answers
            hlaynum = len(hlays)
            # 添加用户问题
            exec(f'self.hlay{hlaynum} = QHBoxLayout()')
            exec(f'hlays += [self.hlay{hlaynum}]')
            exec(f'self.quelabel{hlaynum} = Question(self.scrlaywidget, self.Input.toPlainText())')
            exec(f'questions += [self.quelabel{hlaynum}]')
            exec(f'self.hlay{hlaynum}.addWidget(self.quelabel{hlaynum}, 0, Qt.AlignRight|Qt.AlignVCenter)')
            exec(f'self.scrlay.insertLayout(len(questions), self.hlay{hlaynum})')  # 插入到所有问题之后
            exec(f'self.scrlay.addLayout(self.hlay{hlaynum})')
            # 添加 AI 回答
            hlaynum += 1
            exec(f'self.hlay{hlaynum} = QHBoxLayout()')
            exec(f'hlays += [self.hlay{hlaynum}]')
            exec(f'self.respond{hlaynum} = Answer(self.scrlaywidget, "正在思考……\\n\\n注意：此时窗口可能会未响应，这是正常现象，请不要关闭")')
            exec(f'answers += [self.respond{hlaynum}]')
            exec(f'self.hlay{hlaynum}.addWidget(self.respond{hlaynum})')
            exec(f'self.scrlay.insertLayout(len(questions) + len(answers), self.hlay{hlaynum})') # 插入到所有问题之后
            exec(f'self.scrlay.addLayout(self.hlay{hlaynum})')
            # 异步处理AI响应
            QtCore.QTimer.singleShot(100, self.processAiResponse)
            # 添加完消息后延迟滚动（100ms 确保布局更新）
            QtCore.QTimer.singleShot(100, self.autoScrollToBottom)
            # 清理消息框
            self.Input.clear()
        else:
            AcrylicFlyout.create(
                icon=InfoBarIcon.ERROR,
                title='错误',
                content="不能发送空白消息",
                target=self.Send,
                parent=self,
                isClosable=False,
                aniType=FlyoutAnimationType.PULL_UP
            )

    # def onSend(self):
    #     input_text = self.Input.toPlainText().strip()
    #     if not input_text:
    #         AcrylicFlyout.create(
    #             icon=InfoBarIcon.ERROR,
    #             title='错误',
    #             content="不能发送空白消息",
    #             target=self.Send,
    #             parent=self,
    #             isClosable=False,
    #             aniType=FlyoutAnimationType.PULL_UP
    #         )
    #         return
    #
    #     # 添加用户问题
    #     hlay = QHBoxLayout()
    #     question = Question(self.scrlaywidget, input_text)
    #     hlay.addWidget(question, 0, Qt.AlignRight | Qt.AlignVCenter)
    #     self.scrlay.addLayout(hlay)
    #     self.hlays.append(hlay)
    #     self.questions.append(question)
    #
    #     # 添加AI回答
    #     hlay = QHBoxLayout()
    #     answer = Answer(self.scrlaywidget, "正在思考......    ")
    #     hlay.addWidget(answer)
    #     self.scrlay.addLayout(hlay)
    #     hlays.append(hlay)
    #     answers.append(answer)
    #
    #     # 异步处理AI响应
    #     QtCore.QTimer.singleShot(100, self.processAiResponse)
    #
    #     # 添加完消息后延迟滚动（100ms 确保布局更新）
    #     QtCore.QTimer.singleShot(100, self.autoScrollToBottom)

    def processAiResponse(self):
        try:
            response = sendToAi()
            answers[-1].setMarkdown(response)
        except Exception as e:
            answers[-1].setMarkdown(f"请求失败: {str(e)}")

    def onToggleThemeClicked(self):
        # 切换主题
        toggleTheme()

        # 设置窗口背景色
        if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            color = QColor(25, 33, 42) if isDarkTheme() else QColor(240, 244, 249)
            self.setStyleSheet(f"Main{{background: {color.name()}}}")
        # 设置窗口标题颜色
        self.titleBar.titleLabel.setStyleSheet(f"""
            QLabel{{
                color: {"white" if isDarkTheme() else "black"};
                background: transparent;
                font: 13px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                padding: 0 4px;
            }}
        """)
        # 设置窗口图标
        self.setWindowIcon(QIcon(':/app/img/icon_white.png' if isDarkTheme() else ':/app/img/icon_black'))

        # 设置窗口标题栏额外图标
        self.titleBar.infoBtn.setIcon(FIF.INFO.path())

        # 设置用户消息样式
        for i in questions:
            i.que.setStyleSheet(f'''
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

        # 设置 AI 头像
        for i in answers:
            i.head.setPixmap(QtGui.QPixmap(":/app/img/icon_white.png" if isDarkTheme() else ':/app/img/icon_black.png'))
            i.head.setFixedSize(30, 30)

    def autoScrollToBottom(self):
        # 确保布局更新完成
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )
        # 或使用 QTimer 确保在布局更新后执行
        # QtCore.QTimer.singleShot(100, lambda:
        #     self.scroll.verticalScrollBar().setValue(
        #         self.scroll.verticalScrollBar().maximum()
        #     ))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    setTheme(Theme.AUTO)
    translator = FluentTranslator()
    app.installTranslator(translator)
    main = Main()
    main.show()
    sys.exit(app.exec_())
