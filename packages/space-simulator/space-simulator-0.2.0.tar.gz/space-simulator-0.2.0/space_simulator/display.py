from datetime import datetime, timedelta
import arcade
from space_simulator.sat import R_EARTH, Sat

SCREEN_SIZE = 800
RATIO = SCREEN_SIZE / 40_000_000
SIM_SPEED = 300


class Window(arcade.Window):
    def __init__(self, debug=False):
        super().__init__(SCREEN_SIZE, SCREEN_SIZE, "Orbiter")
        arcade.set_background_color(arcade.color.BLACK)
        self.sat = Sat(10, 10_000_000, 0, 0, 6310)
        self.stats = ""
        self.last_debug = datetime.now()
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
        if datetime.now() - self.last_debug > timedelta(0, 0.5):
            self.stats = str(self.sat)
            self.last_debug = datetime.now()
        win_x = int(self.sat.x * RATIO + SCREEN_SIZE / 2)
        win_y = int(self.sat.y * RATIO + SCREEN_SIZE / 2)
        arcade.draw_text(
            f"x={win_x}, y={win_y}, dist={self.sat.dist}, angle={self.sat.angle}",
            10,
            10,
            arcade.color.WHITE,
            10,
        )
        arcade.draw_text(
            self.stats,
            10,
            40,
            arcade.color.WHITE,
            10,
        )
        arcade.draw_line(
            win_x,
            win_y,
            win_x + self.sat.vx * RATIO * 300,
            win_y + self.sat.vy * RATIO * 300,
            arcade.color.GREEN,
        )
        arcade.draw_line(
            win_x,
            win_y,
            win_x + self.sat.ax * RATIO * 500_000,
            win_y + self.sat.ay * RATIO * 500_000,
            arcade.color.RED,
        )
        arcade.draw_circle_filled(
            SCREEN_SIZE // 2, SCREEN_SIZE // 2, 3, arcade.color.WHITE
        )
        arcade.draw_circle_outline(
            SCREEN_SIZE // 2,
            SCREEN_SIZE // 2,
            SCREEN_SIZE // 2 - 10_000_000 * RATIO,
            arcade.color.LIGHT_GRAY,
            num_segments=50,
        )

    def draw_satelite(self):
        win_x = int(self.sat.x * RATIO + SCREEN_SIZE / 2)
        win_y = int(self.sat.y * RATIO + SCREEN_SIZE / 2)
        arcade.draw_circle_filled(win_x, win_y, 5, arcade.color.LIGHT_GRAY)


def main():
    window = Window()
    arcade.run()


if __name__ == "__main__":
    main()
