import streamlit as st
import speech_recognition as sr
import time

# Function to transcribe speech
def transcribe_speech(api_choice, language):
    # Initialize recognizer class
    r = sr.Recognizer()
    r.pause_threshold = 1.5  # Waits longer before assuming speech is finished

    with sr.Microphone() as source:
        # Adjust for ambient noise to improve recognition accuracy
        r.adjust_for_ambient_noise(source, duration=1)
        
        st.info("Speak now... (Click 'Pause' to pause)")
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            # Choose the API for transcription
            if api_choice == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api_choice == "Sphinx (offline)":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                text = "Unsupported API choice."
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"API request error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

# Main function for the app
def main():
    st.title("Enhanced Speech Recognition App")
    st.write("Use the settings below to customize your experience.")

    # Choose API for speech recognition
    api_choice = st.selectbox("Select Speech Recognition API", ["Google", "Sphinx (offline)"])
    
    # Choose Language
    language = st.selectbox("Select Language", ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE"])
    
    # Button to start/stop recording
    start_button = st.button("Start Recording")
    pause_button = st.button("Pause")

    if start_button:
        text = transcribe_speech(api_choice, language)
        st.write("Transcription:", text)
        
        # Option to save transcription to file
        if st.button("Save Transcription to File"):
            with open("transcription.txt", "w") as f:
                f.write(text)
            st.success("Transcription saved to transcription.txt")

    elif pause_button:
        st.info("Recording paused. Click 'Start Recording' to continue.")

# Run the app
if __name__ == "__main__":
    main()
