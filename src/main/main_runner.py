import os
import ssl as ssl_lib

import certifi
import slack

# Creates and sends the simplest of messages back to the user
from src.main.trophy_runner import TrophyRunner


def send_hello_world(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    hw_class = HelloWorld()

    # Get the onboarding message payload
    # message = onboarding_tutorial.get_message_payload()
    message = hw_class.get_message_payload(channel, user_id)

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

# Class used as a wrapper for the message creation
class HelloWorld:
    def get_message_payload(self, channel, username):
        return {
            # "ts": self.timestamp,
            "channel": channel,
            "username": username,
            # "icon_emoji": self.icon_emoji,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Hey World!"
                        ),
                    },
                }
            ],
        }


# Slack's Real Time Messaging client used to respond to messages and kick back a response
@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    if text and text.lower() == "start":
        return send_hello_world(web_client, user_id, channel_id)

    if text.startswith("!trophy"):
        runner = TrophyRunner(user_id, channel_id, text)
        return runner.process_message(web_client)

# int main() if you will.  Or public static void main(String[] args) if you really like typing
if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()