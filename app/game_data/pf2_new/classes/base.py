import json
import re

from discord import Colour, Embed, File

from app.models.pf2Response import Pf2Response
from app.util.markdown import markdown_pf2
from app.enums.Pf2Rarity import Rarity

class Pf2Thing:
    FOOTER_URL = "https://cdn.discordapp.com/attachments/778998112819085352/964148715067670588/unknown.png"

    CARDS_COLORS = {
        "empty": 0x090A0A,
        "common": 0x7289DA,
        "uncommon": 0xFF6E00,
        "rare": 0x1522B2,
        "unique": 0xA600A6,
    }

    CAST_TIME = {
        "1": ":one:",
        "2": ":two:",
        "3": ":three:",
        "2 or 3": ":two: or :three:",
        "free": ":free:",
        "reaction": ":leftwards_arrow_with_hook:",
        "long": ":alarm_clock:",
    }

    name: str
    level: int
    raw_description: str
    description: str
    additional_descriptions: list[dict[str, str]] | None = None
    pictures: list[str] | None = None
    source: str
    rarity: Rarity
    traits: list[str]

    def cut_success_stages(self, stages_text: str | None = None) -> list:
        if stages_text is None:
            return []
        all_stages = stages_text.split('\n\n')
        print(all_stages)
        sections = []
        stages = ('**Critical Success**', '**Success**', '**Failure**', '**Critical Failure**')
        for row in all_stages:
            for key in stages:
                if key in row:
                    sections.append({'name': key, 'content': row.replace(key, '- ').strip()})
        return sections

    def construct_description(self):
        self.description = self.replace_syntax(self.raw_description)
        self.additional_descriptions = []

        has_stages = False
        stages = ('\n**Critical Success**', '\n**Success**', '\n**Failure**', '\n**Critical Failure**')
        for i in stages:
            if i in self.description:
                has_stages = True

        if not has_stages:
            return

        i = 0
        while i != 4:
            stage = stages[i]
            if stage in self.description:
                i = 4
                continue
            i += 1
        stage = stage[1:]
        if '**Heightened**' in self.description:
            stages_text = self.description[self.description.find(stage):self.description.rfind('**Heightened**')]
        else:
            stages_text = self.description[self.description.find(stage):]
        self.description = self.description.replace(stages_text.strip(), '')
        self.additional_descriptions = self.cut_success_stages(stages_text)
        print(f'{self.additional_descriptions=}')

    @staticmethod
    def replace_syntax(text):
        text = re.sub(  # UUID
            r"@UUID\[([^\]]+)\](?:\{([^}]+)\})?",
            lambda m: m.group(2) if m.group(2) else m.group(1).split(".")[-1],
            text,
        )
        text = re.sub(  # dice
            r"\[\[/r\s+([^\]]+)\]\](?:\{([^}]+)\})?",
            lambda m: m.group(2) if m.group(2) else m.group(1),
            text,
        )
        text = re.sub(  # damage
            r"@Damage\[(\d+)\[([^\]]+)\]\](?:\{([^}]+)\})?",
            lambda m: m.group(3) if m.group(3) else f"{m.group(1)} {m.group(2)}",
            text,
        )
        text = re.sub(
            r'@Damage\[([^\]]+)\]',
            lambda m: m.group(1),
            text
        )
        text = re.sub(  # check
            r"@Check\[([^|]+)\|[^|\]]*(?:\|([^|\]]+))?\]",
            lambda m: f"{m.group(2) + ' ' if m.group(2) else ''}{m.group(1).capitalize()}",
            text,
        )
        text = text.replace('****', '** **')
        return text

    @classmethod
    def from_file(cls, filename: str):
        appendix = "app/game_data/pf2_new/"
        try:
            with open(appendix + filename, "r") as file:
                return cls.from_json(json.loads(file.read()))
        except FileNotFoundError:
            return None

    @classmethod
    def from_json(cls, data: dict):
        obj = cls()
        obj.name = data["name"]
        data = data['system']
        obj.level = data['level']['value']

        description_parsed = markdown_pf2(data["description"]["value"])
        obj.raw_description = description_parsed.text
        obj.pictures = description_parsed.pictures or []

        obj.source = data["publication"]["title"]
        obj.rarity = Rarity.from_string(data["traits"]["rarity"])
        obj.traits = data["traits"]["value"]
        return obj

    def to_embed(self) -> Pf2Response:
        color = self.CARDS_COLORS.get(self.rarity.value)

        embed_card = Embed(title=self.name,
                           description=self.description,
                           color=color)
        embed_card.set_footer(text=self.source, icon_url=self.FOOTER_URL)

        file = None
        for picture in self.pictures:
            file = File(f"temp_images/{picture}.png")
            embed_card.set_image(url=f"attachment://{picture}.png")

        for section in self.additional_descriptions:
            print(section)
            embed_card.add_field(name=section['name'], value=section['content'], inline=False)

        return Pf2Response(embed=embed_card, file=file)

    @staticmethod
    def get_embed_not_found():
        return Embed(
            title="OwO, what's this?",
            description="(по вашему запросу ничего не найдено)",
            colour=Colour.red(),
        )
