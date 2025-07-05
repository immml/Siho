import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

import board
import digitalio
import time
import json

kbd = Keyboard(usb_hid.devices)
m = Mouse(usb_hid.devices)

# === 加载配置 ===
try:
    with open("config.json", "r") as f:
        config_data = json.load(f)
    ACTIONS = config_data.get("actions", [])
except Exception as e:
    print("Error:", e)
    ACTIONS = []

# === 键值映射表（支持字母、数字、符号）===
KEY_MAP = {
    'a': Keycode.A, 'b': Keycode.B, 'c': Keycode.C, 'd': Keycode.D,
    'e': Keycode.E, 'f': Keycode.F, 'g': Keycode.G, 'h': Keycode.H,
    'i': Keycode.I, 'j': Keycode.J, 'k': Keycode.K, 'l': Keycode.L,
    'm': Keycode.M, 'n': Keycode.N, 'o': Keycode.O, 'p': Keycode.P,
    'q': Keycode.Q, 'r': Keycode.R, 's': Keycode.S, 't': Keycode.T,
    'u': Keycode.U, 'v': Keycode.V, 'w': Keycode.W, 'x': Keycode.X,
    'y': Keycode.Y, 'z': Keycode.Z,

    'A': (Keycode.LEFT_SHIFT, Keycode.A),
    'B': (Keycode.LEFT_SHIFT, Keycode.B),
    'C': (Keycode.LEFT_SHIFT, Keycode.C),
    'D': (Keycode.LEFT_SHIFT, Keycode.D),
    'E': (Keycode.LEFT_SHIFT, Keycode.E),
    'F': (Keycode.LEFT_SHIFT, Keycode.F),
    'G': (Keycode.LEFT_SHIFT, Keycode.G),
    'H': (Keycode.LEFT_SHIFT, Keycode.H),
    'I': (Keycode.LEFT_SHIFT, Keycode.I),
    'J': (Keycode.LEFT_SHIFT, Keycode.J),
    'K': (Keycode.LEFT_SHIFT, Keycode.K),
    'L': (Keycode.LEFT_SHIFT, Keycode.L),
    'M': (Keycode.LEFT_SHIFT, Keycode.M),
    'N': (Keycode.LEFT_SHIFT, Keycode.N),
    'O': (Keycode.LEFT_SHIFT, Keycode.O),
    'P': (Keycode.LEFT_SHIFT, Keycode.P),
    'Q': (Keycode.LEFT_SHIFT, Keycode.Q),
    'R': (Keycode.LEFT_SHIFT, Keycode.R),
    'S': (Keycode.LEFT_SHIFT, Keycode.S),
    'T': (Keycode.LEFT_SHIFT, Keycode.T),
    'U': (Keycode.LEFT_SHIFT, Keycode.U),
    'V': (Keycode.LEFT_SHIFT, Keycode.V),
    'W': (Keycode.LEFT_SHIFT, Keycode.W),
    'X': (Keycode.LEFT_SHIFT, Keycode.X),
    'Y': (Keycode.LEFT_SHIFT, Keycode.Y),
    'Z': (Keycode.LEFT_SHIFT, Keycode.Z),

    '0': Keycode.ZERO, '1': Keycode.ONE, '2': Keycode.TWO, '3': Keycode.THREE,
    '4': Keycode.FOUR, '5': Keycode.FIVE, '6': Keycode.SIX, '7': Keycode.SEVEN,
    '8': Keycode.EIGHT, '9': Keycode.NINE,

    ' ': Keycode.SPACE, '\n': Keycode.ENTER,
    '.': Keycode.PERIOD, ',': Keycode.COMMA,
    '!': (Keycode.LEFT_SHIFT, Keycode.ONE),     # Shift + 1 => !
    '?': (Keycode.LEFT_SHIFT, Keycode.MINUS),   # Shift + - => ?
    '@': (Keycode.LEFT_SHIFT, Keycode.TWO),     # Shift + 2 => @
    '#': (Keycode.LEFT_SHIFT, Keycode.THREE),   # Shift + 3 => #
    '$': (Keycode.LEFT_SHIFT, Keycode.FOUR),    # Shift + 4 => $
    '%': (Keycode.LEFT_SHIFT, Keycode.FIVE),    # Shift + 5 => %
    '^': (Keycode.LEFT_SHIFT, Keycode.SIX),     # Shift + 6 => ^
    '&': (Keycode.LEFT_SHIFT, Keycode.SEVEN),   # Shift + 7 => &
    '*': (Keycode.LEFT_SHIFT, Keycode.EIGHT),   # Shift + 8 => *
    '(': (Keycode.LEFT_SHIFT, Keycode.NINE),   # Shift + 9 => (
    ')': (Keycode.LEFT_SHIFT, Keycode.ZERO),   # Shift + 0 => )
    '_': (Keycode.LEFT_SHIFT, Keycode.MINUS),   # Shift + - => _
    '+': (Keycode.LEFT_SHIFT, Keycode.EQUALS),  # Shift + = => +
    '=': Keycode.EQUALS,
    '-': Keycode.MINUS,
    '[': Keycode.LEFT_BRACKET,
    ']': Keycode.RIGHT_BRACKET,
    '{': (Keycode.LEFT_SHIFT, Keycode.LEFT_BRACKET),
    '}': (Keycode.LEFT_SHIFT, Keycode.RIGHT_BRACKET),
    ';': Keycode.SEMICOLON,
    ':': (Keycode.LEFT_SHIFT, Keycode.SEMICOLON),
    "'": Keycode.QUOTE,
    '"': (Keycode.LEFT_SHIFT, Keycode.QUOTE),
    '\\': Keycode.BACKSLASH,
    '|': (Keycode.LEFT_SHIFT, Keycode.BACKSLASH),
    '/': Keycode.FORWARD_SLASH,
    '<': (Keycode.LEFT_SHIFT, Keycode.COMMA),
    '>': (Keycode.LEFT_SHIFT, Keycode.PERIOD),
}

# === 发送单个字符 ===
def send_char(char):
    if char in KEY_MAP:
        keys = KEY_MAP[char]
        if isinstance(keys, tuple):
            kbd.send(*keys)
        else:
            kbd.send(keys)

# === 执行宏函数 ===
def execute_macro(macro_steps):
    for step in macro_steps:
        step_type = step.get("type", "keys")
        current_time = time.monotonic()

        if step_type == "keys":
            keys = [getattr(Keycode, k, None) for k in step.get("keys", [])]
            keys = [k for k in keys if k is not None]
            if keys:
                kbd.send(*keys)
            time.sleep(step.get("delay", 0))

        elif step_type == "text":
            text = step.get("text", "")
            char_delay = step.get("char_delay", 0.1)
            for ch in text:
                send_char(ch)
                time.sleep(char_delay)

        elif step_type == "wait":
            # 🔥 等待固定时间
            delay = step.get("delay", 0)
            if delay > 0:
                print(f"⏳ 等待 {delay} 秒...")
                time.sleep(delay)

        elif step_type == "wait_gpio":
            # 🔥 等待某个 GPIO 达到指定电平
            pin_name = step.get("pin")
            target_level = step.get("level", True)
            timeout = step.get("timeout", None)

            if not hasattr(board, pin_name):
                print(f"⚠️ 引脚 {pin_name} 不可用")
                continue

            wait_pin = getattr(board, pin_name)
            gpio = digitalio.DigitalInOut(wait_pin)
            gpio.direction = digitalio.Direction.INPUT
            gpio.pull = digitalio.Pull.DOWN if target_level else digitalio.Pull.UP

            start_time = time.monotonic()
            print(f"⏳ 正在等待 {pin_name} 变为 {'高' if target_level else '低'} 电平...")

            while True:
                value = gpio.value
                if value == target_level:
                    print(f"✅ 检测到 {pin_name} 已变为目标电平")
                    break
                if timeout and (time.monotonic() - start_time) > timeout:
                    print(f"⏰ 等待超时，继续执行")
                    break
                time.sleep(0.01)

# === 初始化GPIO ===
gpios = []
for item in ACTIONS:
    pin_name = item.get("pin", None)
    if not pin_name or not hasattr(board, pin_name):
        continue
    pin = getattr(board, pin_name)
    gpio = digitalio.DigitalInOut(pin)
    gpio.direction = digitalio.Direction.INPUT
    gpio.pull = digitalio.Pull.DOWN
    gpios.append(gpio)

# 存储按键状态
btn_states = {}
for i in range(len(ACTIONS)):
    btn_states[i] = {
        "pressed": False,
        "last_change": 0
    }

DEBOUNCE_TIME = 0


# === 主循环 ===
while True:
    for i, item in enumerate(ACTIONS):
        gpio = gpios[i] if i < len(gpios) else None
        if not gpio:
            continue

        current_value = gpio.value
        state = btn_states[i]
        current_time = time.monotonic()

        # 消抖
        if current_value == state["pressed"]:
            continue
        if current_time - state["last_change"] < DEBOUNCE_TIME:
            continue

        state["last_change"] = current_time

        # ====== 🔁 改动点：改为在上升沿（低→高）触发 ======
        if current_value:  # 上升沿：从低变为高
            state["pressed"] = True

            # ✅ 在这里触发按键/宏（高电平触发）
            action_type = item.get("type")

            if action_type == "key":
                key_action = item.get("action")
                key = item.get("key")
                keycode = getattr(Keycode, key, getattr(Mouse, key, None))

                if key_action == "click":
                    m.click(keycode)
                elif key_action == "hold":
                    kbd.press(keycode)
                elif key_action == "send":
                    kbd.send(keycode)

            elif action_type == "macro":
                execute_macro(item.get("steps", []))

        else:  # 下降沿：释放按键
            state["pressed"] = False

            # 如果是 hold 类型，释放按键
            if item.get("type") == "key" and item.get("action") == "hold":
                key = getattr(Keycode, item.get("key", ""), None)
                if key:
                    kbd.release(key)

    time.sleep(0.01)