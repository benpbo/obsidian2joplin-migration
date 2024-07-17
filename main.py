import re
import os
from requests.exceptions import HTTPError

from joppy.api import Api

regex = re.compile(r'\[\[(.+)\]\]')

def main(api: Api):
    notes = api.get_all_notes(fields='id,title,body')
    titles = [note.title for note in notes]
    if len(set(titles)) < len(titles):
        print('Unable to handle duplicate titles. Aborting...')
        return

    title_to_id = { note.title: note.id for note in notes }
    def get_link_markdown(match: re.Match[str]) -> str:
        title = match.group(1)
        link_id = title_to_id[title]
        return f'[{title}](:/{link_id})'

    for note in notes:
        assert note.body is not None
        if not regex.search(note.body):
            continue

        assert note.id is not None
        print(f'Updating "{note.title}"')
        api.modify_note(
            note.id,
            body=regex.sub(get_link_markdown, note.body)
        )

if __name__ == '__main__':
    token = os.getenv("API_TOKEN")
    if not token:
        print('Please provide an API token using the API_TOKEN environment variable')
        exit(1)

    api = Api(token=token)

    try:
        main(api)
    except HTTPError as error:
        if error.response.status_code == 403:
            print('API token is wrong')
        else:
            raise error
