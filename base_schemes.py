from scheme import Scheme


class GeneratorScheme(Scheme):
    def init(self):
        self.gen = self.generator()
        self.transitions = []

    def paint(self):
        return next(self.gen)
