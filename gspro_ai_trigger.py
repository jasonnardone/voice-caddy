"""
GSPro AI Announcer - TRIGGER-BASED VERSION
Only activates when screen changes are detected
More efficient - saves API calls and reduces cost
"""

import pytesseract
from PIL import ImageGrab, ImageChops
import pyttsx3
import re
import time
import os
import json
import hashlib
import numpy as np
from datetime import datetime
from anthropic import Anthropic

class TriggerBasedAnnouncer:
    def __init__(self, personality_mode="normal", debug_mode=False, api_key=None):
        """Initialize trigger-based announcer"""
        self.debug_mode = debug_mode
        self.personality_mode = personality_mode
        
        # Initialize Anthropic client
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        
        # Initialize TTS
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.engine.setProperty('volume', 0.9)
        
        # Game state tracking
        self.game_state = {
            'current_hole': None,
            'current_par': None,
            'current_distance': None,
            'last_distance': None,
            'wind_speed': None,
            'shots_on_hole': 0,
            'hole_history': [],
        }
        
        # Screen change detection
        self.last_screenshot = None
        self.last_screenshot_hash = None
        self.change_threshold = 5.0  # Percentage of pixels that need to change
        
        # Region of interest (ROI) for monitoring
        # These are the screen areas where golf info typically appears
        self.roi_regions = {
            'distance': None,  # Will be auto-detected or configured
            'hole_info': None,
            'wind': None,
            'full_screen': True  # Start with full screen
        }
        
        # Load personality
        self.personality_prompt = self.load_personality(personality_mode)
        
        # Stats
        self.stats = {
            'screenshots_taken': 0,
            'changes_detected': 0,
            'api_calls_made': 0,
            'start_time': time.time()
        }
        
        if self.debug_mode:
            os.makedirs('debug_screenshots', exist_ok=True)
        
        print(f"🎤 Trigger-Based AI Announcer initialized!")
        print(f"🎭 Personality: {personality_mode.upper()}")
        print(f"🎯 Trigger mode: Only announces on changes")
    
    def load_personality(self, mode):
        """Load personality from JSON"""
        if os.path.exists('personalities.json'):
            try:
                with open('personalities.json', 'r') as f:
                    data = json.load(f)
                    personalities = data.get('personalities', {})
                if mode in personalities:
                    personality = personalities[mode]
                    if 'voice_rate' in personality:
                        self.engine.setProperty('rate', personality['voice_rate'])
                    return personality['prompt']
            except Exception as e:
                if self.debug_mode:
                    print(f"⚠️  Could not load personalities.json: {e}")
        
        return """You are a professional golf announcer providing live commentary. 
Keep commentary concise (1-2 sentences max)."""
    
    def speak(self, text):
        """Speak text out loud"""
        print(f"🔊 {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def capture_screen(self, region=None):
        """Capture screen or region"""
        try:
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            self.stats['screenshots_taken'] += 1
            return screenshot
        except Exception as e:
            print(f"❌ Error capturing screen: {e}")
            return None
    
    def calculate_image_hash(self, image):
        """Calculate hash of image for quick comparison"""
        # Resize to small size for fast comparison
        small = image.resize((32, 32))
        # Convert to grayscale
        gray = small.convert('L')
        # Get pixel data
        pixels = list(gray.getdata())
        # Create hash
        hash_str = ''.join([str(int(p/32)) for p in pixels])
        return hashlib.md5(hash_str.encode()).hexdigest()
    
    def detect_screen_change(self, current_screenshot):
        """Detect if screen has changed significantly"""
        if self.last_screenshot is None:
            self.last_screenshot = current_screenshot
            self.last_screenshot_hash = self.calculate_image_hash(current_screenshot)
            return True, 100.0  # First run always triggers
        
        # Quick hash comparison first
        current_hash = self.calculate_image_hash(current_screenshot)
        if current_hash == self.last_screenshot_hash:
            return False, 0.0  # No change at all
        
        # If hash differs, calculate actual difference
        try:
            # Resize for faster comparison
            size = (400, 300)
            img1 = self.last_screenshot.resize(size)
            img2 = current_screenshot.resize(size)
            
            # Calculate difference
            diff = ImageChops.difference(img1, img2)
            diff_array = np.array(diff)
            
            # Calculate percentage of changed pixels
            changed_pixels = np.sum(diff_array > 20)  # Threshold for "changed"
            total_pixels = diff_array.size
            change_percentage = (changed_pixels / total_pixels) * 100
            
            if self.debug_mode:
                print(f"📊 Change detected: {change_percentage:.2f}% of pixels changed")
            
            # Update last screenshot if significant change
            if change_percentage >= self.change_threshold:
                self.last_screenshot = current_screenshot
                self.last_screenshot_hash = current_hash
                self.stats['changes_detected'] += 1
                
                # Save change image if debug
                if self.debug_mode:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    current_screenshot.save(f'debug_screenshots/change_{timestamp}.png')
                    diff.save(f'debug_screenshots/diff_{timestamp}.png')
                
                return True, change_percentage
            
            return False, change_percentage
            
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️  Error in change detection: {e}")
            return True, 0.0  # Assume change on error
    
    def ocr_screen(self, screenshot):
        """Perform OCR on screenshot"""
        try:
            text = pytesseract.image_to_string(screenshot)
            if self.debug_mode:
                print("\n" + "="*50)
                print("📝 OCR OUTPUT:")
                print(text[:300])
                print("="*50 + "\n")
            return text
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return ""
    
    def parse_game_state(self, text):
        """Extract game information from OCR text"""
        changes = []
        
        # Distance
        distance_match = re.search(r'(\d{1,3})\s*(?:yards?|yds?|Y)', text, re.IGNORECASE)
        if distance_match:
            new_distance = distance_match.group(1)
            if new_distance != self.game_state['current_distance']:
                self.game_state['last_distance'] = self.game_state['current_distance']
                self.game_state['current_distance'] = new_distance
                changes.append(('distance', new_distance))
        
        # Hole
        hole_match = re.search(r'hole[:\s]*(\d{1,2})', text, re.IGNORECASE)
        if hole_match:
            new_hole = hole_match.group(1)
            if new_hole != self.game_state['current_hole']:
                if self.game_state['current_hole']:
                    self.game_state['hole_history'].append({
                        'hole': self.game_state['current_hole'],
                        'shots': self.game_state['shots_on_hole']
                    })
                self.game_state['current_hole'] = new_hole
                self.game_state['shots_on_hole'] = 0
                changes.append(('hole', new_hole))
        
        # Par
        par_match = re.search(r'par[:\s]*(\d)', text, re.IGNORECASE)
        if par_match:
            new_par = par_match.group(1)
            if new_par != self.game_state['current_par']:
                self.game_state['current_par'] = new_par
                changes.append(('par', new_par))
        
        # Wind
        wind_match = re.search(r'(\d{1,2})\s*mph', text, re.IGNORECASE)
        if wind_match:
            new_wind = wind_match.group(1)
            if new_wind != self.game_state['wind_speed']:
                self.game_state['wind_speed'] = new_wind
                if int(new_wind) >= 10:  # Only announce significant wind
                    changes.append(('wind', new_wind))
        
        # Detect shot (distance changed significantly)
        if (self.game_state['current_distance'] and 
            self.game_state['last_distance']):
            try:
                dist_change = abs(int(self.game_state['current_distance']) - 
                                int(self.game_state['last_distance']))
                if dist_change > 20:
                    self.game_state['shots_on_hole'] += 1
                    changes.append(('shot', self.game_state['shots_on_hole']))
            except:
                pass
        
        return changes
    
    def build_context_from_changes(self, changes):
        """Build context message for AI based on what changed"""
        if not changes:
            return None
        
        gs = self.game_state
        context_parts = []
        
        for change_type, value in changes:
            if change_type == 'hole':
                msg = f"New hole #{value}"
                if gs['current_par']:
                    msg += f", par {gs['current_par']}"
                if gs['current_distance']:
                    msg += f", {gs['current_distance']} yards"
                context_parts.append(msg)
            
            elif change_type == 'distance':
                msg = f"Current distance: {value} yards"
                if gs['shots_on_hole'] > 0:
                    msg += f" (shot #{gs['shots_on_hole']} on this hole)"
                context_parts.append(msg)
            
            elif change_type == 'wind':
                context_parts.append(f"Wind: {value} mph")
        
        if not context_parts:
            return None
        
        context = "Golf situation: " + ". ".join(context_parts)
        context += "\n\nProvide brief announcer commentary (1-2 sentences max). Be entertaining."
        
        return context
    
    def generate_commentary(self, context):
        """Generate AI commentary"""
        if not context:
            return None
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                temperature=0.8,
                system=self.personality_prompt,
                messages=[{"role": "user", "content": context}]
            )
            
            self.stats['api_calls_made'] += 1
            commentary = message.content[0].text.strip()
            
            if self.debug_mode:
                print(f"\n🤖 AI: {commentary}\n")
            
            return commentary
            
        except Exception as e:
            print(f"❌ AI error: {e}")
            return None
    
    def print_stats(self):
        """Print efficiency statistics"""
        runtime = time.time() - self.stats['start_time']
        runtime_min = runtime / 60
        
        print("\n" + "="*60)
        print("📊 EFFICIENCY STATS")
        print("="*60)
        print(f"⏱️  Runtime: {runtime_min:.1f} minutes")
        print(f"📸 Screenshots: {self.stats['screenshots_taken']}")
        print(f"🎯 Changes detected: {self.stats['changes_detected']}")
        print(f"🤖 API calls: {self.stats['api_calls_made']}")
        print(f"💰 Estimated cost: ${self.stats['api_calls_made'] * 0.0001:.4f}")
        
        if self.stats['screenshots_taken'] > 0:
            trigger_rate = (self.stats['changes_detected'] / 
                          self.stats['screenshots_taken']) * 100
            print(f"⚡ Trigger efficiency: {trigger_rate:.1f}%")
            print(f"   (Only {self.stats['changes_detected']} of "
                  f"{self.stats['screenshots_taken']} screenshots triggered)")
        
        print("="*60 + "\n")
    
    def run(self, check_interval=1.0):
        """Main loop - check for changes at interval"""
        print("\n" + "="*60)
        print("🏌️  TRIGGER-BASED AI ANNOUNCER - ACTIVE")
        print("="*60)
        print(f"🎭 Mode: {self.personality_mode.upper()}")
        print(f"🔍 Checking for changes every {check_interval} second(s)")
        print(f"🎯 Trigger threshold: {self.change_threshold}% screen change")
        print(f"💰 Only makes API calls when changes detected")
        print("⌨️  Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        try:
            while True:
                # Capture screen
                screenshot = self.capture_screen()
                if screenshot is None:
                    time.sleep(check_interval)
                    continue
                
                # Check if screen changed
                changed, change_pct = self.detect_screen_change(screenshot)
                
                if changed:
                    print(f"\n🎯 TRIGGER! Screen changed {change_pct:.1f}%")
                    
                    # Perform OCR only on change
                    text = self.ocr_screen(screenshot)
                    
                    # Parse what changed
                    changes = self.parse_game_state(text)
                    
                    if changes:
                        print(f"📋 Changes: {changes}")
                        
                        # Build context and generate commentary
                        context = self.build_context_from_changes(changes)
                        if context:
                            commentary = self.generate_commentary(context)
                            if commentary:
                                self.speak(commentary)
                else:
                    # No change - just wait
                    if self.debug_mode:
                        print(".", end="", flush=True)
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n⛳ Stopping AI Announcer...")
            self.print_stats()
            print("Thanks for playing! 🏌️")


def main():
    """Entry point"""
    import argparse
    
    # Load available personalities
    available_modes = ['normal', 'smartass', 'hype', 'zen', 'pirate', 'british']
    
    if os.path.exists('personalities.json'):
        try:
            with open('personalities.json', 'r') as f:
                data = json.load(f)
                available_modes = list(data.get('personalities', {}).keys())
        except:
            pass
    
    parser = argparse.ArgumentParser(
        description='GSPro Trigger-Based AI Announcer - Efficient commentary',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
TRIGGER MODE - Only activates when screen changes!
- Saves API calls (lower cost)
- More efficient
- Still catches all important changes

Examples:
  python gspro_ai_trigger.py --mode smartass
  python gspro_ai_trigger.py --mode hype --threshold 3.0
  python gspro_ai_trigger.py --mode zen --interval 0.5 --debug
        """
    )
    
    parser.add_argument('--mode', type=str, default='normal',
                        choices=available_modes,
                        help='Announcer personality mode')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Seconds between change checks (default: 1.0)')
    parser.add_argument('--threshold', type=float, default=5.0,
                        help='Change threshold percentage (default: 5.0)')
    parser.add_argument('--api-key', type=str,
                        help='Anthropic API key')
    
    args = parser.parse_args()
    
    # Check for API key
    if not args.api_key and not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Anthropic API key required!")
        print("\nSet it via:")
        print("  export ANTHROPIC_API_KEY='your-key'")
        print("\nGet your key at: https://console.anthropic.com/")
        return
    
    # Initialize
    announcer = TriggerBasedAnnouncer(
        personality_mode=args.mode,
        debug_mode=args.debug,
        api_key=args.api_key
    )
    
    # Set threshold if specified
    if args.threshold:
        announcer.change_threshold = args.threshold
        print(f"🎯 Change threshold set to: {args.threshold}%")
    
    # Run
    announcer.run(check_interval=args.interval)


if __name__ == "__main__":
    main()
