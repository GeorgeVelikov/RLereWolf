PLAYER = "%player%";
ROLE = "%role%";

# General
AGREE_PLAYER = f"I agree with {PLAYER}.";
DISAGREE_PLAYER = f"I disagree with {PLAYER}.";

ASSERT_CERTAIN_PLAYER_ROLE = f"{PLAYER} is a {ROLE}.";
ASSERT_UNCERTAIN_PLAYER_ROLE = f"I think {PLAYER} is a {ROLE}.";
DECLARE_ROLE = f"I am a {ROLE}.";

# Guard specific

# Werewolf specific
WEREWOLF_ATTACK_PLAYER = f"I will attack {PLAYER}.";

# Seer specific

def IsMessageValid(messageTemplate, forPlayer = None, forRole = None):
    if not messageTemplate:
        return False;

    text = messageTemplate;

    if (PLAYER in messageTemplate) and not forPlayer:
        return False;

    if (ROLE in messageTemplate) and not forRole:
        return False;

    return True;