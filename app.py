import streamlit as st
import json
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt
import io
import string
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder

# Import the compare_phonemes function from phoneme_utils
from phoneme_utils import compare_phonemes

# ==========================
# Initialize Session State
# ==========================

# For Phoneme Testing
if 'phoneme_data_testing' not in st.session_state:
    st.session_state.phoneme_data_testing = {}

if 'current_word_index_testing' not in st.session_state:
    st.session_state.current_word_index_testing = 0
    st.session_state.results_testing = []
    st.session_state.has_answered_testing = False
    st.session_state.error_occurred_testing = False
    st.session_state.recognized_text_testing = ''
    st.session_state.correct_testing = False
    st.session_state.recorded_audio_testing = None  # Store recorded audio

# For Phoneme Practice
if 'phoneme_data_practice' not in st.session_state:
    st.session_state.phoneme_data_practice = {}

if 'selected_practice_contrast' not in st.session_state:
    st.session_state.selected_practice_contrast = None

if 'selected_practice_minimal_pairs' not in st.session_state:
    st.session_state.selected_practice_minimal_pairs = None

if 'selected_practice_level' not in st.session_state:
    st.session_state.selected_practice_level = None

if 'practice_sentences' not in st.session_state:
    st.session_state.practice_sentences = []

if 'current_sentence_index_practice' not in st.session_state:
    st.session_state.current_sentence_index_practice = 0

if 'has_answered_practice' not in st.session_state:
    st.session_state.has_answered_practice = False

if 'error_occurred_practice' not in st.session_state:
    st.session_state.error_occurred_practice = False

if 'results_practice' not in st.session_state:
    st.session_state.results_practice = []
    st.session_state.recognized_text_practice = ''
    st.session_state.correct_practice = False
    st.session_state.recorded_audio_practice = None  # Store recorded audio

if 'last_selected_contrast' not in st.session_state:
    st.session_state.last_selected_contrast = None

if 'selected_phoneme_type_practice' not in st.session_state:
    st.session_state.selected_phoneme_type_practice = 'vowels'  # Default to vowels

if 'last_selected_phoneme_type_practice' not in st.session_state:
    st.session_state.last_selected_phoneme_type_practice = None

# ==========================
# Utility Functions
# ==========================

def load_phoneme_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"File `{file_path}` not found. Please ensure it exists in the directory.")
        return {}
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON from `{file_path}`: {e}")
        return {}

def generate_audio(text):
    try:
        tts = gTTS(text=text, lang='en')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

def recognize_speech_from_audio(audio_bytes, expected_word):
    r = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio)
        # Normalize both the result and the expected word
        normalized_result = result.lower().strip()
        normalized_expected = expected_word.lower().strip()

        # Remove punctuation for accurate comparison
        normalized_result = normalized_result.translate(str.maketrans('', '', string.punctuation))
        normalized_expected = normalized_expected.translate(str.maketrans('', '', string.punctuation))

        # Check if the recognized text contains the target word
        correct = normalized_expected in normalized_result.split()
        return result, correct
    except sr.UnknownValueError:
        st.error("Google Speech Recognition could not understand the audio.")
        return "", False
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return "", False

# ==========================
# Session End Functions
# ==========================

def end_session_testing():
    st.write("### Test Complete!")
    st.write("Here are your results:")

    if st.session_state.results_testing:
        results_df = pd.DataFrame(st.session_state.results_testing)
        st.table(results_df[['Word', 'Your Pronunciation', 'Correct']])

        correct_count = results_df['Correct'].sum()
        total_count = len(results_df)
        st.write(f"**You pronounced {correct_count}/{total_count} words correctly.**")

        # Visualization: Pie Chart
        fig, ax = plt.subplots()
        labels = ['Correct', 'Incorrect']
        sizes = [correct_count, total_count - correct_count]
        colors = ['#4CAF50', '#F44336']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write("No results to display.")

    if st.button("Restart Test"):
        st.session_state.current_word_index_testing = 0
        st.session_state.results_testing = []
        st.session_state.has_answered_testing = False
        st.session_state.error_occurred_testing = False
        st.session_state.recognized_text_testing = ''
        st.session_state.correct_testing = False
        st.session_state.recorded_audio_testing = None

def end_session_practice():
    st.write("### Practice Complete!")
    st.write("Here are your results:")

    if st.session_state.results_practice:
        results_df = pd.DataFrame(st.session_state.results_practice)
        st.table(results_df[['Sentence', 'Your Pronunciation', 'Correct']])

        correct_count = results_df['Correct'].sum()
        total_count = len(results_df)
        st.write(f"**You pronounced {correct_count}/{total_count} sentences correctly.**")

        # Visualization: Pie Chart
        fig, ax = plt.subplots()
        labels = ['Correct', 'Incorrect']
        sizes = [correct_count, total_count - correct_count]
        colors = ['#4CAF50', '#F44336']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write("No results to display.")

    if st.button("Restart Practice"):
        st.session_state.current_sentence_index_practice = 0
        st.session_state.results_practice = []
        st.session_state.has_answered_practice = False
        st.session_state.error_occurred_practice = False
        st.session_state.recognized_text_practice = ''
        st.session_state.correct_practice = False
        st.session_state.recorded_audio_practice = None
        st.session_state.selected_practice_contrast = None
        st.session_state.selected_practice_minimal_pairs = None
        st.session_state.selected_practice_level = None
        st.session_state.practice_sentences = []
        st.session_state.last_selected_contrast = None

# ==========================
# Button Callback Functions
# ==========================

def continue_to_next_testing():
    st.session_state.current_word_index_testing += 1
    st.session_state.has_answered_testing = False
    st.session_state.error_occurred_testing = False
    st.session_state.recognized_text_testing = ''
    st.session_state.correct_testing = False
    st.session_state.recorded_audio_testing = None

def continue_to_next_practice():
    st.session_state.current_sentence_index_practice += 1
    st.session_state.has_answered_practice = False
    st.session_state.error_occurred_practice = False
    st.session_state.recognized_text_practice = ''
    st.session_state.correct_practice = False
    st.session_state.recorded_audio_practice = None

# ==========================
# Phoneme Testing Logic
# ==========================

def phoneme_testing(phoneme_type):
    st.title(f"{phoneme_type.capitalize()} Testing")

    # Fetch all words for the selected phoneme type
    all_words = []
    for phoneme, word_list in st.session_state.phoneme_data_testing.get(phoneme_type, {}).items():
        all_words.extend(word_list)

    # Update total_steps based on the number of words across all phonemes
    total_words = len(all_words)
    st.session_state.total_steps_testing = total_words

    # Ensure we are within bounds of the words
    if all_words and st.session_state.current_word_index_testing < len(all_words):
        current_word_data = all_words[st.session_state.current_word_index_testing]
        word = current_word_data['word']
        ipa = current_word_data['ipa']
        sentence = current_word_data['sentence']

        st.write(f"### Pronounce the word in this sentence:")
        st.markdown(f'"{sentence}"')
        st.write(f"**IPA:** {ipa}")

        if st.checkbox("Listen to audio example", key=f"audio_testing_{st.session_state.current_word_index_testing}"):
            audio_bytes = generate_audio(sentence)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')

        if not st.session_state.has_answered_testing:
            st.write("Please click on the microphone to start recording.")

            # Use the correct parameter to change the microphone icon color
            audio_bytes = audio_recorder(
                recording_color="#006400",  # Dark green when recording
                neutral_color="#404040"     # Dark gray when not recording
            )

            if audio_bytes:
                # Store the recorded audio in session state
                st.session_state.recorded_audio_testing = audio_bytes

                # Perform speech recognition
                recognized_text, correct = recognize_speech_from_audio(audio_bytes, word)
                if recognized_text:
                    st.session_state.recognized_text_testing = recognized_text
                    st.session_state.correct_testing = correct
                    st.session_state.has_answered_testing = True

                    st.rerun()
                else:
                    st.error("Could not understand the audio. Please try again.")
                    # Allow re-recording
        else:
            # Display the user's recording with a label
            st.write("Your Recording:")
            if st.session_state.recorded_audio_testing:
                st.audio(st.session_state.recorded_audio_testing, format='audio/wav')

            # Display the ideal pronunciation
            st.write("Ideal Pronunciation:")
            ideal_audio = generate_audio(sentence)
            if ideal_audio:
                st.audio(ideal_audio, format='audio/mp3')

            # Display the recognized text and feedback
            st.write(f"You said: **{st.session_state.recognized_text_testing}**")

            # Clean the recognized text to extract the recognized word
            recognized_words = st.session_state.recognized_text_testing.strip().split()
            if recognized_words:
                recognized_word = recognized_words[-1].lower()
                recognized_word = recognized_word.strip(string.punctuation)
            else:
                recognized_word = ""

            # Compare phonemes and provide feedback
            feedback, _ = compare_phonemes(
                word,
                recognized_word,
                current_word_data.get('phonemic_contrast', [])
            )
            st.write(feedback)

            # Store result
            st.session_state.results_testing.append({
                'Word': word,
                'Your Pronunciation': recognized_word if not st.session_state.correct_testing else 'N/A',
                'Correct': st.session_state.correct_testing
            })

            if st.button("Continue"):
                continue_to_next_testing()
                st.rerun()

        progress = (st.session_state.current_word_index_testing + 1) / st.session_state.total_steps_testing
        st.progress(progress)
        st.write(f"**Progress:** {st.session_state.current_word_index_testing + 1}/{st.session_state.total_steps_testing}")

    else:
        end_session_testing()

# ==========================
# Phoneme Practice Logic
# ==========================

def phoneme_practice():
    practice_type = st.session_state.selected_phoneme_type_practice
    st.title(f"{practice_type.capitalize()} Practice")

    # Fetch all pairs for the selected practice type
    all_pairs = st.session_state.phoneme_data_practice.get(practice_type, {})

    if not all_pairs:
        st.write(f"No data available for {practice_type.capitalize()} practice.")
        return

    # ==========================
    # Step 1: Select Phonemic Contrast
    # ==========================

    st.subheader("Select Phonemic Contrast")

    # Create a list of phonemic contrast options
    contrast_options = list(all_pairs.keys())

    # Get selected contrast
    selected_contrast = st.selectbox("Choose a Phonemic Contrast", contrast_options, key='selected_contrast_option')

    # When the selection changes, reset relevant session state variables
    if st.session_state.get('last_selected_contrast') != selected_contrast:
        st.session_state.last_selected_contrast = selected_contrast
        if selected_contrast:
            st.session_state.selected_practice_contrast = selected_contrast
            st.session_state.selected_practice_minimal_pairs = all_pairs[selected_contrast]
            st.session_state.selected_practice_level = None
            st.session_state.practice_sentences = []
            st.session_state.current_sentence_index_practice = 0
            st.session_state.has_answered_practice = False
            st.session_state.error_occurred_practice = False
            st.session_state.results_practice = []
            st.session_state.recognized_text_practice = ''
            st.session_state.correct_practice = False
            st.session_state.recorded_audio_practice = None
        else:
            st.session_state.selected_practice_contrast = None
            st.session_state.selected_practice_minimal_pairs = None

    # ==========================
    # Step 2: Select Practice Level
    # ==========================
    if st.session_state.selected_practice_contrast is not None:
        st.subheader("Select Practice Level")
        level = st.radio("Choose Practice Level", ["Level 1", "Level 2", "Level 3"], key='practice_level')

        # When the level changes, reset relevant session state variables
        if st.session_state.get('selected_practice_level') != level:
            st.session_state.selected_practice_level = level
            # Prepare the list of sentences based on the selected level
            level_key = f"level_{level.split()[-1]}"

            practice_sentences = []

            for pair_data in st.session_state.selected_practice_minimal_pairs:
                sentence_1 = pair_data[level_key][0]
                sentence_2 = pair_data[level_key][1]

                practice_sentences.append({
                    "sentence": sentence_1,
                    "target_word": pair_data['pair'][0]
                })
                practice_sentences.append({
                    "sentence": sentence_2,
                    "target_word": pair_data['pair'][1]
                })

            st.session_state.practice_sentences = practice_sentences
            # Reset practice state variables
            st.session_state.current_sentence_index_practice = 0
            st.session_state.has_answered_practice = False
            st.session_state.error_occurred_practice = False
            st.session_state.results_practice = []
            st.session_state.recognized_text_practice = ''
            st.session_state.correct_practice = False
            st.session_state.recorded_audio_practice = None

    # ==========================
    # Step 3: Practice Sentences
    # ==========================
    if (st.session_state.selected_practice_contrast is not None and
        st.session_state.selected_practice_level is not None and
        st.session_state.current_sentence_index_practice < len(st.session_state.practice_sentences)):

        current_sentence_data = st.session_state.practice_sentences[st.session_state.current_sentence_index_practice]
        current_sentence = current_sentence_data['sentence']
        target_word = current_sentence_data['target_word']
        current_index = st.session_state.current_sentence_index_practice

        st.subheader(f"Sentence {current_index + 1} of {len(st.session_state.practice_sentences)}")
        st.write(f"**Phonemic Contrast:** {st.session_state.selected_practice_contrast}")
        st.write(f"**Pronounce the following sentence:**")
        st.markdown(f'"{current_sentence}"')

        # Listen to Audio Example
        if st.checkbox("Listen to audio example", key=f"audio_practice_{current_index}"):
            audio_bytes = generate_audio(current_sentence)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')

        if not st.session_state.has_answered_practice:
            st.write("Please click on the microphone to start recording.")

            # Use the correct parameter to change the microphone icon color
            audio_bytes = audio_recorder(
                recording_color="#006400",  # Dark green when recording
                neutral_color="#404040"     # Dark gray when not recording
            )

            if audio_bytes:
                # Store the recorded audio in session state
                st.session_state.recorded_audio_practice = audio_bytes

                # Perform speech recognition
                recognized_text, correct = recognize_speech_from_audio(audio_bytes, target_word)
                if recognized_text:
                    st.session_state.recognized_text_practice = recognized_text
                    st.session_state.correct_practice = correct
                    st.session_state.has_answered_practice = True

                    st.rerun()
                else:
                    st.error("Could not understand the audio. Please try again.")
                    # Allow re-recording
        else:
            # Display the user's recording with a label
            st.write("Your Recording:")
            if st.session_state.recorded_audio_practice:
                st.audio(st.session_state.recorded_audio_practice, format='audio/wav')

            # Display the ideal pronunciation
            st.write("Ideal Pronunciation:")
            ideal_audio = generate_audio(current_sentence)
            if ideal_audio:
                st.audio(ideal_audio, format='audio/mp3')

            # Display the recognized text and feedback
            st.write(f"You said: **{st.session_state.recognized_text_practice}**")

            # Provide feedback
            if st.session_state.correct_practice:
                feedback = f"**Good job!** You pronounced '{target_word}' correctly."
            else:
                feedback = f"**You said '{st.session_state.recognized_text_practice}', but the correct word was '{target_word}'.**"
            st.write(feedback)

            # Store result
            st.session_state.results_practice.append({
                'Sentence': current_sentence,
                'Your Pronunciation': st.session_state.recognized_text_practice,
                'Correct': st.session_state.correct_practice
            })

            if st.button("Continue"):
                continue_to_next_practice()
                st.rerun()

        progress = (st.session_state.current_sentence_index_practice + 1) / len(st.session_state.practice_sentences)
        st.progress(progress)
        st.write(f"**Progress:** {st.session_state.current_sentence_index_practice + 1}/{len(st.session_state.practice_sentences)}")

    # ==========================
    # Check if Practice Session is Complete
    # ==========================
    elif (st.session_state.selected_practice_contrast is not None and
          st.session_state.selected_practice_level is not None and
          st.session_state.current_sentence_index_practice >= len(st.session_state.practice_sentences)):
        end_session_practice()

# ==========================
# Main Function with Sidebar
# ==========================

def main():
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Choose a Section", ["Phoneme Testing", "Phoneme Practice"])

    if section == "Phoneme Testing":
        # Load phoneme testing data if not already loaded
        if not st.session_state.phoneme_data_testing:
            data_testing = load_phoneme_data('phoneme_testing.json')
            st.session_state.phoneme_data_testing = data_testing

        # Submenu for testing modes
        testing_mode = st.sidebar.radio("Select Phoneme Type", ["Vowel Testing", "Diphthong Testing", "Consonant Testing"])

        # Map the testing_type correctly to the plural keys in the JSON
        if testing_mode == "Vowel Testing":
            phoneme_type = "vowels"
        elif testing_mode == "Diphthong Testing":
            phoneme_type = "diphthongs"
        elif testing_mode == "Consonant Testing":
            phoneme_type = "consonants"

        # Run the phoneme testing for all phonemes in the type
        if phoneme_type:
            phoneme_testing(phoneme_type)

    elif section == "Phoneme Practice":
        # Load phoneme practice data if not already loaded
        if not st.session_state.phoneme_data_practice:
            data_practice = load_phoneme_data('phoneme_practice.json')
            st.session_state.phoneme_data_practice = data_practice.get('phoneme_practice', {})

        # Submenu for practice modes
        practice_mode = st.sidebar.radio("Select Phoneme Type", ["Vowel Practice", "Diphthong Practice", "Consonant Practice"])

        # Map the practice_mode correctly to the keys in the JSON
        if practice_mode == "Vowel Practice":
            st.session_state.selected_phoneme_type_practice = "vowels"
        elif practice_mode == "Diphthong Practice":
            st.session_state.selected_phoneme_type_practice = "diphthongs"
        elif practice_mode == "Consonant Practice":
            st.session_state.selected_phoneme_type_practice = "consonants"

        # Reset practice variables if phoneme type changes
        if st.session_state.get('last_selected_phoneme_type_practice') != st.session_state.selected_phoneme_type_practice:
            st.session_state.last_selected_phoneme_type_practice = st.session_state.selected_phoneme_type_practice
            st.session_state.selected_practice_contrast = None
            st.session_state.selected_practice_minimal_pairs = None
            st.session_state.selected_practice_level = None
            st.session_state.practice_sentences = []
            st.session_state.current_sentence_index_practice = 0
            st.session_state.has_answered_practice = False
            st.session_state.error_occurred_practice = False
            st.session_state.results_practice = []
            st.session_state.recognized_text_practice = ''
            st.session_state.correct_practice = False
            st.session_state.recorded_audio_practice = None

        phoneme_practice()

if __name__ == "__main__":
    main()
