import time
import sys, os
from datetime import datetime

from utils import *
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from barlapy.question import Question

db = connect_to_db()

questions = db['questions']

search_query = {"type": "written", "status": "unanswered"}
unanswered_questions = questions.find(search_query).sort([("date", 1)])

print("Found: %d documents" % questions.count_documents(search_query))

start = time.time()

for q in unanswered_questions:
    new_q = Question.from_url(q['url'])

    if new_q.status == 'answered':
        update_ts = datetime.now().isoformat()

        query = {"url": q['url'], "_id": q['_id']} # double security
        new_val = {"$set": {"status": "answered", "updated_at": update_ts}}
        res = questions.update_one(query, new_val)

        print("Modified: %d, id: %d" % (res.modified_count, res.upserted_id))

end = time.time()
print("Elapsed: %d seconds" % (end - start))
