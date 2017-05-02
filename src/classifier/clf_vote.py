from classifier.clf_page import ClfPage


class ClfVote:
    name = 'Final'

    @classmethod
    def predict_person(cls, person):
        fvote = 0
        mvote = 0
        male_confidence = 0.0
        for cname, prediction in person['clf2ans'].items():
            gender, proba = prediction
            is_clf_page = cname == ClfPage.name
            if gender == 'female':
                fvote += 1 + int(is_clf_page) * 0.1
                male_confidence += 100 - proba
            elif gender == 'male':
                mvote += 1 + int(is_clf_page) * 0.1
                male_confidence += proba
            else:
                continue
        # if fvote == mvote:
        if male_confidence == 50:
            return 'UNKNOWN', 50.0
        male_confidence = round(male_confidence / int(fvote + mvote), 2)
        # if fvote > mvote:
        if male_confidence < 50:
            return 'female', 100 - male_confidence
        return 'male', male_confidence
