import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import time

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Clicker Upgrade Game")

        self.coins = 0
        self.coins_per_click = 1
        self.auto_income = 0
        self.click_upgrade_cost = 10
        self.auto_upgrade_cost = 20
        self.env_upgrade_cost = 100
        self.env_index = 0
        self.env_images = ["forest.png", "mountains.png", "river.png", "house.png", "city.png", "sun.png"]

        self.last_time = time.time()

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # фон
        self.bg = ImageTk.PhotoImage(Image.open("assets/bg.png").resize((800, 600)))
        self.bg_image = self.canvas.create_image(0, 0, anchor="nw", image=self.bg)

        self.env_layers = []

        self.coin_text = self.canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), fill="white", text="0 (+0/sec)")
        self.upgrade_btn = tk.Button(self.root, text="Улучшения", command=self.show_upgrades)
        self.upgrade_window = None
        self.root.create_window = self.canvas.create_window(680, 10, anchor="ne", window=self.upgrade_btn)

        self.mine_button = tk.Button(self.root, text="Добыть", font=("Arial", 20), width=10, height=2, command=self.mine)
        self.canvas.create_window(400, 300, window=self.mine_button)

        self.update_ui()
        self.root.after(1000, self.auto_collect)

    def mine(self):
        self.coins += self.coins_per_click
        self.update_ui()

    def auto_collect(self):
        now = time.time()
        delta = now - self.last_time
        self.last_time = now
        self.coins += int(self.auto_income * delta)
        self.update_ui()
        self.root.after(1000, self.auto_collect)

    def update_ui(self):
        self.canvas.itemconfig(self.coin_text, text=f"{self.coins} (+{self.auto_income}/sec)")

    def show_upgrades(self):
        if self.upgrade_window:
            return
        self.upgrade_window = Toplevel(self.root)
        self.upgrade_window.attributes("-fullscreen", True)
        self.upgrade_window.configure(bg="#222")

        tk.Label(self.upgrade_window, text="Улучшения", font=("Arial", 24), fg="white", bg="#222").pack(pady=20)

        tk.Button(self.upgrade_window, text=f"Улучшить клик (+1), стоимость: {self.click_upgrade_cost}",
                  font=("Arial", 16), command=self.upgrade_click).pack(pady=10)

        tk.Button(self.upgrade_window, text=f"Улучшить автодобычу (+2/sec), стоимость: {self.auto_upgrade_cost}",
                  font=("Arial", 16), command=self.upgrade_auto).pack(pady=10)

        tk.Button(self.upgrade_window, text=f"Улучшить окружение, стоимость: {self.env_upgrade_cost}",
                  font=("Arial", 16), command=self.upgrade_environment).pack(pady=10)

        tk.Button(self.upgrade_window, text="Закрыть", font=("Arial", 14),
                  command=self.close_upgrades).pack(pady=40)

    def upgrade_click(self):
        if self.coins >= self.click_upgrade_cost:
            self.coins -= self.click_upgrade_cost
            self.coins_per_click += 1
            self.click_upgrade_cost = int(self.click_upgrade_cost * 1.5)
            self.update_ui()
            self.refresh_upgrades()

    def upgrade_auto(self):
        if self.coins >= self.auto_upgrade_cost:
            self.coins -= self.auto_upgrade_cost
            self.auto_income += 2
            self.auto_upgrade_cost = int(self.auto_upgrade_cost * 1.5)
            self.update_ui()
            self.refresh_upgrades()

    def upgrade_environment(self):
        if self.env_index < len(self.env_images) and self.coins >= self.env_upgrade_cost:
            self.coins -= self.env_upgrade_cost
            img_path = f"assets/{self.env_images[self.env_index]}"
            image = Image.open(img_path).resize((800, 600))
            img_tk = ImageTk.PhotoImage(image)
            self.env_layers.append(img_tk)
            self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
            self.env_index += 1
            self.env_upgrade_cost = int(self.env_upgrade_cost * 1.5)
            self.update_ui()
            self.refresh_upgrades()

    def close_upgrades(self):
        if self.upgrade_window:
            self.upgrade_window.destroy()
            self.upgrade_window = None

    def refresh_upgrades(self):
        self.close_upgrades()
        self.show_upgrades()


if __name__ == "__main__":
    root = tk.Tk()
    game = ClickerGame(root)
    root.mainloop()
