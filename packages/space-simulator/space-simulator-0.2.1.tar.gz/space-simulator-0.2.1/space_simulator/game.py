import arcade

from space_simulator.constants import RATIO, SCREEN_SIZE, SIM_SPEED
from space_simulator.debug import debug_info
from space_simulator.sat import R_EARTH, Sat


class Window(arcade.Window):
    def __init__(self, debug=False):
        super().__init__(SCREEN_SIZE, SCREEN_SIZE, "Orbiter")
        arcade.set_background_color(arcade.color.BLACK)
        self.sat = Sat(10, 10_000_000, 0, 0, 6310)
        self.debug = debug

    def on_draw(self):
        self.clear()
        self.draw_earth()
        self.draw_satelite()
        if self.debug:
            self.draw_debug()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F3:
            self.debug = not self.debug
        if key == arcade.key.ESCAPE:
            self.close()

    def update(self, dt):
        self.sat.step(dt * SIM_SPEED)

    def draw_earth(self):
        arcade.draw_circle_filled(
            SCREEN_SIZE // 2, SCREEN_SIZE // 2, R_EARTH * RATIO, arcade.color.BLUE
        )

    def draw_debug(self):
        debug_info(self.sat)

    def draw_satelite(self):
        win_x = int(self.sat.x * RATIO + SCREEN_SIZE / 2)
        win_y = int(self.sat.y * RATIO + SCREEN_SIZE / 2)
        arcade.draw_circle_filled(win_x, win_y, 5, arcade.color.LIGHT_GRAY)


def main():
    window = Window()
    arcade.run()


if __name__ == "__main__":
    main()
