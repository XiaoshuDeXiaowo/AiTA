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

## 使用说明

<p align="center" style="font-size: 12px">这段文本会告诉你如何自己配置此项目。</p>

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