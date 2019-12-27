import os

import requests
from bs4 import BeautifulSoup

import settings
from formatters import format_offer_discord
from hooks import discord_hook
from jobs.base import JobDefinition, Offer

XKOM_HOT_SHOT_URL = "https://x-kom.pl/goracy_strzal"


def _parse_xkom(xkom_site):
    xkom_soup = BeautifulSoup(xkom_site, "html.parser")

    product_impression = xkom_soup.find("div", {"class": "product-impression"})
    old_price = xkom_soup.find("div", {"class": "old-price"})
    new_price = xkom_soup.find("div", {"class": "new-price"})

    title = product_impression.p.text
    subtitle = "{old_price} → {new_price}".format(
        old_price=old_price.text, new_price=new_price.text
    )
    image_url = product_impression.img["src"]

    return Offer(
        title=title,
        description=subtitle,
        offer_url=XKOM_HOT_SHOT_URL,
        image_url=image_url,
    )


def run():
    hook_url = settings.XKOM_DISCORD_HOOK_URL
    data_url = settings.XKOM_DATA_URL

    xkom_site = requests.get(data_url)
    offer = _parse_xkom(xkom_site.text)

    payload = format_offer_discord(offer)
    discord_hook(hook_url, payload)
