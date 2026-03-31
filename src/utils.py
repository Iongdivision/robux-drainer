import os, sys, ctypes, time, threading, math
from datetime import datetime

def rgb(r, g, b):
    if os.name == 'nt':
        os.system("")
    return f"\033[38;2;{r};{g};{b}m"

def rgb_bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
ITALIC = "\033[3m"

GRAY   = rgb(170, 170, 170)
DGRAY  = rgb(90,  90,  90)
WHITE  = rgb(220, 218, 210)
GREEN  = rgb(80,  220, 140)
RED    = rgb(235, 95,  95)
BLUE   = rgb(120, 185, 255)
PURPLE = rgb(190, 145, 255)
YELLOW = rgb(255, 210, 110)
CYAN   = rgb(80,  210, 220)
ORANGE = rgb(255, 160, 80)
PINK   = rgb(255, 130, 180)

BG_GREEN  = rgb_bg(30,  80,  55)
BG_RED    = rgb_bg(90,  30,  30)
BG_BLUE   = rgb_bg(25,  55,  100)
BG_PURPLE = rgb_bg(60,  40,  100)
BG_YELLOW = rgb_bg(85,  65,  20)
BG_GRAY   = rgb_bg(35,  35,  35)

RED_WHITE_GREEN = [RED, WHITE, GREEN]
PURPLE_BLUE     = [PURPLE, BLUE, CYAN]
FIRE            = [RED, ORANGE, YELLOW]
OCEAN           = [BLUE, CYAN, WHITE]

def rainbow_text(text, colors):
    result = ""
    for i, ch in enumerate(text):
        result += colors[i % len(colors)] + ch
    return result + RESET

def smooth_gradient(text, r1, g1, b1, r2, g2, b2):
    result = ""
    steps = max(len(text) - 1, 1)
    for i, ch in enumerate(text):
        t = i / steps
        result += rgb(int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t)) + ch
    return result + RESET

def wave_gradient(text, offset=0):
    result = ""
    for i, ch in enumerate(text):
        r = int((math.sin(0.3 * (i + offset)      ) + 1) * 127.5)
        g = int((math.sin(0.3 * (i + offset) + 2.0) + 1) * 127.5)
        b = int((math.sin(0.3 * (i + offset) + 4.0) + 1) * 127.5)
        result += rgb(r, g, b) + ch
    return result + RESET

_wave_offset = 0

def _next_offset():
    global _wave_offset
    _wave_offset += 1
    return _wave_offset

def wave_tag(tag):
    return wave_gradient(tag, _next_offset())

_total_tries   = 0
_total_robux   = 0
_total_cookies = 0
_app_name      = "Buyer"
_start_time    = time.time()

def set_app_name(name):
    global _app_name
    _app_name = name

def update_cookie_count():
    global _total_cookies
    try:
        path = os.path.join("input", "cookies.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                _total_cookies = sum(1 for line in f if line.strip())
        else:
            _total_cookies = 0
    except:
        _total_cookies = 0

def add_try():
    global _total_tries
    _total_tries += 1

def add_robux(amount):
    global _total_robux
    _total_robux += amount

def _title_worker():
    while True:
        uptime_seconds = int(time.time() - _start_time)
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        uptime_str = f"{h:d}h {m:02d}m {s:02d}s"
        title = f"{_app_name} | Cookies: {_total_cookies} | Success: {_total_tries} | Drained: {_total_robux} R$ | Uptime: {uptime_str}"
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f"\x1b]0;{title}\x07")
        time.sleep(1)

def now():
    return datetime.now().strftime("%H:%M:%S")

def grad_tag(tag, r1, g1, b1, r2, g2, b2):
    return BOLD + smooth_gradient(tag, r1, g1, b1, r2, g2, b2) + RESET

TAGS = {
    "[#]": grad_tag("[#]", 120, 185, 255,  220, 218, 210),  
    "[!]": grad_tag("[!]", 235, 95,  95,   220, 218, 210), 
    "[+]": grad_tag("[+]", 80,  220, 140,  220, 218, 210), 
    "[-]": grad_tag("[-]", 235, 95,  95,   220, 218, 210), 
    "[*]": grad_tag("[*]", 190, 145, 255,  220, 218, 210), 
    "[~]": grad_tag("[~]", 80,  210, 220,  220, 218, 210),
    "[✓]": grad_tag("[✓]", 80,  220, 140,  220, 218, 210),
}

def log(tag, msg, color=GRAY):
    tag_color = TAGS.get(tag, GRAY + tag + RESET)
    print(f"{DGRAY}[{GRAY}{now()}{DGRAY}]{RESET} {tag_color} {WHITE}{msg}{RESET}")

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

update_cookie_count()
threading.Thread(target=_title_worker, daemon=True).start()
