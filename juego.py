#!/usr/bin/env python3
import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_MAGENTA, -1)

    h, w = stdscr.getmaxyx()
    ground = h - 3
    player_y = ground - 2
    player_x = 6
    vy = 0
    gravity = 0.4
    jump_power = -1.8

    spikes = []
    speed = 1.0
    score = 0
    best = 0
    game_over = False
    started = False
    frame = 0
    spike_timer = 0
    spike_interval = 18

    def reset():
        nonlocal player_y, vy, spikes, score, speed, frame, spike_timer, game_over, started
        player_y = ground - 2
        vy = 0
        spikes = []
        score = 0
        speed = 1.0
        frame = 0
        spike_timer = 0
        game_over = False
        started = False

    def draw_ground():
        for x in range(w):
            color = curses.color_pair(2) if (x + frame // 2) % 6 < 3 else curses.A_NORMAL
            stdscr.addch(ground, x, '=' if (x + frame // 2) % 6 < 3 else '-', color)

    def draw_player(y):
        for dy in range(2):
            for dx in range(3):
                if (dx + dy) % 2 == 0:
                    stdscr.addch(y + dy, player_x + dx, '█', curses.color_pair(1) if not game_over else curses.color_pair(2))
                else:
                    stdscr.addch(y + dy, player_x + dx, ' ', curses.color_pair(1) if not game_over else curses.color_pair(2))

    while True:
        if game_over:
            msg = f"💀 GAME OVER - Score: {score}"
            stdscr.addstr(h // 2 - 1, max(0, w // 2 - len(msg) // 2), msg, curses.color_pair(2) | curses.A_BOLD)
            restart_msg = "Presiona ESPACIO para reintentar"
            stdscr.addstr(h // 2, max(0, w // 2 - len(restart_msg) // 2), restart_msg, curses.color_pair(3))

        if not started and not game_over:
            start_msg = "Presiona ESPACIO para empezar"
            stdscr.addstr(h // 2, max(0, w // 2 - len(start_msg) // 2), start_msg, curses.color_pair(1) | curses.A_BOLD)

        key = stdscr.getch()
        if key == ord(' '):
            if game_over:
                best = max(best, score)
                reset()
            elif not started:
                started = True
            else:
                if player_y >= ground - 2:
                    vy = jump_power

        if key == ord('q'):
            break

        if started and not game_over:
            frame += 1
            vy += gravity
            player_y += vy
            if player_y > ground - 2:
                player_y = ground - 2
                vy = 0

            speed = 1.0 + score * 0.03

            spike_timer += 1
            if spike_timer >= spike_interval:
                spike_timer = -random.randint(0, int(max(8, spike_interval - score * 0.2)))
                spikes.append({'x': w - 1, 'passed': False})

            for s in spikes[:]:
                s['x'] -= speed
                if not s['passed'] and s['x'] + 2 < player_x:
                    s['passed'] = True
                    score += 1
                if s['x'] + 3 < 0:
                    spikes.remove(s)

            for s in spikes:
                if (player_x < s['x'] + 2 and player_x + 3 > s['x'] and
                    player_y < ground - 1 and player_y + 2 > ground - 2):
                    game_over = True
                    best = max(best, score)

            if player_y < 0:
                player_y = 0
                vy = 0

        stdscr.clear()
        draw_ground()
        draw_player(int(player_y))

        for s in spikes:
            stdscr.addch(ground - 1, int(s['x']), '▲', curses.color_pair(2))
            stdscr.addch(ground - 2, int(s['x']), '▲', curses.color_pair(4))

        stdscr.addstr(0, 0, f" Score: {score}", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(0, 15, f"Best: {best}", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(0, w - 12, " [Q] Salir", curses.A_DIM)

        stdscr.refresh()
        time.sleep(0.03)

if __name__ == "__main__":
    curses.wrapper(main)
