import bs4
import time
import json
import requests
import base64
import gopage.util
import gopage.crawler
from os.path import dirname, join


class GIParser:
    @staticmethod
    def get_image_id(html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        name = soup.find('img', class_='rg_ic rg_i').attrs['name']
        name = name.replace(':', '')
        return name

    @staticmethod
    def get_base64_with_id(image_id, html):
        start = html.index('var data=')
        file_html = html[start:].replace('\n', '')
        end = file_html.index('];')
        file_html = file_html[:end + 1]
        file_html = file_html.replace('var data=', '')
        imgs = json.loads(file_html)[0]
        id2base64 = {}
        for iid, content in imgs:
            iid = iid.replace(':', '')
            itype = content[content.find('/') + 1: content.find(';')]
            base64_string = content[content.find(',') + 1:]
            base64_string = base64_string.replace('\\u003d', '=')
            id2base64[iid] = {
                'base64': base64_string,
                'type': itype
            }
        return id2base64.get(image_id)


class ClfFace:
    name = 'FR'
    API_KEY = 't45w4oezhIu3MTxy89-9xFW9XN2uoXnH'
    API_SECRET = 'vYnF72umd6O20m0m8G-i44mlzamY88bG'

    @classmethod
    def get_image(cls, person):
        query = '{} {}'.format(person['name'], person['affiliation'])
        image_html = gopage.crawler.search(query, stype='image')
        if image_html is None:
            return None
        image_id = GIParser.get_image_id(image_html)
        base64_info = GIParser.get_base64_with_id(image_id, image_html)
        image_type = base64_info['type']
        image_base64 = base64_info['base64']

        with open('image.{}'.format(image_type), 'wb') as fh:
            fh.write(base64.decodestring(image_base64.encode('utf-8')))
        return image_base64

    @classmethod
    def face_detect_url(cls, image_base64, retry=2):
        if retry < 1:
            return []
        try:
            url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
            data = {
                "api_key": "t45w4oezhIu3MTxy89-9xFW9XN2uoXnH",
                "api_secret": "vYnF72umd6O20m0m8G-i44mlzamY88bG",
                # "image_file": "@{}".format(image_base64),
                "image_base64": image_base64,
                "return_landmark": "1",
                "return_attributes": "gender"
            }
            r = requests.post(url, data=data)
            rdict = r.json()
            if 'error_message' in rdict and rdict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
                print('sleep')
                retry += 1
                time.sleep(2)
            return rdict['faces']
        except Exception as e:
            print(e)
            return cls.face_detect_url(image_base64, retry - 1)

    @classmethod
    def predict_person(cls, person):
        gender = 'UNKNOWN'
        confidence = 50.0
        image_path = cls.get_image(person)
        if image_path is not None:
            faces = cls.face_detect_url(image_path)
            if len(faces) < 1:
                print('No Face')
                return 'UNKNOWN', confidence
            face = faces[0]
            if 'attributes' in face.keys():
                attr = face['attributes']
                if 'gender' in attr.keys():
                    gender = attr['gender']['value']
                    confidence = 100.0
        if gender == 'Male':
            gender = 'male'
            confidence = round(confidence, 2)
        elif gender == 'Female':
            gender = 'female'
            confidence = round(confidence, 2)
        else:
            gender = 'UNKNOWN'
        return gender, confidence
