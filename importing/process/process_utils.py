from decouple import config
from pusher import Pusher


"""
Pusher for socket during import process 
"""

pusher_client = Pusher(
  app_id=config(u'PUSHER_APP_ID'),
  key=config(u'PUSHER_KEY'),
  secret=config(u'PUSHER_SECRET'),
  cluster=config(u'PUSHER_CLUSTER')
)

pusher_event_name = 'import_process'
pusher_error_event_name = 'import_error'


def pusher_trigger(task_id, event, payload):
    pusher_client.trigger(task_id, event, payload)