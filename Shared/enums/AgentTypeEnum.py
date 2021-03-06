from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class AgentTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    DummyAgent = 100;
    RuleBasedAgent = 200;
    TrainableAgent = 300;

    def __str__(self):
        if self.value == self._None.value:
            return str();

        elif self.value == self.DummyAgent.value:
            return "Dummy Agent";

        elif self.value == self.RuleBasedAgent.value:
            return "Rule-Based Agent";

        elif self.value == self.TrainableAgent.value:
            return "Trainable Agent";
        else:
            raise GameException("Unknown agent type used.");

    @staticmethod
    def Values():
        return [\
            AgentTypeEnum.DummyAgent,\
            AgentTypeEnum.RuleBasedAgent,\
            AgentTypeEnum.TrainableAgent];
