from classifier.clf_vote import ClfVote
from classifier.clf_name import ClfName
from classifier.clf_page import ClfPage


def is_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def predict_gender(person):
    clfs = [
        ClfPage,
        ClfName,
        ClfVote,
    ]
    clf2ans = dict(zip(
        [c.name for c in clfs],
        [{'gender': 'UNKNOWN', 'probability': 'None'}] * len(clfs)
    ))

    if is_chinese(person['name']):
        return clf2ans

    person['clf2ans'] = {}
    for clf in clfs:
        gender, proba = clf.predict_person(person)
        clf2ans[clf.name] = {
            'gender': gender,
            'probability': '{}%'.format(proba)
        }
        if isinstance(clf, ClfVote):
            male_proba = proba if gender == 'male' else 100 - proba
            clf2ans[clf.name]['m_proba'] = '{}%'.format(male_proba)
            clf2ans[clf.name]['f_proba'] = '{}%'.format(100 - male_proba)
        person['clf2ans'][clf.name] = (gender, proba)

    return clf2ans
