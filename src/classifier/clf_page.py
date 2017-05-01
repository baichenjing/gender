import pickle
import gopage.parser
import gopage.crawler
from classifier.database import Database
from os.path import join, dirname


def get_words(content):
    import re
    r = re.compile(r'[a-zA-Z]+|\.\.\.')
    words = re.findall(r, content)
    return [str(word.lower()) for word in words]


class Gpage:
    def __init__(self, person):
        self.person = person
        self.snippets = []

    def get_snippets(self):
        try:
            query = '{} {} his OR her'.format(self.person['name'], self.person['affiliation'])
            gpage = gopage.crawler.search(query, useproxy=False)
            if not gpage:
                return None
            self.snippets = gopage.parser.parse(gpage)
        except Exception:
            return None

    def get_features(self):
        self.get_snippets()
        if not self.snippets or len(self.snippets) == 0:
            return None

        tfHis = 0
        tfHer = 0
        dfHis = 0
        dfHer = 0

        isNameInHisTitle = False
        isNameInHerTitle = False
        words_name = get_words(self.person['name'])

        topThreeSnippets = []
        for pos, snippet in enumerate(self.snippets):
            snippet['name'] = self.person['name'].lower()
            snippet['pos'] = pos + 1

            words_title = get_words(snippet['title'])
            words_content = get_words(snippet['content'])

            if pos < 3:
                topThreeSnippets.extend(words_content)

            numHis = words_content.count('his')
            numHer = words_content.count('her')
            hasHis = numHis > 0
            hasHer = numHer > 0

            if numHis > 0 and isNameInHisTitle is False:
                if words_name[0] in words_title:
                    isNameInHisTitle = True
            if numHer > 0 and isNameInHerTitle is False:
                if words_name[0] in words_title:
                    isNameInHerTitle = True

            tfHis += numHis
            tfHer += numHer

            dfHis += int(hasHis)
            dfHer += int(hasHer)
        totnum = tfHis + tfHer

        if totnum != 0:
            tfHis /= float(totnum)
            tfHer /= float(totnum)
        else:
            tfHis = 0
            tfHer = 0

        numSnippets = len(self.snippets)
        if numSnippets > 0:
            dfHis /= float(numSnippets)
            dfHer /= float(numSnippets)
        else:
            dfHis = 0
            dfHer = 0

        isHisInFirstSnippet = 'his' in topThreeSnippets
        isHerInFirstSnippet = 'her' in topThreeSnippets

        return [
            tfHis, tfHer, dfHis, dfHer,
            int(isHisInFirstSnippet), int(isHerInFirstSnippet),
            int(isNameInHisTitle), int(isNameInHerTitle)
        ]


class ClfPage:
    name = 'WebGP'
    model = None
    threshold = 0.59
    database = Database(name)

    model_file = open(join(dirname(__file__), 'model_page.pk'), 'rb')
    model = pickle.load(model_file, encoding='latin1')
    model_file.close()

    @classmethod
    def predict_person(cls, person):
        dbresult = cls.database.get(person['dbkey'])
        if dbresult is not None:
            return dbresult

        gender, proba = 'UNKNOWN', 'None'
        gpage = Gpage(person)
        features = gpage.get_features()
        if features is None:
            return gender, proba

        mproba = cls.model.predict_proba([features])[0][1]
        fproba = 1 - mproba
        if mproba > cls.threshold:
            gender, proba = 'male', round(mproba, 4) * 100
        else:
            gender, proba = 'female', round(fproba, 4) * 100

        cls.database.put(person['dbkey'], [gender, proba])
        return gender, proba
