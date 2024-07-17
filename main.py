import re
from joppy.api import Api

TOKEN = '2ac144116f437c87f2973dd6d727cbc7e313d6109061ce2b7472eba7898d113d507440f52260a223da12c82f22b2f1e64e316dc5fe074a691c4b41476c277c66'

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
    api = Api(token=TOKEN)
    main(api)
