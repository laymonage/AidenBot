'''
Ticket helper module
(c) 2018 - laymonage
'''

import os
from .dropson import dbx_dl, dbx_ul, toJSON, getJSON

# Path to tickets file in Dropbox
tickets_path = os.getenv('TICKETS_FILE_PATH', None)


def about():
    '''
    Return about message retrieved from Dropbox.
    '''
    about_file = os.getenv('ABOUT_FILE_PATH', None)
    return dbx_dl(about_file).decode('utf-8').strip()


def ticket_add(item, trim=True):
    '''
    Add a ticket.
    item (str): item to be added to the ticket list
    trim (bool): if true, prevent ticket list from exceeding 2000 chars
    '''
    tickets = getJSON(dbx_dl(tickets_path))
    if item in tickets:
        return "Ticket already exists."
    if len('num. \n'.join(tickets + [item])) > 2000 and trim:
        return ("There are currently too many tickets.\n"
                "Please wait until the developer deletes "
                "some of them.")
    tickets.append(item)
    dbx_ul(toJSON(tickets), tickets_path, overwrite=True)
    return "Ticket sent!"


def ticket_get(allowed=True):
    '''
    Return current tickets.
    allowed (bool): if False, return None
    '''
    tickets = getJSON(dbx_dl(tickets_path))
    if not tickets:
        return "No tickets."
    current_tickets = "Tickets:"
    for num, items in enumerate(tickets):
        current_tickets += "\n{}. {}".format(num+1, items)
    return current_tickets if allowed else None


def ticket_rem(num):
    '''
    Remove an item from the ticket list.
    num (int or str): remove the num-th item in the ticket list
    if num == 'all', then all items in the ticket list will be removed
    '''
    tickets = getJSON(dbx_dl(tickets_path))
    if not tickets:
        return "No tickets."
    if num == 'all':
        del tickets[:]
        dbx_ul(toJSON(tickets), tickets_path, overwrite=True)
        return "Ticket list has been emptied."
    try:
        num = int(num)
        del tickets[num-1]
    except IndexError:
        return "Ticket [{}] is not available.".format(num)
    except ValueError:
        return "Wrong format."
    else:
        dbx_ul(toJSON(tickets), tickets_path, overwrite=True)
        return "Ticket [{}] has been removed.".format(num)
