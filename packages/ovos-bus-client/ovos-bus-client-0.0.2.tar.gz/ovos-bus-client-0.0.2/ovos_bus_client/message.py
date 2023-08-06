import re
from mycroft_bus_client.message import Message as _MycroftMessage,  dig_for_message, CollectionMessage
from ovos_utils.log import LOG

try:
    from lingua_franca.parse import normalize
except ImportError:
    # optional LF import
    def normalize(text, *args, **kwargs):
        return text


class Message(_MycroftMessage):
    """Mycroft specific Message class."""

    def utterance_remainder(self):
        """
        DEPRECATED - mycroft-core hack, used by some skills in the wild

        For intents get the portion not consumed by Adapt.

        For example: if they say 'Turn on the family room light' and there are
        entity matches for "turn on" and "light", then it will leave behind
        " the family room " which is then normalized to "family room".

        Returns:
            str: Leftover words or None if not an utterance.
        """
        LOG.warning("Messagw.utterance_remainder has been deprecated!")
        utt = normalize(self.data.get("utterance", ""))
        if utt and "__tags__" in self.data:
            for token in self.data["__tags__"]:
                # Substitute only whole words matching the token
                utt = re.sub(r'\b' + token.get("key", "") + r"\b", "", utt)
        return normalize(utt)
