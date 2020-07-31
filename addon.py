from audio_dl import *
import sys
from file_check import *
from transcription import *
from training import *

VERSION = "0.0.1"


def searchVideo(youtube_link):
    print(youtube_link)

    #Short fix. to move directory up one for github purposes

    os.chdir("..")

    # Gets the custom part of the url and names the video it. E.G. watch=?12342
    # cant put the whole link due to the '/' in the names so we take only the unique part and can be saved and checked later
    # or used in the future for training purposes.
    y_unique = youtube_link[youtube_link.rindex('/') + 1:]
    # Leaves only the unique part of the url left.
    y_unique = y_unique.replace("watch?v=", "")


    version_path = 'youtube_links/' + y_unique + "/" + VERSION + ".txt"
    audio_directory = "youtube_links/" + y_unique + "/"
    audio_path = "youtube_links/" + y_unique + "/" + y_unique
    json_file = "youtube_links/" + y_unique + "/" + y_unique + ".json"
    training_output = "youtube_links/" + y_unique + "/" + "training/"
    training_audio_path = "youtube_links/" + y_unique + "/" + "training/" + y_unique

    # Check if the folder/json already exists if so set to true and don't run the NN instead just access already made
    # Transcription
    #Short fix. to move directory up one for github purposes
    folder_exists = checkIfFileExists(version_path)
    print(folder_exists)

    # Download the audio file from youtube using the youtube-dl package.
    downloadAudio(youtube_link, folder_exists, audio_directory, audio_path)

    # Transcribe the audio into a json file using Deepspeech neural network
    transcribeAudio(audio_path, json_file, folder_exists)

    # Read the json.
    data = readJson(json_file)

    # Remove wav file and add version.txt
    removeAudio(version_path, audio_path, folder_exists)

    # Fill the dictionary with each word, the times and durations of each word
    # fill an array with every timestamp of each occurance of every word.
    try:
        print("Here")
        word_dict, timestamps = createYTCaptionsDictionary(audio_path + ".vtt")
    except TypeError:
        print("Error")
        word_dict, timestamps = createDictionary(data)


    # while True:
    #     search = input(" (Enter 1 to end) Search for a word: ")
    #     if search == '1':
    #         break
    #     search = re.sub("(?<=[a-z])'(?=[a-z])", "", search)
    #     found_words, times = searchForWords(search, word_dict, timestamps)
    #     print(times)
    #     formatTime(times)
    #     print(found_words)
    #     # correct = input("What times have correct results for you: ")
    #     # Enter 1 if you want to download audio (Dev purposes Currently)
    #     # if correct == "1":
    #         # getTrainingClip(correct, youtube_link, training_output, training_audio_path)
    return (word_dict, timestamps)

if __name__ == "__main__":
    yt_link = input("Paste a youtube link that you want translated: ")
    searchVideo(yt_link)
#    searchVideo(yt_link)


