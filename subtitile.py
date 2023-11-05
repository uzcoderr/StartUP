import requests
from bs4 import BeautifulSoup


def get_subtitles(movie_name):
    """Downloads subtitles for a movie from OpenSubtitles.org.

    Args:
      movie_name: The name of the movie to download subtitles for.

    Returns:
      A list of subtitle URLs.
    """

    url = f"https://www.opensubtitles.org/search/sublanguageid-eng/moviename-{movie_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    subtitles = []
    for subtitle in soup.find_all("a", class_="subtitles-list__link"):
        subtitles.append(subtitle["href"])

    return subtitles


# Example usage:

subtitles = get_subtitles("Loki")

# Download the subtitles to the current directory.
for subtitle in subtitles:
    requests.get(subtitle, stream=True).raw.decode_content_as('utf-8').write_to('The Shawshank Redemption.srt')
