import string

def normalize_text_quinettoieuntextepminuscules_suppressionponctuationq(text: str) -> str:
    if text is None:
        return ''
    s = text.lower()
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = ' '.join(s.split())
    return s

class VoteSystem:
    def __init__(self):
        self._candidates = {}

    def add_candidate(self, name: str):
        if name not in self._candidates:
            self._candidates[name] = 0

    def vote(self, name: str):
        if name not in self._candidates:
            raise ValueError('Unknown candidate')
        self._candidates[name] += 1

    def counts(self):
        return dict(self._candidates)

    def winner(self):
        if not self._candidates:
            return None
        return max(self._candidates.items(), key=lambda kv: kv[1])[0]
