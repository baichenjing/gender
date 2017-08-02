from classifier.clf_vote import ClfVote
from classifier.clf_name import ClfName
from classifier.clf_page import ClfPage
from classifier.clf_face import ClfFace


def is_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def predict_gender(person):
    '''
    Arguments:
        person {dict} -- person info dict, including 'name' and 'affiliation'

    Returns:
        clf2ans {dict} -- key: classifier name; value: (gender, probability)
    '''
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

    person['clf2ans'] = {}
    for clf in clfs:
        gender, proba = clf.predict_person(person)
        clf2ans[clf.name] = {
            'gender': gender,
            'probability': proba
        }
        if isinstance(clf, ClfVote):
            male_proba = proba if gender == 'male' else 1 - proba
            clf2ans[clf.name]['m_proba'] = male_proba
            clf2ans[clf.name]['f_proba'] = 1 - male_proba
        person['clf2ans'][clf.name] = (gender, proba)

    return clf2ans


if __name__ == '__main__':
    person = {
        'name': 'Juanzi Li',
        'affiliation': 'Tsinghua'
    }

    from pprint import pprint
    pprint(predict_gender(person))
