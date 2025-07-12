from pydantic import BaseModel
from typing import List


class RollResponse(BaseModel):
    opening: str = "Считаю"
    command: str = ""
    comment: str = ""
    lines_sep: str = "->"
    lines: str | List[str] = ""
    result: str = ""

    def to_str(self):
        comment = self.comment
        command = self.command.replace("*", "\*")
        if self.comment:
            comment = f" для *{self.comment}*"
        self.lines_to_line()
        if '[' in self.lines:
            self.opening = 'Кидаю'
        return f"{self.opening} {command}{comment}\n{self.lines}**{self.result}**"

    def lines_to_line(self):
        if isinstance(self.lines, str):
            self.lines = f"{self.lines_sep} {self.lines}\n"
            return
        lines = map(lambda x: f"{self.lines_sep} {x}\n", self.lines)
        self.lines = ''.join(lines)
