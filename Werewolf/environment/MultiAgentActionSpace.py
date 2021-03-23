import gym

class MultiAgentActionSpace(list):
    def __init__(self, agents_action_space):
        for space in agents_action_space:
            assert isinstance(space, gym.spaces.space.Space);

        super(MultiAgentActionSpace, self).__init__(agents_action_space);
        self._agents_action_space = agents_action_space;

    def sample(self):
        return [space.sample() for space in self._agents_action_space];
