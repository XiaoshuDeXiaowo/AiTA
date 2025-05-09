import sys
from markdown_it import MarkdownIt
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import isDarkTheme
from .text_browser import TextBrowser

# 导入插件
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.wordcount import wordcount_plugin


class MarkdownViewer(TextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 100)
        self.initial_width = 800

        # 禁止用户编辑
        self.setReadOnly(True)
        self.setUndoRedoEnabled(False)

        # 初始化 Markdown 渲染器
        self.md = MarkdownIt()
        self.md.enable(['table', 'code', 'hr', 'image', 'autolink'])

        # 启用插件
        self.md.use(footnote_plugin)
        self.md.use(front_matter_plugin)
        self.md.use(tasklists_plugin)
        self.md.use(wordcount_plugin)

        # 关闭滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setMarkdown(self, text):
        """渲染 Markdown 内容"""
        # Step 1: 转换为 HTML
        html_content = self.md.render(text)

        # Step 2: 构建完整 HTML 结构
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
            {html_content}
        </body>
        </html>
        """

        self.setHtml(full_html)


# ================== 使用示例 ==================
if __name__ == "__main__":

    # 导入窗口库
    from qframelesswindow import *

    app = QApplication(sys.argv)

    window = FramelessWindow()
    window.resize(800, 600)

    viewer = MarkdownViewer()
    viewer.setMarkdown("""
以下是将Markdown代码块转换为实际渲染效果的示例：

---

### 一、基础语法
1. **标题**
# H1
## H2
### H3
#### H4
##### H5
###### H6

2. **文字样式**  
*斜体* 或 _斜体_  
**粗体** 或 __粗体__  
***粗斜体*** 或 ___粗斜体___  
~~删除线~~  
行内`代码`用反引号  

3. **列表**
   - **无序列表**：
     - Item 1
     * Item 2
     + Item 3
   - **有序列表**：
     1. First
     2. Second

4. **引用**
> 引用内容  
> 多行引用

5. **链接与图片**  
[点击访问示例网站](https://example.com)  
![图片占位符（需替换实际图片链接）](https://via.placeholder.com/150)

6. **代码块**
```python
print("Hello, World!")
```

7. **分隔线**
---
***
___

---

### 二、扩展语法
1. **表格**
| 左对齐 | 居中 | 右对齐 |
|:-------|:----:|-------:|
| 单元格 | 内容 |   100  |

2. **任务列表**
- [ ] 未完成任务  
- [x] 已完成任务  

3. **脚注**  
这是一个脚注示例[^1]  
[^1]: 脚注内容显示在此处。

4. **自动链接**  
<https://example.com>

5. **转义字符**  
\* 转义星号  
\# 转义井号  

---

### 三、高级功能
1. **HTML嵌入**  
<span style="color:red">红色文字（需解析器支持）</span>

2. **数学公式**  
行内公式：$E=mc^2$  

块级公式：  
$$
\\sum_{i=1}^n i = \\frac{n(n+1)}{2}
$$

3. **流程图/Mermaid**  
（需安装Mermaid插件支持）
```mermaid
graph TD;
  A-->B;
  A-->C;
```

---

### 注意事项
- **兼容性**：部分功能（如数学公式、Mermaid）需特定工具支持（如Typora、GitHub）。  
- **实际效果**：不同平台对Markdown的渲染可能略有差异。  

如果需要特定功能的详细说明，欢迎进一步提问！ ✨
""")


    layout = QVBoxLayout(window)
    layout.addWidget(viewer)
    layout.setContentsMargins(0, 32, 0, 0)
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())
