import webbrowser, requests, zipfile, io
from bs4 import BeautifulSoup


def subtitles_downloader():
    try:
        # Get Movie Name For Subtitles
        movie_name = input("Enter Movie Name:")

        # replacing spaces with hyphen to get valid link
        legal_movie_name = movie_name.replace(" ", "-")

        # now getting the page for Movie Subtitles in English
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        url = requests.get('https://www.subscene.com/subtitles/' + legal_movie_name + "/english", headers=headers)
        url_soup = BeautifulSoup(url.content, 'html.parser')

        # getting all the urls of english subtitles of the movie name
        urls = []
        for link in url_soup.select('.a1 a', href=True):
            urls.append(link['href'])

        # selecting first link from the list
        sub_link = 'https://www.subscene.com/' + urls[0]
        sub_url = requests.get(sub_link)
        sub_url_soup = BeautifulSoup(sub_url.content, 'html.parser')

        # accessing the download button and getting download link.
        dl_btn = sub_url_soup.select('.download a')
        dl_link = dl_btn[0]['href']
        download_link = 'https://www.subscene.com/' + dl_link

        # getting .srt files from the link using requests.
        r = requests.get(download_link)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()

        # printing confirmation message.
        print("Subtitles Downloaded.Check The Folder where this python file is stored.")

    # handling exception where subtitles are not found
    except IndexError:
        print("No File Found For:" + movie_name)


subtitles_downloader()
