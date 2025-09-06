import requests
from bs4 import BeautifulSoup
from discord import Colour, Embed, File

from app.models.pf2Response import Pf2Response


class SystemSearcher:
    FOOTER_URL = "https://cdn.discordapp.com/attachments/778998112819085352/964148715067670588/unknown.png"

    @staticmethod
    def get_not_found_embed() -> Pf2Response:
        return Pf2Response(
            embed=Embed(
                title="OwO, what's this?",
                description="(по вашему запросу ничего не найдено)",
                colour=Colour.red(),
            )
        )

    @staticmethod
    def get_too_short_embed() -> Pf2Response:
        return Pf2Response(
            embed=Embed(
                title="You baka!",
                description="(поисковой запрос должен быть больше трех символов)",
                colour=Colour.red(),
            )
        )

    @staticmethod
    def get_multiple_choices_embed(choices: dict) -> Pf2Response:
        return Pf2Response(
            embed=Embed(
                title="┗( T﹏T )┛ у меня несколько ответов!",
                description="Выберите нужный из списка:",
                colour=Colour.dark_gold(),
            ),
            choices=choices,
        )

    @staticmethod
    def get_error_embed(service_name: str) -> Pf2Response:
        service_name = service_name.removeprefix("https://")
        service_name = service_name.removeprefix("http://")
        service_name = service_name.removesuffix("/")
        return Pf2Response(
            embed=Embed(
                title="Не могу подключиться ¬_¬",
                description=f"Сервис (с которого я беру инфу) по адресу {service_name} недоступен. Попробуйте позднее",
                colour=Colour.red(),
            )
        )


class SiteSystemSearcher(SystemSearcher):
    base_url: str
    search_url: str

    _session: requests.Session
    _soup: BeautifulSoup

    def __init__(self, *args, **kwargs):
        self._session = requests.Session()

    def get_spell(self, name) -> Pf2Response:
        # optional check for too short
        # request spells_urls with args: _request_search
        # parse it, search for spell there: _parse_spells_page
        # if multiple options, do something or nothing: _parse_spells_page
        # request found spell: _request_spell
        # parse it
        # return
        pass

    def _request_search(self, **params) -> str | None:
        try:
            page = self._session.get(self.search_url, params=params)
        except (requests.Timeout, requests.ConnectTimeout, requests.ConnectionError):
            return None
        if page.status_code != 200:
            return None
        return page.text

    def _prepare_soup(self, page_text):
        self._soup = BeautifulSoup(page_text, "html.parser")

    def _parse_spells_page(self, name, page_text) -> list[str] | None:
        self._prepare_soup(page_text)
        # some stuff with self._soup, returns link to spell (or multiple)
        return

    def _request_spell(self, spell_name) -> str | None:
        try:
            page = self._session.get(self.base_url + spell_name)
        except (requests.Timeout, requests.ConnectTimeout, requests.ConnectionError):
            return None
        if page.status_code != 200:
            return None
        return page.text

    def _parse_spell(self, page_text) -> dict | None:
        self._prepare_soup(page_text)
        # parse spell soup, return stuff to create an embed
        return

    def _assemble_embed(
        self,
        title: str,
        url: str,
        description: str,
        colour: int,
        image: str | None = None,
        footer: str | None = None,
    ) -> Pf2Response:
        embed_card = Embed(title=title, url=url, description=description, colour=colour)
        file = None
        if image:
            file = File(f"temp_images/{image}.png")
            embed_card.set_image(url=f"attachment://{image}.png")
        if footer:
            embed_card.set_footer(text=footer, icon_url=self.FOOTER_URL)
        return Pf2Response(embed=embed_card, file=file)
