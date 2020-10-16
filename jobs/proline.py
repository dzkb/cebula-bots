import requests
from bs4 import BeautifulSoup

import settings
from formatters import format_offer_discord
from hooks import discord_hook
from jobs.base import Offer, prepare_description

URL = "https://proline.pl"
HEADERS = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
        "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    ),
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    ),
}


def _get_response():
    return requests.get(URL, headers=HEADERS)


def _parse_proline(proline_site):
    soup = BeautifulSoup(proline_site, "html.parser")

    old_price = soup.find("td", {"class": "cena_old"}).b.get_text(strip=True)
    new_price = soup.find("td", {"class": "cena_new"}).b.get_text(strip=True)

    link = soup.find("a", {"class": "fotka"})
    offer_url = URL + link["href"]
    image_url = URL + link.img["src"]
    title = link["title"]

    description = prepare_description(old_price, new_price)

    return Offer(
        title=title, description=description, offer_url=offer_url, image_url=image_url
    )


def run():
    response = _get_response()
    offer = _parse_proline(response.text)

    payload = format_offer_discord(offer)
    discord_hook(settings.PROLINE_DISCORD_HOOK_URL, payload)
