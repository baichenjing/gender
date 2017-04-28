from classifier.clf_page import ClfPage


class ClfVote:
    name = 'Final'

    @classmethod
    def predict_person(cls, person):
        fvote = 0
        mvote = 0
        confidence = 0.0
        for cname, prediction in person['clf2ans'].items():
            gender, proba = prediction
            is_clf_page = cname == ClfPage.name
            if gender == 'female':
                fvote += 1 + int(is_clf_page) * 0.1
                confidence += proba
            elif gender == 'male':
                mvote += 1 + int(is_clf_page) * 0.1
                confidence += proba
            else:
                continue
        if fvote == mvote:
            return 'UNKNOWN', 50.0
        confidence = round(confidence / int(fvote + mvote), 2)
        if fvote > mvote:
            return 'female', confidence
        return 'male', confidence
