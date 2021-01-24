import gym

class WerewolfEnvironment(object):
    def __init__(self, configuration):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS);
        # Example for using image as input:
        self.observation_space = spaces.Box(\
            low=0,\
            high=255,\
            shape=(HEIGHT, WIDTH, N_CHANNELS),\
            dtype=np.uint8);

    def step(self, action):
        # Execute one time step within the environment
        return;

    def reset(self):
        # Reset the state of the environment to an initial state
        return;

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        return;
