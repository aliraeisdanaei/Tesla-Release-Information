import json
import sys

RELEASE_FAMILIES_FILENAME = 'release_families.json'

with open(RELEASE_FAMILIES_FILENAME) as f:
    release_family_data = json.load(f)

if len(sys.argv) > 1:
    update_name = sys.argv[1]
else:
    update_name = input("Please input update name: ")
print('Getting all unique descriptions for: ', update_name)

update_descriptions = ''

unique_update_desc = set()

for release_family in release_family_data:
    for update in release_family['updates']:
        if update_name == update['update_name']:
            update_desc = update['update_desc']

            if update_desc not in unique_update_desc:
                unique_update_desc.add(update_desc)

                update_descriptions += update_desc
                update_descriptions += '\n'
                update_descriptions += '\n'

if len(unique_update_desc) == 0:
    print('Nothing found :(')
else:
    print('Found ', len(unique_update_desc), ' unique update descriptions. :)')
    output_filename = f'Descriptions/{update_name}.txt'
    print('Saving descriptions to: ', output_filename)

    with open(output_filename, 'w') as f:
        f.write(update_descriptions)