'''
Database communication object for all of the trophies ever sent
'''
from copy import deepcopy

from src.main.datastore.trophy_class import Trophy
from src.main.db_session import DatabaseSession

SENDER_ID = "sender_id"
RECIPIENT_ID = "recipient_id"
REASON = "reason"
CREATION_TIMESTAMP = "creation_timestamp"

class TrophyDAO():
    db_string = None
    session = None
    Session = None
    engine = None

    def __init__(self):
        pass

    def insert(self, trophy_info):
        session = DatabaseSession().session

        trophy = Trophy(
            sender_id=trophy_info[SENDER_ID],
            recipient_id = trophy_info[RECIPIENT_ID],
            reason = trophy_info[REASON]
        )

        session.add(trophy)
        session.commit()

    '''
    Simply and obviously fetches every single trophy in the entire table
    '''
    def getAll(self):
        session = DatabaseSession.session
        return self.__convert_all__(session.query(Trophy).all())

    def getByRecipient(self, recipient_id):
        session = DatabaseSession.session
        return self.__convert_all__(session.query(Trophy)
                                    .filter(Trophy.recipient_id == recipient_id))

    '''
        Converts the database object into a Dictionary, so that the database object is not passed out of the
        datastore layer.
    '''
    def __convert_all__(self, trophies):
        converted_trophies = []
        for trophy in trophies:
            trophy_dict = {}
            for column in trophy.__dict__:
                trophy_dict[column] = str(getattr(trophy, column))

            converted_trophies.append(deepcopy(trophy_dict))

        return converted_trophies