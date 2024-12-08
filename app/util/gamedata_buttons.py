import discord
from discord.ui.item import Item
from discord.ui.view import _ViewCallback

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180, choices=None, func=None):
        super().__init__(timeout=timeout)
        self._custom_ids = set()
        try:
            new_buttons = self.populate_with_choices(choices, func)
            self._init_children2(new_buttons)
        except Exception as e:
            print(e)


    def _init_children2(self, buttons):
        children = []
        for func in buttons:
            item: Item = func.__discord_ui_model_type__(**func.__discord_ui_model_kwargs__)
            item.callback = _ViewCallback(func, self, item)
            item._view = self
            setattr(self, func.__name__, item)
            children.append(item)
        self._children = children

    def populate_with_choices(self, choices, func):
        buttons = []
        for choice in choices:
            name = f'{choice["name"]} - {choice["trait"]}'
            id_ = self._gen_custom_id(choice["name"])

            @discord.ui.button(label=name, style=discord.ButtonStyle.blurple, custom_id=id_) # or .primary
            async def one_button(cls, interaction: discord.Interaction, button: discord.ui.Button) :
                thingandtrait = button.label.split('-')
                trait = thingandtrait.pop(-1)
                thing = ' - '.join(thingandtrait)
                response = func(thing, trait=trait)
                cls.clear_items()
                buttons = None
                if response.choices is not None:
                    buttons = Buttons()
                    buttons.populate_with_choices(response.choices, func)
                await interaction.response.edit_message(content=response.message, embed=response.embed, view=buttons)

                if response.other_embeds:
                    for embed in response.other_embeds:
                        await interaction.followup.send(embed=embed, mention_author=False)

            buttons.append(one_button)
        return buttons


    def _gen_custom_id(self, name):
        id_ = ''.join(filter(lambda x: x.isalpha, name))
        new_id = id_
        i = 1
        while new_id in self._custom_ids:
            new_id = id_ + str(i)
        self._custom_ids.update([new_id])
        return new_id