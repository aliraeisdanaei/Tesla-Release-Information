import requests
import json
from bs4 import BeautifulSoup

from Release_Family import Release_Family

RELEASE_FAMILIES_FILENAME = 'tesla_release_families.txt'
BASE_URL = 'https://tesla-info.com/release/'

TEST_RESP_FILENAME = 'HTMLS/2023.44.html'

JSON_OUTPUT_FILENAME = 'release_families.json'

def get_release_families(release_families_filename: str) -> list[str]:
    with open(release_families_filename, 'r') as f:
        release_families = f.readlines()
    return [rls.replace('\n', '') for rls in release_families]

def get_soup(base_url: str, release: str) -> BeautifulSoup:
    full_url = f'{base_url}{release}'
    response = requests.get(full_url)
    return BeautifulSoup(response.text, 'html.parser')

def get_soup_from_file(filename: str) -> BeautifulSoup:
    with open(filename, 'r') as f:
        return BeautifulSoup(f.read(), 'html.parser')

    

# soup = get_soup_from_file(TEST_RESP_FILENAME)
# release_family_name = '2023.44'

# release_family = Release_Family(release_family_name, soup)

# print(release_family._releases)
# print(release_family._updates)
# print(release_family.to_dict())

# release_family_dict = release_family.to_dict()
# json_str = json.dumps(release_family_dict)
# with open('release_family.json', 'w') as f:
#     f.write(json_str)

release_families_dict = []
for release_family_name in get_release_families(RELEASE_FAMILIES_FILENAME):
    print('Collecting data for: ', release_family_name)
    release_family = Release_Family(release_family_name, \
        get_soup(BASE_URL, release_family_name))
    # release_family_dict = release_family.to_dict()
    release_families_dict.append(release_family.to_dict())

print('Writing to JSON file: ', JSON_OUTPUT_FILENAME)
with open(JSON_OUTPUT_FILENAME, 'w') as f:
    f.write(json.dumps(release_families_dict))

# soup = get_soup(BASE_URL, release_families[0])
# print(soup)