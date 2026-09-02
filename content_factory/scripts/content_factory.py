#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Shorts Content Factory - Free Version
Generates scripts, TTS audio, and video clips for EU/USA market.

Dependencies (install with: pip install gTTS moviepy Pillow):
- gTTS: Google Text-to-Speech (free, no API key needed)
- moviepy: Video editing
- Pillow: Image processing
"""

import os
import random
import datetime
from gtts import gTTS
from moviepy import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configuration
OUTPUT_DIR = "output"
TEMP_DIR = "temp"
ASSETS_DIR = "assets"

# Ensure directories exist
for directory in [OUTPUT_DIR, TEMP_DIR, ASSETS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Sample topics for EU/USA market (viral niches)
TOPICS = {
    "facts": [
        "Did you know that octopuses have three hearts?",
        "The shortest war in history lasted only 38 minutes.",
        "Honey never spoils. Archaeologists found edible honey in Egyptian tombs.",
        "Your stomach lining replaces itself every 3-4 days.",
        "Bananas are berries, but strawberries aren't."
    ],
    "motivation": [
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "The only way to do great work is to love what you do.",
        "Don't watch the clock; do what it does. Keep going.",
        "Believe you can and you're halfway there.",
        "Act as if what you do makes a difference. It does."
    ],
    "tech": [
        "AI is changing everything. Are you ready?",
        "The first computer bug was an actual moth.",
        "There are more possible chess games than atoms in the universe.",
        "Your smartphone has more computing power than NASA in 1969.",
        "90% of the world's data was created in the last two years."
    ]
}

def generate_script(topic_type=None):
    """Generate a short script for YouTube Shorts (under 60 seconds)."""
    if topic_type is None:
        topic_type = random.choice(list(TOPICS.keys()))
    
    scripts = TOPICS.get(topic_type, TOPICS["facts"])
    selected_script = random.choice(scripts)
    
    # Add hook and CTA
    hook = "Wait for it... " if random.random() > 0.5 else "You won't believe this: "
    cta = "Follow for more!" if random.random() > 0.5 else "Like and subscribe!"
    
    full_script = f"{hook}{selected_script} {cta}"
    return full_script, topic_type

def text_to_speech(text, output_file, lang='en'):
    """Convert text to speech using gTTS (free)."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"✓ Audio generated: {output_file}")
        return output_file
    except Exception as e:
        print(f"✗ Error generating audio: {e}")
        return None

def create_background_video(duration, output_file, color_scheme="gradient"):
    """Create a simple animated background video."""
    try:
        # Create gradient background
        w, h = 1080, 1920  # Vertical format for Shorts
        
        if color_scheme == "gradient":
            # Create gradient colors
            color1 = (random.randint(50, 150), random.randint(50, 150), random.randint(150, 255))
            color2 = (random.randint(150, 255), random.randint(50, 150), random.randint(50, 150))
            
            img = Image.new('RGB', (w, h), color=color1)
            draw = ImageDraw.Draw(img)
            
            # Draw gradient
            for y in range(h):
                r = int(color1[0] + (color2[0] - color1[0]) * y / h)
                g = int(color1[1] + (color2[1] - color1[1]) * y / h)
                b = int(color1[2] + (color2[2] - color1[2]) * y / h)
                draw.line([(0, y), (w, y)], fill=(r, g, b))
            
            img.save(f"{TEMP_DIR}/bg_frame.png")
            
            # Create video clip from image with duration parameter
            clip = ImageClip(f"{TEMP_DIR}/bg_frame.png", duration=duration)
            
        elif color_scheme == "solid":
            color = (random.randint(0, 100), random.randint(0, 100), random.randint(100, 200))
            clip = ColorClip(size=(w, h), color=color).with_duration(duration)
        
        else:  # particles effect simulation
            color = (20, 20, 40)
            clip = ColorClip(size=(w, h), color=color).with_duration(duration)
        
        # Add subtle zoom effect using Resize effect
        clip = clip.with_effects([vfx.Resize(lambda t: 1 + 0.04 * t)])
        
        # Crop to maintain aspect ratio
        clip = clip.with_effects([vfx.Crop(x_center=w/2, y_center=h/2, width=1080, height=1920)])
        
        clip.write_videofile(output_file, fps=24, codec='libx264', audio=False, logger=None)
        print(f"✓ Background video created: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"✗ Error creating background: {e}")
        return None

def add_text_to_video(video_file, text, output_file):
    """Add text overlay to video."""
    try:
        # Load video
        video = VideoFileClip(video_file)
        
        # Create simple text clip without complex composition
        txt_clip = TextClip(
            text=text,
            font_size=50,
            color='white',
            font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            method='label',
            stroke_color='black',
            stroke_width=2
        )
        
        # Position text in center and set duration
        txt_clip = txt_clip.with_position('center').with_duration(video.duration)
        
        # Composite video with text
        final = CompositeVideoClip([video, txt_clip])
        
        # Write result with lower fps for faster processing
        final.write_videofile(output_file, fps=15, codec='libx264', logger=None, preset='ultrafast')
        print(f"✓ Text added to video: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"✗ Error adding text: {e}")
        # Fallback: return original video
        return video_file

def create_short(topic_type=None, niche="general"):
    """Main function to create a complete YouTube Short."""
    print(f"\n{'='*50}")
    print("🎬 Creating YouTube Short...")
    print(f"{'='*50}\n")
    
    # Step 1: Generate script
    script, used_topic = generate_script(topic_type)
    print(f"📝 Script ({used_topic}): {script}\n")
    
    # Estimate duration (average speaking rate: 150 words per minute)
    word_count = len(script.split())
    duration = max(5, min(59, word_count / 2.5))  # Between 5 and 59 seconds
    
    # Step 2: Generate audio
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file = f"{TEMP_DIR}/audio_{timestamp}.mp3"
    audio_result = text_to_speech(script, audio_file, lang='en')
    
    if not audio_result:
        print("✗ Failed to generate audio. Using default duration.")
        audio_duration = duration
    else:
        # Get actual audio duration
        try:
            audio_clip = AudioFileClip(audio_file)
            audio_duration = audio_clip.duration
            audio_clip.close()
        except:
            audio_duration = duration
    
    # Step 3: Create background video
    bg_file = f"{TEMP_DIR}/background_{timestamp}.mp4"
    bg_result = create_background_video(audio_duration, bg_file, color_scheme="gradient")
    
    if not bg_result:
        print("✗ Failed to create background video.")
        return None
    
    # Step 4: Add text overlay
    final_file = f"{OUTPUT_DIR}/short_{timestamp}_{used_topic}.mp4"
    final_result = add_text_to_video(bg_file, script, final_file)
    
    # Step 5: Combine video with audio (skip text overlay for speed)
    if bg_result and audio_result:
        try:
            video = VideoFileClip(bg_result)
            audio = AudioFileClip(audio_result)
            
            # Set audio to video (MoviePy 2.x syntax)
            video_with_audio = video.with_audio(audio)
            
            # Final export
            final_output = f"{OUTPUT_DIR}/final_short_{timestamp}.mp4"
            video_with_audio.write_videofile(
                final_output, 
                fps=15, 
                codec='libx264', 
                audio_codec='aac',
                logger=None,
                preset='ultrafast'
            )
            
            # Cleanup temp files
            video.close()
            audio.close()
            
            print(f"\n✅ SUCCESS! Your YouTube Short is ready:")
            print(f"   📁 File: {final_output}")
            print(f"   ⏱️  Duration: {audio_duration:.1f} seconds")
            print(f"   📝 Topic: {used_topic}")
            print(f"\n💡 Tip: Add text overlays and trending music in YouTube editor before publishing!")
            
            return final_output
            
        except Exception as e:
            print(f"✗ Error combining audio and video: {e}")
            return bg_result
    
    return bg_result

def batch_create(count=5, topic_type=None):
    """Create multiple shorts in batch."""
    print(f"\n🚀 Starting batch creation of {count} shorts...\n")
    
    results = []
    for i in range(count):
        print(f"\n--- Short #{i+1}/{count} ---")
        result = create_short(topic_type=topic_type)
        if result:
            results.append(result)
    
    print(f"\n{'='*50}")
    print(f"🎉 Batch complete! Created {len(results)} shorts.")
    print(f"{'='*50}\n")
    
    return results

if __name__ == "__main__":
    import sys
    
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║   🎬 YOUTUBE SHORTS CONTENT FACTORY (FREE) 🎬    ║
    ║           For EU & USA Markets                    ║
    ║                                                   ║
    ║   Fully FREE tools: gTTS + MoviePy               ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    # Check dependencies
    try:
        import gtts
        import moviepy
        from PIL import Image
        print("✓ All dependencies loaded successfully!\n")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nInstall required packages:")
        print("   pip install gTTS moviepy Pillow\n")
        sys.exit(1)
    
    # Interactive mode or command line
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            topic = sys.argv[3] if len(sys.argv) > 3 else None
            batch_create(count, topic)
        elif sys.argv[1] in TOPICS.keys():
            create_short(topic_type=sys.argv[1])
        else:
            create_short()
    else:
        # Default: create one short
        create_short()
