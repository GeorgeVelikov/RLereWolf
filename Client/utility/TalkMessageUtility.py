from Client.models.TalkMessage import TalkMessage;

import Shared.constants.CommunicationPresetConstants as CommunicationPresets;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Shared.enums.MessageTypeEnum import MessageTypeEnum;

GENERAL_MESSAGES = [\
    TalkMessage("Agree with",\
        CommunicationPresets.AGREE_PLAYER,\
        None,\
        False,\
        MessageTypeEnum.AgreeWith),\

    TalkMessage("Disagree with",\
        CommunicationPresets.DISAGREE_PLAYER,\
        None,\
        False,\
        MessageTypeEnum.DisagreeWith),\

    TalkMessage("Accuse Player of being a",\
        CommunicationPresets.ASSERT_CERTAIN_PLAYER_ROLE,\
        None,\
        True,\
        MessageTypeEnum.AccusePlayerOfRole),\

    TalkMessage("Player might be a",\
        CommunicationPresets.ASSERT_UNCERTAIN_PLAYER_ROLE,\
        None,\
        True,\
        MessageTypeEnum.SuggestPlayerOfRole),\

    TalkMessage("I am a",\
        CommunicationPresets.DECLARE_ROLE,\
        None,\
        True,\
        MessageTypeEnum.DeclareSelfAsRole),\
];

WEREWOLF_MESSAGES = [\
    TalkMessage("Attack",\
        CommunicationPresets.WEREWOLF_ATTACK_PLAYER,\
        PlayerTypeEnum.Werewolf,\
        False,\
        MessageTypeEnum.WerewolfAttack),\
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
