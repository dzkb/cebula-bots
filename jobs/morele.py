import requests

import settings
from formatters import format_offer_discord
from hooks import discord_hook
from jobs.base import Offer


def _parse_morele(morele_site):
    return Offer(title="", description="", offer_url="", image_url="")


def run():
    morele_site = requests.get(settings.MORELE_DATA_URL)
    offer = _parse_morele(morele_site.text)

    payload = format_offer_discord(offer)
    discord_hook(settings.MORELE_DISCORD_HOOK_URL, payload)
