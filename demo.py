from datetime import datetime
from pprint import pprint
from random import choice, randint
from time import sleep

import requests

ISINS = [
    "US88160R1014",  # Tesla
    "US36467W1099",  # Gamestop
    "US0378331005",  # Apple
    "IE00B4L5Y983",  # MSCI World ETF
]

SENTENCES = [
    "Time to get rich, {side}ing {quantity} orders of {isin} should do the trick!",
    "Can't stop now, let's keep this train going! {isin} to the moooooon 🚀 {side} for {quantity}!",
    "Just one more and then I'll go to bed, I promise...",
    "I wonder if I should {side} more {isin}... Ah heck, what could go wrong!",
    "Oh shute, I better {side} some more {isin} quickly",
    "I've never seen {isin} do this... {side}, {side}, {side}!!!",
]

SIDES = ["buy", "sell"]


def sleep_random():
    sleep(randint(1, 4))


def select_random_isin() -> str:
    return choice(ISINS)


def select_random_sentence() -> str:
    return choice(SENTENCES)


def select_random_side() -> str:
    return choice(SIDES)


def select_random_quantity() -> int:
    return randint(1, 200)


def select_random_future_date() -> int:
    return int(datetime.utcnow().timestamp() + randint(10000, 1000000))


def announce_trade(sentence: str, isin: str, side: str, quantity: int):
    print("\n", sentence.format(isin=isin, side=side, quantity=quantity))


def make_trade(isin: str, side: str, quantity: int, valid_until: int) -> bool:
    order = {
        "isin": isin,
        "side": side,
        "quantity": quantity,
        "valid_until": valid_until,
    }

    response = requests.post("http://localhost:8000/orders/", data=order)

    print("🤖 -> ", end="")
    pprint(response.json())


def trade():
    sentence = select_random_sentence()
    isin = select_random_isin()
    side = select_random_side()
    quantity = select_random_quantity()
    valid_until = select_random_future_date()

    announce_trade(sentence, isin, side, quantity)
    make_trade(isin, side, quantity, valid_until)


if __name__ == "__main__":
    while True:
        trade()
        sleep_random()
