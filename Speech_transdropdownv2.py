import os
import azure.cognitiveservices.speech as speechsdk
import tkinter as tk
from tkinter import ttk

# Function to handle speech translation
def translate_speech(input_lang, output_lang):
    # Map human-readable language names to Azure language codes
    language_mapping = {
        "English (US)": "en-US",
        "Hindi (India)": "hi-IN",
        "Malayalam (India)": "ml-IN",
        "English (Text)": "en",
        "Hindi (Text)": "hi",
        "Malayalam (Text)": "ml",
    }
    
    # Get correct language codes
    input_lang = language_mapping[input_lang]
    output_lang = language_mapping[output_lang]
    
    # Configure the Speech Translation service
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=os.environ.get('SPEECH_KEY'),
        region=os.environ.get('SPEECH_REGION')
    )
    speech_translation_config.speech_recognition_language = input_lang
    speech_translation_config.add_target_language(output_lang)

    # Set up microphone audio input
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=speech_translation_config,
        audio_config=audio_config
    )

    print(f"Speak into your microphone in {input_lang}.")
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    # Handle the results
    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Recognized: {}".format(translation_recognition_result.text))
        print(f"Translated into '{output_lang}': {translation_recognition_result.translations[output_lang]}")
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

# Function to be triggered when the "Translate" button is clicked
def on_translate():
    input_lang = input_language_var.get()
    output_lang = output_language_var.get()
    translate_speech(input_lang, output_lang)

# Create a GUI using tkinter
root = tk.Tk()
root.title("Speech Translation")
root.geometry("400x300")

# Language options
language_options = {
    "English (US)": "en-US",
    "Hindi (India)": "hi-IN",
    "Malayalam (India)": "ml-IN",
    "English (Text)": "en",
    "Hindi (Text)": "hi",
    "Malayalam (Text)": "ml",
}

# Dropdown for input language
tk.Label(root, text="Select Input Language:").pack(pady=10)
input_language_var = tk.StringVar()
input_language_dropdown = ttk.Combobox(root, textvariable=input_language_var, state="readonly")
input_language_dropdown['values'] = ["English (US)", "Hindi (India)", "Malayalam (India)"]
input_language_dropdown.current(0)  # Default to first option
input_language_dropdown.pack()

# Dropdown for output language
tk.Label(root, text="Select Output Language:").pack(pady=10)
output_language_var = tk.StringVar()
output_language_dropdown = ttk.Combobox(root, textvariable=output_language_var, state="readonly")
output_language_dropdown['values'] = ["English (Text)", "Hindi (Text)", "Malayalam (Text)"]
output_language_dropdown.current(0)  # Default to first option
output_language_dropdown.pack()

# Button to start translation
translate_button = tk.Button(root, text="Translate", command=on_translate)
translate_button.pack(pady=20)

# Run the application
root.mainloop()
