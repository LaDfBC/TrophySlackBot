from src.main.datastore.trophy_dao import TrophyDAO, SENDER_ID, RECIPIENT_ID, REASON

'''
    Processes messages about giving trophies, adds to database, and returns with the proper message
'''
class TrophyRunner:
    def __init__(self, sender, channel, message_text):
        self.message = message_text
        self.sender = sender
        self.channel = channel

        self.trophy_dao = TrophyDAO()

    def process_message(self, web_client):
        trophy_row = {}
        trophy_row[SENDER_ID] = self.sender

        message_pieces = self.message.split(' ')
        if len(message_pieces) == 2:
            trophy_row[RECIPIENT_ID] = message_pieces[1]
            self.trophy_dao.insert(trophy_row)
            self.respond_on_slack(self.success_message(), web_client)
        elif len(message_pieces) == 3:
            trophy_row[RECIPIENT_ID] = message_pieces[1]
            trophy_row[REASON] = message_pieces[2]
            self.trophy_dao.insert(trophy_row)
            self.respond_on_slack(self.success_message(), web_client)
        else:
            self.respond_on_slack(self.failure_message(), web_client)

    def respond_on_slack(self, message_to_send, web_client):
        # Post the onboarding message in Slack
        response = web_client.chat_postMessage(**message_to_send)

    def failure_message(self):
        return {
            # "ts": self.timestamp,
            "channel": self.channel,
            "username": self.sender,
            # "icon_emoji": self.icon_emoji,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Improper format! Use !trophy <user> <reason>"
                        ),
                    },
                }
            ],
        }

    def success_message(self):
        return {
            # "ts": self.timestamp,
            "channel": self.channel,
            "username": self.sender,
            # "icon_emoji": self.icon_emoji,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Successfully added trophy!"
                        ),
                    },
                }
            ],
        }
