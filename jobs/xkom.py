import logging
import os
from datetime import datetime
from json import JSONDecoder
from time import sleep

import requests
from bs4 import BeautifulSoup

import settings
from formatters import format_offer_discord
from hooks import discord_hook
from jobs.base import JobDefinition, Offer

XKOM_HOT_SHOT_URL = "https://x-kom.pl/goracy_strzal"


def _parse_xkom(xkom_site):
    xkom_soup = BeautifulSoup(xkom_site, "html.parser")

    script = xkom_soup.find("div", class_="container").find("script", type=None).string

    pre_hotshot_marker = r'{"type":"HotShot","extend":'

    hotshot_start_pos = script.find(pre_hotshot_marker) + len(pre_hotshot_marker)

    hotshot, _ = JSONDecoder().raw_decode(script[hotshot_start_pos:])

    promotionEnd = datetime.strptime(hotshot["promotionEnd"], r"%Y-%m-%dT%H:%M:%SZ")
    if promotionEnd < datetime.now():
        return None

    product_name = hotshot["promotionName"]

    old_price = hotshot["oldPrice"]
    new_price = hotshot["price"]
    promotion = hotshot["promotionGainTextLines"][1]
    products_count = hotshot["promotionTotalCount"]
    sold_count = hotshot["saleCount"]

    subtitle = f"""~~{old_price} zł~~ → {new_price} zł (-{promotion})
    Sprzedano {sold_count} z {products_count} szt."""

    image_url = hotshot["promotionPhoto"]["thumbnailUrl"]

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

    if not offer:
        delay = settings.XKOM_RETRY_DELAY_SECS
        max_retries = settings.XKOM_MAX_RETRIES
        logging.getLogger("apscheduler").info(
            f"xkom_job was fired too early. will retry up to {max_retries} times with {delay}s delay"
        )

        retries = 0
        while not offer and retries < max_retries:
            sleep(delay)
            retries += 1
            logging.getLogger("apscheduler").info(
                f"xkom_job retry attempt {retries}/{max_retries}"
            )
            xkom_site = requests.get(data_url)
            offer = _parse_xkom(xkom_site.text)

        if offer:
            logging.getLogger("apscheduler").info(
                f"xkom_job succeeded after {retries} retries"
            )
        else:
            logging.getLogger("apscheduler").warn(
                f"xkom_job failed after {max_retries} retries"
            )

    if offer:
        payload = format_offer_discord(offer)
        discord_hook(hook_url, payload)
