"""
GSPro AI Announcer - Voice commentary with personality
Uses Claude API for intelligent, contextual golf commentary
"""

import pytesseract
from PIL import ImageGrab
import pyttsx3
import re
import time
import os
import json
from datetime import datetime
from anthropic import Anthropic

# Configure Tesseract path for Windows
# If Tesseract is installed in the default location, set the path
if os.name == 'nt':  # Windows
    tesseract_path = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

class GSProAIAnnouncer:
    def __init__(self, personality_mode="normal", debug_mode=False, api_key=None):
        """Initialize the AI announcer"""
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
            'last_announced': None
        }
        
        # Conversation history for context
        self.conversation_history = []
        
        # Load personality
        self.personality_prompt = self.load_personality(personality_mode)
        
        # Create debug folder
        if self.debug_mode:
            os.makedirs('debug_screenshots', exist_ok=True)
        
        print(f"🎤 GSPro AI Announcer initialized!")
        print(f"🎭 Personality mode: {personality_mode.upper()}")
        print(f"🤖 Using Claude AI for commentary")
    
    def load_personality(self, mode):
        """Load personality prompt based on mode"""
        # Try to load from personalities.json first
        if os.path.exists('personalities.json'):
            try:
                with open('personalities.json', 'r') as f:
                    data = json.load(f)
                    personalities = data.get('personalities', {})
                    
                if mode in personalities:
                    personality = personalities[mode]
                    
                    # Set voice rate if specified
                    if 'voice_rate' in personality:
                        self.engine.setProperty('rate', personality['voice_rate'])
                    
                    return personality['prompt']
            except Exception as e:
                print(f"⚠️  Warning: Could not load personalities.json: {e}")
        
        # Fallback to built-in default
        return """You are a professional golf announcer providing live commentary. 
Your style is informative, enthusiastic, and respectful. 
Keep commentary concise (1-2 sentences max). 
Focus on the shot at hand and provide helpful context."""
    
    def speak(self, text):
        """Speak text out loud"""
        print(f"🔊 {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def capture_screen(self):
        """Capture the full screen"""
        try:
            screenshot = ImageGrab.grab()
            if self.debug_mode:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot.save(f'debug_screenshots/screen_{timestamp}.png')
            return screenshot
        except Exception as e:
            print(f"❌ Error capturing screen: {e}")
            return None
    
    def ocr_screen(self, screenshot):
        """Perform OCR on screenshot"""
        try:
            text = pytesseract.image_to_string(screenshot)
            if self.debug_mode:
                print("\n" + "="*50)
                print("📝 OCR OUTPUT:")
                print(text[:500])
                print("="*50 + "\n")
            return text
        except Exception as e:
            print(f"❌ Error performing OCR: {e}")
            return ""
    
    def parse_game_state(self, text):
        """Extract all game information from text"""
        # Distance
        distance_match = re.search(r'(\d{1,3})\s*(?:yards?|yds?|Y)', text, re.IGNORECASE)
        if distance_match:
            self.game_state['last_distance'] = self.game_state['current_distance']
            self.game_state['current_distance'] = distance_match.group(1)
        
        # Hole number
        hole_match = re.search(r'hole[:\s]*(\d{1,2})', text, re.IGNORECASE)
        if hole_match:
            new_hole = hole_match.group(1)
            if new_hole != self.game_state['current_hole']:
                # New hole
                if self.game_state['current_hole']:
                    self.game_state['hole_history'].append({
                        'hole': self.game_state['current_hole'],
                        'shots': self.game_state['shots_on_hole']
                    })
                self.game_state['current_hole'] = new_hole
                self.game_state['shots_on_hole'] = 0
        
        # Par
        par_match = re.search(r'par[:\s]*(\d)', text, re.IGNORECASE)
        if par_match:
            self.game_state['current_par'] = par_match.group(1)
        
        # Wind
        wind_match = re.search(r'(\d{1,2})\s*mph', text, re.IGNORECASE)
        if wind_match:
            self.game_state['wind_speed'] = wind_match.group(1)
        
        # Detect shot (distance changed significantly)
        if (self.game_state['current_distance'] and 
            self.game_state['last_distance'] and
            abs(int(self.game_state['current_distance']) - int(self.game_state['last_distance'])) > 20):
            self.game_state['shots_on_hole'] += 1
    
    def generate_commentary(self):
        """Generate AI commentary based on game state"""
        # Build context message
        context = self.build_context_message()
        
        if not context:
            return None
        
        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                temperature=0.8,
                system=self.personality_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": context
                    }
                ]
            )
            
            commentary = message.content[0].text.strip()
            
            if self.debug_mode:
                print(f"\n🤖 AI Generated: {commentary}\n")
            
            return commentary
            
        except Exception as e:
            print(f"❌ Error generating commentary: {e}")
            return None
    
    def build_context_message(self):
        """Build context message for AI based on game state"""
        gs = self.game_state
        
        # Determine what changed and needs commentary
        messages = []
        
        # New hole announcement
        if gs['current_hole'] and gs['current_hole'] != gs.get('last_announced_hole'):
            msg = f"New hole #{gs['current_hole']}"
            if gs['current_par']:
                msg += f", par {gs['current_par']}"
            if gs['current_distance']:
                msg += f", {gs['current_distance']} yards"
            messages.append(msg)
            gs['last_announced_hole'] = gs['current_hole']
        
        # Distance update (if changed significantly and not a new hole)
        elif (gs['current_distance'] and 
              gs['current_distance'] != gs.get('last_announced_distance') and
              gs['current_distance'] != gs.get('last_distance')):
            msg = f"Current distance: {gs['current_distance']} yards"
            if gs['shots_on_hole'] > 0:
                msg += f" (shot #{gs['shots_on_hole']} on this hole)"
            messages.append(msg)
            gs['last_announced_distance'] = gs['current_distance']
        
        # Wind announcement (if significant and changed)
        if (gs['wind_speed'] and 
            int(gs['wind_speed']) >= 10 and
            gs['wind_speed'] != gs.get('last_announced_wind')):
            messages.append(f"Wind: {gs['wind_speed']} mph")
            gs['last_announced_wind'] = gs['wind_speed']
        
        if not messages:
            return None
        
        # Combine into prompt
        context = "Golf situation: " + ". ".join(messages)
        context += "\n\nProvide brief announcer commentary (1-2 sentences max). Be entertaining and match your personality."
        
        return context
    
    def run(self, interval=3):
        """Main loop"""
        print("\n" + "="*60)
        print("🏌️  GSPro AI ANNOUNCER - ACTIVE")
        print("="*60)
        print(f"🎭 Mode: {self.personality_mode.upper()}")
        print(f"📸 Monitoring screen every {interval} seconds")
        print("🤖 AI-powered commentary enabled")
        print("⌨️  Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        try:
            while True:
                # Capture and OCR
                screenshot = self.capture_screen()
                if screenshot is None:
                    time.sleep(interval)
                    continue
                
                text = self.ocr_screen(screenshot)
                
                # Update game state
                self.parse_game_state(text)
                
                # Generate and speak commentary
                commentary = self.generate_commentary()
                if commentary:
                    self.speak(commentary)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⛳ Stopping AI Announcer...")
            print(f"Final stats: {len(self.game_state['hole_history'])} holes tracked")
            print("Thanks for playing! 🏌️")


def main():
    """Entry point"""
    import argparse
    
    # Load available personalities
    available_modes = ['normal', 'smartass', 'hype', 'zen', 'pirate', 'british']
    personality_descriptions = {}
    
    if os.path.exists('personalities.json'):
        try:
            with open('personalities.json', 'r') as f:
                data = json.load(f)
                personalities = data.get('personalities', {})
                available_modes = list(personalities.keys())
                personality_descriptions = {
                    k: v.get('name', k) 
                    for k, v in personalities.items()
                }
        except:
            pass
    
    parser = argparse.ArgumentParser(
        description='GSPro AI Announcer - Personality-driven golf commentary',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available personality modes:
{chr(10).join(f'  {mode:15} - {personality_descriptions.get(mode, mode)}' for mode in available_modes)}

Examples:
  python gspro_ai_announcer.py --mode smartass
  python gspro_ai_announcer.py --mode hype --debug
  python gspro_ai_announcer.py --list-modes
  
Create custom personalities:
  python personality_creator.py
        """
    )
    
    parser.add_argument('--mode', type=str, default='normal',
                        choices=available_modes,
                        help='Announcer personality mode')
    parser.add_argument('--list-modes', action='store_true',
                        help='List all available personality modes')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    parser.add_argument('--interval', type=int, default=3,
                        help='Seconds between screen captures')
    parser.add_argument('--api-key', type=str,
                        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
    
    args = parser.parse_args()
    
    # List modes if requested
    if args.list_modes:
        print("\n🎭 Available Personality Modes:")
        print("="*60)
        if os.path.exists('personalities.json'):
            with open('personalities.json', 'r') as f:
                data = json.load(f)
                for mode, pdata in data['personalities'].items():
                    print(f"\n🎤 {mode.upper()}")
                    print(f"   Name: {pdata['name']}")
                    if pdata.get('examples'):
                        print(f"   Example: \"{pdata['examples'][0]}\"")
        print("\n")
        return
    
    # Check for API key
    if not args.api_key and not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Anthropic API key required!")
        print("\nSet it via:")
        print("  1. Environment variable: export ANTHROPIC_API_KEY='your-key'")
        print("  2. Command line: --api-key your-key")
        print("\nGet your API key at: https://console.anthropic.com/")
        return
    
    # Initialize and run
    announcer = GSProAIAnnouncer(
        personality_mode=args.mode,
        debug_mode=args.debug,
        api_key=args.api_key
    )
    announcer.run(interval=args.interval)


if __name__ == "__main__":
    main()
