from django.core.management.base import NoArgsCommand, CommandError
from django.db.models import get_models


class Command(NoArgsCommand):
    help = "Prints out project's models & corresponding object count"

    def log(self, msg):
        self.stdout.write(msg)
        self.stderr.write(msg)

    def handle_noargs(self, **options):
        models = get_models(include_auto_created=True)
        if not models:
            raise CommandError("No models created yet")
        self.stderr.write("error:")
        for model in models:
            self.log("Model %s with %i object(s)." % (
                model._meta.model_name.capitalize(),
                model._default_manager.count())
            )