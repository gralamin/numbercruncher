import unittest
import copy
import json
import os
from pathlib import Path

from main import crunch

TEST_CARDS = {}

for card_file in os.listdir("testcards"):
    if not card_file.endswith("json"):
        continue
    file_path = os.path.join("testcards", card_file)
    with open(file_path) as f:
        card = json.load(f)
        key = Path(file_path).stem
        TEST_CARDS[key] = card


class TestNumCrunch(unittest.TestCase):
    def test_simple_gap(self):
        for result in crunch(
            [TEST_CARDS["ambrosia"], TEST_CARDS["auronsinspiration"]], "Ashe"
        ):
            self.assertIsNotNone(result.after_card)
            self.assertEqual(result.slots, 1)
            self.assertEqual(result.card.colors, ["W"])
            self.assertEqual(result.after_card.colors, ["W"])
            self.assertEqual(result.card.name, "ambrosia whiteheart")
            self.assertEqual(result.after_card.name, "auron's inspiration")
            self.assertEqual(result.card.collector_number, 6)
            self.assertEqual(result.after_card.collector_number, 8)
            break
        else:
            self.fail("Expected result")

    def test_no_gap(self):
        auron_copy = copy.deepcopy(TEST_CARDS["auronsinspiration"])
        auron_copy["collector_number"] = "7"
        for _ in crunch([TEST_CARDS["ambrosia"], auron_copy], "Ashe"):
            self.fail("No value expected")

    def test_matching_card(self):
        for result in crunch(
            [
                TEST_CARDS["ambrosia"],
                TEST_CARDS["fakeashe"],
                TEST_CARDS["auronsinspiration"],
            ],
            "Ashe",
        ):
            try:
                self.assertEqual(result.after_card, "Doesn't exist")
            except AttributeError:
                # expected
                pass
            self.assertEqual(result.card.colors, ["W"])
            self.assertEqual(result.card.name, "ashe fake name")
            self.assertEqual(result.card.collector_number, 7)
            break
        else:
            self.fail("Expected result")

    def test_endcolor_startnew(self):
        for result in crunch(
            [TEST_CARDS["zell"], TEST_CARDS["balambtrexaur"]],
            "Ashe",
        ):
            self.assertIsNotNone(result.after_card)
            self.assertEqual(result.slots, 2)
            self.assertEqual(result.card.colors, ["R"])
            self.assertEqual(result.after_card.colors, ["G"])
            self.assertEqual(result.card.name, "zell dincht")
            self.assertEqual(result.after_card.name, "balamb t-rexaur")
            self.assertEqual(result.card.collector_number, 170)
            self.assertEqual(result.after_card.collector_number, 173)
            break
        else:
            self.fail("Expected result")

    def test_multicolor_color_change(self):
        for result in crunch(
            [TEST_CARDS["choco"], TEST_CARDS["cid"]],
            "Ashe",
        ):
            self.fail("No expected result")

    def test_color_change_nogap(self):
        for result in crunch(
            [
                TEST_CARDS["zack"],
                TEST_CARDS["astrologiansplanisphere"],
                TEST_CARDS["dragoonswyvern"],
            ],
            "Ashe",
        ):
            self.fail("No expected result")
