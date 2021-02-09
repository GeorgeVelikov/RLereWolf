import gym;

import Test;
from game.infrastructure.Server import Server;

def main():
    env = gym.make('CartPole-v0')

    for i_episode in range(20):
        observation = env.reset()
        for t in range(10):
            env.render()
            print(observation)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
    env.close()

if __name__ == "__main__":
    server = Server();
    server.Run();

    Test.TestPlayers();
    Test.TestPlayerRoles();
    Test.TestClientConnection();
    #main();
