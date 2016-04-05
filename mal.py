import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler
from urllib.request import build_opener, install_opener
from urllib.request import urlopen

from config import read_mal_config


class AnimeEntry:
    def __init__(self, entry_id, title, english, synonyms, episodes,
                 score, entry_type, status, start_date, end_date, image, synopsis):
        self.id = entry_id
        self.title = title
        self.english = english
        self.synonyms = synonyms
        self.episodes = episodes
        self.score = score
        self.type = entry_type
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.image = image
        self.synopsis = synopsis.replace('<br />', '') if synopsis is not None else None

    @property
    def full_title(self):
        return '{} ({})'.format(self.title, self.type)

    @property
    def info(self):
        return "Synonyms: {}\nEpisodes: {}\nStatus: {}\nAired: {} to {}\nScore: {}{}".format(
            self.synonyms,
            self.episodes, self.status,
            self.start_date, self.end_date,
            self.score,
            "\n\n{}".format(self.synopsis) if self.synopsis is not None else None
        )

    @property
    def markdown(self):
        return '[{}](http://myanimelist.net/anime/{})\n{}'.format(
            self.full_title, self.id, self.info
        )


def authorize():
    mal_config = read_mal_config()

    pass_manager = HTTPPasswordMgrWithDefaultRealm()
    pass_manager.add_password(None, 'http://myanimelist.net/api',
                              mal_config['UserName'], mal_config['Password'])

    auth_handler = HTTPBasicAuthHandler(pass_manager)

    opener = build_opener(auth_handler)
    install_opener(opener)


def search(term):
    parameter = quote_plus(term)
    url = "http://myanimelist.net/api/anime/search.xml?q={}".format(parameter)

    response = urlopen(url).read().decode()

    if len(response) == 0:
        return []

    root = ET.fromstring(response)

    return [AnimeEntry(
        entry_id=entry.find('id').text,
        title=entry.find('title').text,
        english=entry.find('english').text,
        synonyms=entry.find('synonyms').text,
        episodes=entry.find('episodes').text,
        score=entry.find('score').text,
        entry_type=entry.find('type').text,
        status=entry.find('status').text,
        start_date=entry.find('start_date').text,
        end_date=entry.find('end_date').text,
        image=entry.find('image').text,
        synopsis=entry.find('synopsis').text
    ) for entry in root]


authorize()
