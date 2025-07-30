import random

class Robot:
    def __init__(self, warehouse, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.visual_x = x  # float for smooth animation
        self.visual_y = y
        self.carrying = None
        self.warehouse = warehouse
        self.warehouse.add_robot(self)

    def move(self, direction):
        new_x, new_y = self.x, self.y

        if direction == 'up' and self.y > 0:
            new_y -= 1
        elif direction == 'down' and self.y < self.warehouse.height - 1:
            new_y += 1
        elif direction == 'left' and self.x > 0:
            new_x -= 1
        elif direction == 'right' and self.x < self.warehouse.width - 1:
            new_x += 1

        if not self.warehouse.is_occupied(new_x, new_y):
            print(f"{self.name} moved {direction} to ({new_x}, {new_y})")
            self.x = new_x
            self.y = new_y
        else:
            print(f"⚠️ {self.name} can't move to ({new_x}, {new_y}) - position occupied")


    def pick_item(self):
        item = self.warehouse.get_item(self.x, self.y)
        if item and not self.carrying:
            self.carrying = item
            self.warehouse.remove_item(self.x, self.y)

    def drop_item(self):
        if not self.warehouse.get_item(self.x, self.y) and self.carrying:
            self.warehouse.place_item(self.x, self.y, self.carrying)
            self.carrying = None


    def move_random(self):
        directions = ['up', 'down', 'left', 'right']
        random.shuffle(directions)  # Shuffle to try directions in random order

        for direction in directions:
            new_x, new_y = self.x, self.y

            if direction == 'up' and self.y > 0:
                new_y -= 1
            elif direction == 'down' and self.y < self.warehouse.height - 1:
                new_y += 1
            elif direction == 'left' and self.x > 0:
                new_x -= 1
            elif direction == 'right' and self.x < self.warehouse.width - 1:
                new_x += 1
            else:
                continue  # Invalid move (off grid)

            if not self.warehouse.is_occupied(new_x, new_y):
                print(f"{self.name} moves {direction} to ({new_x}, {new_y})")
                self.x = new_x
                self.y = new_y
                return  # Move done
        print(f"{self.name} couldn't move this turn (blocked)")

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y

        # Prioritize horizontal or vertical move based on which distance is greater
        if abs(dx) > abs(dy):
            step = 'right' if dx > 0 else 'left'
        else:
            step = 'down' if dy > 0 else 'up'

        # Try to move; if blocked, try the other axis
        original_pos = (self.x, self.y)
        self.move(step)
        if (self.x, self.y) == original_pos:
            # Move along the other axis if blocked
            step_alt = 'down' if step in ['left', 'right'] and dy != 0 else 'right' if dx != 0 else None
            if step_alt:
                self.move(step_alt)

    def ai_behavior(self):
        drop_zone = (0, 0)

        if self.carrying:
            if (self.x, self.y) == drop_zone:
                self.drop_item()
                return f"{self.name} dropped the item at {drop_zone}."
            else:
                self.move_toward(*drop_zone)
                return f"{self.name} moving toward drop zone {drop_zone}."
        else:
            closest = self.warehouse.find_closest_item(self.x, self.y)
            if closest is None:
                return f"{self.name} found no items."
            if (self.x, self.y) == closest:
                self.pick_item()
                return f"{self.name} picked up an item at {closest}."
            else:
                self.move_toward(*closest)
                return f"{self.name} moving toward item at {closest}."

            
