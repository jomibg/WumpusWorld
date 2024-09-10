from fisrt_order_logic import FOLInterface
from itertools import combinations


class AtemporalKnowledgeBase:

    def __init__(self, m, n):
        self.fols = FOLInterface()
        self.wumpus_alive = True
        # Creat dictionary initially containing proposition WumpusAlive
        self.propositions = {'WA': self.fols.proposition('WA')}
        # Add Stench, Breeze, Wumpus, Pit and FieldOkay proposition to dictionary
        for i in range(n):
            for j in range(m):
                self.propositions[f'S{i}{j}'] = self.fols.proposition(f'S{i}{j}')
                self.propositions[f'B{i}{j}'] = self.fols.proposition(f'B{i}{j}')
                self.propositions[f'W{i}{j}'] = self.fols.proposition(f'W{i}{j}')
                self.propositions[f'P{i}{j}'] = self.fols.proposition(f'P{i}{j}')
                self.propositions[f'OK{i}{j}'] = self.fols.proposition(f'OK{i}{j}')
        # Exactly one Wumpus exists
        wumpus = [self.propositions[f'W{x}{y}'] for x in range(n) for y in range(m)]
        self.fols.add_to_kb(
            self.fols.or_list(wumpus)
        )
        unique_2_sets = list(combinations(wumpus, 2))
        for wp in unique_2_sets:
            self.fols.add_to_kb(
                self.fols.or_(
                    self.fols.not_(wp[0]),
                    self.fols.not_(wp[1])
                )
            )
        # OK iff not pit and not (wumpus and wumpus alive)
        for i in range(n):
            for j in range(m):
                W = self.propositions[f'W{i}{j}']
                WA = self.propositions[f'WA']
                P = self.propositions[f'P{i}{j}']
                OK = self.propositions[f'OK{i}{j}']
                self.fols.add_to_kb(
                    self.fols.or_(W, P, OK) +
                    self.fols.or_(WA, P, OK) +
                    self.fols.or_(self.fols.not_(OK), self.fols.not_(P)) +
                    self.fols.or_(self.fols.not_(OK), self.fols.not_(WA), self.fols.not_(W))
                )
        # Add propositions about correspondence of Wumpus and Stench, Pits and Breeze
        # and propositions explaining when the field is Okay to the knowledge base
        # Bottom left corner
        self.fols.add_to_kb(self.fols.or_(self.propositions['B00'], self.fols.not_(self.propositions['P10'])) +
                            self.fols.or_(self.propositions['B00'], self.fols.not_(self.propositions['P01'])) +
                            self.fols.or_(self.propositions['P10'], self.propositions['P01'],
                                          self.fols.not_(self.propositions['B00']))
                            )
        self.fols.add_to_kb(self.fols.or_(self.propositions['S00'], self.fols.not_(self.propositions['W10'])) +
                            self.fols.or_(self.propositions['S00'], self.fols.not_(self.propositions['W01'])) +
                            self.fols.or_(self.propositions['W10'], self.propositions['W01'],
                                          self.fols.not_(self.propositions['S00']))
                            )
        # Bottom right corner
        self.fols.add_to_kb(self.fols.or_(self.propositions[f'B0{m-1}'], self.fols.not_(self.propositions[f'P0{m-2}'])) +
                            self.fols.or_(self.propositions[f'B0{m-1}'], self.fols.not_(self.propositions[f'P1{m-1}'])) +
                            self.fols.or_(self.propositions[f'P1{m-1}'], self.propositions[f'P0{m-2}'],
                                          self.fols.not_(self.propositions[f'B0{m-1}']))
                            )
        self.fols.add_to_kb(
            self.fols.or_(self.propositions[f'S0{m-1}'], self.fols.not_(self.propositions[f'W0{m-2}'])) +
            self.fols.or_(self.propositions[f'S0{m-1}'], self.fols.not_(self.propositions[f'W1{m-1}'])) +
            self.fols.or_(self.propositions[f'W1{m-1}'], self.propositions[f'W0{m-2}'],
                          self.fols.not_(self.propositions[f'S0{m-1}']))
                            )
        # Top left corner
        self.fols.add_to_kb(
            self.fols.or_(self.propositions[f'B{n-1}0'], self.fols.not_(self.propositions[f'P{n-2}0'])) +
            self.fols.or_(self.propositions[f'B{n-1}0'], self.fols.not_(self.propositions[f'P{n-1}1'])) +
            self.fols.or_(self.propositions[f'P{n-2}0'], self.propositions[f'P{n-1}1'],
                          self.fols.not_(self.propositions[f'B{n-1}0']))
                            )
        self.fols.add_to_kb(
            self.fols.or_(self.propositions[f'S{n-1}0'], self.fols.not_(self.propositions[f'W{n-2}0'])) +
            self.fols.or_(self.propositions[f'S{n-1}0'], self.fols.not_(self.propositions[f'W{n-1}1'])) +
            self.fols.or_(self.propositions[f'W{n-2}0'], self.propositions[f'W{n-1}1'],
                          self.fols.not_(self.propositions[f'S{n-1}0']))
                            )
        # Top right corner
        self.fols.add_to_kb(
            self.fols.or_(self.propositions[f'B{n-1}{m-1}'], self.fols.not_(self.propositions[f'P{n-2}{m-1}'])) +
            self.fols.or_(self.propositions[f'B{n-1}{m-1}'], self.fols.not_(self.propositions[f'P{n-1}{m-2}'])) +
            self.fols.or_(self.propositions[f'P{n-2}{m-1}'], self.propositions[f'P{n-1}{m-2}'],
                          self.fols.not_(self.propositions[f'B{n-1}{m-1}']))
                            )
        self.fols.add_to_kb(
            self.fols.or_(self.propositions[f'S{n-1}{m-1}'], self.fols.not_(self.propositions[f'W{n-2}{m-1}'])) +
            self.fols.or_(self.propositions[f'S{n-1}{m-1}'], self.fols.not_(self.propositions[f'W{n-1}{m-2}'])) +
            self.fols.or_(self.propositions[f'W{n-2}{m-1}'], self.propositions[f'W{n-1}{m-2}'],
                          self.fols.not_(self.propositions[f'S{n-1}{m-1}']))
                            )
        # Vertical edges
        for i in range(1, n-1):
            bi0 = self.propositions[f'B{i}0']
            bim1 = self.propositions[f'B{i}{m-1}']
            si0 = self.propositions[f'S{i}0']
            sim1 = self.propositions[f'S{i}{m-1}']
            # left edge
            self.fols.add_to_kb(
                self.fols.or_(bi0, self.fols.not_(self.propositions[f'P{i+1}0'])) +
                self.fols.or_(bi0, self.fols.not_(self.propositions[f'P{i-1}0'])) +
                self.fols.or_(bi0, self.fols.not_(self.propositions[f'P{i}1'])) +
                self.fols.or_(self.fols.not_(bi0), self.propositions[f'P{i+1}0'],
                              self.propositions[f'P{i-1}0'], self.propositions[f'P{i}1'])
            )
            self.fols.add_to_kb(
                self.fols.or_(si0, self.fols.not_(self.propositions[f'W{i+1}0'])) +
                self.fols.or_(si0, self.fols.not_(self.propositions[f'W{i-1}0'])) +
                self.fols.or_(si0, self.fols.not_(self.propositions[f'W{i}1'])) +
                self.fols.or_(self.fols.not_(si0), self.propositions[f'W{i+1}0'],
                              self.propositions[f'W{i-1}0'], self.propositions[f'W{i}1'])
            )
            # right edge
            self.fols.add_to_kb(
                self.fols.or_(bim1, self.fols.not_(self.propositions[f'P{i+1}{m-1}'])) +
                self.fols.or_(bim1, self.fols.not_(self.propositions[f'P{i-1}{m-1}'])) +
                self.fols.or_(bim1, self.fols.not_(self.propositions[f'P{i}{m-2}'])) +
                self.fols.or_(self.fols.not_(bim1), self.propositions[f'P{i+1}{m-1}'],
                              self.propositions[f'P{i-1}{m-1}'], self.propositions[f'P{i}{m-2}'])
            )
            self.fols.add_to_kb(
                self.fols.or_(sim1, self.fols.not_(self.propositions[f'W{i+1}{m-1}'])) +
                self.fols.or_(sim1, self.fols.not_(self.propositions[f'W{i-1}{m-1}'])) +
                self.fols.or_(sim1, self.fols.not_(self.propositions[f'W{i}{m-2}'])) +
                self.fols.or_(self.fols.not_(sim1), self.propositions[f'W{i+1}{m-1}'],
                              self.propositions[f'W{i-1}{m-1}'], self.propositions[f'W{i}{m-2}'])
            )
            # Horizontal edges
            for j in range(1, m-1):
                b0j = self.propositions[f'B0{j}']
                bn1j = self.propositions[f'B{n-1}{j}']
                s0j = self.propositions[f'S0{j}']
                sn1j = self.propositions[f'S{n-1}{j}']
                # bottom
                self.fols.add_to_kb(
                    self.fols.or_(b0j, self.fols.not_(self.propositions[f'P{0}{j+1}'])) +
                    self.fols.or_(b0j, self.fols.not_(self.propositions[f'P{0}{j-1}'])) +
                    self.fols.or_(b0j, self.fols.not_(self.propositions[f'P{1}{j}'])) +
                    self.fols.or_(self.fols.not_(b0j), self.propositions[f'P{0}{j+1}'],
                                  self.propositions[f'P{0}{j-1}'], self.propositions[f'P{1}{j}'])
                )
                self.fols.add_to_kb(
                    self.fols.or_(s0j, self.fols.not_(self.propositions[f'W{0}{j + 1}'])) +
                    self.fols.or_(s0j, self.fols.not_(self.propositions[f'W{0}{j - 1}'])) +
                    self.fols.or_(s0j, self.fols.not_(self.propositions[f'W{1}{j}'])) +
                    self.fols.or_(self.fols.not_(s0j), self.propositions[f'W{0}{j + 1}'],
                                  self.propositions[f'W{0}{j - 1}'], self.propositions[f'W{1}{j}'])
                )
                # top
                self.fols.add_to_kb(
                    self.fols.or_(bn1j, self.fols.not_(self.propositions[f'P{n-1}{j + 1}'])) +
                    self.fols.or_(bn1j, self.fols.not_(self.propositions[f'P{n-1}{j - 1}'])) +
                    self.fols.or_(bn1j, self.fols.not_(self.propositions[f'P{n-2}{j}'])) +
                    self.fols.or_(self.fols.not_(bn1j), self.propositions[f'P{n-1}{j + 1}'],
                                  self.propositions[f'P{n-1}{j - 1}'], self.propositions[f'P{n-2}{j}'])
                )
                self.fols.add_to_kb(
                    self.fols.or_(sn1j, self.fols.not_(self.propositions[f'W{n - 1}{j + 1}'])) +
                    self.fols.or_(sn1j, self.fols.not_(self.propositions[f'W{n - 1}{j - 1}'])) +
                    self.fols.or_(sn1j, self.fols.not_(self.propositions[f'W{n - 2}{j}'])) +
                    self.fols.or_(self.fols.not_(sn1j), self.propositions[f'W{n - 1}{j + 1}'],
                                  self.propositions[f'W{n - 1}{j - 1}'], self.propositions[f'W{n - 2}{j}'])
                )
            # Central fields
            for i in range(1, n-1):
                for j in range(1, m-1):
                    bij = self.propositions[f'B{i}{j}']
                    sij = self.propositions[f'S{i}{j}']
                    self.fols.add_to_kb(
                        self.fols.or_(bij, self.fols.not_(self.propositions[f'P{i+1}{j}'])) +
                        self.fols.or_(bij, self.fols.not_(self.propositions[f'P{i-1}{j}'])) +
                        self.fols.or_(bij, self.fols.not_(self.propositions[f'P{i}{j+1}'])) +
                        self.fols.or_(bij, self.fols.not_(self.propositions[f'P{i}{j-1}'])) +
                        self.fols.or_(self.fols.not_(bij), self.propositions[f'P{i+1}{j}'],
                                      self.propositions[f'P{i-1}{j}'], self.propositions[f'P{i}{j+1}'],
                                      self.propositions[f'P{i}{j-1}']
                                      )
                    )
                    self.fols.add_to_kb(
                        self.fols.or_(sij, self.fols.not_(self.propositions[f'W{i + 1}{j}'])) +
                        self.fols.or_(sij, self.fols.not_(self.propositions[f'W{i - 1}{j}'])) +
                        self.fols.or_(sij, self.fols.not_(self.propositions[f'W{i}{j + 1}'])) +
                        self.fols.or_(sij, self.fols.not_(self.propositions[f'W{i}{j - 1}'])) +
                        self.fols.or_(self.fols.not_(sij), self.propositions[f'W{i + 1}{j}'],
                                      self.propositions[f'W{i - 1}{j}'], self.propositions[f'W{i}{j + 1}'],
                                      self.propositions[f'W{i}{j - 1}']
                                      )
                    )
                    self.fols.add_to_kb([self.fols.not_(self.propositions['W00'])])
                    self.fols.add_to_kb([self.fols.not_(self.propositions['P00'])])

    def ask_field_ok(self, field_coords):
        x, y = field_coords
        q = self.propositions[f'OK{x}{y}']
        additional = [self.fols.not_(self.propositions['WA'])] if not self.wumpus_alive else [self.propositions['WA']]
        return self.fols.check_entailment(q, additional)

    def ask_field_not_ok(self, field_coords):
        x, y = field_coords
        q = self.fols.not_(self.propositions[f'OK{x}{y}'])
        additional = [self.fols.not_(self.propositions['WA'])] if not self.wumpus_alive else [self.propositions['WA']]
        return self.fols.check_entailment(q, additional)

    def tell_field_observation(self, stench, breeze, field_coords):
        x, y = field_coords
        if stench:
            self.fols.add_to_kb([self.propositions[f'S{x}{y}']])
        else:
            self.fols.add_to_kb([self.fols.not_(self.propositions[f'S{x}{y}'])])
        if breeze:
            self.fols.add_to_kb([self.propositions[f'B{x}{y}']])
        else:
            self.fols.add_to_kb([self.fols.not_(self.propositions[f'B{x}{y}'])])
        self.fols.add_to_kb([self.propositions[f'OK{x}{y}']])

    def ask_wumpus(self, field_coords):
        x, y = field_coords
        q = self.propositions[f'W{x}{y}']
        additional = [self.fols.not_(self.propositions['WA'])] if not self.wumpus_alive else [self.propositions['WA']]
        return self.fols.check_entailment(q, additional)

    def ask_pit(self, field_coords):
        x, y = field_coords
        q = self.propositions[f'P{x}{y}']
        return self.fols.check_entailment(q)

    def ask_stench(self, field_coords):
        x, y = field_coords
        q = self.propositions[f'S{x}{y}']
        return self.fols.check_entailment(q)

    def kill_wumpus(self):
        print('Wumpus screams')
        self.wumpus_alive = False

    def is_wumpus_alive(self):
        return self.wumpus_alive


'''
atemporalTest = AtemporalKnowledgeBase(4, 4)

# Test 0
print('# CHECK (0,0) #')
# 0.1
print(f'Field (0,0) is OK: {atemporalTest.ask_field_ok((0,0))}')
# 0.2
print(f'Wumpus on (0,0) {atemporalTest.ask_wumpus((0,0))}')
# 0.3
print(f'Pit on (0,0) {atemporalTest.ask_pit((0,0))}')
print('Nothing sensed on (0,0)')
atemporalTest.tell_field_observation(False, False, (0,0))
print(f'Field (0,0) is OK: {atemporalTest.ask_field_ok((0,0))}')
print(f'Test stench on (1,0): {atemporalTest.ask_stench((1 ,0))}')
print(f'Field (1,0) is OK: {atemporalTest.ask_field_ok((1,0))}')

# Test 1
# 1.1
print('#THERE IS WUMPUS ON (1,1)#')
atemporalTest.tell_field_observation(True, False, (1, 0))
print(f'Stench on (1,0): {atemporalTest.ask_stench((1 ,0))}')
atemporalTest.tell_field_observation(True, False, (2, 1))
print(f'Stench on (2,1): {atemporalTest.ask_stench((2 ,1))}')
safe11 = atemporalTest.ask_field_ok((1, 1))
print(f'Field (1,1) is safe? {safe11}')
print(f'Field (1,1) is unsafe? {atemporalTest.ask_field_not_ok((1, 1))}')
# 1.2
atemporalTest.tell_field_observation(False, False, (2, 0))
wumpus11 = atemporalTest.ask_wumpus((1, 1))
print(f'Wumpus on (1,1)? {wumpus11}')
print(f'Field (1,1) is unsafe? {atemporalTest.ask_field_not_ok((1, 1))}')

# Test 2 (Wumpus killed)
atemporalTest.kill_wumpus()
safe_after_kill = atemporalTest.ask_field_ok((1, 1))
print(f'Field (1,1) is safe? {safe_after_kill}')

# Test 3 (breeze)
print('THERE IS PIT ON (2,3)')
atemporalTest.tell_field_observation(False, True, (1, 3))
atemporalTest.tell_field_observation(False, True, (3, 3))
safe23 = atemporalTest.ask_field_ok((2, 3))
print(f'Field (2,3) is safe? {safe23}')
pit23 = atemporalTest.ask_pit((2, 3))
print(f'Pit identified {pit23}')

# Test 4 (identify pit)
print('Field (3,2) no breeze or stench')
atemporalTest.tell_field_observation(False, False, (3, 2))
safe22 = atemporalTest.ask_field_ok((2, 2))
pit22 = atemporalTest.ask_pit((2, 2))
pit23 = atemporalTest.ask_pit((2, 3))
print(f'Field (2,2) is safe? {safe22}')
print(f'Pit identified (2,2)? {pit22}')
print(f'Pit identified (2,3)? {pit23}')
'''