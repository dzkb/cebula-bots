import requests
from bs4 import BeautifulSoup

import settings
from formatters import format_offer_discord
from hooks import discord_hook
from jobs.base import JobDefinition, Offer

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}


def _parse_proline(proline_site):
    proline_soup = BeautifulSoup(proline_site, "html.parser")

    old_price = proline_soup.find("td", {"class": "cena_old"}).get_text(strip=True)
    new_price = proline_soup.find("td", {"class": "cena_new"}).get_text(strip=True)

    link = proline_soup.find("a", {"class": "fotka"})
    offer_url = settings.PROLINE_DATA_URL + link["href"]
    image_url = settings.PROLINE_DATA_URL + link.img["src"]
    title = link["title"]

    description = f"{old_price} → {new_price}"

    return Offer(
        title=title, description=description, offer_url=offer_url, image_url=image_url
    )


def run():
    proline_site = requests.get(settings.PROLINE_DATA_URL, headers=headers)
    offer = _parse_proline(proline_site.text)

    payload = format_offer_discord(offer)
    discord_hook(settings.PROLINE_DISCORD_HOOK_URL, payload)
