from scheme import Scheme


class Solid(Scheme):
    # abstract base
    def setall(self, color):
        for led in range(self.strip.num_leds):
            self.strip.smart_set_pixel(*color)


class MaxWhite(Solid):
    pause_between_updates = 60

    def init(self):
        self.setall(0xFFF, 0xFFF, 0xFFF)

    def paint():
        return False


class FullScan(Solid):
    pause_between_updates = 0.001
    color = [0, 0, 0]
    color_step = [1, 0, 0]

    def init(self):
        self.setall(self.color)

    def paint():
        color = [val + step for val, step in zip(self.color, self.color_step)]

        if max(self.color) > 0xFFF:
            self.color = [0, 0, 0]
            self.color_step.append(self.color_step.pop(0))

        self.setall(color)
        return True
