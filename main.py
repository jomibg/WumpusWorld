import os
from agent import Agent
from cave import read_cave
from helpers import handle_percepts

# Read input files
file_name = input("Provide name of the input world file: ")
file_path = os.path.join("input", file_name)
if os.path.exists(file_path):
    cave = read_cave(file_path)
else:
    raise Exception('Input file doesn\'t exist')
# Initialize the game
output_path = os.path.join('output', file_name)
if not os.path.isdir('output'):
    os.makedirs('output')
output_file = open(output_path, 'w')
print("Wumpus cave:")
cave.print_cave()
agent = Agent(cave, output_file)
gold_picked = 0
print("Initial agent location:")
agent.print_current_state()
print("Game started")
glitter = handle_percepts(agent, output_file)


# Run the game
# Agent plays the game through the tell ask interface
while not agent.gameOver:
    plan = []
    unvisited_safe = agent.safe_unvisited()
    plan.extend(agent.plan_route(unvisited_safe, False))
    if len(plan) == 0 and agent.arrow:
        print("Plan shooting Wumpus")
        output_file.write(f"No unvisited safe field identified; Plan shooting Wumpus\n")
        plan.extend(agent.plan_shoot())
    if len(plan) == 0 and gold_picked == 0:
        output_file.\
            write(f"No unvisited safe field identified and no gode picked.\nTake a risk and move to an unvisited field that is not marked as unsafe\n")
        plan.extend(agent.plan_route(agent.non_unsafe_fields(), True))
    if len(plan) == 0 and agent.currentLocation != cave.get_goal_position():
        print("Go to exit")
        output_file.write(f"Move towards the exit\n")
        goal_position = cave.get_goal_position()
        plan.extend(agent.plan_route([(goal_position[0], goal_position[1])], False))
    if len(plan) == 0 and agent.currentLocation == cave.get_goal_position():
        print("Climb out")
        output_file.write(f'Climb out the cave\n')
        plan.append('C')

    while len(plan) > 0:
        action = plan.pop(0)
        agent.make_action(action)
        if action == 'F' or action == 'S':
            glitter = handle_percepts(agent, output_file)
            if agent.gameOver:
                break
            if glitter:
                plan.append('P')
                gold_picked += 1
                glitter = False

print(f'Agent score: {agent.score}')
output_file.write(f'Final score: {agent.score}\n')
output_file.close()
