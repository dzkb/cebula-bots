from collections import namedtuple
from re import match

JobDefinition = namedtuple("JobDefinition", ["id", "function", "trigger"])
Offer = namedtuple("Offer", ["title", "description", "offer_url", "image_url"])


def parse_price(price: str):
    price.replace(",", ".")
    price = match(r"(\d+(\.\d+)?).*", price).group(1)
    return float(price)


def prepare_description(old_price: str, new_price: str, bottom_text: str = None):
    old_price = parse_price(old_price)
    new_price = parse_price(new_price)
    price_diff = old_price - new_price
    discount = round(100 * price_diff / old_price)
    description = (
        f"~~{old_price:.2f}zł~~ → {new_price:.2f}zł "
        f"(-{price_diff:.2f}zł/-{discount:d}%)"
    )
    if bottom_text:
        return description + "\n" + bottom_text
    else:
        return description
