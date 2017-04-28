import pickle
import gopage.parser
import gopage.crawler
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
        query = '{} his OR her'.format(self.person['name'])
        gpage = gopage.crawler.search(query, useproxy=False)
        self.snippets = gopage.parser.parse(gpage)

    def get_features(self):
        self.get_snippets()
        if len(self.snippets) == 0 or self.snippets is None:
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

    model_file = open(join(dirname(__file__), 'model_page.pk'), 'rb')
    model = pickle.load(model_file, encoding='latin1')
    model_file.close()

    @classmethod
    def predict_person(cls, person):
        gender, label = 'UNKNOWN', 'None'
        gpage = Gpage(person)
        features = gpage.get_features()
        if features is None:
            return gender, label
        mproba = cls.model.predict_proba([features])[0][1]
        fproba = 1 - mproba
        if mproba > cls.threshold:
            return 'male', round(mproba, 4) * 100
        return 'female', round(fproba, 4) * 100
