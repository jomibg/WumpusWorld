# Modified Wumpus World Game
The project implements a knowledge-based agent capable of navigating a modified version of the Wumpus World environment, described by Stuart Russell and Peter Norvig in their book Artificial Intelligence: A Modern Approach (chapter 7.2, pp. 236 - 240).  The short description of modified Wumpus World environmen is provided below.

![WW](https://miro.medium.com/v2/resize:fit:441/1*fJyUHswCiQAQ4BHJAsZEsw.png)
## Description
- The Wumpus World is a cave represented by an MxN grid.
- A monster called the Wumpus is located somewhere in the cave; it eats anyone who steps on its field. However, the Wumpus can be killed by the agent, though the agent only has one arrow.
- When the agent shoots the arrow, it moves forward in the direction of the shot until it either hits the Wumpus or a wall.
- Some fields contain bottomless pits that trap anyone who steps on them (except for the Wumpus, who is too large to fall).
- Fortunately, some fields in the cave contain piles of gold, and the agent's goal is to collect as much gold as possible without being eaten or falling into a pit.
- After collecting the gold, or if the mission becomes impossible, the agent must exit the cave using a ladder located on a specific field.

### Environment
- The dimensions of the cave (M and N parameters), the position of the exit, the starting position of the agent, and the locations of gold piles, bottomless pits, and the Wumpus are specified as input.
- There is exactly one Wumpus.
- Each square, except the starting field, can contain a pit with a probability of 0.2.
- Each field, except a pit field, can contain gold.
- The agent starts the game facing east (right).
- At the beginning of the game, the agent knows only its current position and the position of the exit field.
- In any field adjacent (one cell above, below, left, or right) to the Wumpus, the agent can sense a stench.
- In any field adjacent (one cell above, below, left, or right) to a bottomless pit, the agent can sense a breeze.

### Sensors
- Stench: True if the agent is in a square that is directly adjacent (not diagonally) to a square with a Wumpus.
- Breeze: True if the agent is in a square that is directly adjacent (not diagonally) to a square with a pit.
- Glitter: True if the agent is in a square that contains gold.
- Bump: True immediately after the agent collides with a wall.
- Scream: True immediately after the Wumpus is hit by the agent's arrow.

### Actuators
- Forward: Moves the agent one square forward in the direction agent is facing.
- TurnLeft: Rotates the agent 90 degrees to the left.
- TurnRight: Rotates the agent 90 degrees to the right.
- Death: Occurs when the agent dies.
- Grab: Allows the agent to pick up gold if it is in the same square.
- Shoot: Fires an arrow in a straight line in the direction the agent is currently facing.
- Climb: Allows the agent to climb out of the cave, but only from the exit square.

### Performance Measures
- +1000 points for each pile of gold collected if the agent successfully exits the cave alive.
- -1000 points if the agent dies.
- -1 point for every action the agent takes.
- -100 points for shooting the arrow.

## Running the game
Before running the game, ensure that you have a Python environment set up with Python version 3.11, and clone the repository to your machine. You will also need to install the PySAT library by running:

```bash
pip install python-sat==1.8.dev13
```

Next, create an `input` directory and add text files containing descriptions of the worlds in the format specified below. To start the game, run:

```bash
python main.py
```

You will then be prompted to enter the name of the file that contains the world description. The agent will automatically play the game, and the program will provide updates in the terminal about the agent's perceptions, plans, and actions (as described below). Additionally, a log containing all perceived sensations and executed actions will be saved in the file **<cwd>/input/name-of-the-world.txt**.

### Input File Format
The input file **name-of-the-world.txt** specifies the cave dimensions and the locations of key elements.

#### Example of the `wumpus_world.txt` file:

```
M44
A11
B21
P31
B41
S12
B32
W13
S23
G23
B23
P33
B43
S14
B34
P44
GO11
```

#### Meaning of labels in the example:

- `Axy` = The agent starts on the field (x, y).
- `Bxy` = The field (x, y) is breezy.
- `Gxy` = There's gold on the field (x, y).
- `GOxy` = The field (x, y) is the goal (exit from the cave).
- `Mxy` = The cave is x fields high and y fields wide (map size).
- `Pxy` = There's a pit on the field (x, y).
- `Sxy` = The field (x, y) is smelly.
- `Wxy` = The Wumpus is on the field (x, y).

### Terminal Notifications Format
After reading the input files, the encoded cave will be displayed in the terminal. If multiple elements occupy the same field, the element with the highest priority (as indicated by the order of the labels below) will be shown. Here’s an example of an encoded cave:

```
Wumpus cave:
S#BP
WGPB
S#B#
*BPB
```

##### Description:
- `*`: Agent's location
- `W`: Wumpus
- `P`: Pit
- `G`: Gold
- `S`: Stench
- `B`: Breeze
- `#`: Empty field

Once the agent starts playing, you will receive notifications in text format that describe the agent's sensations, plans, and actions, along with the encoded belief state (the agent’s internal representation of the world). Below is an example of these prompts and a description of the agent’s belief state encoding:

```
Initial agent location:
0000
0000
0000
A000

Game started
No breeze or stench sensed
0000
0000
1000
A100

Planed route to (1, 2)
Move to field (1, 2)
Stench sensed
0000
0000
1000
2A00

...
```

##### Description:
- `A`: Agent
- `0`: Unvisited field, not yet identified as safe
- `1`: Unvisited field identified as safe
- `2`: Visited field

### Output File Format
The output file has the same name as the corresponding input file but is located in the **output** directory. It contains information about fields identified as safe at each moment of the game, as well as the agent’s sensations and actions taken. An example of the output file `wumpus_world.txt` is shown below:
```
Field (1, 2) is safe but unvisited
Field (2, 1) is safe but unvisited
Planed route to (1, 2)
Move to field (1, 2)
Stench sensed
Field (2, 1) is safe but unvisited
Planed route to (2, 1)
Move to field (1, 1)
Move to field (2, 1)
Breeze sensed
Field (2, 2) is safe but unvisited
Planed route to (2, 2)
Move to field (2, 2)
Field (2, 3) is safe but unvisited
Field (3, 2) is safe but unvisited
Planed route to (2, 3)
Move to field (2, 3)
Glitter sensed
Stench sensed
Breeze sensed
Picked gold from (2, 3)
Field (3, 2) is safe but unvisited
Planed route to (3, 2)
Move to field (2, 2)
Move to field (3, 2)
Breeze sensed
No unvisited safe field identified; Plan shooting Wumpus
Found out Wumpus on field (1, 3)
Planed route to (1, 2)
Move to field (2, 2)
Move to field (1, 2)
Stench sensed
No unvisited safe field identified; Plan shooting Wumpus
Found out Wumpus on field (1, 3)
Shoot west
Wumpus screams
Stench sensed
Field (1, 3) is safe but unvisited
Planed route to (1, 3)
Move to field (1, 3)
Field (1, 4) is safe but unvisited
Planed route to (1, 4)
Move to field (1, 4)
Stench sensed
Field (2, 4) is safe but unvisited
Planed route to (2, 4)
Move to field (2, 4)
Field (3, 4) is safe but unvisited
Planed route to (3, 4)
Move to field (3, 4)
Breeze sensed
Move towards the exit
Planed route to (1, 1)
Move to field (2, 4)
Move to field (1, 4)
Stench sensed
Move to field (1, 3)
Move to field (1, 2)
Stench sensed
Move to field (1, 1)
Climb out the cave
Final score: 866
```
