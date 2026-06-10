---
name: computer-use
description: Control the desktop using AI vision. Takes screenshots, analyzes them with a multi-modal vision model, and executes mouse/keyboard actions. Use when the user asks to click on something, type text, open apps, navigate UIs, automate desktop tasks, or control their computer with AI. Trigger on "computer use", "control my screen", "click on", "automate desktop", "open app", "do X on my computer", or any request to interact with the desktop GUI.
---

# Computer-Use Skill

AI-powered desktop control using a multi-modal vision model. Takes screenshots of the user's screen, analyzes them to understand the UI, and executes mouse/keyboard actions to accomplish tasks.

## How It Works

1. Takes a screenshot using macOS `screencapture`
2. Sends the screenshot to a multi-modal vision API (OpenAI-compatible)
3. The AI analyzes the screen and outputs actions (CLICK, TYPE, KEY, SCROLL)
4. Actions are executed using pyautogui with automatic Retina coordinate scaling

## Prerequisites

- macOS with Python 3.10+
- Required packages: `pip3 install pyautogui Pillow openai`
- API key for a multi-modal vision model (set via environment variables)

## Usage

Run the script directly with a task:

```bash
python3 ~/.claude/skills/computer-use/scripts/computer-use.py "your task here"
```

Or import and use programmatically:

```python
from computer_use import take_screenshot, chat_with_screenshot, parse_action, execute_action
```

## Supported Actions

The AI outputs actions in these formats (one per line):

| Action | Format | Description |
|--------|--------|-------------|
| Click | `CLICK x y` | Click at screenshot coordinates (auto-scaled for Retina) |
| Type | `TYPE text` | Type the given text |
| Key | `KEY keyname` | Press a key (enter, escape, tab, space, cmd, etc.) |
| Wait | `WAIT seconds` | Pause for the specified duration |
| Scroll | `SCROLL direction` | Scroll up or down |

## Examples

```bash
# Open an app
python3 ~/.claude/skills/computer-use/scripts/computer-use.py "open Safari and go to google.com"

# Click on a UI element
python3 ~/.claude/skills/computer-use/scripts/computer-use.py "click on the Apple menu in the top left"

# Describe what's on screen
python3 ~/.claude/skills/computer-use/scripts/computer-use.py "what apps are currently open"

# Automate a workflow
python3 ~/.claude/skills/computer-use/scripts/computer-use.py "open Finder, go to Downloads, and sort by date modified"
```

## Safety

- **Failsafe**: Move mouse to top-left corner to abort (pyautogui built-in)
- The AI asks for clarification before risky actions
- All actions are printed to the terminal before execution
- Screenshot coordinates are automatically scaled for Retina displays

## Configuration

Set these environment variables before running:

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | (required) | Your API key |
| `API_BASE` | (required) | API endpoint URL (OpenAI-compatible) |
| `MODEL` | (required) | Multi-modal vision model name |

## Limitations

- macOS only (uses `screencapture` and `pyautogui`)
- Requires an OpenAI-compatible vision API to be accessible
- Complex multi-step tasks may need multiple rounds of screenshot-analyze-act
- The AI may not perfectly identify all UI elements
