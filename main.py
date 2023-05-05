import customtkinter as ctk
from random import randint
import settings
from sys import exit


class Game(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Snake')
        self.geometry(f'{settings.WINDOW_SIZE[0]}x{settings.WINDOW_SIZE[1]}')

        self.columnconfigure(list(range(settings.FIELDS[0])), weight=1, uniform='a')
        self.rowconfigure(list(range(settings.FIELDS[1])), weight=1, uniform='a')

        self.snake = [settings.START_POS,
                      (settings.START_POS[0]-1, settings.START_POS[1]),
                      (settings.START_POS[0]-2, settings.START_POS[1])]

        self.initial_direction = settings.DIRECTIONS['right']
        self.direction = self.initial_direction
        self.new_direction = self.direction

        self.loop = None

        self.bind('<Key>', self.get_input)

        self.draw_frames = []

        self.apple_position = (0, 0)
        self.place_apple()

        self.animate()

        self.mainloop()

    def animate(self):
        self.direction = self.new_direction
        new_head = (self.snake[0][0]+self.direction[0], self.snake[0][1]+self.direction[1])
        self.snake.insert(0, new_head)

        if self.snake[0] == self.apple_position:
            self.place_apple()
        else:
            self.snake.pop()

        self.check_game_over()

        self.draw()

        self.loop = self.after(200, self.animate)

    def check_game_over(self):
        snake_head = self.snake[0]
        is_in_x_limits = snake_head[0] >= settings.RIGHT_LIMIT or snake_head[0] < 0
        is_in_y_limits = snake_head[1] >= settings.BOTTOM_LIMIT or snake_head[1] < 0

        if is_in_x_limits or is_in_y_limits or snake_head in self.snake[1:]:
            self.snake = [settings.START_POS,
                      (settings.START_POS[0]-1, settings.START_POS[1]),
                      (settings.START_POS[0]-2, settings.START_POS[1])]
            self.direction = self.initial_direction
            self.new_direction = self.direction

            self.place_apple()

    def get_input(self, event):
        match event.keycode:
            case 37: self.new_direction = settings.DIRECTIONS['left'] if self.direction != settings.DIRECTIONS['right']\
                else self.direction
            case 38: self.new_direction = settings.DIRECTIONS['up'] if self.direction != settings.DIRECTIONS['down']\
                else self.direction
            case 39: self.new_direction = settings.DIRECTIONS['right'] if self.direction != settings.DIRECTIONS['left']\
                else self.direction
            case 40: self.new_direction = settings.DIRECTIONS['down'] if self.direction != settings.DIRECTIONS['up']\
                else self.direction

        print(self.direction)

    def place_apple(self):
        self.apple_position = (randint(0, settings.FIELDS[0]-1), randint(0, settings.FIELDS[1]-1))
        if self.apple_position in self.draw_frames:
            self.place_apple()

    def draw(self):
        if self.draw_frames:
            for frame, position in self.draw_frames:
                frame.grid_forget()

            self.draw_frames = []

        apple_frame = ctk.CTkFrame(self, fg_color=settings.APPLE_COLOR)
        self.draw_frames.append((apple_frame, self.apple_position))

        for index, position in enumerate(self.snake):
            color = settings.SNAKE_BODY_COLOR if index != 0 else settings.SNAKE_HEAD_COLOR

            snake_frame = ctk.CTkFrame(self, fg_color=color, corner_radius=0)
            self.draw_frames.append((snake_frame, position))

        for frame, position in self.draw_frames:
            frame.grid(column=position[0], row=position[1])


if __name__ == '__main__':
    Game()
