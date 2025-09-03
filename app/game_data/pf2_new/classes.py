import json
from app.util.markdown import markdown

from discord import Embed, Colour, File
import re
from app.models.pf2Response import Pf2Response

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
        "long": ":alarm_clock:"
    }

    @staticmethod
    def replace_syntax(text):
        text = re.sub(  # UUID
            r'@UUID\[([^\]]+)\](?:\{([^}]+)\})?',
            lambda m: m.group(2) if m.group(2) else m.group(1).split('.')[-1],
            text
        )
        text = re.sub(  # dice
            r'\[\[/r\s+([^\]]+)\]\](?:\{([^}]+)\})?',
            lambda m: m.group(2) if m.group(2) else m.group(1),
            text
        )
        text = re.sub(  # damage
            r'@Damage\[(\d+)\[([^\]]+)\]\](?:\{([^}]+)\})?',
            lambda m: m.group(3) if m.group(3) else f"{m.group(1)} {m.group(2)}",
            text
        )
        text = re.sub(  # check
            r'@Check\[([^|]+)\|[^|]*(?:\|([^]]+))?\]',
            lambda m: f"{m.group(2) + ' ' if m.group(2) else ''}{m.group(1).capitalize()}",
            text
        )
        return text

    @classmethod
    def from_file(cls, filename: str):
        appendix = 'app/game_data/pf2_new/'
        try:
            with open(appendix+filename, 'r') as file:
                return cls.from_json(json.loads(file.read()))
        except FileNotFoundError:
            return None

    @classmethod
    def from_json(cls, data: dict):
        return cls()


class Spell(Pf2Thing):
    name: str
    type: str
    area: str | None
    description: str
    tags: list[str]
    traits: list[str]
    source: str
    casting_time: str
    rarity: str
    range: str | None
    save: str | None
    duration: str | None
    target: str | None
    pictures: list[str] | None

    def __init__(self, name=None, type=None, area=None, description=None, tags=None, traits=None, source=None, casting_time=None, rarity=None, range=None, save=None, duration=None, target=None, pictures=None):
        self.name = name
        self.type = type
        self.area = area
        self.description = description
        self.source = source
        self.casting_time = casting_time
        self.tags = []
        self.rarity = rarity
        self.range = range
        self.save = save
        self.duration = duration
        self.target = target
        self.pictures = pictures if pictures is not None else []

        if tags:
            for i in tags:
                self.tags.append(i)

        self.traits = []
        if traits:
            for i in traits:
                self.traits.append(i)


    @classmethod
    def from_json(cls, data: dict):
        cls_data = {'name': data['name']}

        data = data['system']

        cls_data['area'] = f"{data['area']['value']}-foot {data['area']['type']}" or None if data.get('area') else None
        cls_data['range'] = data['range']['value'] or None if data.get('range') else None

        if data.get('duration'):
            cls_data['duration'] = data['duration']['value'] or ('sustained' if data['duration']['sustained'] else None) or None

        cls_data['target'] = data['target']['value'] or None if data.get('target') else None

        if data.get('defense'):
            if data['defense'].get('save'):
                cls_data['save'] = data['defense']['save']['statistic'].capitalize()
                if data['defense']['save']['basic']:
                    cls_data['save'] = 'basic ' + cls_data['defence'].capitalize()

        description_parsed = markdown(data['description']['value'])
        cls_data['description'] = description_parsed.text
        cls_data['pictures'] = description_parsed.pictures
        cls_data['traits'] = data['traits']['value']
        if 'cantrip' in cls_data['traits']:
            type_ = 'cantrip'
        elif 'ritual' in cls_data['traits']:
            type_ = 'ritual'
        elif 'focus' in cls_data['traits']:
            type_ = 'focus'
        else:
            type_ = 'spell'
        type_ += f" {data['level']['value']}"
        cls_data['type'] = type_
        cls_data['tags'] = data['traits']['traditions']
        cls_data['source'] = data['publication']['title']
        cls_data['casting_time'] = data['time']['value']
        cls_data['rarity'] = data['traits']['rarity']

        return cls(**cls_data)

    def parse_raw_description(self):
        result = self.replace_syntax(self.description)
        return result

    def construct_description(self):
        type_ = f'*{self.type}*'
        traits = f"`{'`, `'.join(self.traits)}`".upper()
        basic_info = [f"> **Traits** {traits}", f"> **Traditions** {', '.join(self.tags)}"]

        if not self.casting_time.isdigit():
            basic_info.append(f"> **Cast** {self.casting_time}")

        if self.range is not None:
            if self.area is not None:
                basic_info.append(f"> **Range** {self.range}; **Area** {self.area}")
            elif self.target is not None:
                basic_info.append(f"> **Range** {self.range}; **Targets** {self.target}")
            else:
                basic_info.append(f"> **Range** {self.range}")

        elif self.area is not None:
            basic_info.append(f"> **Area** {self.area}")

        elif self.target is not None:
            basic_info.append(f"> **Targets** {self.target}")

        if self.save is not None:
            if self.duration is not None:
                basic_info.append(f"> **Defense** {self.save}; **Duration** {self.duration}")
            else:
                basic_info.append(f"> **Defense** {self.save}")

        elif self.duration is not None:
            basic_info.append(f"> **Duration** {self.duration}")

        data = [type_, '\n'.join(basic_info), self.parse_raw_description()]
        return '\n'.join(data)

    def to_embed(self):
        title = self.name + ' ' + self.CAST_TIME.get(self.casting_time, self.CAST_TIME['long'])
        description = self.construct_description()
        color = self.CARDS_COLORS.get(self.rarity, self.CARDS_COLORS['empty'])
        embed_card = Embed(title=title, description=description, color=color)
        file = None
        for picture in self.pictures:
            file = File(f"temp_images/{picture}.png")
            embed_card.set_image(url=f"attachment://{picture}.png")
            
        embed_card.set_footer(text=self.source, icon_url=self.FOOTER_URL)
        return Pf2Response(embed=embed_card, file=file)


    @staticmethod
    def get_embed_not_found():
        return Embed(
            title="OwO, what's this?",
            description="(по вашему запросу ничего не найдено)",
            colour=Colour.red()
        )
