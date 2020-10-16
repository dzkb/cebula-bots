from datetime import datetime

import requests
from listener import JobMisfireError

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
    response = _get_response()
    offer = _parse_xkom(response.json())

    if not offer:
        return JobMisfireError("xkom fired too early")

    payload = format_offer_discord(offer)
    discord_hook(settings.XKOM_DISCORD_HOOK_URL, payload)
