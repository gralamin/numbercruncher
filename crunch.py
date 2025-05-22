import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class CardData:
    def __init__(self, name, collector_number, colors):
        self.name = name
        self.collector_number = collector_number
        self.colors = colors

    def __str__(self):
        return f"#{self.collector_number} colors {self.colors}, name {self.name}"


class CrunchResult(ABC):
    def __init__(self, card):
        self.card = card

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def exitcode(self):
        pass


class CrunchMatch(CrunchResult):
    def __init__(self, card):
        super().__init__(card)

    def display(self):
        logger.info(f"Found matching card\n {str(self.card)}")

    def exitcode(self):
        return 1


class CrunchOpen(CrunchResult):
    def __init__(self, before_card, after_card, slots):
        self.after_card = after_card
        self.slots = slots
        super().__init__(before_card)

    def display(self):
        logger.info(
            f"Found {self.slots} slots between\n {str(self.card)}\n {str(self.after_card)}"
        )

    def exitcode(self):
        return 0


class SearchState:
    def __init__(self):
        self.before_card = CardData(None, None, None)
        self.after_card = CardData(None, None, None)
        self.last_card = CardData(None, None, None)

    def reset(self):
        # Keep last card, leave rest
        self.before_card = CardData(None, None, None)
        self.after_card = CardData(None, None, None)

    def new_before_card(self, card):
        self.reset()
        self.before_card = card

    def new_last_card(self, card):
        self.last_card = card

    def new_after_card(self, card):
        self.after_card = card


def crunch(cards, card_to_ask):
    state = SearchState()
    search_name = card_to_ask.lower()
    for c in cards:
        if c["variation"] or c["promo"]:
            continue
        if "cardfaces" in c:
            c = c["cardfaces"][0]
        name = c["name"].lower()
        # special casing "a" and "the", move to the end.
        if name.startswith("a "):
            name = name[2:] + ", a"
        elif name.startswith("the "):
            name = name[4:] + ", the"

        try:
            collector_number = int(c["collector_number"])
        except ValueError:
            # Weird collector number, not handled
            continue

        if "card_faces" in c:
            c = c["card_faces"][0]
        colors = c.get("colors", [])

        card_data = CardData(name, collector_number, colors)

        if name.startswith(search_name):
            yield CrunchMatch(card_data)

        if name < search_name:
            logger.debug(f"{name} < {search_name}")
            state.new_before_card(card_data)
        elif name > search_name and state.before_card.name is not None:
            logger.debug(f"{name} > {search_name}")
            state.new_after_card(card_data)
        # Special case: Colors change, but you could appear between, eg Zell and Balamb T-rexaur
        elif (
            name > search_name
            and state.last_card.name
            and state.last_card.name > name
            and state.last_card.colors != colors
        ):
            # More conditions, multicolor is all together
            if len(colors) >= 2 and len(state.last_card.colors) >= 2:
                continue
            state.new_after_card(card_data)
            state.new_before_card(state.last_card)

        if state.after_card.name and state.before_card.name:
            slots = (
                state.after_card.collector_number
                - state.before_card.collector_number
                - 1
            )
            logger.debug(f"{slots} slots")
            if slots > 0:
                yield CrunchOpen(state.before_card, state.after_card, slots)
            state.reset()
        state.new_last_card(card_data)

    if state.before_card.name:
        slots = (
            state.last_card.collector_number - state.before_card.collector_number - 1
        )
        logger.debug(f"{slots} slots at end")
        if slots > 0:
            yield CrunchOpen(state.before_card, state.last_card, slots)
    return
