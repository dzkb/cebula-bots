from collections import namedtuple

JobDefinition = namedtuple("JobDefinition", ["id", "function", "trigger"])
Offer = namedtuple("Offer", ["title", "description", "offer_url", "image_url"])
