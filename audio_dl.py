import os
import youtube_dl
import shutil


ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'embedsubs' :True,
    'writeautomaticsub' : True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'outtmpl': 'youtube_links/file.%(ext)s',
}

ydl_train_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'youtube_links/file.%(ext)s',
}


def downloadAudio(link, folder_exists, audio_directory, fin):
    if not folder_exists:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([link])

    if not folder_exists:
        try:
            shutil.rmtree(audio_directory)
        except OSError:
            pass
        os.makedirs(audio_directory)

    # Rename the wav file of the video to the custom url info.
    if not folder_exists:
        os.rename("youtube_links/file.wav", fin)
        if os.path.exists("youtube_links/file.en.vtt"):
            os.rename("youtube_links/file.en.vtt",fin+".vtt")


def downloadTrainAudio(link, folder_exists, audio_directory, fin):
    if not folder_exists:
        with youtube_dl.YoutubeDL(ydl_train_opts) as ydl:
            result = ydl.download([link])

    if not folder_exists:
        try:
            shutil.rmtree(audio_directory)
        except OSError:
            pass
        os.makedirs(audio_directory)

    # Rename the wav file of the video to the custom url info.
    if not folder_exists:
        os.rename("youtube_links/file.mp3", fin)

