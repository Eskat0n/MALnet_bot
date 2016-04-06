import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler
from urllib.request import build_opener, install_opener
from urllib.request import urlopen

from config import read_mal_config


class Entry:
    def __init__(self, entry_id, title, english, synonyms,
                 score, entry_type, status,
                 start_date, end_date,
                 synopsis, image):
        self.id = entry_id
        self.title = title
        self.full_title = '{} ({})'.format(title, entry_type)
        self.english = english
        self.synonyms = synonyms
        self.score = score
        self.type = entry_type
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.synopsis = (synopsis or '').replace('<br />', '')
        self.image = image

    @property
    def synonyms_info(self):
        return 'Synonyms: {}'.format(self.synonyms)

    @property
    def score_info(self):
        return 'Score: {}'.format(self.score)

    @property
    def status_info(self):
        return 'Status: {}'.format(self.status)

    @property
    def to_markdown(self):
        return '[{}]({})\n{}'.format(self.full_title, self.url, self.all_info)

class AnimeEntry(Entry):
    def __init__(self, entry_id, title, english, synonyms, episodes,
                 score, entry_type, status, start_date, end_date, image, synopsis):
        super().__init__(entry_id, title, english, synonyms,
                         score, entry_type, status,
                         start_date, end_date, synopsis, image)
        self.url = 'http://myanimelist.net/anime/{}'.format(entry_id)
        self.episodes = episodes

    @property
    def all_info(self):
        return "{}\nEpisodes: {}\n{}\nAired: {} to {}\n{}\n\n{}".format(
            self.synonyms_info,
            self.episodes, self.status_info,
            self.start_date, self.end_date,
            self.score_info,
            self.synopsis
        )

class MangaEntry(Entry):
    def __init__(self, entry_id, title, english, synonyms, volumes, chapters,
                 score, entry_type, status, start_date, end_date, image, synopsis):
        super().__init__(entry_id, title, english, synonyms,
                         score, entry_type, status,
                         start_date, end_date, synopsis, image)
        self.url = 'http://myanimelist.net/manga/{}'.format(entry_id)
        self.volumes = volumes
        self.chapters = chapters

def authorize():
    mal_config = read_mal_config()

    pass_manager = HTTPPasswordMgrWithDefaultRealm()
    pass_manager.add_password(None, 'http://myanimelist.net/api',
                              mal_config['UserName'], mal_config['Password'])

    auth_handler = HTTPBasicAuthHandler(pass_manager)

    opener = build_opener(auth_handler)
    install_opener(opener)


def _search(entry_type, term):
    parameter = quote_plus(term)
    url = "http://myanimelist.net/api/{}/search.xml?q={}".format(entry_type, parameter)

    response = urlopen(url).read().decode()
    if len(response) == 0:
        return None

    return ET.fromstring(response)


def search_anime(term):
    root = _search('anime', term)
    if root is None:
        return []

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
        synopsis=entry.find('synopsis').text,
        image=entry.find('image').text
    ) for entry in root]


def search_manga(term):
    root = _search('manga', term)
    if root is None:
        return []

    return [MangaEntry(
        entry_id=entry.find('id').text,
        title=entry.find('title').text,
        english=entry.find('english').text,
        synonyms=entry.find('synonyms').text,
        volumes=entry.find('volumes').text,
        chapters=entry.find('chapters').text,
        score=entry.find('score').text,
        entry_type=entry.find('type').text,
        status=entry.find('status').text,
        start_date=entry.find('start_date').text,
        end_date=entry.find('end_date').text,
        synopsis=entry.find('synopsis').text,
        image=entry.find('image').text
    ) for entry in root]

authorize()
