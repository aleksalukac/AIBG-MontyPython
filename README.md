# AIBG Koala Safari
## _Team: Monty Python_
Team members:
- Tadija Sebez
- Uros Pocek
- Aleksandar Lukac

## How to start

- Final version is in directory Final version
- Start script finalSolution.py in terminal with GameId as parameter

Example:
> ">> C:\finalSolution.py 123" 

Where 123 is gameId.
Packages used: json, Path from pathlib, requests and sys

### Idea

At the beginning we create a pseudo-Hamilton path through the map with the goal to collect as many points as possible using minimal energy. During the walk we try to collect FreeASpot (and not use it) and PandaCrew tiles. 
In the endgame, our bot tries to create a trap for the enemy by stopping and leaving two spots in the neighorhood, where the enemy bot will teleport eventually. After they teleport, our goal is to steal their koalas (stealing enemy's koalas is always our priority).
