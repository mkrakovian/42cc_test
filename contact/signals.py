from django.dispatch import Signal

# Is sent after the model's instance is saved: if the instance is newly created (action='created'), if any of instance's
# fields was changed(action='changed')
insert_log = Signal(providing_args=["object_name", "action", "timestamp"])
