from markdownify import MarkdownConverter
from app.util.tables import TableParser
from markdownify import markdownify as md
from bs4 import Tag
from PIL import Image, ImageDraw, ImageFont
from app.models.markdownResponse import MarkdownResponse
import os
from uuid import uuid4

def _md_tag(el: Tag, **kwargs):
    return md(el.text, **kwargs)


class TableMarkdown(MarkdownConverter):
    pictures = None

    def convert(self, html: str | Tag):
        if isinstance(html, Tag):
            html = str(html)
        return super().convert(html)

    def convert_table(self, el, text, parent_tags):
        t = TableParser(
            el, parse_string=_md_tag,
            #parse_kwargs={'ignore_br': False, 'markdown': False},
            parse_kwargs={'bullets': '-*', 'newline_style':'BACKLASH', 'strip':['hr']},
            align_left="l", style='single', border=True
        )
        
        table_text = t.get_str()

        self._create_table_image(table_text)
        
        return ''

    def _create_table_image(self, table_text: str):
        try:
            font_size = 18
            try:
                font = ImageFont.truetype("consola.ttf", font_size)  # Windows Consolas
            except:
                try:
                    font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)  # Linux
                except:
                    font = ImageFont.load_default()

            lines = table_text.split('\n')

            max_line_length = max(len(line) for line in lines) if lines else 0

            bbox = font.getbbox('A')
            char_width = bbox[2] - bbox[0]
            char_height = bbox[3] - bbox[1]

            padding = 5
            line_spacing = int(char_height * 0.4)
            img_width = max_line_length * char_width + padding * 2
            img_height = len(lines) * char_height + (len(lines) - 1) * line_spacing + padding * 2

            img = Image.new('RGB', (img_width, img_height), 'white')
            draw = ImageDraw.Draw(img)

            y_offset = padding
            for line in lines:
                draw.text((padding, y_offset), line, fill='black', font=font)
                y_offset += char_height + line_spacing

            os.makedirs('temp_images', exist_ok=True)

            uuid = uuid4()
            if self.pictures is None:
                self.pictures = []

            self.pictures.append(uuid)
            img_path = f'temp_images/{uuid}.png'
            img.save(img_path)

            print(f"Таблица сохранена как изображение: {img_path}")

        except Exception as e:
            print(f"Ошибка при создании изображения таблицы: {e}")

class Pf2Markdown(TableMarkdown):
    CAST_TIME = {
        "1": ":one:",
        "2": ":two:",
        "3": ":three:",
        "2 or 3": ":two: or :three:",
        "free": ":free:",
        "reaction": ":leftwards_arrow_with_hook:",
        "long": ":alarm_clock:",
    }

    def convert_span(self, el, text, parent_tags):
        #print(el, text)
        if 'action-glyph' in el.attrs['class']:
            text = el.get_text()
            return self.CAST_TIME.get(text, self.CAST_TIME['long'])
        return text

def markdown_pf2(string: str | Tag):
    cls = Pf2Markdown(bullets='-*', newline_style='BACKLASH', strip=['hr'])
    return MarkdownResponse(text=cls.convert(string), pictures=cls.pictures)

def markdown_dnd_su(string: str | Tag):
    cls = TableMarkdown(bullets='>-*', newline_style='BACKLASH', strip=['hr', 'a'])
    return MarkdownResponse(text=cls.convert(string), pictures=cls.pictures)

def markdown_dnd_wikidot(string: str | Tag):
    cls = TableMarkdown(bullets='>-*', newline_style='BACKLASH', strip=['hr', 'a'])
    return MarkdownResponse(text=cls.convert(string), pictures=cls.pictures)
