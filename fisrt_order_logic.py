from pysat.solvers import Solver
from itertools import count


class FOLInterface:
    def __init__(self):
        self.kb = []
        self.symbol_map = {}
        self.reverse_symbol_map = {}
        self.symbol_counter = count(1)

    def get_symbol(self, name):
        if name not in self.symbol_map:
            symbol = next(self.symbol_counter)
            self.symbol_map[name] = symbol
            self.reverse_symbol_map[symbol] = name
        return self.symbol_map[name]

    def get_name(self, symbol):
        if symbol < 0:
            symbol = -symbol
        return self.reverse_symbol_map[symbol]

    def proposition(self, name):
        return [self.get_symbol(name)]

    def not_(self, prop):
        return [-p for p in prop]

    def or_(self, *props):
        return [[s for p in props for s in p]]

    def or_list(self, props):
        return [[s for p in props for s in p]]

    def add_to_kb(self, clauses):
        self.kb.extend(clauses)

    def cnf_(self):
        return self.kb

    def check_entailment(self, q, additional=None):
        cnf = self.cnf_().copy()
        # Negate the query and add it to the CNF
        negated_query = [self.not_(q)]
        cnf.extend(negated_query)
        # Additional knowledge
        if additional:
            cnf.extend(additional)

        with Solver(bootstrap_with=cnf, name='g3') as solver:
            satisfiable = solver.solve()

        return not satisfiable  # If unsatisfiable, the query is entailed

    def print_kb_cnf(self):
        kb = ""
        for i, clause in enumerate(self.kb):
            for j, symbol in enumerate(clause):
                if symbol < 0:
                    kb += "-"
                    symbol = -symbol
                kb += self.get_name(symbol)
                if j != len(clause) - 1:
                    kb += " V "
            if i != len(self.kb) - 1:
                kb += " ^ "
        return kb


'''
# Example usage
fol = FOLInterface()

# Define propositions
A = fol.proposition('A')
B = fol.proposition('B')
# Create knowledge base
fol.add_to_kb(
    fol.or_(A, fol.not_(B))
)
# Check if B is entailed
query = A
additional_knowledge = [B]
entailed = fol.check_entailment(query, additional_knowledge)

print(f"Knowledge Base: {fol.print_kb_cnf()}")
print(f"Query: {fol.get_name(A[0])}")
print(f"Is A entailed? {entailed}")

query = fol.proposition('C')
additional_knowledge = [B]
entailed = fol.check_entailment(query, additional_knowledge)

print(f"Knowledge Base: {fol.print_kb_cnf()}")
print(f"Query: {fol.get_name(query[0])}")
print(f"Is C entailed? {entailed}")
'''