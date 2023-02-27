import speech_recognition as sr
import pyttsx3
import wolframalpha
import tkinter as tk

# Initialize text-to-speech object
engine = pyttsx3.init()

# Initialize API client
client = wolframalpha.Client("RR8R97-LPG2PU9P7L")

# Function to answer question
def answer_question(question):
    # Use API to get answer to the question
    res = client.query(question)
    answer = next(res.results, None)

    # Check if the answer is available
    if answer is not None:
        # Print the question and answer in the console
        print(f"Question: {question}")
        print(f"Answer: {answer.text}")
        # Speak the answer
        engine.say(answer.text)
        engine.runAndWait()
        # Return the question and answer 
        return question, answer.text
    else:
        # If the answer is not available, return an error message
        error_message = "Sorry, I couldn't find an answer to your question."
        # Print the error message in the console
        print(error_message)
        # Speak the error message using text-to-speech
        engine.say(error_message)
        engine.runAndWait()
        # Return the error message as a tuple
        return question, error_message

# Function to transcribe audio and call answer_question function
def transcribe_audio():
    # initialise speech recognition object
    speech_recognizer = sr.Recognizer()

    # Use default microphone as audio source
    with sr.Microphone() as source:
        # Reduce input noise
        speech_recognizer.adjust_for_ambient_noise(source)
        # Listen the input question from user
        audio = speech_recognizer.listen(source)

    # convert audio to text using SpeechRecognition library
    try:
        text = speech_recognizer.recognize_google(audio)
        # Call answer_question function with text
        question, answer = answer_question(text)
        # Update answer label in the GUI with question and answer
        answer_label.config(text=f"Question: {question}\nAnswer: {answer}")
        # Handle exceptions
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))

# GUI
root = tk.Tk()

# Add label to GUI
instruction_label = tk.Label(root, text="Press the button and ask your question.")
instruction_label.pack()

# Add button to get audio input
button = tk.Button(root, text="Ask a question", command=transcribe_audio)
button.pack()

# Label for question and answer
answer_label = tk.Label(root, text="Question: \nAnswer: ")
answer_label.pack()

# Start GUI
root.mainloop()
