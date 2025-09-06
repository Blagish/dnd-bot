import logging
import re

from bs4 import BeautifulSoup

from app.game_data.classes import SiteSystemSearcher
from app.models.pf2Response import Pf2Response
from app.util.markdown import markdown_dnd_su

logger = logging.getLogger(__name__)


class DndRuSiteSearcher(SiteSystemSearcher):
    base_url = "https://dnd.su/"
    search_url = "https://dnd.su/spells/?search="

    COLOUR = 0xFE650C

    def __init__(self, use_2024=False):
        super().__init__()
        if use_2024:
            self.base_url = "https://next.dnd.su/"
            self.search_url = "https://next.dnd.su/spells/?search="

    def get_spell(self, name) -> Pf2Response:
        if len(name) < 4:
            return self.get_too_short_embed()

        search_txt = self._request_search(search=name)
        if search_txt is None:
            return self.get_error_embed(self.base_url)

        spells = self._parse_spells_page(name, search_txt)
        if spells is None:
            return self.get_not_found_embed()
        elif len(spells) > 1:
            return self.get_multiple_choices_embed({})  # spells

        spell = spells[0]
        spell_url = self.base_url + spell.a.get("href")
        spell_text = self._request_spell(spell.a.get("href"))
        if spell_text is None:
            return self.get_not_found_embed()

        result = self._parse_spell(spell_text)
        title = spell.get_text().replace('PH24', '').replace('PH14', '').strip()
        return self._assemble_embed(
            title=title, colour=self.COLOUR, url=spell_url, footer='dnd.su', **result
        )

    def _parse_spells_page(self, name, page_text) -> list | None:
        super()._parse_spells_page(name, page_text)
        # print(self._soup.get_text())
        results = self._soup.find_all("h2", attrs={"class": "card-title"})
        possible_result = None
        diff = 1e9

        if results[0].get_text().startswith("По вашему"):
            logger.debug("no results")
            return None

        for tag in results[:2]:
            title = tag.get_text()
            logger.debug(f"title is {title}")
            parts = title.split(" [")
            title = parts[1]
            if "а" <= name[0] <= "я":
                title = parts[0]
            if len(title) - len(name) < diff:
                diff = len(title) - len(name)
                possible_result = tag

        if possible_result is None:
            logger.debug("no results")
            return None

        return [possible_result]

    def _parse_spell(self, page_text) -> dict:
        super()._parse_spell(page_text)
        card = self._soup.find(
            "div", attrs={"class": "card__body", "itemprop": "articleBody"}
        )
        content = markdown_dnd_su(card)
        card_text = re.sub(r"> (?!\*\*)", "", content.text)
        card_text = card_text.replace("\n  ", "\n")
        return {"description": card_text}

    def get_english_name(self, name):
        page = self._request_spell(name)
        if page is None:
            return None
        soup = BeautifulSoup(page, "html.parser")
        results = soup.find_all("h2", attrs={"class": "card-title"})
        possible_result = None
        diff = 1e9
        if results[0].get_text().startswith("По вашему"):
            return None
        for tag in results:
            title = tag.get_text()
            parts = title.split(" [")
            title = parts[0]
            if len(title) - len(name) < diff:
                diff = len(title) - len(name)
                possible_result = parts[1][:-1]
        return possible_result


if __name__ == "__main__":
    searcher = DndRuSiteSearcher(use_2024=False)
    spell = searcher.get_spell("огненный шар").embed
    print(spell.title)
    print(spell.description)
