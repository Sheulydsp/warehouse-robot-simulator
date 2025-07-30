from colorama import Fore, Style, init
init(autoreset=True)  # Automatically reset colors after each print


class Warehouse:
    def __init__(self, width, height):
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.robots = []

    def place_item(self, x, y, item):
        self.grid[y][x] = item

    def get_item(self, x, y):
        return self.grid[y][x]

    def remove_item(self, x, y):
        self.grid[y][x] = None

    def add_robot(self, robot):
        self.robots.append(robot)

    def is_occupied(self, x, y):
        for robot in self.robots:
            if robot.x == x and robot.y == y:
                return True
        return False

    def display(self):
        grid_display = [["." for _ in range(self.width)] for _ in range(self.height)]

        # Show items
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is not None:
                    grid_display[y][x] = Fore.YELLOW + "B" + Style.RESET_ALL

        # Show robots (last one takes priority visually if overlap)
        for robot in self.robots:
            # Color robots green, and use first letter of their name
            grid_display[robot.y][robot.x] = Fore.GREEN + robot.name[0].upper() + Style.RESET_ALL

        print("\nWarehouse Grid:")
        for row in grid_display:
            print(" ".join(row))
        print()  # Add spacing

    def find_closest_item(self, x, y):
        closest = None
        min_dist = float('inf')

        for iy in range(self.height):
            for ix in range(self.width):
                if self.grid[iy][ix] is not None:
                    dist = abs(ix - x) + abs(iy - y)  # Manhattan distance
                    if dist < min_dist:
                        min_dist = dist
                        closest = (ix, iy)
        return closest
        

    
