import tkinter as tk
import time
from threading import Thread
import random


class TrafficLightSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Симуляция светофора")
        self.root.geometry("800x600")


        self.is_running = False
        self.traffic_light_on = True
        self.current_light = "red"
        self.light_timer = 0
        self.cycle_phase = "red_to_green"


        self.red_duration = 8
        self.yellow_after_red = 3
        self.green_duration = 8
        self.yellow_after_green = 3

        # Координаты
        self.crosswalk = {"start": 150, "end": 350, "y": 150, "height": 100}
        self.stop_lines = {"left": 110, "right": 390}

        # Списки объектов
        self.pedestrians = []
        self.cars = []

        # Создание интерфейса
        self.create_widgets()

        # Запуск анимации
        self.animate()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='light gray')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="СИМУЛЯТОР ПЕШЕХОДНОГО ПЕРЕХОДА",
                 font=("Arial", 16, "bold"), bg='light gray').pack(pady=10)

        sim_frame = tk.Frame(main_frame, bg='light gray')
        sim_frame.pack(fill=tk.BOTH, expand=True)

        # Панель светофора
        left_panel = tk.Frame(sim_frame, bg='light gray')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        light_frame = tk.Frame(left_panel, bg='black', relief=tk.RAISED, bd=3)
        light_frame.pack(pady=20)

        self.lights = {}
        colors = [("red", 'red'), ("yellow", 'yellow'), ("green", 'green')]
        for name, color in colors:
            canvas = tk.Canvas(light_frame, width=80, height=80, bg='black', highlightthickness=0)
            canvas.pack(pady=10)
            circle = canvas.create_oval(10, 10, 70, 70, fill='gray', outline='white', width=2)
            self.lights[name] = (canvas, circle)

        self.timer_label = tk.Label(left_panel, text="ТАЙМЕР: 0", font=("Arial", 14, "bold"),
                                    bg='light gray', fg='dark blue')
        self.timer_label.pack(pady=10)

        self.status_label = tk.Label(left_panel, text="СВЕТОФОР: ВЫКЛ", font=("Arial", 12),
                                     bg='light gray', fg='red')
        self.status_label.pack(pady=5)

        # Холст
        right_panel = tk.Frame(sim_frame, bg='light gray')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.canvas = tk.Canvas(right_panel, width=500, height=400, bg='light gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_scene()

        # Кнопки
        button_frame = tk.Frame(main_frame, bg='light gray')
        button_frame.pack(pady=20)

        # Создаем кнопки и сохраняем ссылки
        self.start_button = tk.Button(button_frame, text="Начать симуляцию",
                                      command=self.start_simulation, font=("Arial", 10),
                                      bg='green', fg='white', width=15, height=1)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(button_frame, text="Завершить симуляцию",
                                     command=self.stop_simulation, font=("Arial", 10),
                                     bg='red', fg='white', width=15, height=1, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.toggle_button = tk.Button(button_frame, text="Выключить светофор",
                                       command=self.toggle_traffic_light, font=("Arial", 10),
                                       bg='orange', fg='white', width=15, height=1, state=tk.DISABLED)
        self.toggle_button.grid(row=0, column=2, padx=5)

        self.add_ped_button = tk.Button(button_frame, text="Добавить пешехода",
                                        command=self.add_pedestrian, font=("Arial", 10),
                                        bg='blue', fg='white', width=15, height=1, state=tk.DISABLED)
        self.add_ped_button.grid(row=0, column=3, padx=5)

        self.add_car_button = tk.Button(button_frame, text="Добавить машину",
                                        command=self.add_car, font=("Arial", 10),
                                        bg='dark red', fg='white', width=15, height=1, state=tk.DISABLED)
        self.add_car_button.grid(row=0, column=4, padx=5)

    def draw_scene(self):
        # ТЕМНО-СЕРЫЙ ФОН В КЛЕТКУ
        dark_gray1 = '#606060'
        dark_gray2 = '#707070'
        cell = 20
        for y in range(0, 150, cell):
            for x in range(0, 500, cell):
                col = dark_gray1 if ((x // cell) + (y // cell)) % 2 == 0 else dark_gray2
                self.canvas.create_rectangle(x, y, x + cell, y + cell, fill=col, outline='#505050')
        for y in range(250, 400, cell):
            for x in range(0, 500, cell):
                col = dark_gray1 if ((x // cell) + ((y - 250) // cell)) % 2 == 0 else dark_gray2
                self.canvas.create_rectangle(x, y, x + cell, y + cell, fill=col, outline='#505050')


        grass = '#2e8b57'
        cs, ce = self.crosswalk["start"], self.crosswalk["end"]
        self.canvas.create_rectangle(0, 55, cs, 95, fill=grass)
        self.canvas.create_rectangle(ce, 55, 500, 95, fill=grass)
        self.canvas.create_rectangle(0, 305, cs, 345, fill=grass)
        self.canvas.create_rectangle(ce, 305, 500, 345, fill=grass)

        # БОЛЬШИЕ ДЕРЕВЬЯ
        tree_positions = [40, 130, 370, 460]
        for x in tree_positions:
            self.canvas.create_rectangle(x - 4, 30, x + 4, 70, fill='#8B4513', outline='#654321', width=2)
            self.canvas.create_oval(x - 20, 10, x + 20, 50, fill='#2E8B57', outline='#006400', width=1)
            self.canvas.create_oval(x - 15, 5, x + 15, 35, fill='#228B22', outline='#006400', width=1)

        for x in tree_positions:
            self.canvas.create_rectangle(x - 4, 290, x + 4, 330, fill='#8B4513', outline='#654321', width=2)
            self.canvas.create_oval(x - 20, 270, x + 20, 310, fill='#2E8B57', outline='#006400', width=1)
            self.canvas.create_oval(x - 15, 265, x + 15, 295, fill='#228B22', outline='#006400', width=1)

        # Дорога
        self.canvas.create_rectangle(0, 150, 500, 250, fill='gray')
        # Левая часть (до перехода)
        for x in range(10, self.crosswalk["start"] - 10, 30):
            self.canvas.create_line(x, 200, x + 15, 200, fill='white', width=2)
        # Правая часть (после перехода)
        for x in range(self.crosswalk["end"] + 10, 490, 30):
            self.canvas.create_line(x, 200, x + 15, 200, fill='white', width=2)

        # Зебра
        for y in range(self.crosswalk["y"], self.crosswalk["y"] + self.crosswalk["height"], 23):
            self.canvas.create_rectangle(self.crosswalk["start"], y,
                                         self.crosswalk["end"], y + 10, fill='white')

        # СТОП-ЛИНИИ (красные)
        for side, x in self.stop_lines.items():
            self.canvas.create_line(x, self.crosswalk["y"] - 2, x,
                                    self.crosswalk["y"] + self.crosswalk["height"] + 2,
                                    fill='red', width=3)

        # Текст
        self.canvas.create_text(250, 75, text="ТРОТУАР", font=("Arial", 16, "bold"), fill='white')
        self.canvas.create_text(250, 325, text="ТРОТУАР", font=("Arial", 16, "bold"), fill='white')
        self.canvas.create_line(self.crosswalk["start"], 140, self.crosswalk["end"], 140,
                                fill='white', width=3, dash=(5, 5))

    def start_simulation(self):
        if not self.is_running:
            self.is_running = True
            self.traffic_light_on = True
            self.cycle_phase = "red_to_green"

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.toggle_button.config(state=tk.NORMAL)
            self.add_ped_button.config(state=tk.NORMAL)
            self.add_car_button.config(state=tk.NORMAL)

            Thread(target=self.run_simulation, daemon=True).start()
            self.auto_spawn()

    def stop_simulation(self):
        self.is_running = False

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.toggle_button.config(state=tk.DISABLED)
        self.add_ped_button.config(state=tk.DISABLED)
        self.add_car_button.config(state=tk.DISABLED)

        for light in self.lights.values():
            light[0].itemconfig(light[1], fill='gray')
        self.status_label.config(text="СВЕТОФОР: ВЫКЛ", fg='red')

        for ped in self.pedestrians:
            for item in ped['items']:
                self.canvas.delete(item)
        self.pedestrians.clear()

        for car in self.cars:
            for item in car['items']:
                self.canvas.delete(item)
        self.cars.clear()

    def toggle_traffic_light(self):
        self.traffic_light_on = not self.traffic_light_on
        if self.traffic_light_on:
            self.toggle_button.config(text="Выключить светофор")
            self.status_label.config(text="СВЕТОФОР: ВКЛ", fg='green')
        else:
            self.toggle_button.config(text="Включить светофор")
            self.status_label.config(text="СВЕТОФОР: ВЫКЛ", fg='red')
            for light in self.lights.values():
                light[0].itemconfig(light[1], fill='gray')

    def add_pedestrian(self, auto=False):
        if not self.is_running or (auto and random.random() > 0.4):
            return

        x = random.randint(self.crosswalk["start"] + 10, self.crosswalk["end"] - 10)
        color = random.choice(['blue', 'red', 'green', 'purple', 'orange', 'brown'])

        items = [
            self.canvas.create_oval(x - 8, 50, x + 8, 66, fill='#ffcc99', outline='black'),
            self.canvas.create_rectangle(x - 6, 66, x + 6, 90, fill=color, outline='black'),
            self.canvas.create_line(x - 4, 90, x - 8, 100, fill='black', width=2),
            self.canvas.create_line(x + 4, 90, x + 8, 100, fill='black', width=2),
            self.canvas.create_line(x - 6, 70, x - 12, 80, fill='black', width=2),
            self.canvas.create_line(x + 6, 70, x + 12, 80, fill='black', width=2)
        ]

        self.pedestrians.append({
            'items': items,
            'x': x, 'y': 50,
            'state': 'walking_to_crosswalk',
            'target_y': 140 - 50,
            'speed': random.uniform(1.0, 2.0)
        })

    def add_car(self, auto=False):
        if not self.is_running or (auto and random.random() > 0.4):
            return

        side = random.choice(['left', 'right'])
        direction = 'right' if side == 'left' else 'left'

        # РАЗНЫЕ Y-координаты для разных направлений
        if direction == 'right':
            y_top = 160
            y_bottom = 180
            start_x = -50
        else:
            y_top = 210
            y_bottom = 230
            start_x = 550

        color = random.choice(['red', 'blue', 'green', 'yellow', 'black', 'white', 'silver'])
        base_speed = random.uniform(4.0, 8.0)

        if direction == 'right':
            items = [
                self.canvas.create_rectangle(start_x, y_top, start_x + 40, y_bottom, fill=color, outline='black'),
                self.canvas.create_rectangle(start_x + 5, y_top - 5, start_x + 35, y_top, fill=color, outline='black'),
                self.canvas.create_rectangle(start_x + 8, y_top - 3, start_x + 32, y_top - 1, fill='light blue',
                                             outline='black'),
                self.canvas.create_oval(start_x + 5, y_bottom, start_x + 12, y_bottom + 7, fill='black'),
                self.canvas.create_oval(start_x + 28, y_bottom, start_x + 35, y_bottom + 7, fill='black'),
                self.canvas.create_oval(start_x + 38, y_top + 10, start_x + 40, y_top + 12, fill='yellow')
            ]
        else:
            items = [
                self.canvas.create_rectangle(start_x - 40, y_top, start_x, y_bottom, fill=color, outline='black'),
                self.canvas.create_rectangle(start_x - 35, y_top - 5, start_x - 5, y_top, fill=color, outline='black'),
                self.canvas.create_rectangle(start_x - 32, y_top - 3, start_x - 8, y_top - 1, fill='light blue',
                                             outline='black'),
                self.canvas.create_oval(start_x - 35, y_bottom, start_x - 28, y_bottom + 7, fill='black'),
                self.canvas.create_oval(start_x - 12, y_bottom, start_x - 5, y_bottom + 7, fill='black'),
                self.canvas.create_oval(start_x - 40, y_top + 10, start_x - 38, y_top + 12, fill='yellow')
            ]

        self.cars.append({
            'items': items,
            'x': start_x,
            'y': (y_top + y_bottom) / 2,
            'direction': direction,
            'state': 'moving',
            'speed': base_speed * 0.5,
            'target_speed': base_speed,
            'stop_line_x': self.stop_lines[side],
            'has_crossed': False,
            'is_stopped': False,
            'should_stop': False
        })

    def auto_spawn(self):
        if self.is_running:
            self.add_pedestrian(auto=True)
            self.add_car(auto=True)
            self.root.after(2000, self.auto_spawn)

    def run_simulation(self):
        while self.is_running:
            if self.traffic_light_on:
                self.cycle_phase = "red_to_green"
                self.set_light("red")
                for i in range(self.red_duration):
                    if not self.is_running or not self.traffic_light_on:
                        break
                    self.light_timer = self.red_duration - i
                    self.update_display()
                    time.sleep(1)

                self.set_light("yellow")
                for i in range(self.yellow_after_red):
                    if not self.is_running or not self.traffic_light_on:
                        break
                    self.light_timer = self.yellow_after_red - i
                    self.update_display()
                    time.sleep(1)

                self.cycle_phase = "green_to_red"
                self.set_light("green")
                for i in range(self.green_duration):
                    if not self.is_running or not self.traffic_light_on:
                        break
                    self.light_timer = self.green_duration - i
                    self.update_display()
                    time.sleep(1)

                self.set_light("yellow")
                for i in range(self.yellow_after_green):
                    if not self.is_running or not self.traffic_light_on:
                        break
                    self.light_timer = self.yellow_after_green - i
                    self.update_display()
                    time.sleep(1)

    def set_light(self, color):
        self.current_light = color
        for name, (canvas, circle) in self.lights.items():
            fill_color = color if name == color else 'gray'
            canvas.itemconfig(circle, fill=fill_color)

    def update_display(self):
        self.timer_label.config(text=f"ТАЙМЕР: {self.light_timer}")

        status_text = {
            "red": ("КРАСНЫЙ:", 'red'),
            "yellow": ("ЖЕЛТЫЙ:" if self.cycle_phase == "red_to_green"
                       else "ЖЕЛТЫЙ:", 'orange'),
            "green": ("ЗЕЛЕНЫЙ:", 'green')
        }
        text, color = status_text.get(self.current_light, ("", "black"))
        self.status_label.config(text=text, fg=color)

    def animate(self):
        # Пешеходы
        for ped in self.pedestrians[:]:
            if ped['state'] == 'finished':
                for item in ped['items']:
                    self.canvas.delete(item)
                self.pedestrians.remove(ped)
                continue

            if ped['state'] == 'walking_to_crosswalk':
                if ped['y'] < ped['target_y']:
                    ped['y'] += ped['speed']
                    for item in ped['items']:
                        self.canvas.move(item, 0, ped['speed'])
                else:
                    ped['state'] = 'waiting'

            elif ped['state'] == 'waiting':
                if self.traffic_light_on:
                    if self.current_light == 'green':
                        ped['state'] = 'crossing'
                        ped['target_y'] = 350
                    elif self.current_light == 'yellow' and self.cycle_phase == "green_to_red":
                        ped['state'] = 'crossing'
                        ped['target_y'] = 350

            elif ped['state'] == 'crossing':
                if self.current_light == 'green':
                    speed = ped['speed']
                elif self.current_light == 'yellow':
                    speed = ped['speed'] * 2.0 if self.cycle_phase == "green_to_red" else ped['speed'] * 1.3
                elif self.current_light == 'red':
                    speed = ped['speed'] * 3.0
                else:
                    speed = ped['speed']

                if ped['y'] < ped['target_y']:
                    ped['y'] += speed
                    for item in ped['items']:
                        self.canvas.move(item, 0, speed)
                else:
                    ped['state'] = 'finished'

        # Машины 
        for car in self.cars[:]:
            if (car['direction'] == 'right' and car['x'] > 550) or \
               (car['direction'] == 'left' and car['x'] < -100):
                for item in car['items']:
                    self.canvas.delete(item)
                self.cars.remove(car)
                continue

            if car['direction'] == 'right':
                distance_to_line = car['stop_line_x'] - car['x']
                has_crossed = car['x'] >= car['stop_line_x']
            else:
                distance_to_line = car['x'] - car['stop_line_x']
                has_crossed = car['x'] <= car['stop_line_x']

            car['has_crossed'] = has_crossed

            if self.traffic_light_on:
                if self.current_light == 'red':
                    car['should_stop'] = False
                    if car['speed'] < car['target_speed']:
                        car['speed'] = min(car['speed'] + 0.3, car['target_speed'])
                    car['is_stopped'] = False
                elif self.current_light in ['yellow', 'green']:
                    car['should_stop'] = True
                    if has_crossed:
                        car['speed'] = car['target_speed'] * 1.2 if self.current_light == 'yellow' and self.cycle_phase == "red_to_green" else car['speed']
                    else:
                        braking_distance = max(50, car['speed'] * 20)
                        if distance_to_line < braking_distance:
                            brake_factor = 1.0 - (distance_to_line / braking_distance)
                            brake_power = min(1.5, car['speed'] * brake_factor * 1.5)
                            car['speed'] = max(car['speed'] - brake_power, 0)
                            if distance_to_line < 5 or car['speed'] < 0.1:
                                car['speed'] = 0
                                car['is_stopped'] = True
                        else:
                            if car['speed'] < car['target_speed']:
                                car['speed'] = min(car['speed'] + 0.2, car['target_speed'])
            else:
                car['should_stop'] = False
                if car['speed'] < car['target_speed']:
                    car['speed'] = min(car['speed'] + 0.3, car['target_speed'])

            dx = car['speed'] if car['direction'] == 'right' else -car['speed']
            car['x'] += dx
            for item in car['items']:
                self.canvas.move(item, dx, 0)

        self.root.after(50, self.animate)


def main():
    root = tk.Tk()
    TrafficLightSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
