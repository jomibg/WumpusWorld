from knowledge_base import AtemporalKnowledgeBase
from helpers import *
import heapq

class Agent:

    def __init__(self, cave, file):
        self.cave = cave
        self.caveHeight, self.caveWidth = cave.get_dimensions()
        self.kb = AtemporalKnowledgeBase(self.caveWidth, self.caveHeight)
        self.beliefState = [[0 for _ in range(self.caveWidth)] for _ in range(self.caveHeight)]
        start = cave.get_start_position()
        self.beliefState[start[0]][start[1]] = 2
        self.currentLocation = start
        self.goalLocation = cave.get_goal_position()
        self.facing = 0
        self.arrow = True
        self.score = 0
        self.gold_score = 0
        self.gameOver = False
        self.file = file

    def forward(self):
        x, y = self.currentLocation
        if self.facing == 0:
            y += 1
        elif self.facing == 90:
            x += 1
        elif self.facing == 180:
            y -= 1
        elif self.facing == 270:
            x -= 1

        if x < 0 or y < 0 or x >= self.caveHeight or y >= self.caveWidth:
            print('Bump')
            return
        else:
            print(f'Move to field {(x+1,y+1)}')
            self.file.write(f'Move to field {(x+1,y+1)}\n')
            self.currentLocation[0] = x
            self.currentLocation[1] = y
            self.score -= 1

    def turn_left(self):
        self.facing = (self.facing + 90) % 360
        self.score -= 1

    def turn_right(self):
        self.facing = (self.facing - 90) % 360
        self.score -= 1

    def shoot(self):
        if not self.arrow:
            return
        self.score -= 100
        if self.facing == 0:
            for j in range(self.currentLocation[1], self.caveWidth):
                # if there is Wumpus in this direction
                if self.cave.check_field(self.currentLocation[0], j)[0]:
                    self.kb.kill_wumpus()
                    self.file.write("Wumpus screams\n")
        if self.facing == 90:
            for i in range(self.currentLocation[0], self.caveHeight):
                if self.cave.check_field(i, self.currentLocation[1])[0]:
                    self.kb.kill_wumpus()
                    self.file.write("Wumpus screams\n")
        if self.facing == 180:
            for j in range(self.currentLocation[1], -1, -1):
                if self.cave.check_field(self.currentLocation[0], j)[0]:
                    self.kb.kill_wumpus()
                    self.file.write("Wumpus screams\n")
        if self.facing == 270:
            for i in range(self.currentLocation[0], -1, -1):
                if self.cave.check_field(i, self.currentLocation[1])[0]:
                    self.kb.kill_wumpus()
                    self.file.write("Wumpus screams\n")
        self.arrow = False

    def pick(self):
        if self.cave.check_field(self.currentLocation[0], self.currentLocation[1])[-1]:
            self.gold_score += 1000
            field = (self.currentLocation[0]+1, self.currentLocation[1]+1)
            print(f"Picked gold from {field}")
            self.file.write(f"Picked gold from {field}\n")
        self.score -= 1
        self.cave.pick_gold(self.currentLocation)

    def climb(self):
        if self.currentLocation == self.goalLocation:
            self.gameOver = True
        self.score += self.gold_score
        self.score -= 1

    def make_action(self, action):
        if not self.gameOver:
            if action == 'TL':
                self.turn_left()
            if action == 'TR':
                self.turn_right()
            if action == 'F':
                self.forward()
            if action == 'S':
                self.shoot()
            if action == 'P':
                self.pick()
            if action == 'C':
                self.climb()

    def neighborhood_cells(self, risk, current_field):
        # return neighboring cells that are OK(either visited or unvisited)
        cells = dict()

        if (current_field[0] + 1) < self.caveHeight:
            up_condition = self.beliefState[current_field[0] + 1][current_field[1]] >= 0 \
                if risk else self.beliefState[current_field[0] + 1][current_field[1]] > 0
            if up_condition:
                cells['U'] = (current_field[0] + 1, current_field[1])
        if (current_field[0] - 1) >= 0:
            down_condition = self.beliefState[current_field[0] - 1][current_field[1]] >= 0 \
                if risk else self.beliefState[current_field[0] - 1][current_field[1]] > 0
            if down_condition:
                cells['D'] = (current_field[0] - 1, current_field[1])
        if (current_field[1] + 1) < self.caveWidth:
            right_condition = self.beliefState[current_field[0]][current_field[1] + 1] >= 0 \
                if risk else self.beliefState[current_field[0]][current_field[1] + 1] > 0
            if right_condition:
                cells['R'] = (current_field[0], current_field[1] + 1)
        if (current_field[1] - 1) >= 0:
            left_condition = self.beliefState[current_field[0]][current_field[1] - 1] >= 0 \
                if risk else self.beliefState[current_field[0]][current_field[1] - 1] > 0
            if left_condition:
                cells['L'] = (current_field[0], current_field[1] - 1)
        return cells

    def plan_next_move(self, goals, risk, current_field, facing):
        if len(goals) == 0:
            raise Exception('No goals found')
        f_values = dict()
        actions = dict()
        angles = dict()
        neighbourhood = self.neighborhood_cells(risk, current_field)
        if not neighbourhood:
            return f_values, actions, angles
        for cell in neighbourhood.keys():
            actions[neighbourhood[cell]] = []
            current_angle = facing
            # g_value initial cost of moving forward to cell
            g_value = -1
            # add cost of rotating in closer direction
            target_angle = 0
            if cell == 'U':
                target_angle = 90
            elif cell == 'L':
                target_angle = 180
            elif cell == 'D':
                target_angle = 270
            angles[neighbourhood[cell]] = target_angle
            action = efficient_rotation(current_angle, target_angle)
            while current_angle != target_angle:
                actions[neighbourhood[cell]].append(action)
                g_value -= 1
                current_angle += 90 if action == 'TL' else -90
                current_angle %= 360
            actions[neighbourhood[cell]].append('F')
            # h_value is distance between cell and goal
            h_value = -min([abs(neighbourhood[cell][0] - goal[0]) + abs(neighbourhood[cell][1] - goal[1])
                            for goal in goals])
            f_values[neighbourhood[cell]] = g_value + h_value
        return actions, f_values, angles

    def plan_route(self, goals, risk):
        if len(goals) == 0:
            return []
        q = []
        current = (self.currentLocation[0], self.currentLocation[1])
        actions_global = {current: []}
        f_values_global = {current: 0}
        angles_global = {current: self.facing}
        came_from = {current: None}
        heapq.heappush(q, (0, current))
        while len(q) > 0:
            value, current = heapq.heappop(q)
            if current in goals:
                print(f'Planed route to {(current[0]+1, current[1]+1)}')
                self.file.write(f'Planed route to {(current[0]+1, current[1]+1)}\n')
                actions_goal = []
                while came_from[current] is not None:
                    actions_goal = actions_global[current] + actions_goal
                    current = came_from[current]
                return actions_goal
            actions, f_values, angles = self.plan_next_move(goals, risk, current, angles_global[current])
            for nb, tentative_value in f_values.items():
                if tentative_value > f_values_global.get(nb, -2**31):
                    f_values_global[nb] = tentative_value
                    angles_global[nb] = angles[nb]
                    came_from[nb] = current
                    actions_global[nb] = actions[nb]
                    if nb not in q:
                        heapq.heappush(q, (-tentative_value, nb))
        return []
    def percept(self):
        x, y = self.currentLocation
        wumpus, pit, stench, breeze, glitter = self.cave.check_field(x, y)
        if (wumpus and self.kb.is_wumpus_alive()) or pit:
            self.gameOver = True
            print("Agent died!")
            self.score -= 1000
            self.file.write("Agent dies a miserable death! \n")
        else:
            self.beliefState[x][y] = 2
        return [stench, breeze, glitter]

    def tell_kb(self, stench, breeze):
        self.kb.tell_field_observation(stench, breeze, self.currentLocation)

    def identify_safe_fields(self):
        for i in range(self.caveHeight):
            for j in range(self.caveWidth):
                ok = self.kb.ask_field_ok((i, j))
                if ok and self.beliefState[i][j] == 0:
                    self.beliefState[i][j] = 1

    def non_unsafe_fields(self):
        unvisited_fields = set()
        for i in range(self.caveHeight):
            for j in range(self.caveWidth):
                unvisited = self.beliefState[i][j] == 0
                if unvisited and not self.kb.ask_field_not_ok((i, j)):
                    unvisited_fields.add((i, j))
        return unvisited_fields

    def safe_unvisited(self):
        unvisited_fields = set()
        for i in range(self.caveHeight):
            for j in range(self.caveWidth):
                ok = self.beliefState[i][j] == 1
                if ok:
                    self.file.write(f'Field {(i+1,j+1)} is safe but unvisited\n')
                    unvisited_fields.add((i, j))
        return unvisited_fields

    def identify_possible_wumpus(self):
        possible_wumpus = dict()
        for i in range(self.caveHeight):
            for j in range(self.caveWidth):
                if self.beliefState[i][j] != 2:
                    continue
                stench = self.kb.ask_stench((i, j))
                if stench:
                    for d in get_directions():
                        condition1 = 0 <= i + d[0] < self.caveHeight
                        condition2 = 0 <= j + d[1] < self.caveWidth
                        if condition1 and condition2:
                            x = i + d[0]
                            y = j + d[1]
                            if self.beliefState[x][y] <= 0:
                                if self.kb.ask_wumpus((x, y)):
                                    print(f'Found out Wumpus on field {(x+1, y+1)}')
                                    self.file.write(f'Found out Wumpus on field {(x+1, y+1)}\n')
                                    return x, y
                                if not possible_wumpus.get((x, y)):
                                    possible_wumpus[(x, y)] = 1
                                else:
                                    possible_wumpus[(x, y)] += 1
        if possible_wumpus == {}:
            return None
        else:
            probable_location = max(possible_wumpus, key=possible_wumpus.get)
            print(f'Most probable Wumpus location {probable_location}')
            self.file.write(f'Most probable Wumpus location {probable_location}\n')
            return probable_location

    def shoot_wumpus_directly(self, potential_wumpus):
        actions = []
        if potential_wumpus[0] == self.currentLocation[0] or potential_wumpus[1] == self.currentLocation[1]:
            current_angle = self.facing
            if potential_wumpus[0] > self.currentLocation[0]:
                target_angle = 90
            if potential_wumpus[1] > self.currentLocation[1]:
                target_angle = 0
            if potential_wumpus[0] < self.currentLocation[0]:
                target_angle = 270
            if potential_wumpus[1] < self.currentLocation[1]:
                target_angle = 180
            action = efficient_rotation(current_angle, target_angle)
            while current_angle != target_angle:
                actions.append(action)
                current_angle += 90 if action == 'TL' else -90
                current_angle %= 360
            actions.append('S')
            if current_angle == 90:
                self.file.write("Shoot north\n")
            elif current_angle == 180:
                self.file.write('Shoot east\n')
            elif current_angle == 270:
                self.file.write('Shoot south\n')
            elif current_angle == 0:
                self.file.write('Shoot west\n')
        return actions

    def plan_shoot(self):
        possible_wumpus = self.identify_possible_wumpus()
        actions = []
        if possible_wumpus is None:
            return actions
        if not (possible_wumpus[0] == self.currentLocation[0] or possible_wumpus[1] == self.currentLocation[1]):
            q = []
            for i in range(self.caveHeight):
                if self.beliefState[i][possible_wumpus[1]] > 0:
                    heapq.heappush(q, (abs(i - possible_wumpus[0]), (i, possible_wumpus[1])))
            for j in range(self.caveWidth):
                if self.beliefState[possible_wumpus[0]][j] > 0:
                    heapq.heappush(q, (abs(j - possible_wumpus[1]), (possible_wumpus[0], j)))
            v, goal = heapq.heappop(q)
            actions.extend(self.plan_route([goal], False))
        else:
            actions.extend(self.shoot_wumpus_directly(possible_wumpus))
        return actions

    def print_current_state(self):
        for i in range(self.caveHeight - 1, -1, -1):
            for j in range(self.caveWidth):
                if j == self.caveWidth - 1:
                    if i == self.currentLocation[0] and j == self.currentLocation[1]:
                        print('A')
                    else:
                        print(self.beliefState[i][j])
                else:
                    if i == self.currentLocation[0] and j == self.currentLocation[1]:
                        print('A', end="")
                    else:
                        print(self.beliefState[i][j], end="")
        print()
