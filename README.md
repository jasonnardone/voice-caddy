# GSPro AI Announcer - Complete Guide

🎤 **AI-powered golf commentary with customizable personalities**

Transform your GSPro experience with an AI announcer that provides intelligent, entertaining commentary in various personality modes - from professional sportscaster to smartass comedian!

## 🌟 Features

- **10+ Built-in Personalities**: Professional, Smartass, Hype Man, Zen Master, Pirate, British, and more!
- **Custom Personalities**: Create your own unique announcer styles
- **Context-Aware Commentary**: AI understands game state and provides relevant commentary
- **Real-time Analysis**: Tracks holes, distances, wind, and shot history
- **Natural Voice**: Text-to-speech with adjustable speed per personality
- **Debug Mode**: See exactly what the AI sees and how it responds

## 📋 Requirements

1. **Python 3.8+**
2. **Tesseract OCR** (for screen reading)
3. **Anthropic API Key** (for AI commentary)
4. **Python packages**: `anthropic`, `pytesseract`, `Pillow`, `pyttsx3`

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Install Python packages
pip install anthropic pytesseract Pillow pyttsx3

# Install Tesseract OCR
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

### Step 2: Get Your API Key

1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Create an API key
4. Set it as environment variable:

**Windows:**
```cmd
set ANTHROPIC_API_KEY=your-key-here
```

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY=your-key-here
```

Or add to your `.bashrc`/`.zshrc`:
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Run the Announcer

```bash
# Start with default (professional) mode
python gspro_ai_announcer.py

# Try smartass mode
python gspro_ai_announcer.py --mode smartass

# Enable debug mode to see what's happening
python gspro_ai_announcer.py --mode hype --debug
```

## 🎭 Built-in Personalities

### 1. **Normal** (Professional)
Professional golf announcer - informative and respectful.
```bash
python gspro_ai_announcer.py --mode normal
```
*Example: "145 yards to the pin. A great opportunity for birdie here."*

### 2. **Smartass** 🤣
Sarcastic, witty, and hilarious - doesn't hold back!
```bash
python gspro_ai_announcer.py --mode smartass
```
*Example: "145 yards... should be easy unless you're allergic to fairways."*

### 3. **Hype** 🔥
MAXIMUM ENERGY! Makes every shot EPIC!
```bash
python gspro_ai_announcer.py --mode hype
```
*Example: "ONE HUNDRED AND FORTY FIVE YARDS! THIS IS YOUR MOMENT!"*

### 4. **Zen** 🧘
Calm, meditative, peaceful Bob Ross style.
```bash
python gspro_ai_announcer.py --mode zen
```
*Example: "145 yards ahead... just you, the ball, and this beautiful moment."*

### 5. **Pirate** 🏴‍☠️
Yarr! Golf on the high seas!
```bash
python gspro_ai_announcer.py --mode pirate
```
*Example: "145 yards to the treasure, matey! Let's plunder this green!"*

### 6. **British** 🇬🇧
Posh, eloquent, David Attenborough meets golf.
```bash
python gspro_ai_announcer.py --mode british
```
*Example: "A rather splendid 145 yards to the pin. Do carry on."*

### 7. **Drill Sergeant** 💪
Military motivation! Golf is WAR!
```bash
python gspro_ai_announcer.py --mode drill_sergeant
```
*Example: "145 YARDS SOLDIER! EXECUTE THAT SHOT WITH PRECISION!"*

### 8. **Shakespeare** 🎭
Theatrical and epic! Golf in iambic pentameter!
```bash
python gspro_ai_announcer.py --mode shakespeare
```
*Example: "Hark! 145 yards doth separate thee from glory's embrace!"*

### 9. **Robot** 🤖
Beep boop! Logical, mechanical, slightly awkward.
```bash
python gspro_ai_announcer.py --mode robot
```
*Example: "DISTANCE CALCULATED: 145 yards. INITIATING GOLF PROTOCOL."*

### 10. **Sportscaster** 📺
Classic sports commentary - Jim Nantz style.
```bash
python gspro_ai_announcer.py --mode sportscaster
```
*Example: "145 yards out, and this is where champions are made."*

## 🎨 Create Custom Personalities

Want a medieval knight announcer? Surfer dude? Noir detective? Create your own!

```bash
python personality_creator.py
```

Follow the prompts to create your custom personality:
1. Enter an ID (e.g., "surfer")
2. Give it a name (e.g., "Beach Bro Announcer")
3. Describe the personality style
4. Set voice speed
5. Add example lines

Then use it:
```bash
python gspro_ai_announcer.py --mode surfer
```

### Example Custom Personalities

**Surfer Dude:**
```
Personality: "You are a surfer dude golf announcer. Use beach/surf terminology. 
Everything is 'gnarly', 'radical', or 'totally tubular'. 1-2 sentences max, bro!"

Example: "145 yards, dude! Time to catch that gnarly green wave!"
```

**Noir Detective:**
```
Personality: "You are a 1940s noir detective announcer. Dark, mysterious, dramatic. 
Use detective metaphors. 1-2 sentences max, gumshoe."

Example: "145 yards through the fog of doubt. This case is getting interesting."
```

**Medieval Knight:**
```
Personality: "You are a medieval knight announcer. Golf is a noble quest. 
Use chivalric language. 1-2 sentences max, good sir knight!"

Example: "145 yards to thy noble quest's end! May thy swing be true!"
```

## ⚙️ Command Line Options

```bash
python gspro_ai_announcer.py [OPTIONS]

Options:
  --mode MODE          Personality mode (default: normal)
  --list-modes         Show all available personalities
  --debug              Enable debug mode (shows OCR and AI reasoning)
  --interval N         Seconds between screen captures (default: 3)
  --api-key KEY        Anthropic API key (or use env var)
  --help               Show this help message
```

## 🔧 Advanced Configuration

### Adjust Voice Speed

Edit `personalities.json`:
```json
{
  "personalities": {
    "smartass": {
      "voice_rate": 160
    }
  }
}
```

Or edit directly in code:
```python
self.engine.setProperty('rate', 160)  # 100-200
```

### Adjust AI Temperature

More creative/random responses:
```python
temperature=0.9  # Higher = more creative (0.0-1.0)
```

### Change AI Model

In `gspro_ai_announcer.py`:
```python
model="claude-sonnet-4-20250514"  # Current
model="claude-opus-4-20250514"    # More creative/powerful
```

## 🐛 Troubleshooting

### "No API key found"
Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### "Tesseract not found"
Install Tesseract OCR (see Quick Start)

### OCR not detecting distances
1. Run with `--debug` flag
2. Check `debug_screenshots/` folder
3. Make sure GSPro is visible and not minimized
4. Adjust GSPro UI scale if text is too small

### Voice too fast/slow
Adjust `voice_rate` in `personalities.json` or code

### Commentary not relevant
The AI bases commentary on what it can read from screen. Enable debug mode to see what it's detecting. You may need to adjust regex patterns in `parse_game_state()`.

## 💡 Tips for Best Experience

1. **Use Debug Mode First**: Run with `--debug` to see what the system captures
2. **Adjust Interval**: Start with 3 seconds, increase if your PC is slow
3. **Try Different Personalities**: Each brings unique entertainment value
4. **Create Custom Personalities**: Make it YOUR experience
5. **Keep GSPro Visible**: Don't minimize or cover the window
6. **Check API Usage**: Monitor your Anthropic API usage in the console

## 📊 What Gets Tracked

The AI announcer tracks:
- ✅ Current hole number and par
- ✅ Distance to pin (yards)
- ✅ Wind speed (mph)
- ✅ Number of shots per hole
- ✅ Hole history
- ✅ Distance changes (to detect shots)

And provides commentary on:
- 🎯 New holes ("Hole 5, par 4, 387 yards")
- 📏 Distance updates ("145 yards remaining")
- 💨 Significant wind ("12 mph crosswind")
- 🏌️ Shot context (based on hole progress)

## 🎮 Integration with GSPro

The announcer works by:
1. Taking screenshots of GSPro every few seconds
2. Using OCR to read game information
3. Passing that information to Claude AI
4. Claude generates contextual commentary
5. Text-to-speech announces the commentary

**No GSPro API integration needed!** It works entirely through screen reading.

## 🚀 Future Ideas

Want to contribute? Here are some ideas:
- [ ] GUI interface for easier setup
- [ ] Voice cloning for ultimate customization
- [ ] Shot tracking and statistics
- [ ] Club recommendations based on distance
- [ ] Multiplayer commentary (track multiple players)
- [ ] Integration with streaming (OBS overlay)
- [ ] Mobile app control
- [ ] Web interface for personality creation

## 📝 Files Overview

- `gspro_ai_announcer.py` - Main AI announcer script
- `personalities.json` - Personality definitions
- `personality_creator.py` - Tool to create custom personalities
- `requirements.txt` - Python dependencies
- `README_AI.md` - This file

## 🤝 Support & Community

Having issues? Want to share your custom personality?
- Check the troubleshooting section above
- Enable debug mode to see what's happening
- Share your custom personalities with the community!

## 📜 License

Open source - use and modify as you wish!

---

**Enjoy your AI-powered golf announcer! ⛳🎤**
