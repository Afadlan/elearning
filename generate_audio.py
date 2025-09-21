import os
import pyttsx3
from pathlib import Path

def create_audio_files():
    """Generate audio files from text scripts using text-to-speech"""
    
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Configure voice settings for clear pronunciation
    voices = engine.getProperty('voices')
    if voices:
        # Try to use a female voice for variety
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            # Use the first available voice
            engine.setProperty('voice', voices[0].id)
    
    # Set speech rate (slower for B1 level learners)
    engine.setProperty('rate', 150)  # Default is usually 200
    
    # Set volume
    engine.setProperty('volume', 0.9)
    
    # Audio files to generate
    audio_files = [
        {
            'script': 'audio/script1-city-center.txt',
            'output': 'audio/directions-city-center.wav',
            'mp3': 'audio/directions-city-center.mp3'
        },
        {
            'script': 'audio/script2-museum.txt',
            'output': 'audio/directions-museum.wav',
            'mp3': 'audio/directions-museum.mp3'
        },
        {
            'script': 'audio/script3-shopping-district.txt',
            'output': 'audio/directions-shopping-district.wav',
            'mp3': 'audio/directions-shopping-district.mp3'
        },
        {
            'script': 'audio/script4-route-planning.txt',
            'output': 'audio/complex-route-planning.wav',
            'mp3': 'audio/complex-route-planning.mp3'
        },
        {
            'script': 'audio/script5-emergency-navigation.txt',
            'output': 'audio/expert-navigation-scenarios.wav',
            'mp3': 'audio/expert-navigation-scenarios.mp3'
        }
    ]
    
    print("Generating audio files...")
    
    for audio_file in audio_files:
        try:
            # Read the script
            with open(audio_file['script'], 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"Generating {audio_file['output']}...")
            
            # Generate WAV file
            engine.save_to_file(text, audio_file['output'])
            engine.runAndWait()
            
            print(f"✓ Created {audio_file['output']}")
            
            # Convert to MP3 using ffmpeg if available
            try:
                import subprocess
                mp3_command = [
                    'ffmpeg', '-i', audio_file['output'], 
                    '-acodec', 'mp3', '-ab', '128k', 
                    audio_file['mp3'], '-y'
                ]
                subprocess.run(mp3_command, check=True, capture_output=True)
                print(f"✓ Created {audio_file['mp3']}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"⚠ Could not create MP3 version of {audio_file['output']} (ffmpeg not available)")
                
        except Exception as e:
            print(f"✗ Error generating {audio_file['output']}: {str(e)}")
    
    print("\nAudio generation complete!")
    print("\nGenerated files:")
    for audio_file in audio_files:
        if os.path.exists(audio_file['output']):
            size = os.path.getsize(audio_file['output'])
            print(f"  {audio_file['output']} ({size} bytes)")
        if os.path.exists(audio_file['mp3']):
            size = os.path.getsize(audio_file['mp3'])
            print(f"  {audio_file['mp3']} ({size} bytes)")

if __name__ == "__main__":
    # Check if required packages are available
    try:
        import pyttsx3
        create_audio_files()
    except ImportError:
        print("Error: pyttsx3 is required for audio generation.")
        print("Install it with: pip install pyttsx3")
        print("\nAlternatively, you can use online TTS services or record the audio manually.")
        print("The script files are ready in the audio/ directory.")
