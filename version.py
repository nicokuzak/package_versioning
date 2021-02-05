"""
Given a requirements file, adds the current latest version of all the libraries.

python /Users/nkuzak003/Documents/personal/package_versioning/version.py \
    --load /Users/nkuzak003/Documents/personal/anomalydetection_autoencoders/requirements.txt
"""
import argparse

from bs4 import BeautifulSoup
import requests

def get_version(lib):
    url = 'https://pypi.org/project/' + lib
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    line = soup.find('h1', class_='package-header__name')
    return line.text.strip('\n').strip().replace(' ', '==')

def save_reqs(ret, args):
    print('Saving new requirements.txt...')
    save = args.save
    if save is None:
        save = args.load
    with open(save, 'w') as f:
        f.write('\n'.join(ret))

def main(args):
    with open(args.load) as f:
        lines = f.readlines()
    lines = [l.strip('\n') for l in lines]

    ret = []
    for lib in lines:
        if '=' in lib:
            if '==' in lib:
                lib = lib[:lib.find('=')]
            else:
                lib = lib[:lib.find('>')]
        ret += [get_version(lib)]
    
    save_reqs(ret, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--load',
                        type=str,
                        required=True,
                        help='/path/to/load/file/')
    parser.add_argument(
        '--save',
        type=str,
        help='/path/to/save/file')

    args = parser.parse_args()
    main(args)
