# Digits Revival
# Python remake of the NY Times Digits game
from random import *
from tkinter import *
from time import *


class Number_circle:
    def __init__(self, position, number):
        self.position = position
        self.initial_value = number
        self.current_value = self.initial_value
        self.visible = True
        self.selected = False

    def get_x(self):
        return ((self.position * 60) - 30) % 180

    def get_y(self):
        return (((self.position // 4) + 1) * 50) - 25

    def set_current_value(self, value):
        self.current_value = value

    def get_current_value(self):
        return self.current_value

    def restore_initial_value(self):
        self.current_value = self.initial_value

    def get_visible(self):
        return self.visible

    def set_visible(self):
        self.visible = True

    def set_invisible(self):
        self.visible = False

    def get_selected(self):
        return self.selected

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False


class Action_circle:
    def __init__(self, position, action):
        self.position = position
        self.selected = False
        self.action = action

    def get_x(self):
        return (((self.position * 36) - 18) % 180)

    def get_y(self):
        return 20

    def get_selected(self):
        return self.selected

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def get_action(self):
        return self.action


class Digits:

    def __init__(self, scale):
        self.scale = scale

        self.target = randint(100, 500)
        self.numbers = []

        self.calc_stack = []
        self.undo_stack = []

        self.generate_numbers()
        self.number_circles = []
        self.generate_number_circles()
        self.action_circles = []
        self.generate_actions_circles()

        self.root = Tk()
        self.root.title("Digits Revival")

        self.target_display = Label(self.root, text=str(self.target), font=("Arial", 40 * self.scale), justify="center")
        self.target_display.grid(row=0, column=0)

        self.numbers_display = Canvas(self.root, width=180 * self.scale, height=100 * self.scale)
        self.numbers_display.grid(row=1, column=0)

        self.actions_display = Canvas(self.root, width=180 * self.scale, height=40 * self.scale)
        self.actions_display.grid(row=2, column=0)

        self.draw_number_circles()
        self.draw_action_circles()

        self.numbers_display.bind("<Button-1>", self.number_click)
        self.actions_display.bind("<Button-1>", self.action_click)

        self.root.mainloop()

    def reset(self):
        self.unselect_all_numbers()
        self.unselect_all_actions()
        self.calc_stack = []
        self.undo_stack = []
        self.numbers = []
        self.generate_numbers()
        self.number_circles = []
        self.generate_number_circles()
        self.target = randint(100, 500)
        self.target_display.config(text=str(self.target))
        self.draw_number_circles()
        self.draw_action_circles()
        self.target_display.update()
        self.numbers_display.update()
        self.actions_display.update()

    def generate_numbers(self):
        low_pool = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        high_pool = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        for i in range(6):
            unique = False
            while not unique:
                if i < 1:
                    new_number = randint(2, 5)
                elif i < 2:
                    new_number = choice(low_pool)
                elif i < 4:
                    new_number = choice(high_pool)
                else:
                    new_number = choice(low_pool + high_pool)

                if new_number not in self.numbers:
                    unique = True
                    self.numbers.append(new_number)
        self.numbers.sort()

    def generate_number_circles(self):
        for i in range(1, 7):
            number_circle = Number_circle(i, self.numbers[i - 1])
            self.number_circles.append(number_circle)

    def draw_number_circles(self):
        self.numbers_display.delete("all")
        for number_circle in self.number_circles:
            if number_circle.get_selected():
                fill_colour = "green"
            else:
                fill_colour = "white"
            if number_circle.get_visible():
                self.numbers_display.create_oval((number_circle.get_x() - 20) * self.scale,
                                                 (number_circle.get_y() - 20) * self.scale,
                                                 (number_circle.get_x() + 20) * self.scale,
                                                 (number_circle.get_y() + 20) * self.scale,
                                                 width=3 * self.scale, outline="red", fill=fill_colour)
                self.numbers_display.create_text(number_circle.get_x() * self.scale, number_circle.get_y() * self.scale,
                                                 text=str(number_circle.get_current_value()),
                                                 font=("Arial", 14 * self.scale), justify="center", fill="black")
        self.numbers_display.update()

    def generate_actions_circles(self):
        self.action_circles.append(Action_circle(1, "<="))
        self.action_circles.append(Action_circle(2, "+"))
        self.action_circles.append(Action_circle(3, "-"))
        self.action_circles.append(Action_circle(4, "x"))
        self.action_circles.append(Action_circle(5, "/"))

    def draw_action_circles(self):
        self.actions_display.delete("all")
        for action_circle in self.action_circles:
            if action_circle.get_selected():
                fill_colour = "green"
            else:
                fill_colour = "white"
            self.actions_display.create_oval((action_circle.get_x() - 10) * self.scale,
                                             (action_circle.get_y() - 10) * self.scale,
                                             (action_circle.get_x() + 10) * self.scale,
                                             (action_circle.get_y() + 10) * self.scale,
                                             width=3 * self.scale, outline="orange", fill=fill_colour)
            self.actions_display.create_text(action_circle.get_x() * self.scale, action_circle.get_y() * self.scale,
                                             text=str(action_circle.get_action()),
                                             font=("Arial", 10 * self.scale), justify="center", fill="black")
        self.actions_display.update()

    def number_click(self, event):
        x = event.x // self.scale
        y = event.y // self.scale

        position = self.get_number_position(x, y)

        if position != None and not self.number_circles[position].get_selected():
            if not self.number_circles[position].get_selected():
                self.number_circles[position].select()
            else:
                self.number_circles[position].unselect()

            self.calc_stack.append(position)

            if len(self.calc_stack) == 2:
                self.number_circles[self.calc_stack[0]].unselect()
                del self.calc_stack[0]

            if len(self.calc_stack) == 3:
                self.number_circles[self.calc_stack[0]].set_invisible()
                self.undo_stack.append([self.calc_stack[0], self.number_circles[self.calc_stack[0]].get_current_value(),
                                        self.calc_stack[2],
                                        self.number_circles[self.calc_stack[2]].get_current_value()])
                if self.calc_stack[1] == "+":
                    total = self.number_circles[self.calc_stack[0]].get_current_value() + self.number_circles[
                        self.calc_stack[2]].get_current_value()
                    self.number_circles[self.calc_stack[2]].set_current_value(total)
                elif self.calc_stack[1] == "-":
                    total = self.number_circles[self.calc_stack[0]].get_current_value() - self.number_circles[
                        self.calc_stack[2]].get_current_value()
                    if total > 0:
                        self.number_circles[self.calc_stack[2]].set_current_value(total)
                    else:
                        self.number_circles[self.calc_stack[0]].set_visible()
                elif self.calc_stack[1] == "x":
                    total = self.number_circles[self.calc_stack[0]].get_current_value() * self.number_circles[
                        self.calc_stack[2]].get_current_value()
                    self.number_circles[self.calc_stack[2]].set_current_value(total)
                elif self.calc_stack[1] == "/":
                    if self.number_circles[self.calc_stack[0]].get_current_value() % self.number_circles[
                        self.calc_stack[2]].get_current_value() == 0:
                        total = self.number_circles[self.calc_stack[0]].get_current_value() / self.number_circles[
                            self.calc_stack[2]].get_current_value()
                        self.number_circles[self.calc_stack[2]].set_current_value(int(total))
                    else:
                        self.number_circles[self.calc_stack[0]].set_visible()

                if total == self.target:
                    self.success_animation(total)
                    sleep(1.5)
                    self.reset()

                self.calc_stack = []
                self.unselect_all_numbers()
                self.unselect_all_actions()

            self.draw_number_circles()
            self.draw_action_circles()

    def success_animation(self, total):
        for i in range(100):
            self.numbers_display.create_text(randint(5 * self.scale, 175 * self.scale),
                                             randint(5 * self.scale, 95 * self.scale),
                                             justify="center",
                                             fill=choice(["red", "yellow", "blue", "green", "pink", "orange"]),
                                             text=str(total),
                                             font=("arial", randint(30 * self.scale, 80 * self.scale)))
            self.numbers_display.update()
        self.numbers_display.create_text(90 * self.scale, 50 * self.scale,
                                         justify="center", fill="white", text=str(total),
                                         font=("arial", 105 * self.scale))
        self.numbers_display.create_text(90 * self.scale, 50 * self.scale,
                                         justify="center", fill="black", text=str(total),
                                         font=("arial", 100 * self.scale))
        self.numbers_display.update()

    def get_number_position(self, x, y):
        for i in range(6):
            if x >= self.number_circles[i].get_x() - 20 and x <= self.number_circles[i].get_x() + 20 and y >= \
                    self.number_circles[i].get_y() - 20 and y <= self.number_circles[i].get_y() + 20:
                return i
        return None

    def action_click(self, event):
        x = event.x // self.scale
        y = event.y // self.scale

        position = self.get_action_position(x, y)

        if position != None:
            action = self.action_circles[position].get_action()

            if action == "<=" and len(self.undo_stack) > 0:
                undo_operation = self.undo_stack[-1]
                del self.undo_stack[-1]

                self.number_circles[undo_operation[0]].set_current_value(undo_operation[1])
                self.number_circles[undo_operation[2]].set_current_value(undo_operation[3])

                self.number_circles[undo_operation[0]].set_visible()

                self.draw_number_circles()

            elif len(self.calc_stack) == 1:
                self.action_circles[position].select()
                self.calc_stack.append(action)

            elif len(self.calc_stack) == 2:
                self.unselect_all_actions()
                self.action_circles[position].select()
                self.calc_stack[1] = action

            self.draw_action_circles()

    def get_action_position(self, x, y):
        for i in range(5):
            if x >= self.action_circles[i].get_x() - 10 and x <= self.action_circles[i].get_x() + 10 and y >= \
                    self.action_circles[i].get_y() - 10 and y <= self.action_circles[i].get_y() + 10:
                return i
        return None

    def unselect_all_numbers(self):
        for number_circle in self.number_circles:
            number_circle.unselect()

    def unselect_all_actions(self):
        for action_circle in self.action_circles:
            action_circle.unselect()

    def show_all_numbers(self):
        for number_circle in self.number_circles:
            number_circle.set_visible()

    def hide_all_numbers(self):
        for number_circle in self.number_circles:
            number_circle.set_invisible()


if __name__ == "__main__":
    a = Digits(scale=3)
