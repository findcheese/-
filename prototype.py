import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import time
class MazeMenu:
    
    def __init__(self, root):
        self.root = root
        self.root.title("게임 메뉴")
        self.root.geometry("800x600")

        self.main_background_image = tk.PhotoImage(file="main_background.png")
        self.background_label = tk.Label(root, image=self.main_background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_button = tk.Button(root, text="게임 시작", command=self.start_game, width=20, height=2, font=("Arial", 16, "bold"), bg="#FFC0CB", fg="black")
        self.start_button.pack(pady=(250, 10))

        self.records_button = tk.Button(root, text="기록 보기", command=self.show_records, width=20, height=2, font=("Arial", 16, "bold"), bg="#FFC0CB", fg="black")
        self.records_button.pack(pady=20)

        self.quit_button = tk.Button(root, text="게임 종료", command=self.root.destroy, width=20, height=2, font=("Arial", 16, "bold"), bg="#FFC0CB", fg="black")
        self.quit_button.pack(pady=20)

        self.records = []        

    def start_game(self):
        self.root.withdraw()  # 메뉴 창 숨기기
        game_root = tk.Toplevel(self.root)
        maze_painter = MazePainter(game_root, self)
        game_root.protocol("WM_DELETE_WINDOW", self.show_menu)
        game_root.after(1000, maze_painter.start_timer)          
        game_root.mainloop()
    
    def show_menu(self):
        self.root.deiconify()

    def show_records(self):
        # 기록 창 열기
        records_window = tk.Toplevel(self.root)
        records_window.title("기록")
        records_window.geometry("300x150")

        records_label = tk.Label(records_window, text="기록 목록", font=("Helvetica", 14))
        records_label.pack(pady=10)

        sorted_records = sorted(self.records)

        for i, record in enumerate(sorted_records, start=1):
            record_text = f"{i}등: {record} 초"
            record_label = tk.Label(records_window, text=record_text)
            record_label.pack()
        
class MazePainter:
    
    def __init__(self, root, menu):
        self.root = root
        self.menu = menu
        self.root.title("행성 탈출")
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.canvas = tk.Canvas(root, width=1440, height=800)
        self.canvas.pack()        
        self.background_image = tk.PhotoImage(file="background.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        
        self.mx = 1
        self.my = 1
        
        global item
        item = False
        
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]                
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        for y in range(10):
            for x in range(18):
                if self.maze[y][x] != 1:
                    self.canvas.create_rectangle(x * 80, y * 80, x * 80 + 80, y * 80 + 80, fill="white", width=0)

        self.img = tk.PhotoImage(file="cat.png")
        self.img1 = tk.PhotoImage(file="bomb.png") 

        self.images = []  # 스페이스로 생성된 이미지 좌표를 저장할 리스트
        self.canvas.create_image(self.mx * 80 + 40, self.my * 80 + 40, image=self.img, tag="MYCHR")

        global exit_x, exit_y
        self.exit_x = random.randint(7,18)
        self.exit_y = random.randint(0,9)
        self.maze[self.exit_y][self.exit_x] = 0
        
        global item_x, item_y
        self.item_x = random.randint(4, 6)
        self.item_y = random.randint(0, 5)
        self.maze[self.item_y][self.item_x] = 2
        
        self.exit_img = tk.PhotoImage(file="gate.png")
        self.canvas.create_image(self.exit_x * 80 + 40, self.exit_y * 80 + 40, image=self.exit_img, tag="EXIT")
        self.item_img = tk.PhotoImage(file="item.png")
        self.canvas.create_image(self.item_x * 80 + 40, self.item_y * 80 + 40, image=self.item_img, tag="ITEM")

        self.restart_button = tk.Button(root, text="게임 재시작", command=self.game_restart, bg="#FFC0CB", fg="black", font=("Arial", 12))
        self.restart_button.place(x=10, y=10)

        button_space = 20

        self.quit_button = tk.Button(root, text="게임 종료", command=self.game_quit, bg="#FFC0CB", fg="black", font=("Arial", 12))
        self.quit_button.place(x=10 + self.restart_button.winfo_reqwidth() + button_space, y=10)

        self.start_time = None  # 게임 시작 시간을 저장할 변수를 추가합니다.
        self.timer_label = tk.Label(root, text="Time: 0.00", font=("Helvetica", 12))
        self.timer_label.place(x=700, y=10)  # 상단 왼쪽에 위치하도록 조정      

    def key_down(self, e):
        key = e.keysym
        if key == "space":
            self.show_image()
        elif key in {"Up", "Down", "Left", "Right"}:
            self.move_character(key)

    def key_up(self, e):
        pass

    def move_character(self, direction):
        if direction == "Up" and self.maze[self.my - 1][self.mx] != 1:
            self.my = self.my - 1
        elif direction == "Down" and self.maze[self.my + 1][self.mx] != 1:
            self.my = self.my + 1
        elif direction == "Left" and self.maze[self.my][self.mx - 1] != 1:
            self.mx = self.mx - 1
        elif direction == "Right" and self.maze[self.my][self.mx + 1] != 1:
            self.mx = self.mx + 1

        if self.mx == self.exit_x and self.my == self.exit_y:
            self.game_win()

        if self.mx == self.item_x and self.my == self.item_y:
            self.game_item()

        self.canvas.delete("MYCHR")
        self.canvas.create_image(self.mx * 80 + 40, self.my * 80 + 40, image=self.img, tag="MYCHR")

    def show_image(self):
        image = self.canvas.create_image(self.mx * 80 + 40, self.my * 80 + 40, image=self.img1, tag="PAINTED_IMAGE")
        self.images.append((self.mx, self.my, image))  # 이미지 좌표를 저장
        self.root.after(3000, lambda: (self.canvas.delete(image), self.color_cells()))

    def color_cells(self):
        for mx, my, _ in self.images:

            if item == False:
                relative_coordinates = [(0, 0), (0, -1), (0, 1), (1, 0), (-1, 0)]
                for m, n in relative_coordinates:
                    self.maze[my + m][mx + n] = 1
                
                if self.maze[self.my][self.mx] == 1:
                    self.game_over()
                if self.maze[self.exit_y][self.exit_x] ==  1:
                    self.game_lose()
                if self.maze[self.item_y][self.item_x] == 1:
                    global item_x, item_y
                    self.item_x = random.randint(4, 8)
                    self.item_y = random.randint(0, 5)
                    self.maze[self.item_y][self.item_x] = 2
                    self.item_img = tk.PhotoImage(file="item.png")
                    self.canvas.create_image(self.item_x * 80 + 40, self.item_y * 80 + 40, image=self.item_img, tag="ITEM")
                
                for i, j in relative_coordinates:
                    new_my, new_mx = my + i, mx + j

                    if 0 <= new_my < len(self.maze) and 0 <= new_mx < len(self.maze[0]) and self.maze[new_my][new_mx] == 1:
                        self.maze[new_my][new_mx] = 0
                        self.canvas.create_rectangle(new_mx * 80, new_my * 80, new_mx * 80 + 80, new_my * 80 + 80,
                                                     fill="white", width=0)
                        self.canvas.create_rectangle(new_mx * 80, new_my * 80, new_mx * 80 + 79, new_my * 80 + 79,
                                                     fill="light green", width=0, tag="EXPLODED")

                self.root.after(1000, lambda: (self.canvas.delete("EXPLODED"), self.clear_images()))
            
            elif item == True:
                relative_coordinates = [(0, 0), (0, -1), (0, 1), (1, 0), (-1, 0), (0, -2), (0, 2), (2, 0), (-2, 0)]
                
                for m, n in relative_coordinates:
                    self.maze[my + m][mx + n] = 1

                if self.maze[self.my][self.mx] == 1:
                    self.game_over()
                if self.maze[self.exit_y][self.exit_x] ==  1:
                    self.game_lose()                
                for i, j in relative_coordinates:
                    new_my, new_mx = my + i, mx + j

                    if 0 <= new_my < len(self.maze) and 0 <= new_mx < len(self.maze[0]) and self.maze[new_my][new_mx] == 1:
                        self.maze[new_my][new_mx] = 0
                        self.canvas.create_rectangle(new_mx * 80, new_my * 80, new_mx * 80 + 80, new_my * 80 + 80,
                                                     fill="white", width=0)
                        self.canvas.create_rectangle(new_mx * 80, new_my * 80, new_mx * 80 + 79, new_my * 80 + 79,
                                                     fill="light green", width=0, tag="EXPLODED")

                self.root.after(1000, lambda: (self.canvas.delete("EXPLODED"), self.clear_images()))            
            
    def game_item(self):
        self.canvas.delete("ITEM")
        global item
        item = True
        self.canvas.create_rectangle(self.item_x * 80, self.item_y * 80, self.item_x * 80 + 80,
                                     self.item_y * 80 + 80,fill="white", width=0)
    def clear_images(self):
        self.images.clear()
    
    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.start_time:
            elapsed_time = round(time.time() - self.start_time, 2)
            self.timer_label.config(text=f"Time: {elapsed_time}")
            self.root.after(100, self.update_timer)  

    def game_win(self):
        elapsed_time = round(time.time() - self.start_time, 2) 
        self.menu.records.append(elapsed_time)
        message = f" 소요 시간: {elapsed_time} 초."
        self.show_game_result_win("축하합니다!", message) 
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")         

    def game_over(self):
        self.show_game_result_lose("폭탄피격") 
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")       
    
    def game_lose(self):
        self.show_game_result_lose("출구붕괴")
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")          
    
    def show_game_result_win(self, title, message):
        
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("800x600")

        self.win_background_image = tk.PhotoImage(file="win_background.png")
        self.win_background_label = tk.Label(result_window, image=self.win_background_image)
        self.win_background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        result_label = tk.Label(result_window, text=message, font=("Helvetica", 14))
        result_label.pack(pady=20)

        button_style = ttk.Style()
        button_style.configure("TButton", padding=5, font=("Arial", 12))

        restart_button = ttk.Button(result_window, text="게임 재시작", command=self.game_restart, style="TButton")
        restart_button.pack(side="left", padx=20)

        quit_button = ttk.Button(result_window, text="게임 종료", command=self.game_quit, style="TButton")
        quit_button.pack(side="right", padx=20)                

    def show_game_result_lose(self, title):
        
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("400x300")

        self.lose_background_image = tk.PhotoImage(file="lose_background.png")
        self.lose_background_label = tk.Label(result_window, image=self.lose_background_image)
        self.lose_background_label.place(relx=0, rely=0, relwidth=1, relheight=1)       

        button_style = ttk.Style()
        button_style.configure("TButton", padding=5, font=("Arial", 12))

        restart_button = ttk.Button(result_window, text="게임 재시작", command=self.game_restart, style="TButton")
        restart_button.pack(side="left", padx=20)

        quit_button = ttk.Button(result_window, text="게임 종료", command=self.game_quit, style="TButton")
        quit_button.pack(side="right", padx=20)
    
    def game_restart(self):
        self.root.destroy()  # 현재 게임 화면 종료
        self.menu.show_menu()  # 메뉴 화면 보여주기

    def game_quit(self):
        self.root.destroy()  # 현재 게임 화면 종료
        self.menu.root.destroy()  # 전체 프로그램 종료
    
if __name__ == "__main__":
    root_menu = tk.Tk()
    menu = MazeMenu(root_menu)
    root_menu.mainloop()
