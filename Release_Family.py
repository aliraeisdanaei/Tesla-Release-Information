import re
from bs4 import BeautifulSoup

class Update:
    def __init__(self, update_name: str, description: str):
        self._update_name = update_name
        self._countries = []
        self._models = []
        self._description = description

    def to_dict(self):
        return {
            'update_name': self._update_name,
            'update_desc': self._description
        }

class Release_Family:
    def __init__(self, release_family_name: str, soup: BeautifulSoup):
        self._release_family_name = release_family_name
        self._soup = soup
        self._releases = {}
        self._regional_availability = {
            'North America': [],
            'Europe': [],
            'RoW': []
        }

        self._updates = []

        self.set_releases_information()
        self.set_updates()
    
    def to_dict(self):
        return {
            'release_family_name': self._release_family_name,
            'releases': self._releases,
            'updates': [update.to_dict() for update in self._updates]
        }

    @classmethod
    def get_percentage(cls, raw_percentage: str) -> float:
        if '(no cars)' in raw_percentage:
            return 0
        percentage = re.findall(r'\d+\.\d+', raw_percentage)
        if percentage:
            return float(percentage[0])
        raise ValueError(f'No percentage found in {raw_percentage}.')

    def set_releases_information(self):
        releases_paragraph = self._soup.find('h2', string=f'Release {self._release_family_name}').next_element.next_element.next_element
        releases_links = releases_paragraph.findAll('a')
        for release_tag in releases_links:
            release = release_tag.get_text() 
            percentage = Release_Family.get_percentage(release_tag.next_element.next_element)
            # print(release, percentage)

            self._releases[release] = percentage
    
    def set_updates(self):
        update_title_tag = self._soup.find_all('h3', class_='mt-4 mt-lg-0')
        update_desc_tag = self._soup.find_all('div', class_='col-lg-9')

        assert(len(update_desc_tag) == len(update_title_tag))

        for i, update_title in enumerate(update_title_tag):
            update_title = update_title.get_text().replace('\n', '')
            update_desc = update_desc_tag[i].get_text().replace('\n', '').replace('\u2022 ', '')
            # print(update_title)
            # print(update_desc)
            self._updates.append(Update(update_title, update_desc))

        # print(self._updates[0])
        # print(vars(self._updates[0]))

    # def __vars__(self)

        