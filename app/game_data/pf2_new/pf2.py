import json
from markdownify import markdownify as md

from app.game_data.pf2_new.searcher import initialize_spell_indexer, find_spell, search_spells
from discord import Embed, Colour
import re

def markdown(string: str):
    return md(string, bullets='-*', newline_style='BACKLASH', strip=['hr'])

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
    "free": ":free:",
    "reaction": ":leftwards_arrow_with_hook:",
    "long": ":alarm_clock:"
}


class Spell:
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

    def __init__(self, name, type, area, description, tags, traits, source, casting_time, rarity, range, save, duration, target):
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

        for i in tags:
            self.tags.append(i)
        self.traits = []
        for i in traits:
            self.traits.append(i)

    @classmethod
    def from_file(cls, filename: str):
        appendix = 'app/game_data/pf2_new/'
        try:
            with open(appendix+filename, 'r') as file:
                return cls.from_json(json.loads(file.read()))
        except Exception:
            return None

    @classmethod
    def from_json(cls, data: dict):
        name = data['name']
        data = data['system']

        area = None
        if data.get('area'):
            area = f"{data['area']['value']}-foot {data['area']['type']}" or None

        range = None
        if data.get('range'):
            range = data['range']['value'] or None

        duration = None
        if data.get('duration'):
            duration = data['duration']['value'] or ('sustained' if data['duration']['sustained'] else None) or None

        target = None
        if data.get('target'):
            target = data['target']['value'] or None

        defence = None
        if data.get('defense'):
            if data['defense'].get('save'):
                defence = data['defense']['save']['statistic'].capitalize()
                if data['defense']['save']['basic']:
                    defence = 'basic ' + defence.capitalize()

        description = markdown(data['description']['value'])
        traits = data['traits']['value']
        if 'cantrip' in traits:
            type_ = 'cantrip'
        elif 'ritual' in traits:
            type_ = 'ritual'
        elif 'focus' in traits:
            type_ = 'focus'
        else:
            type_ = 'spell'
        type_ += f" {data['level']['value']}"
        traditions = data['traits']['traditions']
        source = data['publication']['title']
        casting_time = data['time']['value']
        rarity = data['traits']['rarity']

        return cls(name=name, type=type_, area=area, description=description, traits=traits, tags=traditions, source=source, casting_time=casting_time, rarity=rarity, range=range, save=defence, duration=duration, target=target)

    def parse_raw_description(self):
        roll_command_id = '1275792662754230313'

        pattern = r'\[\[/r\s+([^\]]+)\]\]\{([^}]+)\}'
        replacement = r'<roll:1275792662754230313 expression:\1> \2'
        result = re.sub(pattern, replacement, self.description)
        return result


    def construct_description(self):
        type_ = '*' + self.type + '*'
        traits = '`' + '`, `'.join(self.traits) + '`'
        basic_info = [f"> **Traditions** {', '.join(self.tags)}"]
        if self.range is not None:
            if self.area is not None:
                basic_info.append(f"> **Range** {self.range}; **Area** {self.area}")
            elif self.target is not None:
                basic_info.append(f"> **Range** {self.range}; **Target** {self.target}")
            else:
                basic_info.append(f"> **Range** {self.range}")

        elif self.area is not None:
            basic_info.append(f"> **Area** {self.area}")

        elif self.target is not None:
            basic_info.append(f"> **Target** {self.target}")

        if not self.casting_time.isdigit():
            basic_info.append(f"> **Cast** {self.casting_time}")

        if self.duration is not None:
            basic_info.append(f"> **Duration** {self.duration}")

        if self.save is not None:
            basic_info.append(f"> **Defense** {self.save}")

        data = [type_, traits.upper(), '\n'.join(basic_info), self.description]
        return '\n'.join(data)

    def to_embed(self):
        title = self.name + ' ' + CAST_TIME.get(self.casting_time, CAST_TIME['long'])
        description = self.construct_description()
        color = CARDS_COLORS.get(self.rarity, CARDS_COLORS['empty'])
        embed_card = Embed(title=title, description=description, color=color)
        embed_card.set_footer(text=self.source, icon_url=FOOTER_URL)
        return embed_card

    @staticmethod
    def get_embed_not_found():
        return Embed(
            title="OwO, what's this?",
            description="(по вашему запросу ничего не найдено)",
            colour=Colour.red()
        )

if __name__ == '__main__':
    initialize_spell_indexer()

    # Демонстрируем поиск заклинаний по фразе
    query = 'the artist'
    print(f"=== Поиск заклинаний по фразе '{query}' ===")
    detect_spells = search_spells(query)
    for result in detect_spells:
        print(f"- {result['name']} (рейтинг: {result['score']}, тип: {result['match_type']})")

    print(f"\nВсего найдено заклинаний с '{query}': {len(detect_spells)}")

    # Загружаем одно конкретное заклинание
    if detect_spells:
        print(f"\n=== Загружаем заклинание: {detect_spells[0]['name']} ===")
        spell_path = detect_spells[0]['path']
        with open(spell_path, 'r') as file:
            spell = Spell.from_json(json.loads(file.read()))
        print(vars(spell))
        embed = spell.to_embed()
        print(embed.title)
        print(embed.description)
        print(embed.footer)

