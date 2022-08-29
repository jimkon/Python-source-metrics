
class HTMLPage:
    def __init__(self):
        self._html_str = ""

    def add(self, element):
        self._html_str = f"{self._html_str}\n<div>{element}</div>"

    @property
    def html(self):
        return self._html_str
