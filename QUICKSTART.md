# 🚀 QUICK START GUIDE

## Choose Your Path

### Path A: Basic Voice Caddy (5 minutes, FREE)
```bash
pip install pytesseract Pillow pyttsx3
python test_setup.py
python gspro_voice_caddy.py --debug
```
✅ Simple distance announcements
✅ Free forever
✅ No API keys needed

---

### Path B: AI Announcer (10 minutes, ~$5/year)
```bash
pip install pytesseract Pillow pyttsx3 anthropic
export ANTHROPIC_API_KEY="your-key"  # Get from https://console.anthropic.com
python demo_ai_announcer.py --mode smartass  # Test it first!
python gspro_ai_announcer.py --mode smartass  # Then use with GSPro
```
✅ 10+ personality modes
✅ Intelligent commentary
✅ Unlimited customization

---

## Windows Users
Just double-click:
- `install.bat` - Install everything
- `start_caddy.bat` - Run basic version
- `start_ai_announcer.bat` - Run AI version

---

## Test Without GSPro
```bash
# Test basic setup
python test_setup.py

# Demo AI personalities
python demo_ai_announcer.py --compare
```

---

## Create Custom Personality
```bash
python personality_creator.py
```

---

## Need Help?
- Check `README.md` for basic version
- Check `README_AI.md` for AI version
- Check `COMPARISON.md` to decide which to use
