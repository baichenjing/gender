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
                male_confidence += 1 - proba
            elif gender == 'male':
                mvote += 1 + int(is_clf_page) * 0.1
                male_confidence += proba
            else:
                continue

        if male_confidence == 0.5:
            return 'UNKNOWN', 0.5

        male_confidence = round(male_confidence / int(fvote + mvote), 2)
        if male_confidence < 0.5:
            return 'female', 1 - male_confidence

        return 'male', male_confidence
