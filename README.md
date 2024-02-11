# Laser-Dot-Collaborative-Pygame-Environment-
Laser Dot game is built in Pygame for collaboration games between agents and humans.

---
3 arguments
* Player1 [human or agent]
* Player2 [human or agent]
* UI [True False]
* Ignore Time [Ture False]
Example
```
python game.py human agent True False
```
If any of the two players are human UI will turn on even if the argument is false.

If Ignore Time is False, Pygame maintains 60 Frames per second.

For human players, the controls are UP and DOWN for player one and LEFT and RIGHT for player 2
