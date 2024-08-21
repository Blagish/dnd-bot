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
    parse_string = str
    data = None

    def __init__(
        self,
        table,
        parse_string=None,
        style=DEFAULT,
        align_left="c",
        border=False,
        internal=True,
    ):
        if parse_string is not None:
            self.parse_string = parse_string

        self.pretty = PrettyTable()
        if table.tbody:
            table = table.tbody
        self.data = table.children
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
            for c in child.children:
                if c != "\n":
                    a.append(self.parse_string(c, ignore_br=False))
            if len(a) == len(headers):
                self.pretty.add_row(a)

    def find_headers(self):
        next(self.data)
        header = next(self.data)
        headers = []
        for h in header.children:
            if h != "\n":
                headers.append(self.parse_string(h, ignore_br=False))
        if len(headers) < 2:  # it was a title; maybe next row
            next(self.data)
            header = next(self.data)
            headers = []
            for h in header.children:
                if h != "\n":
                    headers.append(self.parse_string(h, ignore_br=False))
        return headers

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
        return "`" + self.get_str() + "`"
