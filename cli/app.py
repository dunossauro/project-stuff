from typing import Any

from httpx import get
from packaging.version import Version
from rich import print
from typer import Typer

app = Typer()

BASE_URL = 'https://pypi.org/pypi/{package}/json'


def license_metadata(classifiers: list[str]) -> str:
    for classifier in classifiers:
        if 'License' in classifier:
            return classifier
    return ''


def last_release(releases: dict[str, Any]) -> dict[str, str]:
    release = sorted(releases, key=Version)[-1]

    return {'relase': release, 'date': releases[release][0]['upload_time']}


def first_release(releases: dict[str, Any]) -> dict[str, str]:
    release = sorted(releases, key=Version)[0]

    try:
        return {
            'release': release,
            'date': releases[release][0]['upload_time'],
        }
    except KeyError:
        return {'release': release, 'data': ''}


@app.command()
def package_data(package: str):
    response = get(BASE_URL.format(package=package), timeout=None)

    data = response.json()

    license = license_metadata(data['info']['classifiers'])
    l_release = last_release(data['releases'])
    f_release = first_release(data['releases'])
    url = data['info']['package_url'] + '#history'

    print(
        {
            'package': package,
            'url': url,
            'licença': license,
            'primeira_release': f_release,
            'release_atual': l_release,
        }
    )
