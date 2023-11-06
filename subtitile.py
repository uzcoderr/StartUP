import open_subtitles
os = open_subtitles.OpenSubtitles()
os.login()
file_info = os.get_subtitle_file_info("file.mkv", "en", True)
os.download_subtitle(file_info['file_no'])