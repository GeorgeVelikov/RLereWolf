from Client.models.TalkMessage import TalkMessage;

import Shared.constants.CommunicationPresetConstants as CommunicationPresets;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

VILLAGER_MESSAGES = [\
    TalkMessage(CommunicationPresets.AGREE_PLAYER, PlayerTypeEnum.Villager),\
    TalkMessage(CommunicationPresets.DISAGREE_PLAYER, PlayerTypeEnum.Villager),\
    TalkMessage(CommunicationPresets.ASSERT_CERTAIN_PLAYER_ROLE, PlayerTypeEnum.Villager),\
    TalkMessage(CommunicationPresets.ASSERT_UNCERTAIN_PLAYER_ROLE, PlayerTypeEnum.Villager),\
    TalkMessage(CommunicationPresets.DECLARE_ROLE, PlayerTypeEnum.Villager),\
    TalkMessage(CommunicationPresets.VOTE_PLAYER, PlayerTypeEnum.Villager),\
];

WEREWOLF_MESSAGES = [\
    TalkMessage(CommunicationPresets.WEREWOLF_ATTACK_PLAYER, PlayerTypeEnum.Werewolf),\
];

SEER_MESSAGES = [\
    TalkMessage(CommunicationPresets.SEER_DIVINE_PLAYER_ROLE, PlayerTypeEnum.Seer),\
];

GUARD_MESSAGES = [\
    TalkMessage(CommunicationPresets.GUARD_NOT_IN_HOUSE, PlayerTypeEnum.Guard),\
];

ALL_MESSAGES = sum([],\
    VILLAGER_MESSAGES,\
    WEREWOLF_MESSAGES,\
    SEER_MESSAGES,\
    GUARD_MESSAGES,\
[]);

def Messages(role = None):
    # Villager messages are default for everyone
    messagesForRole = [m for m in ALL_MESSAGES\
        if m.PlayerType == PlayerTypeEnum.Villager\
            or (role and m.PlayerType == role)]

    return messagesForRole;
