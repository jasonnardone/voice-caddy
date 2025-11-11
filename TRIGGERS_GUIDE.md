# 🎯 Trigger-Based AI Announcer Guide

## Why Use Triggers?

The **original version** checks the screen every 2-3 seconds and makes an API call each time.
- 📊 ~1200 checks per hour
- 💰 ~1200 API calls per hour = ~$0.12/hour

The **trigger version** only activates when the screen actually changes.
- 📊 ~3600 checks per hour (faster checks)
- 💰 ~10-30 API calls per hour = ~$0.003/hour
- 💰 **40x cheaper!** ⚡

---

## 🚀 Quick Start

### Basic Trigger Mode
```bash
python gspro_ai_trigger.py --mode smartass
```

### With Debug (see what's triggering)
```bash
python gspro_ai_trigger.py --mode smartass --debug
```

### Adjust Sensitivity
```bash
# More sensitive (trigger on smaller changes)
python gspro_ai_trigger.py --mode smartass --threshold 2.0

# Less sensitive (only major changes)
python gspro_ai_trigger.py --mode smartass --threshold 10.0
```

### Faster Checking
```bash
# Check every 0.5 seconds (default is 1.0)
python gspro_ai_trigger.py --mode smartass --interval 0.5
```

---

## 🎯 How Triggers Work

### Change Detection Process

1. **Take Screenshot** (every 0.5-1 second)
2. **Calculate Hash** (quick fingerprint of image)
3. **Compare to Last Screenshot**
   - If hash same → No change, skip everything
   - If hash different → Calculate actual difference
4. **If Change >= Threshold** → TRIGGER!
   - Run OCR
   - Parse game state
   - Generate AI commentary
   - Speak announcement

### What Triggers an Announcement?

✅ **Always Triggers:**
- New hole
- Distance change > 20 yards
- Wind change (if >= 10 mph)

❌ **Never Triggers:**
- Ball animation (no text change)
- Camera movement (same info displayed)
- Background changes (grass, trees, etc.)

---

## ⚙️ Configuration

### Basic Settings (Command Line)

```bash
# Change threshold (% of screen that must change)
--threshold 5.0    # Default: 5% of pixels must change

# Check interval (seconds between checks)
--interval 1.0     # Default: check every 1 second

# Debug mode
--debug           # Show what's being detected
```

### Advanced Settings (trigger_config.json)

```json
{
  "trigger_settings": {
    "change_threshold": 5.0,
    "check_interval": 1.0
  },
  
  "distance_triggers": {
    "enabled": true,
    "min_change": 20
  },
  
  "wind_triggers": {
    "enabled": true,
    "min_wind_mph": 10
  }
}
```

---

## 🎯 ROI (Region of Interest) Mode

**Even more efficient!** Monitor only specific screen areas.

### Why Use ROI?

Instead of checking the entire screen, only monitor:
- Distance display area
- Hole info panel
- Wind indicator
- Player panel

**Benefits:**
- Faster change detection
- More accurate triggers
- Lower CPU usage
- Ignores irrelevant screen areas

### Setup ROI

#### Option 1: Quick Setup (Default Regions)
```bash
python roi_calibrator.py
# Choose option 1: Quick Calibration
```

#### Option 2: Custom Regions
```bash
python roi_calibrator.py
# Choose option 2: Interactive Calibration
# Follow prompts to define your regions
```

#### Option 3: Manual Configuration

Edit `trigger_config.json`:
```json
{
  "regions_of_interest": {
    "enabled": true,
    "regions": {
      "distance_display": {
        "enabled": true,
        "bbox": [800, 100, 1100, 200],
        "description": "Distance to pin area"
      },
      "hole_info": {
        "enabled": true,
        "bbox": [50, 50, 300, 150],
        "description": "Hole number and par"
      }
    }
  }
}
```

**Finding Coordinates:**
1. Take a screenshot
2. Open in paint/photoshop
3. Hover over corners to get coordinates
4. Format: [left, top, right, bottom]

---

## 📊 Efficiency Comparison

### Full Screen Monitoring
```
Hour: 3600 checks
Changes: ~30 detected
API Calls: ~30
Cost: ~$0.003/hour
```

### ROI Monitoring
```
Hour: 3600 checks (even faster!)
Changes: ~25 detected (more accurate)
API Calls: ~25
Cost: ~$0.0025/hour
CPU: 50% lower
```

---

## 🔧 Troubleshooting

### Not Triggering Enough

**Problem:** Missing some announcements

**Solutions:**
```bash
# Lower threshold (more sensitive)
python gspro_ai_trigger.py --threshold 2.0

# Check faster
python gspro_ai_trigger.py --interval 0.5

# Debug to see what's detected
python gspro_ai_trigger.py --debug
```

### Triggering Too Much

**Problem:** Announces on small changes

**Solutions:**
```bash
# Higher threshold (less sensitive)
python gspro_ai_trigger.py --threshold 10.0

# Use ROI to ignore irrelevant areas
python roi_calibrator.py
```

### OCR Not Reading Text

**Problem:** Triggers but doesn't announce

**Solutions:**
1. Check if text is visible in debug screenshots
2. Adjust GSPro UI scale (make text bigger)
3. Ensure window is not minimized
4. Try ROI to focus on text areas only

---

## 💰 Cost Control

### Built-in Limits

The trigger version includes cost controls:
```json
{
  "cost_control": {
    "max_api_calls_per_round": 50,
    "warning_at_calls": 40
  }
}
```

### Monitor Usage

At the end of each session:
```
📊 EFFICIENCY STATS
⏱️  Runtime: 45.2 minutes
📸 Screenshots: 2712
🎯 Changes detected: 28
🤖 API calls: 28
💰 Estimated cost: $0.0028
⚡ Trigger efficiency: 1.0%
   (Only 28 of 2712 screenshots triggered)
```

### Typical Costs

**18-hole round:**
- Continuous mode: ~$0.15-0.30
- Trigger mode: ~$0.01-0.03
- **Savings: ~90%** 💰

---

## 🎮 Usage Patterns

### Practice Session (1 hour)
```bash
# Efficient mode
python gspro_ai_trigger.py --mode normal --threshold 5.0

Expected:
- ~20-30 API calls
- Cost: ~$0.003
```

### Competitive Round (2 hours)
```bash
# Don't miss any changes
python gspro_ai_trigger.py --mode smartass --threshold 2.0 --interval 0.5

Expected:
- ~40-60 API calls
- Cost: ~$0.006
```

### Streaming/Content (3 hours)
```bash
# Maximum entertainment
python gspro_ai_trigger.py --mode hype --threshold 3.0

Expected:
- ~60-90 API calls
- Cost: ~$0.009
```

---

## 🧪 Testing

### Test Without GSPro

```bash
# Test the trigger system
python gspro_ai_trigger.py --mode smartass --debug

# Watch debug output to see:
# - When triggers fire
# - What changes detected
# - What commentary generated
```

### Benchmark Your Settings

```bash
# Run for 5 minutes and check stats
python gspro_ai_trigger.py --mode normal --debug
# Ctrl+C after 5 minutes
# Review efficiency stats
```

---

## 📈 Optimization Tips

### For Best Efficiency

1. **Use ROI**: Define specific regions
2. **Adjust Threshold**: Find sweet spot (3-7%)
3. **Reasonable Interval**: 0.5-1.5 seconds
4. **Monitor Stats**: Check efficiency after rounds

### For Best Experience

1. **Lower Threshold**: Catch more changes (2-3%)
2. **Faster Checks**: 0.5 second interval
3. **Full Screen**: Don't use ROI if you want to catch everything
4. **Debug Mode**: See what's happening

---

## 🎯 Recommended Settings

### Beginner (Learning)
```bash
python gspro_ai_trigger.py --mode normal --threshold 5.0 --interval 1.0
```

### Balanced (Best for most)
```bash
python gspro_ai_trigger.py --mode smartass --threshold 3.0 --interval 0.75
```

### Maximum Entertainment
```bash
python gspro_ai_trigger.py --mode hype --threshold 2.0 --interval 0.5
```

### Ultra Efficient (Minimize cost)
```bash
python gspro_ai_trigger.py --mode zen --threshold 7.0 --interval 1.5
# Plus ROI regions configured
```

---

## 🆚 Comparison: Continuous vs Trigger

| Aspect | Continuous | Trigger |
|--------|-----------|---------|
| **Checks/hour** | 1200 | 3600 |
| **API calls/hour** | 1200 | 20-30 |
| **Cost/hour** | $0.12 | $0.003 |
| **CPU usage** | Medium | Low |
| **Accuracy** | Good | Excellent |
| **Miss chances** | None | Very rare |
| **Best for** | Guaranteed catch | Efficiency |

---

## 🚀 Next Level: Combined ROI + Triggers

```bash
# 1. Calibrate ROI
python roi_calibrator.py

# 2. Run with optimized settings
python gspro_ai_trigger.py --mode smartass --threshold 3.0

# Results:
# - Only checks relevant screen areas
# - Triggers only on actual changes
# - Ignores animations, camera moves, etc.
# - ~95% reduction in API calls vs continuous
```

---

## 📝 Quick Reference

### Start Commands
```bash
# Basic
python gspro_ai_trigger.py --mode smartass

# With ROI
python roi_calibrator.py  # First time setup
python gspro_ai_trigger.py --mode smartass

# Debug
python gspro_ai_trigger.py --mode smartass --debug

# Custom sensitivity
python gspro_ai_trigger.py --mode smartass --threshold 3.0 --interval 0.5
```

### Files
- `gspro_ai_trigger.py` - Main trigger-based script
- `trigger_config.json` - Configuration file
- `roi_calibrator.py` - ROI setup tool

---

**Ready to save 90% on API costs? Use trigger mode! 🎯💰**
