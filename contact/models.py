from django.db import models
from contact.signals import insert_log
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.db.models import get_models, get_app
from django.utils import timezone


class BaseLogModel(models.Model):
    def save(self, *args, **kwargs):
        model = self._meta.model
        changed = False
        new = False
        try:
            other = model._default_manager.get(pk=self.pk)
            for field in other._meta.fields:
                if getattr(other, field.name) != getattr(self, field.name):
                    changed = True
                    break
        except:
            new = True
        super(BaseLogModel, self).save(*args, **kwargs)
        if not changed and new:
            insert_log.send(sender=self.__class__, object_name=str(self), action='created', timestamp=timezone.now())
        elif changed:
            insert_log.send(sender=self.__class__, object_name=str(self), action='changed', timestamp=timezone.now())

    class Meta:
        abstract = True


class Person(BaseLogModel):
    name = models.CharField('Name', max_length=30)
    surname = models.CharField('Last Name', max_length=30)
    birth = models.DateField('Date of Birth')
    pic = models.ImageField('photo', upload_to='person', blank=True, null=True)
    bio = models.TextField('Biography')
    skype = models.CharField('Skype ID', max_length=15)
    jabber = models.EmailField('Jabber ID')
    email = models.EmailField('Email address')
    contacts = models.TextField('Other contacts')

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the pic field
        try:
            other = Person.objects.get(pk=self.pk)
            if other.pic != self.pic:
                other.pic.delete(save=False)
        except:
            pass  # when a new photo nothing is done, normal case
        super(Person, self).save(*args, **kwargs)


class Request(BaseLogModel):
    path = models.TextField('path')
    method = models.CharField('method', max_length=15)
    encoding = models.CharField('encoding', max_length=25)
    user_agent = models.TextField("client's user agent")
    ip = models.CharField("client's IP address", max_length=20)

    def __unicode__(self):
        return self.ip


class Log(models.Model):
    object = models.CharField('object name', max_length=150)
    action = models.CharField('action', max_length=10)
    timestamp = models.DateTimeField('date and time')


@receiver([post_delete, insert_log], sender=Person)
def logger(sender, **kwargs):
    if kwargs.get('instance'):
        Log.objects.create(
            object=str(kwargs['instance']),
            action='deleted',
            timestamp=timezone.now()
        )
    else:
        Log.objects.create(
            object=kwargs['object_name'],
            action=kwargs['action'],
            timestamp=kwargs['timestamp']
        )

# The following code helps to register the signal with multiple senders. We are interested in logging only those models,
# which are children of the BaseLogModel.

# for sender in [model for model in get_models(get_app('contact')) if issubclass(model, BaseLogModel)]:
#     insert_log.connect(logger, sender=sender)
#     post_delete.connect(logger, sender=sender)

@receiver(post_delete, sender=Person)
def person_pic_delete(sender, instance, **kwargs):
    instance.pic.delete(False)