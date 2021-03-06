# RLereWolf


## What is this?

RLereWolf is a, Python developed, framework for the social deduction game [Werewolf](https://en.wikipedia.org/wiki/Ultimate_Werewolf). The development of which is part of my undergraduate thesis at [University of Aberdeen](https://www.abdn.ac.uk/). RLereWolf provides the base Werewolf game which can be played multiplayer with either other people or bots (agents). 

It also provides AI developers with an easy to use and integrate to framework for training agents to play Werewolf. The game's implementation allows users to create/join games of up to 75 players in which the players can be other humans, "dummy" agent players, rule-based agent players and/or reinforcement learning agent players, trained with OpenAI Gym.


## Setup
The development of RLereWolf is done in Visual Studio 2019 as a "PyProject" using Python 3.9. In order to setup RLereWolf for development "out of the box" you need to

1. Install Python 3.9
2. Install Visual Studio 2019 with Python support (You can use your preferred editor/IDE, just be aware setting it up might be a bit more awkward)
3. Install the requirements - "pip3.9 install -r requirements.txt"
4. Select any of the pre-made boot configurations (Client, Server, Client + Server etc.) or add your own in the [project startup settings](https://github.com/GeorgeVelikov/RLereWolf/blob/main/Werewolf.sln.startup.json), as seen in:
![image](https://user-images.githubusercontent.com/45877509/110208917-acce1500-7e81-11eb-8d52-6e47b80a66c4.png)

## Structure

### Client

The client contains a basic tkinter and pygubu GUI which sends calls to the server in order to play the games hosted on the **Server**.

![image](https://user-images.githubusercontent.com/45877509/110209199-0125c480-7e83-11eb-9157-2c1ff8242388.png)

![image](https://user-images.githubusercontent.com/45877509/110209305-9de86200-7e83-11eb-87a1-b59bd1250e96.png)


### Server

The socket server that controls multiple games and the players in them. The server keeps logs of the server status, each game and is the effective _game moderator_.

### Shared

Various logic, dtos, utility methods that are used accross the **Client**, **Server** and **Werewolf** projects.

### Werewolf

Holds the game, game logic and currently holds the agent players and is referenced by the **Server** project.

## Other

 My undergerduate thesis, more info coming soon™
