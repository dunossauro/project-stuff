from datetime import datetime
from typing import Any

from httpx import get
from packaging.version import Version
from rich import print
from typer import Typer

app = Typer()

BASE_URL = 'https://pypi.org/pypi/{package}/json'


def format_date(date: str) -> str:
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y')


def license_metadata(info: dict[str, Any]) -> str:
    if (license := info.get('license')) and license:
        return license

    if (license := info.get('license_expression')) and license:
        return license

    for classifier in info['classifiers']:
        if 'License' in classifier:
            return classifier
    return ''


def last_release(releases: dict[str, Any]) -> dict[str, str]:
    release = sorted(releases, key=Version)[-1]

    return {
        'relase': release,
        'date': format_date(releases[release][0]['upload_time']),
    }


def first_release(releases: dict[str, Any]) -> dict[str, str]:
    release = sorted(releases, key=Version)[0]

    try:
        return {
            'relase': release,
            'date': format_date(releases[release][0]['upload_time']),
        }
    except KeyError:
        return {'release': release, 'data': ''}


@app.command()
def package_data(package: str):
    response = get(BASE_URL.format(package=package), timeout=None)

    data = response.json()

    author = data['info']['author']
    home_page = data['info']['home_page']
    license = license_metadata(data['info'])
    l_release = last_release(data['releases'])
    f_release = first_release(data['releases'])
    url = data['info']['package_url'] + '#history'

    print(
        {
            'author': author,
            'homepage': home_page,
            'package': package,
            'url': url,
            'license': license,
            'first release': f_release,
            'last release': l_release,
        }
    )
