from aqua_cli import name, __version__
import requests

url = 'https://api.github.com/repos/nyf9b/aqua-cli/releases/latest'
latest_version = None

def check_update():
    try:
        get_update(latest_version, url)
    except:
        print('Couldn\'t check for updates. Are you connected to the Internet?')

def get_update(latest_version, url):
    latest_version = requests.get(url=url).json()['tag_name']

    if latest_version == __version__:
        print('No update available.')
        return

    print(f'A new release is available: v{latest_version}\nUpdate {name} with pip: pip install --upgrade aqua-cli')