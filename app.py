import streamlit as st
import json
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt
import io
from gtts import gTTS
import string

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
    st.session_state.recording_started_testing = False
    st.session_state.error_occurred_testing = False
    st.session_state.current_recording_word_testing = ''

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

if 'recording_started_practice' not in st.session_state:
    st.session_state.recording_started_practice = False

if 'error_occurred_practice' not in st.session_state:
    st.session_state.error_occurred_practice = False

if 'current_recording_word_practice' not in st.session_state:
    st.session_state.current_recording_word_practice = ''

if 'results_practice' not in st.session_state:
    st.session_state.results_practice = []

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

def recognize_speech(expected_word):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Recording in progress, please speak the sentence...")
        audio = r.listen(source)
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
# Button Callback Functions
# ==========================

# For Phoneme Testing
def start_recording_testing(word, index):
    st.session_state.recording_started_testing = True
    st.session_state.current_recording_word_testing = word
    st.session_state.current_recording_index_testing = index

def continue_to_next_testing():
    st.session_state.current_word_index_testing += 1
    st.session_state.has_answered_testing = False
    st.session_state.recording_started_testing = False
    st.session_state.error_occurred_testing = False
    st.session_state.current_recording_word_testing = ''

def retry_current_testing():
    st.session_state.has_answered_testing = False
    st.session_state.error_occurred_testing = False
    st.session_state.recording_started_testing = False
    st.session_state.current_recording_word_testing = ''

# For Phoneme Practice
def start_recording_practice(sentence_data, index):
    st.session_state.recording_started_practice = True
    st.session_state.current_recording_word_practice = sentence_data['target_word']
    st.session_state.current_sentence_index_practice = index

def continue_to_next_practice():
    st.session_state.current_sentence_index_practice += 1
    st.session_state.has_answered_practice = False
    st.session_state.recording_started_practice = False
    st.session_state.error_occurred_practice = False
    st.session_state.current_recording_word_practice = ''

def retry_current_practice():
    st.session_state.has_answered_practice = False
    st.session_state.error_occurred_practice = False
    st.session_state.recording_started_practice = False
    st.session_state.current_recording_word_practice = ''

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
        st.session_state.recording_started_testing = False
        st.session_state.current_recording_word_testing = ''

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
        st.session_state.recording_started_practice = False
        st.session_state.current_recording_word_practice = ''
        st.session_state.selected_practice_contrast = None
        st.session_state.selected_practice_minimal_pairs = None
        st.session_state.selected_practice_level = None
        st.session_state.practice_sentences = []
        st.session_state.last_selected_contrast = None

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
            # Start Recording button: disabled if recording_started is True
            st.button(
                "Start Recording",
                key=f"start_testing_{st.session_state.current_word_index_testing}",
                on_click=start_recording_testing,
                args=(word, st.session_state.current_word_index_testing),
                disabled=st.session_state.recording_started_testing
            )

        # If recording has started, perform recognition
        if st.session_state.recording_started_testing:
            # Perform speech recognition
            recognized_text, correct = recognize_speech(st.session_state.current_recording_word_testing)
            if recognized_text:
                st.write(f"You said: **{recognized_text}**")
                st.session_state.has_answered_testing = True
                st.session_state.recording_started_testing = False  # Re-enable for next word

                # Clean the recognized text to extract the recognized word
                recognized_words = recognized_text.strip().split()
                if recognized_words:
                    recognized_word = recognized_words[-1].lower()
                    # Remove punctuation from the recognized word
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

                # Store result with the recognized word if incorrect
                st.session_state.results_testing.append({
                    'Word': word,
                    'Your Pronunciation': recognized_word if not correct else 'N/A',
                    'Correct': correct
                })

                st.button(
                    "Continue",
                    key=f"continue_testing_{st.session_state.current_word_index_testing}",
                    on_click=continue_to_next_testing
                )
            else:
                st.error("Could not understand the audio. Please try again.")
                st.session_state.has_answered_testing = True
                st.session_state.error_occurred_testing = True
                st.session_state.recording_started_testing = False  # Re-enable button for retry

                col1, col2 = st.columns(2)
                with col1:
                    st.button(
                        "Retry",
                        key=f"retry_testing_{st.session_state.current_word_index_testing}",
                        on_click=retry_current_testing
                    )
                with col2:
                    st.button(
                        "Continue",
                        key=f"continue_testing_{st.session_state.current_word_index_testing}",
                        on_click=continue_to_next_testing
                    )

        progress = (st.session_state.current_word_index_testing + 1) / st.session_state.total_steps_testing if st.session_state.total_steps_testing > 0 else 0
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
            st.session_state.recording_started_practice = False
            st.session_state.error_occurred_practice = False
            st.session_state.results_practice = []
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
            st.session_state.recording_started_practice = False
            st.session_state.error_occurred_practice = False
            st.session_state.results_practice = []

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
            # Start Recording button
            st.button(
                "Start Recording",
                key=f"start_practice_{current_index}",
                on_click=start_recording_practice,
                args=(current_sentence_data, current_index),
                disabled=st.session_state.recording_started_practice
            )

        # If recording has started, perform recognition
        if st.session_state.recording_started_practice:
            # Perform speech recognition
            recognized_text, correct = recognize_speech(current_sentence_data['target_word'])
            if recognized_text:
                st.write(f"You said: **{recognized_text}**")
                st.session_state.has_answered_practice = True
                st.session_state.recording_started_practice = False

                # Provide feedback
                if correct:
                    feedback = f"**Good job!** You pronounced '{current_sentence_data['target_word']}' correctly."
                else:
                    feedback = f"**You said '{recognized_text}', but the correct word was '{current_sentence_data['target_word']}'.**"
                st.write(feedback)

                # Store result
                st.session_state.results_practice.append({
                    'Sentence': current_sentence,
                    'Your Pronunciation': recognized_text,
                    'Correct': correct
                })

                st.button(
                    "Continue",
                    key=f"continue_practice_{current_index}",
                    on_click=continue_to_next_practice
                )
            else:
                st.error("Could not understand the audio. Please try again.")
                st.session_state.has_answered_practice = True
                st.session_state.error_occurred_practice = True
                st.session_state.recording_started_practice = False

                col1, col2 = st.columns(2)
                with col1:
                    st.button(
                        "Retry",
                        key=f"retry_practice_{current_index}",
                        on_click=retry_current_practice
                    )
                with col2:
                    st.button(
                        "Continue",
                        key=f"continue_practice_{current_index}",
                        on_click=continue_to_next_practice
                    )

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
            st.session_state.recording_started_practice = False
            st.session_state.error_occurred_practice = False
            st.session_state.results_practice = []

        phoneme_practice()

if __name__ == "__main__":
    main()
