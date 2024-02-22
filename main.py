from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font, PhotoImage, TclError

canvas_width = 1200
canvas_height = 600

root = Tk()
root.title("CG MINI PROJECT")

background_image = PhotoImage(file="final.gif")
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.create_image(0, 0, anchor="nw", image=background_image)
canvas.pack()

color_cycle = cycle(["light grey", "grey", "ivory4", "azure3", "white smoke"])
ball_radius = 25
ball_score = 1
ball_speed = 100
ball_interval = 2000
initial_difficulty = 0.95
catcher_color = "white"
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20
catcher = canvas.create_arc(catcher_start_x, catcher_start_y, catcher_start_x + catcher_width,
                            catcher_start_y + catcher_height, start=200, extent=140, style="arc", outline=catcher_color,
                            width=3)

game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)
score = 0
score_text = canvas.create_text(10, 10, anchor="nw", font=game_font, fill="white", text="Score: " + str(score))
lives_remaining = 3
lives_text = canvas.create_text(canvas_width - 10, 10, anchor="ne", font=game_font, fill="white",
                                text="Lives: " + str(lives_remaining))
balls = []
difficulty = initial_difficulty


def create_ball():
    if lives_remaining != 0:
        x = randrange(10, canvas_width - 2 * ball_radius)
        y = 40
        random_number = randrange(100)
        if random_number < 15:
            ball_color = "red"
            ball_score_multiplier = -3
        elif random_number < 25:
            ball_color = "gold"
            ball_score_multiplier = 5
        else:
            ball_color = next(color_cycle)
            ball_score_multiplier = 1
        new_ball = canvas.create_oval(x, y, x + 2 * ball_radius, y + 2 * ball_radius, fill=ball_color, width=0)
        balls.append((new_ball, ball_score_multiplier))
    root.after(ball_interval, create_ball)


def move_balls():
    for ball_info in balls.copy():
        ball, multiplier = ball_info
        try:
            (ball_x, ball_y, ball_x2, ball_y2) = canvas.coords(ball)
            canvas.move(ball, 0, 1)
            if ball_y2 > canvas_height:
                ball_dropped(ball_info)
        except TclError:
            balls.remove(ball_info)
    root.after(10, move_balls)



def ball_dropped(ball_info):
    ball, _ = ball_info
    balls.remove(ball_info)
    ball_color = canvas.itemcget(ball, "fill")
    if ball_color != "red":
        lose_a_life()
    canvas.delete(ball)
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: " + str(score))
        root.destroy()


def lose_a_life():
    global lives_remaining, difficulty
    lives_remaining -= 1
    canvas.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))
    reset_difficulty()


def reset_difficulty():
    global difficulty
    difficulty = initial_difficulty


def check_catch():
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = canvas.coords(catcher)
    for ball, multiplier in balls:
        (ball_x, ball_y, ball_x2, ball_y2) = canvas.coords(ball)
        if catcher_x < ball_x and ball_x2 < catcher_x2 and catcher_y2 - ball_y2 < 40:
            balls.remove((ball, multiplier))
            canvas.delete(ball)
            increase_score(ball_score * multiplier)
    root.after(10, check_catch)


def increase_score(points):
    global score
    score += points
    canvas.itemconfigure(score_text, text="Score: " + str(score))


def move_left(event):
    (x1, y1, x2, y2) = canvas.coords(catcher)
    if x1 > 0:
        canvas.move(catcher, -20, 0)


def move_right(event):
    (x1, y1, x2, y2) = canvas.coords(catcher)
    if x2 < canvas_width:
        canvas.move(catcher, 20, 0)


root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.focus_set()

root.after(1000, create_ball)
root.after(1000, move_balls)
root.after(1000, check_catch)

root.mainloop()
