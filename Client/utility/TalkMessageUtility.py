from Client.models.TalkMessage import TalkMessage;

import Shared.constants.CommunicationPresetConstants as CommunicationPresets;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

GENERAL_MESSAGES = [\
    TalkMessage("Agree", CommunicationPresets.AGREE_PLAYER, None),\
    TalkMessage("Disagree", CommunicationPresets.DISAGREE_PLAYER, None),\
    TalkMessage("Certain role" , CommunicationPresets.ASSERT_CERTAIN_PLAYER_ROLE, None),\
    TalkMessage("Uncertain role", CommunicationPresets.ASSERT_UNCERTAIN_PLAYER_ROLE, None),\
    TalkMessage("Declare", CommunicationPresets.DECLARE_ROLE, None),\
    TalkMessage("Declare Vote", CommunicationPresets.VOTE_PLAYER, None),\
];

WEREWOLF_MESSAGES = [\
    TalkMessage("Attack", CommunicationPresets.WEREWOLF_ATTACK_PLAYER, PlayerTypeEnum.Werewolf),\
];

SEER_MESSAGES = [\
    TalkMessage("Divine", CommunicationPresets.SEER_DIVINE_PLAYER_ROLE, PlayerTypeEnum.Seer),\
];

GUARD_MESSAGES = [\
    TalkMessage("Not in house", CommunicationPresets.GUARD_NOT_IN_HOUSE, PlayerTypeEnum.Guard),\
];

ROLES_THAT_CAN_WHISPER = [\
    PlayerTypeEnum.Werewolf,\
];

ALL_MESSAGES = sum([\
    GENERAL_MESSAGES,\
    WEREWOLF_MESSAGES,\
    SEER_MESSAGES,\
    GUARD_MESSAGES,\
], []);

TALK_MESSAGES = sum([\
    GENERAL_MESSAGES,\
    SEER_MESSAGES,\
    GUARD_MESSAGES,\
], []);

WHISPER_MESSAGES = sum([\
    WEREWOLF_MESSAGES,\
], []);

def TalkMessagesForRole(role = None):
    # Villager messages are default for everyone
    messagesForRole = [m for m in TALK_MESSAGES\
        if not m.PlayerType or (role and m.PlayerType == role)]

    return messagesForRole;

def WhisperMessagesForRole(role):
    messagesForRole = [m for m in WHISPER_MESSAGES\
        if role and m.PlayerType == role]

    return messagesForRole;
