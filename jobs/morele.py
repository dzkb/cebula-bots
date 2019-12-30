import requests
from bs4 import BeautifulSoup

import settings
from formatters import format_offer_discord
from hooks import discord_hook
from jobs.base import Offer


def _parse_morele(morele_site):
    morele_soup = BeautifulSoup(morele_site, "html.parser")

    product_link = morele_soup.find("div", {"class": "promo-box-name"}).a
    title = product_link.text
    offer_url = product_link["href"]
    image_url = morele_soup.find("a", {"class": "prom-box-image"}).img["src"]

    old_price = morele_soup.find("div", {"class": "promo-box-old-price"}).text
    new_price = morele_soup.find("div", {"class": "promo-box-new-price"}).text
    coupon = morele_soup.find("div", {"class": "promo-box-code-value"}).text

    description = f"{old_price} → {new_price} (kod: {coupon})"

    return Offer(
        title=title, description=description, offer_url=offer_url, image_url=image_url
    )


def run():
    morele_site = requests.get(settings.MORELE_DATA_URL)
    offer = _parse_morele(morele_site.text)

    payload = format_offer_discord(offer)
    discord_hook(settings.MORELE_DISCORD_HOOK_URL, payload)
