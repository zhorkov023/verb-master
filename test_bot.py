#!/usr/bin/env python3
"""
Test script for the Spanish Verb Trainer Bot
Run this to test the core functionality without needing a Telegram bot token.
"""

from verb_engine import VerbEngine
from config import PERSONS, TENSES
import json

def test_verb_engine():
    """Test the verb engine functionality."""
    print("🧪 Testing Verb Engine...")
    
    # Initialize engine
    engine = VerbEngine()
    
    # Test basic functionality
    print(f"✅ Loaded {engine.get_total_verbs()} verbs")
    
    # Test random challenge generation
    challenge = engine.get_random_challenge()
    print(f"✅ Generated challenge: {challenge['verb']} in {challenge['tense_display']} for {challenge['person']}")
    print(f"   Correct answer: {challenge['correct_answer']}")
    
    # Test answer checking
    correct_answer = challenge['correct_answer']
    
    # Test exact match
    assert engine.check_answer(correct_answer, correct_answer) == True
    print("✅ Exact match test passed")
    
    # Test case insensitive
    assert engine.check_answer(correct_answer.upper(), correct_answer) == True
    print("✅ Case insensitive test passed")
    
    # Test accent tolerance
    if 'á' in correct_answer:
        no_accent = correct_answer.replace('á', 'a')
        assert engine.check_answer(no_accent, correct_answer) == True
        print("✅ Accent tolerance test passed")
    
    # Test wrong answer
    assert engine.check_answer("wrong", correct_answer) == False
    print("✅ Wrong answer test passed")
    
    print("✅ All verb engine tests passed!\n")

def test_verb_data():
    """Test the verb data structure."""
    print("🧪 Testing Verb Data...")
    
    with open('verbs_data.json', 'r', encoding='utf-8') as f:
        verbs_data = json.load(f)
    
    # Check structure
    for verb, conjugations in verbs_data.items():
        # Check all tenses are present
        for tense in TENSES.keys():
            assert tense in conjugations, f"Missing tense {tense} for verb {verb}"
            
            # Check all persons are present (6 conjugations per tense)
            assert len(conjugations[tense]) == 6, f"Wrong number of conjugations for {verb} in {tense}"
    
    print(f"✅ Verified structure for {len(verbs_data)} verbs")
    print("✅ All verb data tests passed!\n")

def test_config():
    """Test configuration."""
    print("🧪 Testing Configuration...")
    
    # Check persons
    assert len(PERSONS) == 6
    print("✅ All 6 persons configured")
    
    # Check tenses
    assert len(TENSES) == 6
    print("✅ All 6 tenses configured")
    
    print("✅ All configuration tests passed!\n")

def demo_bot_interaction():
    """Demonstrate how the bot would work."""
    print("🎮 Bot Interaction Demo...")
    
    engine = VerbEngine()
    
    # Simulate 3 challenges
    for i in range(3):
        print(f"\n--- Challenge {i+1} ---")
        challenge = engine.get_random_challenge()
        
        print(f"🔤 Conjugar el verbo:")
        print(f"**{challenge['verb']}** en **{challenge['tense_display']}** para **{challenge['person']}**")
        print(f"Respuesta correcta: {challenge['correct_answer']}")
        
        # Test some variations
        variations = [
            challenge['correct_answer'],
            challenge['correct_answer'].upper(),
            challenge['correct_answer'].replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        ]
        
        for var in variations:
            if engine.check_answer(var, challenge['correct_answer']):
                print(f"✅ '{var}' would be accepted")
            else:
                print(f"❌ '{var}' would be rejected")

if __name__ == "__main__":
    print("🚀 Spanish Verb Trainer Bot - Test Suite\n")
    
    try:
        test_config()
        test_verb_data()
        test_verb_engine()
        demo_bot_interaction()
        
        print("\n🎉 All tests passed! The bot is ready to use.")
        print("\nTo run the bot:")
        print("1. Set your Telegram bot token")
        print("2. Run: python main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check the error and fix any issues.")
