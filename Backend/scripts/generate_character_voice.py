#!/usr/bin/env python3
"""
Generate character voice introduction using Google Cloud Text-to-Speech
"""

import sys
import json
import os
import base64
from pathlib import Path

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False
    print("Warning: google-cloud-texttospeech not installed. Using gtts fallback.", file=sys.stderr)

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

def generate_voice_google_cloud(text, output_path, voice_name="en-US-Neural2-F"):
    """Generate voice using Google Cloud Text-to-Speech (premium quality)"""
    if not GOOGLE_TTS_AVAILABLE:
        return False
    
    try:
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Voice configuration (Neural2 voices are high quality)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        # Audio configuration
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        
        return True
    except Exception as e:
        print(f"Google Cloud TTS error: {e}", file=sys.stderr)
        return False

def generate_voice_gtts(text, output_path):
    """Generate voice using gTTS (free, lower quality)"""
    if not GTTS_AVAILABLE:
        return False
    
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        return True
    except Exception as e:
        print(f"gTTS error: {e}", file=sys.stderr)
        return False

def create_character_introduction(character_data):
    """Create an introduction text for the character"""
    name = character_data.get('name', 'Unknown Character')
    description = character_data.get('description', '')
    
    # Extract key details from description
    intro_text = f"Hello, I am {name}. {description}"
    
    # Limit to reasonable length (TTS works better with shorter text)
    if len(intro_text) > 500:
        intro_text = intro_text[:497] + "..."
    
    return intro_text

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "Usage: python generate_character_voice.py <character_json> <output_path>"
        }))
        sys.exit(1)
    
    character_json_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        # Read character data
        with open(character_json_path, 'r') as f:
            character_data = json.load(f)
        
        # Create introduction text
        intro_text = create_character_introduction(character_data)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Try Google Cloud TTS first (better quality)
        success = generate_voice_google_cloud(intro_text, output_path)
        
        # Fallback to gTTS if Google Cloud fails
        if not success:
            success = generate_voice_gtts(intro_text, output_path)
        
        if success:
            # Get file size
            file_size = os.path.getsize(output_path)
            
            # Read audio file and encode to base64
            with open(output_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            result = {
                "success": True,
                "audioPath": output_path,
                "audioBase64": f"data:audio/mp3;base64,{audio_base64}",
                "text": intro_text,
                "fileSize": file_size,
                "duration": None  # Would need audio analysis library to calculate
            }
        else:
            result = {
                "success": False,
                "error": "No text-to-speech library available. Install google-cloud-texttospeech or gtts."
            }
        
        print(json.dumps(result))
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
