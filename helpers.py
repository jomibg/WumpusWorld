def handle_percepts(agent, output_file):
    stench, breeze, glitter = agent.percept()
    if glitter:
        print('Glitter sensed')
        output_file.write(f'Glitter sensed\n')
    if stench:
        print('Stench sensed')
        output_file.write('Stench sensed\n')
    if breeze:
        print('Breeze sensed')
        output_file.write('Breeze sensed\n')
    if not stench and not breeze:
        print('No breeze or stench sensed')
    agent.tell_kb(stench, breeze)
    agent.identify_safe_fields()
    agent.print_current_state()
    return glitter


def get_directions():
    return [(0, 1), (1, 0), (0, -1), (-1, 0)]


def efficient_rotation(current_angle, target_angle):
    l = (target_angle - current_angle) % 360
    r = (current_angle - target_angle) % 360
    if l < r:
        return 'TL'
    else:
        return 'TR'
