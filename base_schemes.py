from scheme import Scheme


class GeneratorScheme(Scheme):
    def init(self):
        self.gen = self.generator()

    def paint(self):
        return next(self.gen)
