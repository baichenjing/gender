from classifier.clf_vote import ClfVote
from classifier.clf_name import ClfName
from classifier.clf_page import ClfPage
from classifier.clf_face import ClfFace
from classifier.database import Database

RECENT_DB = Database('recent')


def is_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def predict_gender(person):
    clfs = [
        ClfPage,
        ClfName,
        ClfFace,
        ClfVote,
    ]
    clf2ans = dict(zip(
        [c.name for c in clfs],
        [{'gender': 'UNKNOWN', 'probability': 'None'}] * len(clfs)
    ))

    if is_chinese(person['name']):
        return clf2ans

    try:
        person['name'] = person['name'].lower()
        person['affiliation'] = person['affiliation'].lower()
    except Exception:
        pass

    person['dbkey'] = '{}*:*{}'.format(person['name'], person['affiliation'])
    person['clf2ans'] = {}
    for clf in clfs:
        gender, proba = clf.predict_person(person)
        clf2ans[clf.name] = {
            'gender': gender,
            'probability': '{:.2f}%'.format(proba)
        }
        if isinstance(clf, ClfVote):
            male_proba = proba if gender == 'male' else 100 - proba
            clf2ans[clf.name]['m_proba'] = '{:.2f}%'.format(male_proba)
            clf2ans[clf.name]['f_proba'] = '{:.2f}%'.format(100 - male_proba)
        person['clf2ans'][clf.name] = (gender, proba)

    RECENT_DB.put(person['dbkey'], clf2ans)

    return clf2ans
