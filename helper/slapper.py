'''
Slapping module for LINE bots
(c) 2018 - laymonage
'''

import random


def slap(subject, target, me):
    '''
    Return a message stating "Subject slapped target with a random object."
    subject: an object returned by LineBotApi.get_profile method
    target (str): slapping target
    me: like subject, but for your own profile
    '''
    slap_items = ["frying pan", "baseball bat", "cricket bat", "guitar",
                  "crowbar", "wooden stick", "nightstick", "golf club",
                  "katana", "hand", "laptop", "book", "drawing book",
                  "mouse", "keyboard"]
    s_name = subject.display_name
    itsme = subject == me
    has_my_name = not itsme and me.display_name.title() in s_name.title()

    if has_my_name:
        if me.display_name.lower() == s_name.lower():
            slap_msg = ("IMPERSONATOR! >:(\n"
                        "I slapped you back and forth with a {} "
                        "for impersonating my creator."
                        .format(random.choice(slap_items)))
        else:
            slap_msg = ("NOT FUNNY! >:("
                        "I slapped you back and forth with a {} "
                        "for making fun of my creator."
                        .format(random.choice(slap_items)))

    if "Aiden" in target.title():
        if itsme:
            slap_msg = ("{} gently slapped me.\n"
                        "Sorry, {} :("
                        .format(s_name, s_name))
        elif has_my_name:
            slap_msg = slap_msg[:-1] + " AND trying to slap me."
        else:
            slap_msg = ("I slapped {} with a {} for trying to slap me."
                        .format(s_name, random.choice(slap_items)))

    elif ''.join(c for c in target.lower() if c.isalpha()) == "me":
        if itsme:
            slap_msg = ("Sorry, {}, but I can't bring myself to "
                        "slap you :("
                        .format(s_name))
        elif has_my_name:
            slap_msg = slap_msg[:-1] + " AND asking me to slap you."
        else:
            slap_msg = ("I slapped {} with a {} at their request."
                        .format(s_name, random.choice(slap_items)))

    elif "myself" in target.lower():
        if itsme:
            slap_msg = ("Sorry, {}, but I can't let you slap yourself :("
                        .format(s_name))
        elif has_my_name:
            slap_msg = slap_msg[:-1] + " AND wanted to slap yourself."
        else:
            slap_msg = ("{} slapped themself with a {}."
                        .format(s_name, random.choice(slap_items)))

    elif me.display_name.title() in target.title():
        slap_msg = ("You shouldn't include my creator's name in your "
                    "slapping target.")

    else:
        slap_msg = ("{} slapped {} with a {}."
                    .format(s_name, target, random.choice(slap_items)))

    return slap_msg
