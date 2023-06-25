from typing import Any, Dict, List

import httpx
from packaging.version import Version
from rich import print
from typer import Typer


app = Typer()
pypi_url = 'https://pypi.org/pypi/{package}/json'


def send_request(package: str) -> Dict[str, Any]:
    response = httpx.get(pypi_url.format(package=package), timeout=None)
    return response.json()


def get_last_release(releases: Dict[str, Any]) -> Dict[str, str]:
    release = max(releases, key=Version)
    return {
        'release': release,
        'date': releases[release][0]['upload_time']
    }


def get_first_release(releases: Dict[str, Any]) -> Dict[str, str]:
    release = sorted(releases, key=Version)[0]
    try:
        return {
            'release': release,
            'date': releases[release][0]['upload_time'],
        }
    except KeyError:
        return {'release': release, 'date': ''}


def get_license(classifiers: List[str]) -> str:
    return next((
        classifier for classifier in classifiers if 'License' in classifier
        ),
        ''
    )


@app.command()
def package_data(package: str):
    data = send_request(package)
    license = get_license(data['info']['classifiers'])
    l_release = get_last_release(data['releases'])
    f_release = get_first_release(data['releases'])
    url = f"{data['info']['package_url']}#history"

    print(
        {
            'package': package,
            'url': url,
            'licença': license,
            'primeira_release': f_release,
            'release_atual': l_release,
        }
    )


@app.command()
def total_versions(package: str):
    data = send_request(package)
    total = len(data['releases'].keys())
    print(f"Total de versões disponíveis para o pacote {package}: {total}")


@app.command()
def package_versions(package: str):
    data = send_request(package)
    print(f"Versões disponíveis para o pacote {package}:")
    print(list(data['releases'].keys()))


@app.command()
def total_downloads(package: str):
    data = send_request(package)
    download_counts = [
        release['downloads']
        for release in data['releases'].values()
        if 'downloads' in release
    ]
    print(
        f"Total de downloads para o pacote {package}: {sum(download_counts)}"
    )


@app.command()
def package_info(package: str):
    data = send_request(package)
    print(
        {
            'package': package,
            'info': data['info']
        }
    )

