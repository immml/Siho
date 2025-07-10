## 🐍 羲和: Raspberry Pi Pico / CircuitPython GPIO HID 宏控制器

> ⚙️ 一个基于 Raspberry Pi Pico 或支持 CircuitPython 的开发板的开源宏控制器程序，可以通过 GPIO 引脚触发键盘、鼠标操作或执行复杂的宏任务。

---

### 📋 简介

羲和（siho-HID） 是一个为 Raspberry Pi Pico（或其他 CircuitPython 支持的开发板）设计的多功能宏控制器程序，它允许你通过物理按钮或外部信号控制键盘输入、鼠标操作以及自定义宏指令。

你可以用它来：

- 自动化按键组合
- 控制游戏连招
- 实现硬件触发器（如直播控制、工业自动化）
- 模拟键盘/鼠标操作
- 多阶段等待逻辑控制

---

### 🧰 特性

- ✅ 支持 GPIO 上升沿触发
- ✅ 可配置宏步骤（keys, text, wait, wait_gpio）
- ✅ 支持文本自动输入
- ✅ 支持等待固定时间或等待特定 GPIO 电平
- ✅ 配置文件驱动，无需修改代码即可更新功能
- ✅ 支持消抖处理，防止误触发

---

### 🛠️ 硬件要求

- Raspberry Pi Pico 或任何支持 CircuitPython 的开发板
- USB 数据线（用于连接电脑）
- 按钮或传感器（用于触发 GPIO）

---

### 📁 文件说明

| 文件名        | 描述                                     |
| ------------- | ---------------------------------------- |
| `code.py`     | 主程序，包含完整的宏逻辑                 |
| `config.json` | 用户可编辑的配置文件，定义每个引脚的行为 |

---

### 🧪 示例配置 (`config.json`)

```json
{
  "actions": [
    {
      "pin": "GP18",
      "type": "macro",
      "steps": [
        {"type": "keys", "keys": ["LEFT_GUI", "R"], "delay": 0.5},


        {"type": "text", "text": "cmd", "char_delay": 0.1},

        {"type": "keys", "keys": ["CTRL", "SPACE"], "delay": 0.5},

        {"type": "keys", "keys": ["ENTER"], "delay": 1.0},

        {"type": "text", "text": "start  https://www.bilibili.com/video/av546403908", "char_delay": 0.05},

        {"type": "keys", "keys": ["ENTER"], "delay": 0.5},
        
        {"type": "wait", "delay": 1},

        {"type": "keys", "keys": ["ENTER"], "delay": 0.5},

        {"type": "wait", "delay": 1},

        {"type": "keys", "keys": ["ENTER"], "delay": 0.5},

        {"type": "wait", "delay": 1},

        {"type": "keys", "keys": ["ENTER"], "delay": 0.5}
      ]
    }
  ]
}

```

---

### 📦 使用方法

1. **安装 CircuitPython**
   - 下载对应开发板的 `.uf2` 文件：[CircuitPython.org](https://circuitpython.org/board/raspberry_pi_pico)
   - 将开发板进入 Bootloader 模式（按住 BOOTSEL 插入 USB），然后将 `.uf2` 文件拖入出现的 U盘设备。

2. **上传代码**
   - 将 下载好的main.zip解压到树莓派内

   - 触发你配置的 GPIO 引脚（例如按下按钮），观察是否执行预设的宏动作。

---

### 🔧 依赖库

请确保你的 `lib/` 目录中包含以下库：

- `adafruit_hid`

可以从 [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases) 下载并提取所需 `.mpy` 文件。

---

### 📜 许可证（License）

本项目采用 **Apache License, Version 2.0** 开源协议。

```markdown
Copyright 2025 鲁林祺

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

有关完整许可条款，请参阅 [LICENSE](https://github.com/Linqi18/RPI-HID/blob/main/LICENSE) 文件。

---

### 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

- Fork 本项目
- 创建新分支 (`git checkout -b feature/new-feature`)
- 提交更改 (`git commit -m 'Add new feature'`)
- 推送至远程分支 (`git push origin feature/new-feature`)
- 创建 Pull Request

---

### 📞 联系方式

如果你有任何问题、建议或需要帮助，请在 GitHub 上提 Issue，或者联系作者：

- GitHub: [@Linqi18](https://github.com/Linqi18)
- Email: 2836980096@qq.com
- 爱发电 [immml正在创作mc工具 整合包和badusb工具 | 爱发电](https://afdian.com/a/immml)

---

### ❤️ 感谢阅读 & Star

如果你觉得这个项目有用，别忘了给个 ⭐ Star 来鼓励我继续维护和更新！
