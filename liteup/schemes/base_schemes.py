from liteup.schemes.scheme import Scheme


class GeneratorScheme(Scheme):
    ui_select = False

    def init(self):
        self.gen = self.generator()
        self.transitions = []

    def paint(self):
        return next(self.gen)
