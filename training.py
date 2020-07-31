from audio_dl import *


def getTrainingClip(timestamp, link, folder, training_audio_path):
    downloadTrainAudio(link, False, folder, training_audio_path)
