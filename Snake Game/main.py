import random
import tkinter as tk
import customtkinter as ctk
import sys

# Window Creation
window = ctk.CTk()
window.title("Snake Game")
window.geometry("500x540")
window.configure(fg_color="black")
window.resizable(False, False)

# Canvas + Snake + Food
canvas = tk.Canvas(window, height=500, width=500, background="black", highlightthickness=0)
snake = [canvas.create_rectangle(100, 100, 120, 120, fill="green")]
food = [canvas.create_oval(100, 100, 120, 120, fill="red")]

# Variables
dx, dy = 20, 0
score = 0

# Functions
def start_game():
    welcome_label.destroy()
    start_button.destroy()
    canvas.place(relx=0.5, rely=0.537, anchor="center")
    move_snake()
    window.bind("<Key>", change_direction)
    score_label.place(relx=0.5, rely=0.03, anchor="center")

def move_snake():
    global score

    # Wall Collision
    x1, y1, x2, y2 = canvas.coords(snake[0])
    if x1 < 0 or y1 < 0 or x2 > 500 or y2 > 500:
        end_game()
        return

    # Store previous positions
    positions = [canvas.coords(seg) for seg in snake]

    # Move head
    canvas.move(snake[0], dx, dy)

    # Move body
    for i in range(1, len(snake)):
        canvas.coords(snake[i], positions[i - 1])

    # Self Collision
    head_coords = canvas.coords(snake[0])
    for segment in snake[1:]:
        if canvas.coords(segment) == head_coords:
            end_game()
            return

    # Food Collision
    fx1, fy1, fx2, fy2 = canvas.coords(food[0])
    if head_coords[0] == fx1 and head_coords[1] == fy1:
        # Add new segment
        last_x1, last_y1, last_x2, last_y2 = canvas.coords(snake[-1])
        new_segment = canvas.create_rectangle(last_x1, last_y1, last_x2, last_y2, fill="green")
        snake.append(new_segment)

        score += 1
        score_label.configure(text=f"Score: {score}")

        # Move food to new location
        new_x = random.randint(0, 24) * 20
        new_y = random.randint(0, 24) * 20
        canvas.coords(food[0], new_x, new_y, new_x + 20, new_y + 20)

    window.after(150, move_snake)

def end_game():
    score_label.place_forget()
    game_over_label.place(relx=0.5, rely=0.3, anchor="center")
    restart_button.place(relx=0.5, rely=0.6, anchor="center")
    quit_button.place(relx=0.5, rely=0.75, anchor="center")
    total_score_label.configure(text=f"Total Score: {score}")
    total_score_label.place(relx=0.5, rely=0.4, anchor="center")

def change_direction(event):
    global dx, dy
    key = event.char.lower()
    arrow = event.keysym

    if (key == "w" or arrow == "Up") and dy == 0:
        dx, dy = 0, -20
    elif (key == "s" or arrow == "Down") and dy == 0:
        dx, dy = 0, 20
    elif (key == "d" or arrow == "Right") and dx == 0:
        dx, dy = 20, 0
    elif (key == "a" or arrow == "Left") and dx == 0:
        dx, dy = -20, 0

def restart_game():
        global dx, dy, score, snake, food

        # Reset direction and score
        dx, dy = 20, 0
        score = 0
        score_label.configure(text=f"Score: {score}")

        # Destroy game-over elements
        game_over_label.place_forget()
        restart_button.place_forget()
        quit_button.place_forget()
        total_score_label.place_forget()

        # Clear old snake and food
        for segment in snake:
            canvas.delete(segment)
        for f in food:
            canvas.delete(f)

        # Recreate snake and food
        snake = [canvas.create_rectangle(100, 100, 120, 120, fill="green")]
        food = [canvas.create_oval(200, 200, 220, 220, fill="red")]

        # Re-show score and canvas
        canvas.place(relx=0.5, rely=0.537, anchor="center")
        score_label.place(relx=0.5, rely=0.03, anchor="center")

        # Restart snake movement
        move_snake()

def quit_game():
    sys.exit()

# UI Elements
welcome_label = ctk.CTkLabel(window, text="Snake Game", font=("Arial", 60, "bold"), text_color="white")
welcome_label.place(relx=0.5, rely=0.35, anchor="center")

start_button = ctk.CTkButton(window, width=140, height=60, fg_color="white", corner_radius=15,
                              text="Start", font=("Arial", 24, "bold"), text_color="black", command=start_game)
start_button.place(relx=0.5, rely=0.6, anchor="center")

score_label = ctk.CTkLabel(window, text=f"Score: {score}", font=("Arial", 26, "bold"), text_color="white")

game_over_label = ctk.CTkLabel(window, text="💀 Game Over 💀", font=("Arial", 45, "bold"), text_color="white")

restart_button = ctk.CTkButton(window, width=140, height=60, fg_color="white", corner_radius=15,
                                text="Restart", font=("Arial", 24, "bold"), text_color="black", command=restart_game)

quit_button = ctk.CTkButton(window, width=140, height=60, fg_color="white", corner_radius=15,
                                text="Quit", font=("Arial", 24, "bold"), text_color="black", command=quit_game)

total_score_label = ctk.CTkLabel(window, text=f"Total Score: {score}", font=("Arial", 35, "bold"), text_color="white")

window.mainloop()
