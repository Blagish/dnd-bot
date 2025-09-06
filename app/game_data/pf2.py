from typing import Any

import loguru
import requests
from bs4 import BeautifulSoup
from discord import Colour, Embed

from app.models.pf2Response import Pf2Response
from app.util.tables import TableParser

logger = loguru.logger

tags_with_new_strings = ("p", "li", "h1", "h2", "h3")
tags_to_ignore_parse = ("footer",)

ACTIONS = {
    "action1": ":one:",
    "action2": ":two:",
    "action3": ":three:",
    "actionF": ":free:",
    "Reaction": ":leftwards_arrow_with_hook:",
}

CARDS_COLORS = {
    "EMPTY": 0x090A0A,
    "NORMAL": 0x7289DA,
    "NORMAL_LEGACY": 0x9CACE5,
    "UNCOMMON": 0xFF6E00,
    "RARE": 0x1522B2,
    "UNIQUE": 0xA600A6,
}

FOOTER_URL = "https://cdn.discordapp.com/attachments/778998112819085352/964148715067670588/unknown.png"


def parse_content(element: Any, ignore_br=True, markdown=True) -> str:
    if isinstance(element, str):
        if element.strip(" ") == "":
            return ""
        return element
    if not ignore_br and element.name == "br":
        return " "
    if element.name == "i":
        action_class = element.attrs["class"][1]
        return ACTIONS.get(action_class, "")
    if element.text == "" or element.name in tags_to_ignore_parse:
        return ""

    if element.name == "table":
        table = TableParser(
            element,
            parse_string=parse_content,
            parse_kwargs={"ignore_br": False, "markdown": False},
            align_left="l",
            style="ms",
        )
        table_text = table.get_for_embed()
        if table_text == "":
            return ""
        return table.get_for_embed() + "\n"

    style1 = style2 = ""
    text = ""
    if markdown:
        if element.name in tags_with_new_strings:
            style2 = "\n"
            if element.name == "li":
                style1 = "- "
        elif element.attrs.get("data-toggle") is not None:
            style1 = style2 = "__"
        elif element.name == "em":
            style1 = style2 = "*"
        elif element.name == "strong":
            style1 = style2 = "**"
    for child in element.children:
        text += parse_content(child, ignore_br=ignore_br, markdown=markdown)
    return f"{style1}{text}{style2}"


def get_info(
    name, trait=None, mention_multiple=False, cut_description=True
) -> Pf2Response:
    logger.debug(f"pf: looking for {name}")
    search_url = "https://pf2easy.com/php/search.php"
    action_url = "https://pf2easy.com/php/actionInfo.php"
    year = 2023
    normal_color_key = "NORMAL"
    name = name.strip().replace("'", "’")
    response = requests.post(search_url, {"name": name, "year": year})
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("button")

    if trait is not None:
        trait = trait.upper().strip()

    if len(results) == 0:
        year = 2022
        normal_color_key = "NORMAL_LEGACY"
        response = requests.post(search_url, {"name": name, "year": year})
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("button")

    if trait:
        results = list(filter(lambda x: trait in x.find("small").text, results))

    if len(results) == 0:
        logger.debug("no results")
        return Pf2Response(
            embed=Embed(
                title="OwO, what's this?",
                description="(по вашему запросу ничего не найдено)",
                colour=Colour.red(),
            )
        )

    ans = None
    if len(results) == 1:
        ans = results[0]
    else:
        for i in results:
            if i.find("strong").text == name:
                ans = i

    if ans is None and len(results) > 1:
        logger.debug(f"{len(results)=}")
        choices = []
        for i in results[:5]:
            choices.append(
                {"name": i.find("strong").text, "trait": i.find("small").text}
            )
        return Pf2Response(
            embed=Embed(
                title="┗( T﹏T )┛ у меня несколько ответов!",
                description="Выберите нужный из списка:",
                colour=Colour.dark_gold(),
            ),
            choices=choices,
        )

    # if (
    #     ans.find("strong").text.lower() != name
    #     and mention_multiple
    #     and len(results) > 1
    # ):
    #     ans_text = "Нашла больше одного варианта ответа. Какой вас больше устраивает?\n"
    #     for i in range(min(len(results), 4)):
    #         ans_type = results[i].find("small").text or ""
    #         ans_name = results[i].find("strong").text or ""
    #         ans_text += f"{i+1}. {ans_name} *({ans_type.lower()})*\n"
    #     ans_text += "Выберите ответ реакцией с соответствующим числом."
    #     return ans_text

    res_id = ans.find("input").attrs["value"]
    data = requests.post(action_url, {"id_feature": res_id, "year": year})
    soup = BeautifulSoup(data.text, "html.parser")
    message = ""

    color = CARDS_COLORS["EMPTY"]
    source = soup.find("div", attrs={"class": "source"}).text
    description = ""
    if len(h1s := soup.find_all("h1")) > 0:  # is a spell/feat with levels most likely
        title = (
            parse_content(h1s[0], markdown=False)
            .replace("×", "")
            .replace("\n", "")
            .strip()
        )
        if ":" in title:
            title = title[: title.find(":")].title() + " " + title[title.find(":") :]
        else:
            title = title.title()
        level = (
            soup.find("h2").text.replace("×", "").replace("\n", "").lower()
        )  # not only a level, but feat type, etc.
        description = f"*{level}*\n"
    else:  # most likely a rule or smth
        title = soup.find_all("h2")[-1].text.replace("×", "").replace("\n", "").title()

    if (traits := soup.find("section", attrs={"class": "traits"})) is not None:
        traits_text = traits.get_text("|").split("|")
        color = CARDS_COLORS.get(traits_text[0], CARDS_COLORS[normal_color_key])
        description += f'> **Traits** `{"`, `".join(traits_text)}`\n'

    #addon = False
    if (details := soup.find("section", attrs={"class": "details"})) is not None:
        if "addon" not in details.attrs["class"]:
            details_text = "> " + parse_content(details).replace("\n**", "\n> **")
            details_text = details_text.replace("Traditions", "Traditions ")
            description += details_text
        #else:
            #addon = True  # добавить потом типа таблицы в общем да как в архетипах.

    if (content := soup.find("section", attrs={"class": "content"})) is not None:
        description += parse_content(content)

    if (
        len(
            contents_extra := soup.find_all(
                "section", attrs={"class": ["content extra"]}
            )
        )
        > 0
    ):
        for content_extra in contents_extra:
            description += parse_content(content_extra)
            # embed_card.add_field(name='', value=parse_content(content_extra), inline=False)

    if (
        len(
            details_addon := soup.find_all(
                "section", attrs={"class": ["details addon"]}
            )
        )
        > 0
    ):
        for detail_addon in details_addon:
            description += parse_content(detail_addon)
            # embed_card.add_field(name='', value=parse_content(content_extra), inline=False)
    if cut_description:
        if len(description) <= 2048:
            embed_card = Embed(title=title, description=description, color=color)
            embed_card.set_footer(text=source, icon_url=FOOTER_URL)
            logger.debug("results found")
            return Pf2Response(message=message, embed=embed_card)
        else:
            sep = description.rfind("\n", 0, 2047)
            embed_card = Embed(title=title, description=description[:sep], color=color)
            description = description[sep + 1 :]
            other_embeds = []
            while len(description) > 2048:
                sep = description.rfind("\n", 0, 2047)
                other_embeds.append(
                    Embed(
                        title=title + " (cont.)",
                        description=description[:sep],
                        color=color,
                    )
                )
                description = description[sep + 1 :]
            other_embeds.append(
                Embed(title=title + " (cont.)", description=description, color=color)
            )
            return Pf2Response(
                message=message, embed=embed_card, other_embeds=other_embeds
            )
    else:
        embed_card = Embed(title=title, description=description, color=color)
        embed_card.set_footer(text=source, icon_url=FOOTER_URL)
        logger.debug("results found")
        return Pf2Response(message=message, embed=embed_card)


if __name__ == "__main__":
    # res = get_info("earth", trait='CREATURE 1', cut_description=True)
    # res = get_info("leaf weave", trait='armor', cut_description=True)
    res = get_info("howling blizzard", cut_description=True)
    print(res.embed.title, res.embed.description, len(res.embed.description), sep="\n")
    # print(res.other_embeds)
