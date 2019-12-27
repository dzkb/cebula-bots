def format_offer_discord(offer):
    return {
        "embeds": [
            {
                "title": offer.title,
                "description": offer.description,
                "url": offer.offer_url,
                "thumbnail": {"url": offer.image_url},
            }
        ]
    }
