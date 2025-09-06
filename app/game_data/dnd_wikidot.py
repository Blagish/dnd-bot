import logging

from app.game_data.classes import SiteSystemSearcher
from app.models.pf2Response import Pf2Response
from app.util.markdown import markdown_dnd_wikidot

logger = logging.getLogger(__name__)

blacklisted_tags = []
CARDS_COLORS = {"NORMAL": 0xC4AF63, "UNEARTHED_ARCANA": 0x980082}
tags_with_new_strings = ("p", "li", "h1", "h2", "h3")


class DndEnSiteSearcher(SiteSystemSearcher):
    base_url = "http://dnd5e.wikidot.com/"
    search_url = "http://dnd5e.wikidot.com/spells"

    CARDS_COLORS = {"NORMAL": 0xC4AF63, "UNEARTHED_ARCANA": 0x980082}

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
        title = self._soup.find("div", attrs={"class": "page-title"}).get_text()
        colour = self.CARDS_COLORS["NORMAL"]
        if "(UA)" in title:
            colour = self.CARDS_COLORS["UNEARTHED_ARCANA"]
        return self._assemble_embed(title=title, colour=colour, url=spell_url, **result)

    def _parse_spells_page(self, name, page_text) -> list | None:
        super()._parse_spells_page(name, page_text)
        results = self._soup.find_all(
            lambda x: x and x.name == "td" and x.a and name in x.get_text().lower()
        )
        possible_result = None
        diff = 1e9

        if len(results) == 0:
            return None

        for tag in results:
            title = tag.get_text()
            logger.debug(f"title is {title}")
            if len(title) - len(name) < diff:
                diff = len(title) - len(name)
                possible_result = tag
        if possible_result:
            return [possible_result]
        return None

    def _parse_spell(self, page_text) -> dict:
        super()._parse_spell(page_text)
        card = self._soup.find("div", attrs={"id": "page-content"})
        ps = card.find_all("p")
        source = ps[0].get_text()
        source = source[source.find(" ") :]
        content = markdown_dnd_wikidot(card).text
        content = (
            content.replace("**Casting Time", "> **Casting Time")
            .replace("**Range", "> **Range")
            .replace("**Components", "> **Components")
            .replace("**Duration", "> **Duration")
        )
        return {"description": content, "footer": source}

if __name__ == "__main__":
    # print(get_spell("chaos bolt").description)
    searcher = DndEnSiteSearcher()
    spell = searcher.get_spell("fireball").embed
    print(spell.title)
    print(spell.description)
