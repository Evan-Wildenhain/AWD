import os
import json
import regex as re
from simliarity import *


def strTimeToSeconds(time):
    seconds = 0
    time = re.split('[:.]', time)
    seconds += float(time[0]) * 3600
    seconds += float(time[1]) * 60
    seconds += float(time[2])
    seconds += float(time[3]) / 1000
    return round(seconds, 2)


def transcribeAudio(audio_path, json_file, folder_exists):
    if not folder_exists:
        try:
            os.remove(json_file)
        except OSError:
            pass
        os.system("deepspeech --model 7model.pbmm --json --audio " + audio_path + " >> " + json_file)


def readJson(json_file):
    with open(json_file) as f:
        return json.load(f)

def createYTCaptionsDictionary(fpath):
    word_dict = {}
    full_timestamps = []
    try:
        with open(fpath) as f:
            end_of_line_time_uncorrected = re.findall('-> [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]', f.read(), re.MULTILINE)
        end_of_line_time_corrected = []
        for i in range(0, len(end_of_line_time_uncorrected), 2):
            end_of_line_time_corrected.append(re.sub("-> ", "", end_of_line_time_uncorrected[i]))
        f.close()
    except FileNotFoundError:
        return

    with open(fpath) as f:
        match = re.findall('.*<c>.*', f.read(), re.MULTILINE)
        end_of_line_time_corrected.reverse()
    for line in match:
        words = re.sub(
            '</c><[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]><c>|<[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]><c>',
            "", line)
        timestamps = re.findall('[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]', line)
        timestamps.append(end_of_line_time_corrected.pop())
        full_timestamps += timestamps
        words = re.sub('</c>', "", words)
        words = words.split()
        for index, word in enumerate(words):
            if word == "":
                continue
            elif word not in word_dict:
                word_dict[word] = ([strTimeToSeconds(timestamps[index])], [0])
            else:
                word_dict[word][0].append(strTimeToSeconds(timestamps[index]))
    return word_dict, full_timestamps

def createDictionary(data):
    # Storage of word_dict is ([time],[duration])
    word_dict = {}
    timestamps = []

    for name in data['transcripts'][0]['words']:
        word = name['word']
        time = name['start_time ']
        duration = name['duration']
        word = simliarityTranscription(word)
        word = re.sub("(?<=[a-z])'(?=[a-z])", "", word)
        if word in word_dict:
            word_dict[word][0].append(time)
            word_dict[word][1].append(duration)
        else:
            word_dict[word] = ([time], [duration])
        timestamps.append(time)
    return (word_dict, timestamps)


def searchForWords(searched_words, word_dict, timestamps):

    used_words = []
    if searched_words != "":
        lookup = searched_words.split()
        lookup.reverse()
    else:
        all_words_times = []
        for value in word_dict:
            all_words_times += word_dict[value][0]
            used_words.append(value)
        all_words_times.sort()
        return used_words, all_words_times

    if len(lookup) >= 2:
        phrase = True


    if searched_words[-1] == ' ':
        used_words, last_word = simliarityLookup(lookup[0].lower(), word_dict, True)
    else:
        used_words, last_word = simliarityLookup(lookup[0].lower(), word_dict, False)

    if len(lookup) == 1:
        last_word.sort()
        return used_words, last_word

    prev_word = set(last_word)

    next_word = []
    # Continues in reverse order skipping the last word E.G. "my name is" - "name", "my"
    for word in lookup[1:]:
        curr_word = []
        next_word, phrase_times = simliarityLookup(word, word_dict, phrase)
        for times in phrase_times:
            try:
                if timestamps[timestamps.index(times) + 1] in prev_word:
                    curr_word.append(times)
            except IndexError:
                continue
        used_words.append(next_word)
        prev_word = set(curr_word)


    result = []
    for times in curr_word:
        each_time = []
        for i in range(0, len(lookup)):
            each_time.append(timestamps[timestamps.index(times) + i])
        result.append(each_time)

    result.sort()
    return used_words, result


def formatTime(times):
    print("Total Results found: ", len(times))
    if len(times) == 0:
        return
    elif isinstance(times[0], float) or isinstance(times[0], int):
        for time in times:
            if time // 3600 >= 1:
                print("{}:{:02d}:{:02d}.{:.0f}".format(int(time // 3600), int(time // 60), int(time % 60),
                                                       int(time % 1 * 100)), end="  ")
            else:
                print("{:02d}:{:02d}.{:.0f}".format(int(time // 60), int(time % 60), int(time % 1 * 100)), end="  ")
        return
    elif isinstance(times[0], list):
        for sub in times:
            for time in sub:
                if time // 3600 >= 1:
                    print("{}:{:02d}:{:02d}.{:.0f}".format(int(time // 3600), int(time // 60), int(time % 60),
                                                           int(time % 1 * 100)), end="  ")
                else:
                    print("{:02d}:{:02d}.{:.0f}".format(int(time // 60), int(time % 60), int(time % 1 * 100)),
                          end="  ")
            print()
        return
    return


