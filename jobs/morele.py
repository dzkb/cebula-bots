import requests
import settings
from bs4 import BeautifulSoup
from formatters import format_offer_discord
from hooks import discord_hook

from jobs.base import Offer, prepare_description

URL = "https://morele.net"
HEADERS = {
    "accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
        "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    ),
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    ),
}


def _get_response():
    return requests.get(URL, headers=HEADERS)


def _parse_morele(morele_site):
    soup = BeautifulSoup(morele_site, "html.parser")

    link = soup.find("div", {"class": "promo-box-name"}).a
    title = link.text
    offer_url = link["href"]
    image_url = soup.find("a", {"class": "prom-box-image"}).img["src"]

    old_price = soup.find("div", {"class": "promo-box-old-price"}).get_text(strip=True)
    new_price = soup.find("div", {"class": "promo-box-new-price"}).get_text(strip=True)

    coupon = soup.find("div", {"class": "promo-box-code-value"}).text

    description = prepare_description(old_price, new_price, f"kod: {coupon}")

    return Offer(
        title=title, description=description, offer_url=offer_url, image_url=image_url
    )


def run():
    morele_site = _get_response()
    offer = _parse_morele(morele_site.text)

    payload = format_offer_discord(offer)
    discord_hook(settings.MORELE_DISCORD_HOOK_URL, payload)
