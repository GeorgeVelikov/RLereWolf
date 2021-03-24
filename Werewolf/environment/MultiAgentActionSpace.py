import gym

# https://github.com/koulanurag/ma-gym/blob/3d61773a1dd5ced942453f25a4d8404766d6a5bc/ma_gym/envs/utils/action_space.py
class MultiAgentActionSpace(list):
    def __init__(self, agents_action_space):
        for space in agents_action_space:
            assert isinstance(space, gym.spaces.space.Space);

        super(MultiAgentActionSpace, self).__init__(agents_action_space);
        self._agents_action_space = agents_action_space;

    def sample(self):
        return [space.sample() for space in self._agents_action_space];
