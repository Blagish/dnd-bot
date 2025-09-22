import re

from app.game_data.pf2_new.classes.base import Pf2Thing

class Feat(Pf2Thing):
    action: str | None = None
    action_type: str
    type: str
    prerequisites: list[str] | None = None
    category: str

    @classmethod
    def from_json(cls, data: dict):
        obj = super().from_json(data)
        data = data["system"]

        obj.action_type = data['actionType']['value']
        if obj.action_type == 'action':
            obj.action = str(data['actions']['value'])
        obj.category = data['category']
        obj.prerequisites = []
        if prers := data['prerequisites'].get('value'):
            for i in prers:
                obj.prerequisites.append(i['value'])

        type_ = 'feat'
        obj.type = f'{obj.traits[0]} {obj.category} {type_} {obj.level}'
        obj.construct_description()
        return obj

    def construct_description(self):
        super().construct_description()
        type_ = f"*{self.type}*"
        traits = f"`{'`, `'.join(self.traits)}`".upper()
        data = [type_, f"> **Traits** {traits}"]

        if self.prerequisites:
            data.append(f"> **Prerequisites** {', '.join(self.prerequisites)}")

        data.append(self.description.strip())

        self.description = '\n'.join(data)

    def to_embed(self):
        response = super().to_embed()
        if self.action_type == 'action':
            response.embed.title += ' ' + self.CAST_TIME.get(self.action, self.CAST_TIME["long"])

        return response