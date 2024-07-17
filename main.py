import re
from joppy.api import Api

TOKEN = '2ac144116f437c87f2973dd6d727cbc7e313d6109061ce2b7472eba7898d113d507440f52260a223da12c82f22b2f1e64e316dc5fe074a691c4b41476c277c66'

regex = re.compile(r'\[\[.+\]\]')

def main(api: Api):
    notes = api.get_all_notes(fields='id,title,body')
    for note in notes:
        assert note.body is not None
        matches = regex.findall(note.body)
        if not matches:
            continue

        print(note.title)
        for match in matches:
            print(match)
        print()

if __name__ == '__main__':
    api = Api(token=TOKEN)
    main(api)
