# 多媒体多语言处理工具套件

一个功能强大的多媒体处理工具套件，集成了视频音频处理、语音识别、文本翻译、语音合成和字幕翻译等多种功能。支持将英文视频自动翻译为中文配音版本，以及批量处理字幕文件翻译。

## 🌟 主要功能

### 🎬 视频多语言处理管道 (`video_multilang_pipeline.py`)
- **视频音频提取**: 使用 MoviePy 从视频中提取高质量音频
- **智能语音识别**: 基于 OpenAI Whisper 模型的多语言语音转文字
- **自动文本翻译**: 集成有道翻译API实现高质量英中翻译
- **文本转语音合成**: 使用 Google TTS 生成自然中文语音
- **视频音轨合成**: 通过 FFmpeg 将翻译后的音轨与原视频合成
- **批量处理**: 支持批量处理多个视频文件
- **GPU加速**: 支持CUDA加速的Whisper语音识别

### 📝 字幕翻译工具 (`according_to_src.py`)
- **SRT字幕解析**: 完整支持SRT格式字幕文件
- **双语字幕生成**: 生成包含原文和译文的双语字幕
- **批量字幕处理**: 自动处理目录下所有英文字幕文件
- **智能跳过机制**: 自动跳过已翻译的文件
- **时间轴保持**: 完整保持原字幕的时间轴和格式

### 🔧 测试和调试工具 (`test.py`)
- **设备检测**: 自动检测并显示可用的计算设备（CPU/GPU）
- **Whisper模型测试**: 快速测试语音识别功能

## 📁 项目结构

```
多媒体多语言处理工具/
├── video_multilang_pipeline.py    # 主视频处理管道
├── according_to_src.py           # 字幕翻译工具
├── Input_mp4/                    # 输入视频文件目录
├── Output_mp4/                   # 输出视频文件目录
├── Subs/                         # 字幕文件目录
│   ├── *.eng.srt                # 英文字幕文件
│   └── *.zh&eng.srt             # 生成的中英双语字幕
├── temp/                         # 临时文件目录
│   ├── *_audio.mp3              # 提取的音频文件
│   ├── *_en.txt                 # 识别的英文文本
│   ├── *_zh.txt                 # 翻译的中文文本
│   └── *_zh.mp3                 # 合成的中文音频
├── ffmpeg/                       # FFmpeg 工具包
│   ├── bin/                     # 可执行文件
│   ├── lib/                     # 库文件
│   └── include/                 # 头文件
└── README.md                     # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- CUDA支持的GPU（可选，用于加速语音识别）
- 稳定的网络连接（用于API调用）

### 依赖安装

```bash
# 基础依赖
pip install pysrt requests googletrans==4.0.0rc1 gtts whisper-openai moviepy tqdm torch

# 如果需要GPU加速（推荐）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 使用方法

#### 1. 视频多语言处理

**准备工作：**
1. 将需要处理的MP4视频文件放入 `Input_mp4/` 目录
2. 确保网络连接正常（需要访问翻译API）

**运行处理：**
```bash
python video_multilang_pipeline.py
```

**处理流程：**
1. 🎵 **音频提取**: 从视频中提取高质量音频
2. 🎤 **语音识别**: 使用Whisper模型转录英文文本
3. 🌐 **文本翻译**: 通过有道API翻译为中文
4. 🔊 **语音合成**: 将中文文本转换为语音
5. 🎬 **视频合成**: 将中文音轨与原视频合并

**输出结果：**
- 处理后的中文配音视频保存在 `Output_mp4/` 目录
- 临时文件（音频、文本）保存在 `temp/` 目录

#### 2. 字幕翻译处理

**准备工作：**
1. 将英文字幕文件（`.eng.srt`）放入 `Subs/` 目录
2. 文件命名格式：`电影名.eng.srt`

**运行翻译：**
```bash
python according_to_src.py
```

**输出结果：**
- 生成双语字幕文件：`电影名.zh&eng.srt`
- 包含原英文文本和中文翻译


## ⚙️ 核心技术

### 语音识别技术
- **Whisper模型**: 支持 `tiny`、`base`、`small`、`medium`、`large` 多种规模
- **设备优化**: 自动选择最优计算设备（CPU/GPU）
- **多语言支持**: 专门优化英语识别准确度
- **实时进度**: 提供详细的处理进度显示

### 翻译服务
- **有道翻译API**: 企业级翻译服务
- **智能分段**: 自动将长文本分段处理（每段最多200词）
- **错误处理**: 完善的API调用错误处理机制
- **频率控制**: 内置请求频率限制，避免API限制

### 音频处理
- **高质量提取**: 使用MoviePy进行无损音频提取
- **格式支持**: 支持MP3、WAV等多种音频格式
- **音轨合成**: 通过FFmpeg实现专业级音视频合成

### 字幕处理
- **SRT标准**: 完全兼容SRT字幕格式标准
- **时间轴保持**: 精确保持原字幕时间轴
- **编码安全**: 使用UTF-8编码确保中文正确显示
- **双语布局**: 优化的双语字幕显示格式

## 🔧 高级配置

### Whisper模型选择

不同模型的特点：
- `tiny`: 最快速度，较低准确度（~39MB）
- `base`: 平衡速度和准确度（~74MB）
- `small`: 更高准确度（~244MB）
- `medium`: 专业级准确度（~769MB）
- `large`: 最高准确度（~1550MB）

修改 `video_multilang_pipeline.py` 中的模型参数：
```python
text = transcribe_audio(audio_path, model_name="base")  # 可选: tiny, base, small, medium, large
```

### 翻译语言配置

支持多种目标语言：
```python
# 在 translate_text 函数中修改目标语言
translate_text(text, dest_lang="zh-cn")  # 中文
translate_text(text, dest_lang="ja")     # 日语
translate_text(text, dest_lang="ko")     # 韩语
translate_text(text, dest_lang="fr")     # 法语
```

### API配置自定义

如需使用自己的有道翻译API密钥：
```python
# 在对应文件中修改以下配置
APP_KEY = '你的APP_KEY'
APP_SECRET = '你的APP_SECRET'
```

## 📊 性能优化

### GPU加速设置
```python
# 检查GPU可用性
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"使用设备: {device}")
```

### 批处理优化
- **并行处理**: 支持多文件并行处理
- **内存管理**: 自动清理临时文件
- **错误恢复**: 单个文件错误不影响批处理继续

### 网络优化
- **重试机制**: API调用失败自动重试
- **频率限制**: 避免API调用过于频繁
- **超时处理**: 网络超时自动处理

## 📋 输出格式详解

### 视频处理输出

**原始视频**: `input.mp4`
**处理后视频**: `input_zh.mp4`
- 保持原视频画质和分辨率
- 替换为中文配音音轨
- 保持视频时长不变

### 字幕文件输出

**英文字幕格式**:
```srt
1
00:04:29,060 --> 00:04:30,896
You should consider yourself lucky.

2
00:04:31,200 --> 00:04:33,500
This is the best place in the world.
```

**双语字幕格式**:
```srt
1
00:04:29,060 --> 00:04:30,896
You should consider yourself lucky.
你应该觉得自己很幸运。

2
00:04:31,200 --> 00:04:33,500
This is the best place in the world.
这是世界上最好的地方。
```

## 🔍 故障排除

### 常见问题

**1. GPU不可用**
```bash
# 检查CUDA安装
nvidia-smi
# 重新安装PyTorch CUDA版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**2. API调用失败**
- 检查网络连接
- 验证API密钥是否有效
- 确认API调用频率未超限

**3. FFmpeg错误**
- 确保FFmpeg路径正确配置
- 检查视频文件格式是否支持
- 验证输出目录写入权限

**4. 内存不足**
- 使用较小的Whisper模型
- 减少批处理文件数量
- 增加系统虚拟内存

### 调试模式

启用详细日志输出：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 使用场景

### 教育学习
- 🎓 **语言学习**: 生成双语字幕辅助语言学习
- 📚 **教学资源**: 将英文教学视频本地化
- 🌍 **国际交流**: 快速处理国际会议视频

### 内容创作
- 🎬 **影视制作**: 快速生成多语言版本
- 📺 **自媒体**: 扩大内容受众范围
- 🎮 **游戏本地化**: 游戏视频内容翻译

### 企业应用
- 💼 **培训材料**: 企业培训视频多语言化
- 🏢 **会议记录**: 国际会议自动翻译
- 📈 **产品宣传**: 产品介绍视频本地化

## 📄 技术规格

### 支持格式
- **视频输入**: MP4, AVI, MOV, MKV
- **音频输出**: MP3, WAV
- **字幕格式**: SRT
- **文本编码**: UTF-8

### 系统要求
- **操作系统**: Windows, macOS, Linux
- **Python版本**: 3.7+
- **内存需求**: 最少4GB RAM（推荐8GB+）
- **存储空间**: 根据处理文件大小而定
- **网络要求**: 稳定的互联网连接

### 性能指标
- **语音识别**: 实时倍数0.1-1.0x（取决于模型和硬件）
- **翻译速度**: 每分钟约200-500词
- **音频合成**: 每分钟文本约需10-30秒
- **视频合成**: 通常与原视频时长相当

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📜 许可证

本项目仅供学习和个人使用。使用时请遵守：
- 有道翻译API使用条款
- OpenAI Whisper许可证
- Google TTS服务条款
- FFmpeg许可证

## 🙏 致谢

- [OpenAI Whisper](https://github.com/openai/whisper) - 强大的语音识别模型
- [有道翻译API](https://ai.youdao.com/) - 高质量翻译服务
- [Google TTS](https://gtts.readthedocs.io/) - 文本转语音服务
- [MoviePy](https://zulko.github.io/moviepy/) - 视频处理库
- [FFmpeg](https://ffmpeg.org/) - 多媒体处理工具

---

**开发提示**: 如需自定义功能或参数，请参考各个Python文件中的详细注释和配置选项。

**技术支持**: 如遇到技术问题，请检查依赖安装、网络连接和系统配置。