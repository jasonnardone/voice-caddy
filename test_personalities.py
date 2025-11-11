"""
Personality Tester - Preview different AI caddy personalities
Tests each personality with sample golf scenarios
"""

import os
import sys
import json

try:
    import anthropic
except ImportError:
    print("❌ Error: anthropic package not installed")
    print("Run: pip install anthropic")
    sys.exit(1)

# Load personalities from JSON file
def load_personalities():
    """Load personalities from personalities.json"""
    json_path = os.path.join(os.path.dirname(__file__), 'personalities.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data['personalities']

CADDY_PERSONALITIES = load_personalities()


def test_personality(client, personality_name, scenario):
    """Test a personality with a given scenario"""
    personality = CADDY_PERSONALITIES[personality_name]
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            system=personality['prompt'],
            messages=[
                {"role": "user", "content": f"Current situation: {scenario}\n\nGenerate a short caddy comment (1-2 sentences max) about this shot. Be in character."}
            ]
        )

        return message.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


def main():
    """Test all personalities with sample scenarios"""
    
    # Get API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set!")
        print("\nSet it with:")
        print("  Windows: set ANTHROPIC_API_KEY=your_key_here")
        print("  Mac/Linux: export ANTHROPIC_API_KEY=your_key_here")
        print("\nGet your key at: https://console.anthropic.com/")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Test scenarios
    scenarios = [
        {
            "name": "Difficult Shot from Rough",
            "context": "Hole 7, Par 4. 185 yards to pin. You're in the deep rough. Wind at 12 mph. Last shot was a slice into the rough."
        },
        {
            "name": "Easy Green-Side Shot",
            "context": "Hole 3, Par 5. 45 yards to pin. On the fairway. No wind. You've been playing well today."
        },
        {
            "name": "Long Drive Opportunity",
            "context": "Hole 11, Par 5. 520 yards to pin. On the tee. Slight tailwind at 5 mph. Wide open fairway."
        },
        {
            "name": "Tricky Putt",
            "context": "Hole 18, Par 3. 15 feet to pin. On the green with significant break. You've missed the last 3 putts."
        }
    ]
    
    print("\n" + "="*70)
    print("🎭 AI CADDY PERSONALITY TESTER")
    print("="*70)
    print("\nTesting all personalities with different golf scenarios...")
    print("This helps you choose which personality you'll enjoy most!")
    print()
    
    for scenario in scenarios:
        print("\n" + "="*70)
        print(f"⛳ SCENARIO: {scenario['name']}")
        print("="*70)
        print(f"📍 {scenario['context']}")
        print()
        
        for personality_name, personality_config in CADDY_PERSONALITIES.items():
            print(f"🎭 {personality_config['name'].upper()}:")
            print("   ", end="")
            
            response = test_personality(client, personality_name, scenario['context'])
            print(response)
            print()
    
    print("="*70)
    print("✅ Testing complete!")
    print("\nTo use your favorite personality:")
    print("  python gspro_ai_caddy.py --personality PERSONALITY_NAME")
    print("\nExamples:")
    print("  python gspro_ai_caddy.py --personality smartass")
    print("  python gspro_ai_caddy.py --personality encouraging")
    print("  python gspro_ai_caddy.py --personality drunk")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
