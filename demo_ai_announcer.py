"""
Demo/Test script for GSPro AI Announcer
Tests the AI commentary without needing GSPro running
Simulates various golf scenarios
"""

import os
import time
from anthropic import Anthropic
import pyttsx3
import json

class AnnouncerDemo:
    def __init__(self, personality_mode="smartass", api_key=None):
        """Initialize demo"""
        self.personality_mode = personality_mode
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        
        # Initialize TTS with error handling
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)
            self.engine.setProperty('volume', 0.9)
            self.tts_available = True
        except Exception as e:
            print(f"⚠️  Warning: TTS engine failed to initialize: {e}")
            print("📝 Will print commentary instead of speaking")
            self.engine = None
            self.tts_available = False
        
        # Load personality
        self.personality_prompt = self.load_personality(personality_mode)
        
        print(f"🎭 Testing {personality_mode.upper()} mode")
        if not self.tts_available:
            print("⚠️  TTS disabled - commentary will be printed only")
    
    def load_personality(self, mode):
        """Load personality from JSON"""
        if os.path.exists('personalities.json'):
            with open('personalities.json', 'r') as f:
                data = json.load(f)
                personalities = data.get('personalities', {})
                if mode in personalities:
                    return personalities[mode]['prompt']
        return "Professional golf announcer. 1-2 sentences max."
    
    def speak(self, text):
        """Speak text"""
        print(f"\n🔊 {text}")
        
        if self.tts_available and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"⚠️  TTS error: {e}")
                print("📝 (Commentary printed above)")
        else:
            print("📝 (TTS not available - commentary printed only)")
    
    def get_commentary(self, scenario):
        """Generate AI commentary for scenario"""
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                temperature=0.8,
                system=self.personality_prompt,
                messages=[{"role": "user", "content": scenario}]
            )
            return message.content[0].text.strip()
        except Exception as e:
            return f"Error: {e}"
    
    def demo_scenarios(self):
        """Run through demo scenarios"""
        scenarios = [
            {
                "name": "Opening Tee",
                "context": "New hole #1, par 4, 387 yards. First shot of the round."
            },
            {
                "name": "Good Position",
                "context": "Current distance: 145 yards. Perfect wedge distance. Second shot on hole."
            },
            {
                "name": "Trouble",
                "context": "Current distance: 200 yards. Third shot on a par 4. Things not going well."
            },
            {
                "name": "Windy Conditions",
                "context": "Current distance: 165 yards. Wind: 18 mph crosswind. Challenging conditions."
            },
            {
                "name": "Short Game",
                "context": "Current distance: 50 yards. Fourth shot on par 4. Need to get up and down."
            },
            {
                "name": "New Hole - Easy",
                "context": "New hole #3, par 3, 147 yards. Should be makeable."
            },
            {
                "name": "New Hole - Monster",
                "context": "New hole #8, par 5, 587 yards. The longest hole on the course."
            },
            {
                "name": "Pressure Putt",
                "context": "Current distance: 15 yards. On the green for potential birdie. Don't mess it up."
            }
        ]
        
        print("\n" + "="*60)
        print("🏌️  AI ANNOUNCER DEMO - TESTING SCENARIOS")
        print("="*60)
        print(f"Mode: {self.personality_mode.upper()}")
        print("="*60 + "\n")
        
        for i, scenario in enumerate(scenarios, 1):
            try:
                print(f"\n{'='*60}")
                print(f"Scenario {i}/{len(scenarios)}: {scenario['name']}")
                print(f"{'='*60}")
                print(f"📋 Context: {scenario['context']}")
                
                # Generate commentary
                print("🤖 Generating commentary...")
                commentary = self.get_commentary(
                    f"Golf situation: {scenario['context']}\n\n"
                    "Provide brief announcer commentary (1-2 sentences max). "
                    "Be entertaining and match your personality."
                )
                
                # Speak it
                if commentary:
                    self.speak(commentary)
                else:
                    print("⚠️  No commentary generated")
                
                # Pause between scenarios
                if i < len(scenarios):
                    print("\n⏸️  Pausing before next scenario...")
                    time.sleep(2)
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Demo interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error in scenario {i}: {e}")
                continue
        
        print("\n" + "="*60)
        print("✅ Demo complete!")
        print(f"Completed {i} of {len(scenarios)} scenarios")
        print("="*60)


def compare_personalities():
    """Compare different personalities on same scenario"""
    scenario = "Current distance: 145 yards. Second shot on a par 4."
    
    personalities = ['normal', 'smartass', 'hype', 'zen', 'pirate', 'british']
    
    print("\n" + "="*60)
    print("🎭 PERSONALITY COMPARISON")
    print("="*60)
    print(f"Scenario: {scenario}")
    print("="*60 + "\n")
    
    for personality in personalities:
        print(f"\n{'='*60}")
        print(f"🎤 {personality.upper()} MODE")
        print("="*60)
        
        try:
            demo = AnnouncerDemo(personality_mode=personality)
            commentary = demo.get_commentary(
                f"Golf situation: {scenario}\n\n"
                "Provide brief announcer commentary (1-2 sentences max)."
            )
            print(f"💬 {commentary}")
            demo.speak(commentary)
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main demo menu"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Demo/Test the AI Announcer')
    parser.add_argument('--mode', type=str, default='smartass',
                        help='Personality mode to test')
    parser.add_argument('--compare', action='store_true',
                        help='Compare all personalities on same scenario')
    parser.add_argument('--no-speech', action='store_true',
                        help='Skip text-to-speech (print only - faster testing)')
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
    
    if args.compare:
        compare_personalities(no_speech=args.no_speech)
    else:
        demo = AnnouncerDemo(personality_mode=args.mode, api_key=args.api_key)
        if args.no_speech:
            demo.tts_available = False
            print("📝 TTS disabled - commentary will be printed only (faster)")
        demo.demo_scenarios()


if __name__ == "__main__":
    main()