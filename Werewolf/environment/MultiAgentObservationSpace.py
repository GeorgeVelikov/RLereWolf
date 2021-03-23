import gym;

# https://github.com/koulanurag/ma-gym/blob/master/ma_gym/envs/utils/observation_space.py
class MultiAgentObservationSpace(list):
    def __init__(self, agents_observation_space):
        for space in agents_observation_space:
            assert isinstance(space, gym.spaces.space.Space);

        super().__init__(agents_observation_space);
        self._agents_observation_space = agents_observation_space;

    def sample(self):
        return [space.sample() for space in self._agents_observation_space];

    def contains(self, observations):
        for space, observation in zip(self._agents_observation_space, observations):
            if not space.contains(observation):
                return False;
        else:
            return True;
