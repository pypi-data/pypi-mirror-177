from aqua_cli import name, __version__
from aqua_cli.utils import check_update

def about():
    print(f'{name} v{__version__}')
    check_update.check_update()