

class CaveObject:
    def __init__(self):
        self.W = False
        self.P = False
        self.S = False
        self.B = False
        self.G = False
        self.Go = False

    def add_value(self, symbol):
        if symbol == '*':
            self.Go = True
        elif symbol == 'G':
            self.G = True
        elif symbol == 'W':
            self.W = True
        elif symbol == 'P':
            self.P = True
        elif symbol == 'S':
            self.S = True
        elif symbol == "B":
            self.B = True
        else:
            return ValueError("Wrong symbol")

    def check_value(self):
        return [self.W, self.P, self.S, self.B, self.G]

    def get_symbol(self):
        if self.Go:
            return '*'
        elif self.W:
            return 'W'
        elif self.P:
            return 'P'
        elif self.G:
            return 'G'
        elif self.S:
            return 'S'
        elif self.B:
            return 'B'
        else:
            return '#'


class Cave:
    def __init__(self, m, n):
        self.height = m
        self.width = n
        self.map = [[CaveObject() for i in range(n)] for j in range(m)]
        self.goal = [0, 0]
        self.start = [0, 0]

    def set_start_position(self, x, y):
        self.start[0] = x
        self.start[1] = y

    def get_start_position(self):
        return self.start

    def get_goal_position(self):
        return self.goal

    def get_dimensions(self):
        return self.height, self.width

    def check_field(self, x, y):
        return self.map[x][y].check_value()

    def add_element(self, x, y, symbol):
        if symbol == '*':
            self.goal[0] = x
            self.goal[1] = y
        try:
            self.map[x][y].add_value(symbol)
        except ValueError:
            raise Exception("Wrong input format")

    def print_cave(self):
        for i in range(self.height-1, -1, -1):
            for j in range(self.width):
                if j == self.width - 1:
                    print(self.map[i][j].get_symbol())
                else:
                    print(self.map[i][j].get_symbol(), end="")
        print()


    def pick_gold(self, coordinates):
        if self.map[coordinates[0]][coordinates[1]].check_value()[-1]:
            self.map[coordinates[0]][coordinates[1]].G = False
def read_cave(file_path):
    wumpus_cave = None
    with open(file_path, 'r') as file:
        for line in file:
            symbol = line.strip()
            if symbol:
                if symbol[0] == 'M':
                    wumpus_cave = Cave(int(symbol[1]), int(symbol[2]))
                elif symbol[0] == 'A' and wumpus_cave:
                    wumpus_cave.set_start_position(int(symbol[1]) - 1, int(symbol[2]) - 1)
                elif symbol[0] == 'B' and wumpus_cave:
                    wumpus_cave.add_element(int(symbol[1]) - 1, int(symbol[2]) - 1, 'B')
                elif symbol[0] == 'G' and symbol[1] == 'O' and wumpus_cave:
                    wumpus_cave.add_element(int(symbol[2]) - 1, int(symbol[3]) - 1, '*')
                elif symbol[0] == 'G' and wumpus_cave:
                    wumpus_cave.add_element(int(symbol[1]) - 1, int(symbol[2]) - 1, 'G')
                elif symbol[0] == 'P' and wumpus_cave:
                    wumpus_cave.add_element(int(symbol[1]) - 1, int(symbol[2]) - 1, 'P')
                elif symbol[0] == 'S' and wumpus_cave:
                    wumpus_cave.add_element(int(symbol[1]) - 1, int(symbol[2]) - 1, 'S')
                elif symbol[0] == 'W' and wumpus_cave:
                    wumpus_cave.add_element(int(symbol[1]) - 1, int(symbol[2]) - 1, 'W')
                else:
                    raise Exception('Invalid input format')
    return wumpus_cave


'''
for file in os.listdir('input'):
    cave = read_cave(f"input/{file}")
    cave.print_cave()
    print()
'''