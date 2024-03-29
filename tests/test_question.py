import unittest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from barlapy.question import Question

class TestQuestionParsing(unittest.TestCase):
    def setUp(self):
        # sorry this is awful ¯\_(ツ)_/¯
        self.qtext_cases = [
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D9%88%D8%B6%D8%B9%D9%8A%D8%A9-%D9%85%D9%84%D8%B9%D8%A8-%D9%85%D9%88%D9%84%D8%A7%D9%8A-%D8%B9%D8%A8%D8%AF-%D8%A7%D9%84%D9%84%D9%87-%D8%A8%D8%A7%D9%84%D8%B1%D8%A8%D8%A7%D8%B7",
                "text": 'السيد الوزير المحترم،\nفوجئ الرياضيون بالوضعية السيئة التي عليها عشب ملعب مركب مولاي عبد الله بالرباط، و عليه فإننا نسائلكم عن الإجراءات التي ستعتمدونها للتحقيق في هذا الأمر و إعادة هذا الملعب لمستواه العادي حتى يكون صالحا لإجراء مباريات كرة القدم.'
            },
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D8%A5%D9%86%D8%B4%D8%A7%D8%A1-%D8%A8%D9%86%D8%A7%D9%8A%D8%A9-%D8%BA%D9%8A%D8%B1-%D9%82%D8%A7%D9%86%D9%88%D9%86%D9%8A%D8%A9",
                "text": 'أقدم أحد المواطنين على بناء مبنى محادي لأسلاك الربط الكهربائي دون مراعاة المسافة المنصوص عليها في القانون بشكل يهدد حياة الاخرين ، حيث توجد هذه البناية بدوار الحميدشات جماعة المعشات، في الطريق الجهوية رقم 301 ما بين مركز الصويرية القديمة ومركز خميس اولاد الحاج قيادة الصويرية القديمة اقليم آسفي، \nوقد تمت مراسلة الجماعة فيما يخص هذه البناية، كما تم إيفاد لجنة للتعمير تابعة لعمالة اقليم آسفي لتعاين الامر، إلا أن الاشغال لازالت مستمرة ، الامر الذي يبين بالملموس بأن هناك تواطؤا ما بين السلطة المحلية والشخص صاحب البناية. \nلذا نطلب منكم السيد الوزير إيفاد لجنة لمعاينة هذا الخرق؟ وما هي الإجراءات والتدابير التي ستتخذونها في هذا الصدد؟'
            },
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D8%B4%D9%81%D9%88%D9%8A%D8%A9/%D8%A7%D9%84%D8%AA%D9%84%D8%A7%D8%B9%D8%A8-%D8%A8%D8%A7%D9%84%D9%85%D8%A7%D9%84-%D8%A7%D9%84%D8%B9%D8%A7%D9%85-%D9%81%D9%8A-%D8%A7%D9%84%D8%B5%D9%81%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D9%85%D9%88%D9%85%D9%8A%D8%A9-%D8%A7%D9%84%D9%85%D8%B4%D8%A8%D9%88%D9%87%D8%A9-0",
                "text": 'السيد الوزير المحترم،\nإن كراء المرافق العمومية من الملفات التي تشوبها اختلالات خطيرة تفوت على الدولة موارد مالية كبيرة من خلال إجراء صفقات عمومية مشبوهة.\nوفي هذا الإطار نسائلكم السيد الوزير المحترم:\n- كيف يتم التصدي للتلاعب بالمال العام في الصفقات العمومية المشبوهة؟'
            }

        ]

        self.qid_cases = [
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D9%85%D8%A2%D9%84-%D8%AA%D9%88%D9%82%D9%8A%D8%B9-%D8%A7%D8%AA%D9%81%D8%A7%D9%82%D9%8A%D8%A9-%D8%A7%D9%84%D8%B4%D8%B1%D8%A7%D9%83%D8%A9-%D8%A8%D9%8A%D9%86-%D9%85%D8%AC%D9%84%D8%B3-%D8%AC%D9%87%D8%A9-%D8%B7%D9%86%D8%AC%D8%A9-%D8%AA%D8%B7%D9%88%D8%A7%D9%86-%D8%A7%D9%84%D8%AD%D8%B3%D9%8A%D9%85%D8%A9",
                "id": 24401
            },
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D9%88%D8%B6%D8%B9%D9%8A%D8%A9-%D9%85%D8%B1%D8%A8%D9%8A%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85-%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%8A-%D8%A8%D8%B9%D8%AF-%D9%82%D8%B1%D8%A7%D8%B1-%D8%A7%D9%84%D8%A5%D8%B3%D8%AA%D8%BA%D9%86%D8%A7%D8%A1-%D8%B9%D9%86%D9%87%D9%86-%D8%A8%D8%B9%D8%AF-%D8%B3%D9%86%D9%88%D8%A7%D8%AA",
                "id": 1
            }
        ]

        self.qauthors_cases = [
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D9%88%D8%B6%D8%B9%D9%8A%D8%A9-%D9%85%D8%B1%D8%A8%D9%8A%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85-%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%8A-%D8%A8%D8%B9%D8%AF-%D9%82%D8%B1%D8%A7%D8%B1-%D8%A7%D9%84%D8%A5%D8%B3%D8%AA%D8%BA%D9%86%D8%A7%D8%A1-%D8%B9%D9%86%D9%87%D9%86-%D8%A8%D8%B9%D8%AF-%D8%B3%D9%86%D9%88%D8%A7%D8%AA",
                "authors": ["عمر بلافريج"]
            },
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D8%BA%D9%8A%D8%A7%D8%A8-%D8%A7%D9%84%D8%AD%D8%B2%D9%85-%D9%88%D8%A7%D9%84%D8%B5%D8%B1%D8%A7%D9%85%D8%A9-%D9%81%D9%8A-%D8%A7%D9%84%D8%AA%D8%B9%D8%A7%D9%85%D9%84-%D9%85%D8%B9-%D8%A7%D9%84%D8%B1%D8%B9%D8%A7%D8%A9-%D8%A7%D9%84%D8%B1%D8%AD%D9%84-%D8%A8%D8%A5%D9%82%D9%84%D9%8A%D9%85-%D8%A7%D8%B4%D8%AA%D9%88%D9%83%D8%A9",
                "authors": ["الحسين ازوكاغ", "خديجة رضواني"]
            },
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D8%AC-%D8%A5%D8%B3%D9%83%D8%A7%D9%86-%D9%85%D8%AE%D9%8A%D9%85%D8%A7%D8%AA-%D8%A7%D9%84%D9%88%D8%AD%D8%AF%D8%A9-%D8%A8%D8%A7%D9%84%D8%B3%D9%85%D8%A7%D8%B1%D8%A9-0",
                "authors": ["محمود امري", "حياة سكيحيل", "ابراهيم الضعيف", "منينة مودن", "عالي الرزمة"]
            }
        ]

        self.qtype_cases = [
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D8%B7%D9%84%D8%A8-%D8%A5%D9%8A%D9%81%D8%A7%D8%AF-%D9%84%D8%AC%D9%86%D8%A9-%D9%84%D9%84%D8%AA%D8%AD%D9%82%D9%8A%D9%82-%D8%A8%D8%B3%D8%A8%D8%A8-%D9%85%D8%B9%D8%A7%D9%86%D8%A7%D8%A9-%D8%A8%D8%B9%D8%B6-%D8%B3%D8%A7%D9%83%D9%86%D8%A9-%D8%A5%D9%82%D9%84%D9%8A%D9%85-%D8%B5%D9%81%D8%B1%D9%88-%D9%85%D9%86",
                "type": "written"
            },
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D8%B4%D9%81%D9%88%D9%8A%D8%A9/%D9%88%D8%B6%D8%B9%D9%8A%D8%A9-%D8%A3%D8%B1%D8%A8%D8%A7%D8%A8-%D9%88%D9%83%D8%A7%D9%84%D8%A7%D8%AA-%D9%83%D8%B1%D8%A7%D8%A1-%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A8%D8%A7%D9%84%D9%85%D8%BA%D8%B1%D8%A8",
                "type": "oral"
            }
        ]

        self.qdate_cases = [
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D9%85%D8%B9%D8%A7%D9%86%D8%A7%D8%A9-%D8%B7%D9%84%D8%A8%D8%A9-%D8%A7%D9%84%D9%83%D9%84%D9%8A%D8%A9-%D9%85%D8%AA%D8%B9%D8%AF%D8%AF%D8%A9-%D8%A7%D9%84%D8%AA%D8%AE%D8%B5%D8%B5%D8%A7%D8%AA-%D8%A8%D8%A3%D8%B3%D9%81%D9%8A-%D9%85%D8%B9-%D9%85%D8%B5%D9%84%D8%AD%D8%A9-%D8%A7%D9%84%D8%B4%D8%A4%D9%88%D9%86",
                "date": datetime(2017, 7, 7)
            }
        ]

        self.qanswer_parsing_cases = [
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D9%85%D8%B9%D8%A7%D9%86%D8%A7%D8%A9-%D8%B7%D9%84%D8%A8%D8%A9-%D8%A7%D9%84%D9%83%D9%84%D9%8A%D8%A9-%D9%85%D8%AA%D8%B9%D8%AF%D8%AF%D8%A9-%D8%A7%D9%84%D8%AA%D8%AE%D8%B5%D8%B5%D8%A7%D8%AA-%D8%A8%D8%A3%D8%B3%D9%81%D9%8A-%D9%85%D8%B9-%D9%85%D8%B5%D9%84%D8%AD%D8%A9-%D8%A7%D9%84%D8%B4%D8%A4%D9%88%D9%86",
                "answer_url": "https://www.chambredesrepresentants.ma/sites/default/files/reponses_questions_ecrites/rq_1132_0.pdf",
                "date": datetime(2018, 10, 30)
            },

            # Note: the following question is old enough (the oldest unanswered)
            # not to be answered in the future...
            {
                "url": "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D8%B9%D9%85%D9%84%D9%8A%D8%A9-%D8%A7%D9%84%D9%86%D8%B5%D8%A8-%D8%A7%D9%84%D8%AA%D9%8A-%D8%AA%D8%B9%D8%B1%D8%B6-%D9%84%D9%87%D8%A7-%D8%A7%D9%84%D9%85%D8%B3%D8%AC%D9%84%D9%88%D9%86-%D8%A8%D8%AA%D8%AC%D8%B2%D8%A6%D8%A9-%D8%A7%D9%84%D8%B5%D9%81%D8%A7-%D8%A8%D9%85%D8%AF%D9%8A%D9%86%D8%A9-%D8%A3%D8%B3%D9%81%D9%8A",
                "answer_url": "",
                "date": ''
            }
        ]

    def test_text_parsing(self):
        self.maxDiff = None
        for q in self.qtext_cases:
            self.assertEqual(Question.from_url(q['url']).get_text(), q['text'])

    def test_id_parsing(self):
        for q in self.qid_cases:
            self.assertEqual(Question.from_url(q['url']).get_id(), q['id'])

    def test_authors_parsing(self):
        for q in self.qauthors_cases:
            self.assertListEqual(Question.from_url(q['url']).get_authors(), q['authors'])

    def test_question_type_parsing(self):
        for q in self.qtype_cases:
            self.assertEqual(Question.from_url(q['url']).get_type(), q['type'])

    def test_question_date_parsing(self):
        for q in self.qdate_cases:
            self.assertEqual(Question.from_url(q['url']).get_date(), q['date'])

    def test_answer_parsing(self):
        for q in self.qanswer_parsing_cases:
            question = Question.from_url(q['url'])
            self.assertEqual(question.get_answer()['url'], q['answer_url'])
            if q['date'] != '':
                self.assertEqual(question.get_answer()['date'], q['date'])
            else:
                self.assertEqual(question.get_answer()['date'], q['date'])

if __name__ == '__main__':
    unittest.main()

