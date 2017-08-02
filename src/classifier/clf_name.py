import json
from os.path import join, dirname


class ClfName:
    name = 'Name'
    n2g_file = open(join(dirname(__file__), 'model_name.json'))
    fname2gender = json.load(n2g_file)

    @classmethod
    def get_firstname(self, name):
        try:
            name = name.lower()
        except Exception:
            pass
        return name.split(' ')[0]

    @classmethod
    def predict_person(cls, person):
        try:
            fistname = cls.get_firstname(person['name'])
            gender = cls.fname2gender[fistname]
            return gender, 1
        except KeyError:
            return 'UNKNOWN', 0.5
