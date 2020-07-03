import os
from json import loads

import requests
from bs4 import BeautifulSoup

import settings
from formatters import format_offer_discord
from hooks import discord_hook
from jobs.base import JobDefinition, Offer

XKOM_HOT_SHOT_URL = "https://x-kom.pl/goracy_strzal"


def _parse_xkom(xkom_site):
    xkom_soup = BeautifulSoup(xkom_site, "html.parser")

    app_div = xkom_soup.find("div", id="app")

    product_name = app_div.find("h1").get_text()

    price_spans = (
        app_div.find("div", order=3)
        .find_all("div", recursive=False)[1]
        .find_all("div", recursive=False)[1]
        .find_all("span")[:2]
    )

    old_price = price_spans[0].get_text()
    new_price = price_spans[1].get_text()

    subtitle = f"{old_price} → {new_price}"

    json_script_content = app_div.find("script").string

    image_url = loads(json_script_content)["image"][0]

    return Offer(
        title=product_name,
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
