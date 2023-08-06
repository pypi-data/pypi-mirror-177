from typing import Dict


class AI21Object:

    def __init__(self, dictionary: Dict):
        self.values = dictionary
        for k, v in dictionary.items():
            if isinstance(v, dict):
                setattr(self, k, AI21Object(v))
            elif isinstance(v, list):
                setattr(self, k, [AI21Object(i) for i in v])
            else:
                setattr(self, k, v)

    def __repr__(self):
        return str(self.values)

    def __getitem__(self, item):
        return getattr(self, item)

