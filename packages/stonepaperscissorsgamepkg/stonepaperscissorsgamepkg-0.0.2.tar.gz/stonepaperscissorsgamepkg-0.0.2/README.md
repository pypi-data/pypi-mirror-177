Rock Paper Scissors - a basic program to play rock,paper,scissors with PC
=========================================================================

# A fun Python package to play rock paper scissors with PC
This is just a basic stress-buster game module to play with your PC
Created by Aswin Venkat <aswinvenk8@gmail.com>

Installation
============

Run the following to install:

```python
pip install stonepaperscissorsgamepkg
```

Methods
=======

1. obj.game(count:int)
    Count -> The number of times you want to play the game with PC

2. obj.rules()
    Will display the rules of the game

3. obj.clear_score()
    Will clear the score (initialise the score back to 0)

4. obj.display_result()
    Will display the result of the game.

5. obj.condition(pc='', player='')
    entering ['stone' or 'paper' or 'scissors'] in pc='{}' and player='{}' will directly give you the result

Usage
=====

```python
from stonepaperscissors import *
g=Game()

# Play a game
>> g.game(5)

# Display Result
>> g.display_result()

# Display rules
>> g.rules()

# Reset the scores
>> g.clear_score()
```