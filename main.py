from joppy.api import Api

TOKEN = '2ac144116f437c87f2973dd6d727cbc7e313d6109061ce2b7472eba7898d113d507440f52260a223da12c82f22b2f1e64e316dc5fe074a691c4b41476c277c66'

def main(api: Api):
    print(api.get_all_notes())

if __name__ == '__main__':
    api = Api(token=TOKEN)
    main(api)
