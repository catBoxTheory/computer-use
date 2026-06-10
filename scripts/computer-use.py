#!/usr/bin/env python3
"""
Computer-Use Skill
AI-powered desktop control using Mimo v2.5 vision model.
Takes screenshots, analyzes them, and executes mouse/keyboard actions.
"""
import os
import sys
import json
import base64
import subprocess
import time
from openai import OpenAI
from PIL import Image
import pyautogui

# Mimo API configuration — set these environment variables before running
MIMO_API_KEY = os.environ.get("MIMO_API_KEY")
MIMO_API_BASE = os.environ.get("MIMO_API_BASE", "https://token-plan-sgp.xiaomimimo.com/v1")
MODEL = os.environ.get("MIMO_MODEL", "mimo-v2.5")

if not MIMO_API_KEY:
    raise ValueError("MIMO_API_KEY environment variable is required. Export it before running.")

# Safety settings
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.3

client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_API_BASE)

def take_screenshot():
    """Take a screenshot and return base64 encoded image."""
    path = "/tmp/cua_screenshot.png"
    subprocess.run(["screencapture", "-x", path], check=True)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def parse_action(response_text):
    """Parse AI response for actions to execute."""
    actions = []
    lines = response_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("CLICK"):
            parts = line.split()
            if len(parts) >= 3:
                actions.append({"type": "click", "x": int(parts[1]), "y": int(parts[2])})
        elif line.startswith("TYPE"):
            text = line[5:]
            actions.append({"type": "type", "text": text})
        elif line.startswith("KEY"):
            key = line[4:].strip()
            actions.append({"type": "key", "key": key})
        elif line.startswith("WAIT"):
            seconds = float(line[5:].strip()) if len(line) > 5 else 1
            actions.append({"type": "wait", "seconds": seconds})
        elif line.startswith("SCROLL"):
            direction = line[7:].strip() if len(line) > 7 else "down"
            actions.append({"type": "scroll", "direction": direction})
    return actions

def get_screen_scale():
    """Get the scale factor between screenshot and screen coordinates."""
    import PIL.Image
    subprocess.run(["screencapture", "-x", "/tmp/_scale_test.png"], check=True)
    img = PIL.Image.open("/tmp/_scale_test.png")
    screen = pyautogui.size()
    scale_x = img.width / screen.width
    scale_y = img.height / screen.height
    return scale_x, scale_y

SCALE_X, SCALE_Y = get_screen_scale()

def execute_action(action):
    """Execute a single action."""
    if action["type"] == "click":
        screen_x = int(action["x"] / SCALE_X)
        screen_y = int(action["y"] / SCALE_Y)
        print(f"  -> Clicking at screen ({screen_x}, {screen_y}) [screenshot: ({action['x']}, {action['y']})]")
        pyautogui.click(screen_x, screen_y)
    elif action["type"] == "type":
        print(f"  -> Typing: {action['text']}")
        pyautogui.typewrite(action["text"], interval=0.05)
    elif action["type"] == "key":
        print(f"  -> Pressing key: {action['key']}")
        pyautogui.press(action["key"])
    elif action["type"] == "wait":
        print(f"  -> Waiting {action['seconds']}s")
        time.sleep(action["seconds"])
    elif action["type"] == "scroll":
        amount = -3 if action["direction"] == "down" else 3
        print(f"  -> Scrolling {action['direction']}")
        pyautogui.scroll(amount)

SCREEN_W, SCREEN_H = pyautogui.size()

SYSTEM_PROMPT = f"""You are a computer-use AI assistant. You can see the user's screen via screenshots and control it.

Screen resolution: {SCREEN_W}x{SCREEN_H}
The screenshot may be at a different resolution (e.g. Retina 2x). Coordinates you give will be automatically scaled.

When the user gives you a task, respond with a series of actions to accomplish it.
Each action should be on its own line in this exact format:

CLICK x y        - Click at pixel coordinates (x, y) in the screenshot
TYPE text         - Type the given text
KEY keyname       - Press a key (enter, escape, tab, space, backspace, etc.)
WAIT seconds      - Wait for the specified seconds
SCROLL direction  - Scroll up or down

After performing actions, describe what you did and whether the task is complete.
If you need to see the result before continuing, say "NEED_SCREENSHOT" and wait.

IMPORTANT: Only output actions when you're ready to execute them. First analyze the screenshot, then output actions."""

def chat_with_screenshot(user_message, screenshot_b64=None):
    """Send a message with optional screenshot to the AI."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    if screenshot_b64:
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_message},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}}
            ]
        })
    else:
        messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=4096,
    )
    return response.choices[0].message.content

def main():
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = input("What would you like me to do? > ")

    print(f"\nTask: {task}")
    print("=" * 50)

    print("Taking screenshot...")
    screenshot = take_screenshot()

    print("Analyzing screen...")
    response = chat_with_screenshot(task, screenshot)
    print(f"\nAI Response:\n{response}\n")

    actions = parse_action(response)
    if actions:
        print(f"Executing {len(actions)} action(s)...")
        for action in actions:
            execute_action(action)
            time.sleep(0.5)

        print("\nTaking screenshot of result...")
        time.sleep(1)
        result_screenshot = take_screenshot()
        result = chat_with_screenshot("What happened after the actions? Is the task complete?", result_screenshot)
        print(f"\nResult:\n{result}")
    else:
        print("No actions to execute. The AI may need more information.")

if __name__ == "__main__":
    main()
