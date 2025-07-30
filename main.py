import time
from warehouse import Warehouse
from robot import Robot

def main():
    w = Warehouse(5, 5)
    r1 = Robot(w, "Alpha", x=1, y=1)
    r2 = Robot(w, "Beta", x=4, y=4)

    w.place_item(2, 2, 'Box')
    w.place_item(3, 1, 'Box')

    print("Starting smarter AI robot simulation. Press Ctrl+C to stop.\n")

    while True:
        for robot in w.robots:
            robot.ai_behavior()
        w.display()
        time.sleep(1)

if __name__ == "__main__":
    main()
