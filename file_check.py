import os


def checkIfFileExists(path):
    if not os.path.exists(path):
        return False
    else:
        return True

def removeAudio(path,audio,folder_exists):
    if not folder_exists:
        os.mknod(path)
        os.remove(audio)