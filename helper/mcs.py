'''
Magic Conch Shell helper module.
(c) 2018 - laymonage
'''

import random


def ask(question, id_=False):
    '''
    Return something a magic conch shell would say.
    question (str): any question
    id_ (bool): if true, use Indonesian
    '''
    kka = ["Ya.", "Tidak."]
    mcs = ["Yes.", "No."]

    if "Akan" in question.title():
        kka.append("Mungkin suatu hari.")
    elif "Will " in question.title():
        mcs.append("Maybe someday.")

    if ("Belum" in question.title() or
            "Sudah" in question.title() or
            "Belom" in question.title() or
            "Udah" in question.title() or
            "Udeh" in question.title()):
        kka.remove("Ya.")
        kka.remove("Tidak.")
        kka.append("Sudah.")
        kka.append("Belum.")

    if id_:
        result = random.choice(kka)
    else:
        result = random.choice(mcs)

    if "jawab" in question.lower() and "lain" in question.lower():
        result = "Coba tanya lagi."
    if (("say" in question.lower() or
         "answer" in question.lower() or
         "reply" in question.lower()) and
            ("thing else" in question.lower() or
             "other than" in question.lower())):
        result = "Try asking again."

    return result
