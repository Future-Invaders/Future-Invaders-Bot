"""Class to represent a card"""

class LanguagesStrings():
    en: str
    fr: str

class Release():
    uuid: str
    name: LanguagesStrings
    date: str

class Faction():
    uuid: str
    name: LanguagesStrings

class CardType():
    uuid: str
    name: LanguagesStrings

class Rarity():
    uuid: str
    name: LanguagesStrings
    max_card_count: int

class Image():
    uuid: str
    path: str

class LanguagesImages():
    en: Image
    fr: Image

class Card():
    uuid: str
    endpoint: str
    url: str
    name: LanguagesStrings
    cost: str
    income: str
    weapons: int
    durability: int
    body: dict
    release: Release
    faction: Faction
    card_type: CardType
    rarity: Rarity
    images: LanguagesImages
    arsenal: [dict]
    tags: [dict]
