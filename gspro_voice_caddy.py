"""
GSPro Voice Caddy - OCR-based assistant
Captures screen, reads text, and announces golf information via TTS
"""

import pytesseract
from PIL import ImageGrab, Image
import pyttsx3
import re
import time
import os
from datetime import datetime

class GSProVoiceCaddy:
    def __init__(self, debug_mode=False):
        """Initialize the voice caddy"""
        self.debug_mode = debug_mode
        self.engine = pyttsx3.init()
        
        # Configure TTS voice (adjust speed and volume)
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Track last announced values to avoid repeats
        self.last_distance = None
        self.last_wind = None
        self.last_hole = None
        
        # Create debug folder if needed
        if self.debug_mode:
            os.makedirs('debug_screenshots', exist_ok=True)
        
        print("🎤 GSPro Voice Caddy initialized!")
        print(f"Debug mode: {self.debug_mode}")
    
    def speak(self, text):
        """Speak text out loud"""
        print(f"🔊 Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def capture_screen(self):
        """Capture the full screen"""
        try:
            screenshot = ImageGrab.grab()
            
            # Save debug screenshot if enabled
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
                print("="*50)
                print(text)
                print("="*50 + "\n")
            
            return text
        except Exception as e:
            print(f"❌ Error performing OCR: {e}")
            return ""
    
    def parse_distance(self, text):
        """Extract distance to pin from text"""
        # Common patterns: "145 yards", "145Y", "145 yds", etc.
        patterns = [
            r'(\d{1,3})\s*(?:yards?|yds?|Y)\s*(?:to)?',  # "145 yards to"
            r'(?:distance|to pin)[:\s]*(\d{1,3})',         # "Distance: 145"
            r'(\d{1,3})\s*(?:yd|y)\b',                     # "145 yd"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                distance = match.group(1)
                # Sanity check (golf distances typically 0-600 yards)
                if 0 < int(distance) < 600:
                    return distance
        return None
    
    def parse_wind(self, text):
        """Extract wind information from text"""
        # Patterns: "Wind: 12 mph", "12mph", etc.
        patterns = [
            r'wind[:\s]*(\d{1,2})\s*(?:mph|m\.p\.h\.?)?',
            r'(\d{1,2})\s*mph\s*wind',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                wind_speed = match.group(1)
                if 0 <= int(wind_speed) <= 50:  # Reasonable wind speeds
                    return wind_speed
        return None
    
    def parse_hole(self, text):
        """Extract hole number from text"""
        # Pattern: "Hole 5", "Hole: 5", etc.
        match = re.search(r'hole[:\s]*(\d{1,2})', text, re.IGNORECASE)
        if match:
            hole_num = match.group(1)
            if 1 <= int(hole_num) <= 18:
                return hole_num
        return None
    
    def parse_par(self, text):
        """Extract par from text"""
        match = re.search(r'par[:\s]*(\d)', text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    
    def parse_lie(self, text):
        """Extract lie information"""
        # Look for rough, fairway, green, etc.
        lies = ['rough', 'fairway', 'green', 'bunker', 'sand', 'tee']
        text_lower = text.lower()
        for lie in lies:
            if lie in text_lower:
                return lie.title()
        return None
    
    def analyze_and_announce(self, text):
        """Parse OCR text and announce relevant information"""
        # Extract information
        distance = self.parse_distance(text)
        wind = self.parse_wind(text)
        hole = self.parse_hole(text)
        par = self.parse_par(text)
        lie = self.parse_lie(text)
        
        # Build announcement
        announcements = []
        
        # Announce hole change
        if hole and hole != self.last_hole:
            announcement = f"Hole {hole}"
            if par:
                announcement += f", par {par}"
            announcements.append(announcement)
            self.last_hole = hole
        
        # Announce distance (main info)
        if distance and distance != self.last_distance:
            announcements.append(f"{distance} yards")
            self.last_distance = distance
        
        # Announce wind if significant
        if wind and wind != self.last_wind:
            wind_val = int(wind)
            if wind_val >= 5:  # Only announce if 5+ mph
                announcements.append(f"{wind} mile per hour wind")
            self.last_wind = wind
        
        # Announce lie if detected
        if lie and self.debug_mode:
            announcements.append(f"Lie: {lie}")
        
        # Speak if we have something to say
        if announcements:
            full_announcement = ". ".join(announcements)
            self.speak(full_announcement)
    
    def run(self, interval=2):
        """Main loop - capture, OCR, and announce"""
        print("\n" + "="*60)
        print("🏌️  GSPro VOICE CADDY - ACTIVE")
        print("="*60)
        print("📸 Monitoring screen every {} seconds".format(interval))
        print("🎯 Will announce: Distance, Hole changes, Wind")
        print("⌨️  Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        try:
            while True:
                # Capture screen
                screenshot = self.capture_screen()
                if screenshot is None:
                    time.sleep(interval)
                    continue
                
                # Perform OCR
                text = self.ocr_screen(screenshot)
                
                # Analyze and announce
                self.analyze_and_announce(text)
                
                # Wait before next capture
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⛳ Stopping GSPro Voice Caddy...")
            print("Thanks for using Voice Caddy! Good round! 🏌️")


def main():
    """Entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GSPro Voice Caddy - OCR-based assistant')
    parser.add_argument('--debug', action='store_true', 
                        help='Enable debug mode (saves screenshots and shows OCR output)')
    parser.add_argument('--interval', type=int, default=2,
                        help='Seconds between screen captures (default: 2)')
    
    args = parser.parse_args()
    
    # Initialize and run
    caddy = GSProVoiceCaddy(debug_mode=args.debug)
    caddy.run(interval=args.interval)


if __name__ == "__main__":
    main()
