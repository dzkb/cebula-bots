import logging
from datetime import datetime
from time import sleep

import requests
import settings
from formatters import format_offer_discord
from hooks import discord_hook

from jobs.base import Offer, prepare_description

OFFER_URL = "https://x-kom.pl/goracy_strzal"
URL = "https://mobileapi.x-kom.pl/api/v1/xkom/hotShots/current"
PARAMS = {"onlyHeader": "true"}
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "time-zone": "UTC",
    "x-api-key": "sJSgnQXySmp6pqNV",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
        "/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    ),
}


def _get_response():
    return requests.get(URL, params=PARAMS, headers=HEADERS)


def _parse_xkom(hotshot, skip_date_check: bool = False):
    promotionEnd = datetime.strptime(hotshot["PromotionEnd"], r"%Y-%m-%dT%H:%M:%SZ")
    if not skip_date_check and promotionEnd < datetime.now():
        # fired too soon
        return False

    old_price = str(hotshot["OldPrice"])
    new_price = str(hotshot["Price"])

    offer_url = OFFER_URL
    image_url = hotshot["PromotionPhoto"]["ThumbnailUrl"]
    title = hotshot["PromotionName"]

    products_count = hotshot["PromotionTotalCount"]
    sold_count = hotshot["SaleCount"]

    description = prepare_description(
        old_price, new_price, f"Sprzedano {sold_count} z {products_count} szt."
    )

    return Offer(
        title=title,
        description=description,
        offer_url=offer_url,
        image_url=image_url,
    )


def run():
    retries = 0
    MAX_RETRIES = 5

    while retries < MAX_RETRIES:
        response = _get_response()
        if response.status_code == 200:
            try:
                json_payload = response.json()
            except ValueError:
                logging.getLogger("apscheduler").exception(
                    "xkom_job expected json payload as response but didn't get it! "
                    "scraping and/or parsing need to be investigated!"
                )
                return False

            try:
                offer = _parse_xkom(json_payload)
            except (KeyError, ValueError):
                logging.getLogger("apscheduler").exception(
                    "xkom_job received unexpected json payload structure! scraping "
                    "and/or parsing need to be investigated!"
                )
                return False

            if offer:
                payload = format_offer_discord(offer)
                discord_hook(settings.XKOM_DISCORD_HOOK_URL, payload)
                return True
        retries += 1
        logging.getLogger("apscheduler").debug(
            "xkom_job was fired too soon and will retry in "
            f"{settings.XKOM_RETRY_DELAY_SECS}s ({retries}/{MAX_RETRIES})"
        )
        sleep(settings.XKOM_RETRY_DELAY_SECS)

    logging.getLogger("apscheduler").warn(
        f"xkom_job failed after {MAX_RETRIES} retries"
    )
    return False
