from warehouse import Warehouse
from robot import Robot

def test_robot_collision_avoidance():
    w = Warehouse(5, 5)
    r1 = Robot(w, "Alpha", x=1, y=1)
    r2 = Robot(w, "Beta", x=2, y=1)

    r1.move('right')  # Trying to move into r2's position
    assert (r1.x, r1.y) == (1, 1)  # Move should be blocked

    r2.move('down')  # r2 moves away
    assert (r2.x, r2.y) == (2, 2)

    r1.move('right')  # Now it should succeed
    assert (r1.x, r1.y) == (2, 1)
