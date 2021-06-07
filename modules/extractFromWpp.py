import re
from nltk.tokenize import sent_tokenize


class Extractor:
    def __init__(self, username) -> None:
        self.sent_messages = []
        self.username = username

    def extract(self) -> list:
        """
        Extracts all messages sent by the person with the username used to initialize the class
        """

        # Open file containing a some long chats involving the user
        with open("compiledWppChats.txt", "r", encoding="UTF-8") as file:
            messages = file.readlines()

        # Define media messages to exclude
        media_messages = [
            "imagem ocultada",
            "áudio ocultado",
            "‎figurinha omitida",
            "‎Ligação de vídeo perdida",
            "‎Ligação de voz perdida",
            "‎vídeo omitido",
            "‎GIF omitido",
        ]

        # Loop through all messages
        for message in messages:
            # Check if the message was sent by the user
            if len(re.findall(self.username, message)) > 0:
                # Clean metadata
                text = re.sub(r"^.*:\s", "", message)
                # Check for media files
                if (
                    text not in media_messages
                    and " ".join(message.split()[-2:]) != "documento omitido"
                ):
                    # Split message in list of sentences
                    sentences = sent_tokenize(message)
                    # Loop through all sentences
                    for sentence in sentences:
                        # Clean metadata
                        text = re.sub(r"^.*:\s", "", message)
                        # Append the sentence
                        self.sent_messages += [text]

        return self.sent_messages
