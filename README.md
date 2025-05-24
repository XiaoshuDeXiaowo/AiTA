<p align="center">
  <img width="30%" align="center" src="resource/img/icon_black.png" alt="logo">
</p>
<h1 align="center">人工智能旅行社客服</h1>
<p align="center">一款基于DeepSeek大模型的人工智能旅行社客服系统软件</p>
<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.11.9-blue.svg?color=00B16A" alt="Python 3.11.9"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PyQt-5.15.9-blue?color=00B16A" alt="PyQt 5.15.9"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win64%20|%20macOS%20|%20Linux-blue?color=00B16A" alt="Platform Win64 | macOS | Linux"/>
  </a>
</p>

## 源代码使用说明

1. 下载[此项目的源代码](https://github.com/XiaoshuDeXiaowo/AiTA/archive/refs/tags/v0.1_Snapshot.zip)；

2. 解压缩这个下载下来的压缩包；

3. 进入解压缩的文件夹，运行：

  ```bash
  pip3 install -r requirements.txt
  ```

4. 使用文本编辑器打开 `main.py` ，然后将第 47 行修改成：

  ```python
  client = OpenAI(api_key="< 你的 DeepSeek API Key >", base_url="https://api.deepseek.com")
  ```

5. 保存，然后就可以运行啦！

## 任务列表

### 与 AI 对话

- [x] 实现与 DeepSeek-V3 的基本交流
- [ ] 实现与 DeepSeek-R1 的基本交流
- [ ] 实现[流式输出](https://api-docs.deepseek.com/zh-cn/faq#%E4%B8%BA%E4%BB%80%E4%B9%88%E6%88%91%E6%84%9F%E8%A7%89-api-%E8%BF%94%E5%9B%9E%E6%AF%94%E7%BD%91%E9%A1%B5%E7%AB%AF%E6%85%A2)

### 窗口

- [x] 实现 Fluent Design
- [x] 实现系统菜单
- [x] 实现按下 `Enter` 键发送、`Shift` + `Enter` 换行
- [ ] 实现设置界面
- [ ] 实现 可选的 亚克力材质窗口（透明效果）
- [ ] 实现国际化
- [ ] 按下 `Alt` + `空格` 时系统菜单在正确的位置显示
- [ ] 修复点击系统菜单中的 “移动(M)” 项时鼠标指针位置错误的问题
- [ ] 聊天记录中自己的话可以渲染换行
- [ ] 聊天记录中自己的话不会被遮挡（宽度能够正常计算）
- [ ] 系统菜单在高分屏下能显示在正确的位置

### 应用程序

- [x] 使用  `PyInstaller` 打包
- [x] 在 Windows 上打包
- [ ] 在 macOS 上打包
- [ ] 在 Linux 上打包
- [ ] 添加版本信息 (exe)
- [ ] 使用 `Nuitka` 编译
- [ ] 优化启动速度

## 许可证

GPL-3.0。请在将此程序二次发布时保留此许可证。
