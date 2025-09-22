import re

from app.game_data.pf2_new.classes.base import Pf2Thing

class Spell(Pf2Thing):
    type: str
    area: str | None = None
    tags: list[str]
    casting_time: str
    range: str | None = None
    save: str | None = None
    duration: str | None = None
    target: str | None = None

    @classmethod
    def from_json(cls, data: dict):
        obj = super().from_json(data)

        data = data["system"]

        obj.area = (
            f"{data['area']['value']}-foot {data['area']['type']}" or None
            if data.get("area")
            else None
        )
        obj.range = (
            data["range"]["value"] or None if data.get("range") else None
        )

        if data.get("duration"):
            obj.duration = (
                data["duration"]["value"]
                or ("sustained" if data["duration"]["sustained"] else None)
                or None
            )

        obj.target = (
            data["target"]["value"] or None if data.get("target") else None
        )

        if data.get("defense"):
            if data["defense"].get("save"):
                obj.save = data["defense"]["save"]["statistic"].capitalize()
                if data["defense"]["save"]["basic"]:
                    obj.save = "basic " + obj.save

        if "cantrip" in obj.traits:
            type_ = "cantrip"
        elif "ritual" in obj.traits:
            type_ = "ritual"
        elif "focus" in obj.traits:
            type_ = "focus"
        else:
            type_ = "spell"
        type_ += f" {obj.level}"
        obj.type = type_

        obj.tags = data["traits"]["traditions"]
        obj.casting_time = data["time"]["value"]

        obj.construct_description()
        return obj

    def cut_heightened(self, heightened: str | None = None) -> list:
        if heightened is None:
            return []
        all_hs = heightened.split('\n\n')
        sections = []
        H_PATTERN = r"(\*\*Heightened\s\(\+?\d+\w?\w?\)\*\*)"
        for row in all_hs:
            print(row)
            key = re.search(H_PATTERN, row).group(0)
            sections.append({'name': key, 'content': re.sub(H_PATTERN, '> ', row).strip()})
        return sections

    def construct_description(self):
        super().construct_description()

        heightened = None
        if '\n**Heightened' in self.description:
            self.description, heightened = self.description[:self.description.find('**Heightened (')], self.description[self.description.find('**Heightened ('):]

        type_ = f"*{self.type}*"
        traits = f"`{'`, `'.join(self.traits)}`".upper()
        data = [ type_,
            f"> **Traits** {traits}"
        ]
        if len(self.tags):
            data.append(f"> **Traditions** {', '.join(self.tags)}")

        if not self.casting_time.isdigit():
            data.append(f"> **Cast** {self.casting_time}")

        if self.range is not None:
            if self.area is not None:
                data.append(f"> **Range** {self.range}; **Area** {self.area}")
            elif self.target is not None:
                data.append(
                    f"> **Range** {self.range}; **Targets** {self.target}"
                )
            else:
                data.append(f"> **Range** {self.range}")

        elif self.area is not None:
            data.append(f"> **Area** {self.area}")

        elif self.target is not None:
            data.append(f"> **Targets** {self.target}")

        if self.save is not None:
            if self.duration is not None:
                data.append(
                    f"> **Defense** {self.save}; **Duration** {self.duration}"
                )
            else:
                data.append(f"> **Defense** {self.save}")

        elif self.duration is not None:
            data.append(f"> **Duration** {self.duration}")

        data.append(self.description.strip())

        self.description = "\n".join(data)
        self.additional_descriptions += self.cut_heightened(heightened)

    def to_embed(self):
        response = super().to_embed()
        response.embed.title += ' ' + self.CAST_TIME.get(self.casting_time, self.CAST_TIME["long"])

        return response
