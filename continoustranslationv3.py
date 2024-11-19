import os
import azure.cognitiveservices.speech as speechsdk

def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=os.environ.get('SPEECH_KEY'),
        region=os.environ.get('SPEECH_REGION')
    )
    
    # Set the input language (e.g., Hindi)
    speech_translation_config.speech_recognition_language = "hi-IN"
    
    # Set the target language (e.g., English)
    to_language = "en"
    speech_translation_config.add_target_language(to_language)

    # Set up the microphone input
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=speech_translation_config,
        audio_config=audio_config
    )

    # Function to handle the recognized speech results
    def handle_translation_result(evt):
        if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
            print("Recognized: {}".format(evt.result.text))
            print(f"Translated into '{to_language}': {evt.result.translations[to_language]}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")
        elif evt.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.result.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region values?")

    # Attach the event handler for when recognition results are available
    translation_recognizer.recognized.connect(handle_translation_result)

    # Start continuous recognition
    print("Starting continuous translation. Speak into your microphone in Hindi.")
    translation_recognizer.start_continuous_recognition()

    # Keep the program running until manually stopped
    try:
        while True:
            pass  # Keeps the program running and processing speech recognition
    except KeyboardInterrupt:
        print("\nContinuous recognition stopped by user.")

    # Stop the recognizer gracefully after interruption
    translation_recognizer.stop_continuous_recognition()

recognize_from_microphone()
