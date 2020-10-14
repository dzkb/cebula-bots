import logging
from datetime import datetime
from decimal import Decimal
from time import sleep

import requests
import settings
from formatters import format_offer_discord
from hooks import discord_hook

from jobs.base import Offer

XKOM_HOT_SHOT_URL = "https://x-kom.pl/goracy_strzal"
XKOM_HOT_SHOT_API_URL = "https://mobileapi.x-kom.pl/api/v1/xkom/hotShots/current"
XKOM_PARAMS = {"onlyHeader": "true"}
XKOM_HEADERS = {
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


def _send_request():
    return requests.get(XKOM_HOT_SHOT_API_URL, params=XKOM_PARAMS, headers=XKOM_HEADERS)


def _parse_xkom(hotshot, skip_date_check: bool = False):
    promotionEnd = datetime.strptime(hotshot["PromotionEnd"], r"%Y-%m-%dT%H:%M:%SZ")
    if not skip_date_check and promotionEnd < datetime.now():
        # fired too soon
        return False

    title = hotshot["PromotionName"]

    old_price = Decimal(hotshot["OldPrice"])
    new_price = Decimal(hotshot["Price"])
    price_diff = Decimal(hotshot["PromotionGainValue"])
    discount = round(100 * price_diff / old_price)

    products_count = hotshot["PromotionTotalCount"]
    sold_count = hotshot["SaleCount"]

    description = f"""~~{old_price} zł~~ → {new_price} zł (-{price_diff}zł/-{discount}%)
        Sprzedano {sold_count} z {products_count} szt."""

    image_url = hotshot["PromotionPhoto"]["ThumbnailUrl"]

    return Offer(
        title=title,
        description=description,
        offer_url=XKOM_HOT_SHOT_URL,
        image_url=image_url,
    )


def run():
    retries = 0
    MAX_RETRIES = 5

    while retries < MAX_RETRIES:
        response = _send_request()
        if response.status_code == 200:
            try:
                offer = _parse_xkom(response.json())
            except ValueError:
                logging.getLogger("apscheduler").exception(
                    "xkom_job expected json payload as response but didn't get it! "
                    "scraping and/or parsing need to be investigated!"
                )
                return False
            except KeyError:
                logging.getLogger("apscheduler").exception(
                    "xkom_job received unexpected json payload structure! scraping "
                    "and/or parsing need to be investigated!"
                )
                return False
            else:
                if offer:
                    payload = format_offer_discord(offer)
                    print(payload)
                    exit(0)
                    discord_hook(settings.XKOM_DISCORD_HOOK_URL, payload)
                    return True
                else:
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
