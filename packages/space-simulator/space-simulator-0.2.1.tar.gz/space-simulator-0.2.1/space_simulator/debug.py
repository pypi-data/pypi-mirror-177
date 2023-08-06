import arcade

from space_simulator.constants import RATIO, SCREEN_SIZE
from space_simulator.sat import Sat


def debug_info(sat: Sat):
    win_x = int(sat.x * RATIO + SCREEN_SIZE / 2)
    win_y = int(sat.y * RATIO + SCREEN_SIZE / 2)
    arcade.draw_text(
        f"x={win_x}, y={win_y}, dist={sat.dist}, angle={sat.angle}",
        10,
        10,
        arcade.color.WHITE,
        10,
    )
    arcade.draw_line(
        win_x,
        win_y,
        win_x + sat.vx * RATIO * 300,
        win_y + sat.vy * RATIO * 300,
        arcade.color.GREEN,
    )
    arcade.draw_line(
        win_x,
        win_y,
        win_x + sat.ax * RATIO * 500_000,
        win_y + sat.ay * RATIO * 500_000,
        arcade.color.RED,
    )
    arcade.draw_circle_filled(SCREEN_SIZE // 2, SCREEN_SIZE // 2, 3, arcade.color.WHITE)
    arcade.draw_circle_outline(
        SCREEN_SIZE // 2,
        SCREEN_SIZE // 2,
        SCREEN_SIZE // 2 - 10_000_000 * RATIO,
        arcade.color.LIGHT_GRAY,
        num_segments=50,
    )
