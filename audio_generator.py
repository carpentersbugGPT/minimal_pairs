from gtts import gTTS
import os
import json

# Load minimal pairs data
def load_minimal_pairs(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

data = load_minimal_pairs('minimal_pairs.json')

# Function to generate audio
def generate_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"Audio saved as {filename}")

# Generate audio for Level 1
for item in data['level_1']:
    for word in item['pair']:
        filename = f"audio/{word}.mp3"
        if not os.path.exists(filename):
            generate_audio(word, filename)

# Generate audio for Level 2 and Level 3
for level in ['level_2', 'level_3']:
    for item in data[level]:
        for pair in item['pair']:
            sentence = pair['sentence']
            # Create a safe filename
            filename = f"audio/{'_'.join(sentence.lower().split())}.mp3"
            if not os.path.exists(filename):
                generate_audio(sentence, filename)
