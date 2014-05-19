from django.db import models


class Person(models.Model):
    name = models.CharField('Name', max_length=30)
    surname = models.CharField('Last Name', max_length=30)
    birth = models.DateField('Date of Birth')
    bio = models.TextField('Biography')
    skype = models.CharField('Skype ID', max_length=15)
    jabber = models.EmailField('Jabber ID')
    email = models.EmailField('Email address')
    contacts = models.TextField('Other contacts')

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)
