import sys, os
from datetime import datetime

from utils import *
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from barlapy.question import Question

db = connect_to_db()

questions = db['questions']
unanswered_questions = questions.find({"type": "written", "status": "unanswered"}).sort([("date", 1)])

i = 0

for q in unanswered_questions:
    new_q = Question.from_url(q['url'])

    if new_q.status == 'answered':
        update_ts = datetime.now().isoformat()

        query = {"url": q['url'], "_id": q['_id']} # double security
        new_val = {"$set": {"status": "answered", "updated_at": update_ts}}
        res = questions.update_one(query, new_val)

        print("Modified: %d, id: %d" % (res.modified_count, res.upserted_id)
