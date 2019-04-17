"""
Slapping module for LINE bots.

(c) 2018 - laymonage
"""

import random


def slap(subject, target, myself):
    """
    Return a message stating "Subject slapped target with a random object.".

    subject: an object returned by LineBotApi.get_profile method
    target (str): slapping target
    me: like subject, but for your own profile
    """
    slap_items = ["frying pan", "baseball bat", "cricket bat", "guitar",
                  "crowbar", "wooden stick", "nightstick", "golf club",
                  "katana", "hand", "laptop", "book", "drawing book",
                  "mouse", "keyboard"]
    s_name = subject.display_name
    itsme = subject.user_id == myself.user_id
    has_my_name = not itsme and myself.display_name.title() in s_name.title()

    def impersonator():
        """Slap the subject if the slap subject's name contains my name."""
        if myself.display_name.lower() == s_name.lower():
            temp_msg = ("IMPERSONATOR! >:(\n"
                        "I slapped you back and forth with a {} "
                        "for impersonating my creator."
                        .format(random.choice(slap_items)))
        else:
            temp_msg = ("NOT FUNNY! >:("
                        "I slapped you back and forth with a {} "
                        "for making fun of my creator."
                        .format(random.choice(slap_items)))
        return temp_msg

    def aiden():
        """Slap the subject if target name contains "Aiden"."""
        if itsme:
            temp_msg = ("{s} gently slapped me.\n"
                        "Sorry, {s} :("
                        .format(s=s_name))
        elif has_my_name:
            temp_msg = slap_msg[:-1] + " AND trying to slap me."
        else:
            temp_msg = ("I slapped {} with a {} for trying to slap me."
                        .format(s_name, random.choice(slap_items)))
        return temp_msg

    def justme():
        """Slap the subject if target name's letters only consist of "me"."""
        if itsme:
            temp_msg = ("Sorry, {}, but I can't bring myself to "
                        "slap you :("
                        .format(s_name))
        elif has_my_name:
            temp_msg = slap_msg[:-1] + " AND asking me to slap you."
        else:
            temp_msg = ("I slapped {} with a {} at their request."
                        .format(s_name, random.choice(slap_items)))
        return temp_msg

    def own():
        """Slap the subject if target name contains "Myself"."""
        if itsme:
            temp_msg = ("Sorry, {}, but I can't let you slap yourself :("
                        .format(s_name))
        elif has_my_name:
            temp_msg = slap_msg[:-1] + " AND wanted to slap yourself."
        else:
            temp_msg = ("{} slapped themself with a {}."
                        .format(s_name, random.choice(slap_items)))
        return temp_msg

    if has_my_name:
        slap_msg = impersonator()
    if "Aiden" in target.title():
        slap_msg = aiden()
    elif ''.join(c for c in target.lower() if c.isalpha()) == "me":
        slap_msg = justme()
    elif "myself" in target.lower():
        slap_msg = own()
    elif myself.display_name.title() in target.title():
        slap_msg = ("You shouldn't include my creator's name in your "
                    "slapping target.")

    else:
        slap_msg = ("{} slapped {} with a {}."
                    .format(s_name, target, random.choice(slap_items)))

    return slap_msg
