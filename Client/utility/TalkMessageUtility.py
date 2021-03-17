from Client.models.TalkMessage import TalkMessage;

import Shared.constants.CommunicationPresetConstants as CommunicationPresets;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

GENERAL_MESSAGES = [\
    TalkMessage("Agree", CommunicationPresets.AGREE_PLAYER, None, False),\
    TalkMessage("Disagree", CommunicationPresets.DISAGREE_PLAYER, None, False),\
    TalkMessage("Accuse Certain Role" , CommunicationPresets.ASSERT_CERTAIN_PLAYER_ROLE, None, True),\
    TalkMessage("Accuse Uncertain Role", CommunicationPresets.ASSERT_UNCERTAIN_PLAYER_ROLE, None, True),\
    TalkMessage("Declare Role", CommunicationPresets.DECLARE_ROLE, None, True),\
];

WEREWOLF_MESSAGES = [\
    TalkMessage("Attack", CommunicationPresets.WEREWOLF_ATTACK_PLAYER, PlayerTypeEnum.Werewolf, False),\
];

SEER_MESSAGES = [\
];

GUARD_MESSAGES = [\
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
