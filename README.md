# Computer-Use

AI-powered desktop control using a multi-modal vision model. Takes screenshots of your screen, analyzes them with AI, and executes mouse/keyboard actions to accomplish tasks.

## How It Works

```
Screenshot → AI Analyze → Execute Actions → Repeat
```

1. Captures your screen using macOS `screencapture`
2. Sends the screenshot to a multi-modal vision API
3. The AI identifies UI elements and outputs actions (click, type, key press, scroll)
4. Actions are executed with automatic Retina display coordinate scaling

## Prerequisites

- macOS (uses `screencapture` and `pyautogui`)
- Python 3.10+
- API key for a multi-modal vision model (OpenAI-compatible endpoint)

## Installation

```bash
# Clone the repo
git clone https://github.com/catBoxTheory/computer-use.git
cd computer-use

# Install dependencies
pip3 install pyautogui Pillow openai

# Set your API key and endpoint
export API_KEY="your-api-key-here"
export API_BASE="https://your-api-endpoint/v1"
```

## Usage

```bash
# With a task argument
python3 scripts/computer-use.py "open Safari and go to google.com"

# Interactive mode
python3 scripts/computer-use.py

# Examples
python3 scripts/computer-use.py "what apps are currently open"
python3 scripts/computer-use.py "click on the Apple menu in the top left"
python3 scripts/computer-use.py "open Finder, go to Downloads, sort by date"
```

## Supported Actions

| Action | Format | Description |
|--------|--------|-------------|
| Click | `CLICK x y` | Click at screenshot coordinates (auto-scaled for Retina) |
| Type | `TYPE text` | Type the given text |
| Key | `KEY keyname` | Press a key (enter, escape, tab, cmd, etc.) |
| Wait | `WAIT seconds` | Pause for the specified duration |
| Scroll | `SCROLL direction` | Scroll up or down |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | (required) | Your API key |
| `API_BASE` | (required) | API endpoint URL (OpenAI-compatible) |
| `MODEL` | (required) | Multi-modal vision model name |

## Safety

- **Failsafe**: Move mouse to top-left corner to abort instantly
- All actions are printed to the terminal before execution
- The AI asks for clarification before risky actions
- No destructive actions by default

## Limitations

- macOS only
- Requires an OpenAI-compatible vision API to be accessible
- Keyboard actions go to whatever app is currently focused
- Complex multi-step tasks may need multiple rounds

## License

MIT
