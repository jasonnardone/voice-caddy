"""
Test script to verify OCR and TTS setup
Run this BEFORE trying the full voice caddy
"""

import sys

def test_imports():
    """Test if all required libraries are installed"""
    print("="*60)
    print("🧪 Testing imports...")
    print("="*60)
    
    try:
        import pytesseract
        print("✅ pytesseract imported successfully")
    except ImportError:
        print("❌ pytesseract not found. Run: pip install pytesseract")
        return False
    
    try:
        from PIL import Image, ImageGrab
        print("✅ Pillow (PIL) imported successfully")
    except ImportError:
        print("❌ Pillow not found. Run: pip install Pillow")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError:
        print("❌ pyttsx3 not found. Run: pip install pyttsx3")
        return False
    
    print()
    return True


def test_tesseract():
    """Test if Tesseract OCR is installed and accessible"""
    print("="*60)
    print("🔍 Testing Tesseract OCR...")
    print("="*60)
    
    import pytesseract
    from PIL import Image

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\tesseract.exe'
    
    try:
        # Try to get version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
        print()
        return True
    except Exception as e:
        print(f"❌ Tesseract not found or not in PATH")
        print(f"Error: {e}")
        print()
        print("📋 Installation instructions:")
        print("Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("Mac: brew install tesseract")
        print("Linux: sudo apt-get install tesseract-ocr")
        print()
        print("If already installed, add to PATH or specify location in code:")
        print("pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        print()
        return False


def test_tts():
    """Test text-to-speech"""
    print("="*60)
    print("🔊 Testing Text-to-Speech...")
    print("="*60)
    
    import pyttsx3
    
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        print("✅ TTS engine initialized")
        print("🔊 You should hear: 'Testing voice caddy'")
        
        engine.say("Testing voice caddy. One hundred and forty five yards.")
        engine.runAndWait()
        
        print("✅ TTS test complete")
        print()
        return True
    except Exception as e:
        print(f"❌ TTS error: {e}")
        print()
        return False


def test_screen_capture():
    """Test screen capture"""
    print("="*60)
    print("📸 Testing Screen Capture...")
    print("="*60)
    
    from PIL import ImageGrab
    
    try:
        screenshot = ImageGrab.grab()
        width, height = screenshot.size
        print(f"✅ Screen captured: {width}x{height} pixels")
        
        # Save test screenshot
        screenshot.save('test_screenshot.png')
        print("✅ Screenshot saved as 'test_screenshot.png'")
        print()
        return True
    except Exception as e:
        print(f"❌ Screen capture error: {e}")
        print()
        return False


def test_ocr_on_screen():
    """Capture screen and test OCR on it"""
    print("="*60)
    print("🔬 Testing OCR on current screen...")
    print("="*60)
    print("⚠️  Make sure you have some text visible on your screen!")
    print()
    
    import pytesseract
    from PIL import ImageGrab
    import time
    
    print("Capturing screen in 3 seconds...")
    time.sleep(3)
    
    try:
        screenshot = ImageGrab.grab()
        text = pytesseract.image_to_string(screenshot)
        
        print("✅ OCR completed!")
        print()
        print("📝 Text detected on screen:")
        print("-" * 60)
        print(text[:500])  # Print first 500 characters
        if len(text) > 500:
            print("... (truncated)")
        print("-" * 60)
        print()
        
        if len(text.strip()) > 10:
            print("✅ OCR is working! Text was detected.")
            return True
        else:
            print("⚠️  Very little text detected. Make sure:")
            print("   - There is readable text on screen")
            print("   - Text is not too small")
            print("   - Screen is not blank")
            return False
            
    except Exception as e:
        print(f"❌ OCR test failed: {e}")
        print()
        return False


def test_distance_parsing():
    """Test the distance parsing logic"""
    print("="*60)
    print("🎯 Testing Distance Parsing...")
    print("="*60)
    
    import re
    
    def parse_distance(text):
        patterns = [
            r'(\d{1,3})\s*(?:yards?|yds?|Y)\s*(?:to)?',
            r'(?:distance|to pin)[:\s]*(\d{1,3})',
            r'(\d{1,3})\s*(?:yd|y)\b',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                distance = match.group(1)
                if 0 < int(distance) < 600:
                    return distance
        return None
    
    test_cases = [
        ("145 yards to pin", "145"),
        ("Distance: 234", "234"),
        ("387Y", "387"),
        ("52 yds", "52"),
        ("No distance here", None),
    ]
    
    all_passed = True
    for test_input, expected in test_cases:
        result = parse_distance(test_input)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{test_input}' → {result} (expected: {expected})")
        if result != expected:
            all_passed = False
    
    print()
    if all_passed:
        print("✅ All parsing tests passed!")
    else:
        print("⚠️  Some parsing tests failed")
    print()
    return all_passed


def main():
    """Run all tests"""
    print()
    print("🏌️  GSPro Voice Caddy - Setup Test")
    print("="*60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    
    if results[-1][1]:  # Only continue if imports worked
        results.append(("Tesseract", test_tesseract()))
        results.append(("TTS", test_tts()))
        results.append(("Screen Capture", test_screen_capture()))
        results.append(("Distance Parsing", test_distance_parsing()))
        
        if results[1][1]:  # If Tesseract works
            results.append(("OCR on Screen", test_ocr_on_screen()))
    
    # Summary
    print()
    print("="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    all_passed = all([r[1] for r in results])
    if all_passed:
        print("🎉 All tests passed! You're ready to use the voice caddy!")
        print()
        print("Next steps:")
        print("1. Launch GSPro")
        print("2. Run: python gspro_voice_caddy.py --debug")
        print("3. Play golf and listen for announcements!")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before running the voice caddy.")
    print()


if __name__ == "__main__":
    main()
