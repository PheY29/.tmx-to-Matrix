import time
import pytmx
import os
import math
import colorama

colorama.init(autoreset=True)


class TmxMapToMatrix:
    def __init__(self):
        self.green = colorama.Fore.GREEN
        self.reset_color = colorama.Fore.RESET

        self.folder_path = os.getcwd()
        self.tmx_map_name = self.obtain_tmx_map_name(self.folder_path)
        self.tmx_map = pytmx.TiledMap(self.tmx_map_name)

        self.tile_size = self.tmx_map.tilewidth  # 16
        self.map_width = self.tmx_map.width
        self.map_height = self.tmx_map.height

        self.map_matrix = [[1 for _ in range(self.tmx_map.width)] for _ in range(self.tmx_map.height)]

    def run(self):
        running = True
        while running:
            print(f"Make sure you have the {self.green}.TMX map with his .TSX data and .PNG sprite "
                  f"sheet{self.reset_color} in the current folder")
            print(f"All your collision layer on Tilled {self.green}must be named with 'collision'{self.reset_color} "
                  f"in their name")
            print(f"All collision layers found are actually : {self.green}{ttm.obtain_collision_layer()}"
                  f"{self.reset_color}")
            good = input("It is right ? y/n : ")

            if good == "y":
                map_matrix_name = input("Named your matrix file : ")
                self.update_matrix()
                self.save_matrix(map_matrix_name + ".json")
                running = not running
            else:
                print("leaving . . .")
                time.sleep(5)
                quit()

    def obtain_tmx_map_name(self, folder_path):
        tmx_found = False
        for path, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith(".tmx"):
                    return filename
                else:
                    pass

        if not tmx_found:
            print(f"No {self.green}'.tmx'{self.reset_color} file in the folder")
            time.sleep(5)
            quit()

    def obtain_collision_layer(self):
        dic = self.tmx_map.layernames
        collision_layer = []
        for layer_name in dic:
            if "collision" in layer_name:
                collision_layer.append(layer_name)

        if not collision_layer:
            print(f"{self.green}no layer contain 'collision' in their name{self.reset_color}")
            time.sleep(5)
            quit()

        return collision_layer

    def update_matrix(self):
        for layer in self.obtain_collision_layer():
            for obj in self.tmx_map.get_layer_by_name(layer):
                x_start = int(obj.x // self.tile_size)
                y_start = int(obj.y // self.tile_size)
                width = max(math.ceil(float(obj.width / 16)), 1)
                height = max(math.ceil(float(obj.height / 16)), 1)

                for x in range(x_start, (x_start + width)):
                    for y in range(y_start, (y_start + height)):
                        self.map_matrix[y][x] = 0

    def save_matrix(self, file_name):
        with open(file_name, 'w') as file:
            for row in self.map_matrix:
                row_str = ','.join(map(str, row))
                file.write(row_str + '\n')


if __name__ == "__main__":
    ttm = TmxMapToMatrix()
    ttm.run()
