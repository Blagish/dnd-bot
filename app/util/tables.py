from prettytable import (
    PrettyTable,
    MSWORD_FRIENDLY,
    DEFAULT,
    PLAIN_COLUMNS,
    MARKDOWN,
    ORGMODE,
    SINGLE_BORDER,
    DOUBLE_BORDER,
)


class TableParser:
    parse_string_func = str
    parse_kwargs = None
    data = None

    caption = ''
    extra = ''

    def __init__(
        self,
        table,
        parse_string=None,
        parse_kwargs=None,
        style=DEFAULT,
        align_left="c",
        border=False,
        internal=True,
    ):
        if parse_string is not None:
            self.parse_string_func = parse_string
        if parse_kwargs is not None:
            self.parse_kwargs = parse_kwargs

        self.pretty = PrettyTable()
        if table.caption:
            self.caption = f'### {table.caption.text}\n'

        headers = None
        if table.thead:
            headers = self.find_headers(table.thead.tr)
        if table.tbody:
            table = table.tbody
        self.data = table.children
        if not headers:
            headers = self.find_headers()

        self.pretty.field_names = headers
        self.set_style(style)
        self.align_left_column(align_left)
        self.pretty.border = border
        self.pretty.preserve_internal_border = internal

        for child in self.data:
            if child == "\n":
                continue
            a = []
            if not hasattr(child, 'children'):
                continue
            for c in child.children:
                if c != "\n":
                    a.append(self.parse_string(c))
            if len(a) == len(headers):
                self.pretty.add_row(a)

    def find_headers(self, header=None):
        if header is None:
            header = next(self.data)
        while header.text.strip() == '':
            header = next(self.data)
        headers = []
        for h in header.children:
            if h != "\n":
                poss_header = self.parse_string(h)
                while poss_header in headers:
                    poss_header = poss_header + '*'
                if poss_header == '':
                    continue
                headers.append(poss_header)
        if len(headers) < 2:  # it was a title; maybe next row
            next(self.data)
            header = next(self.data)
            headers = []
            for h in header.children:
                if h != "\n":
                    poss_header = self.parse_string(h)
                    while poss_header in headers:
                        poss_header = poss_header + '*'
                    if poss_header == '':
                        continue
                    headers.append(poss_header)
        return headers

    def parse_string(self, element):
        if self.parse_kwargs is None:
            return self.parse_string_func(element)
        return self.parse_string_func(element, **self.parse_kwargs)

    def set_style(self, style):
        styles = {
            "ms": MSWORD_FRIENDLY,
            "plain": PLAIN_COLUMNS,
            "org": ORGMODE,
            "mark": MARKDOWN,
            "single": SINGLE_BORDER,
            "double": DOUBLE_BORDER,
        }
        self.pretty.set_style(styles.get(style, DEFAULT))

    def align_left_column(self, pos):
        if pos not in "lcr":
            pos = "c"
        self.pretty.align[self.pretty.field_names[0]] = pos

    def get_table(self):
        return self.pretty

    def get_str(self):
        return str(self.pretty)

    def get_for_embed(self):
        if self.get_str() == '':
            return ''
        return f"{self.caption}`" + self.get_str().strip() + "`"