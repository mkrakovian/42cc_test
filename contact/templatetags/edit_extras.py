from django.template import Library, TemplateSyntaxError, Node, Variable, VariableDoesNotExist
from django.core.urlresolvers import reverse

register = Library()


class EditLinkNode(Node):
    def __init__(self, obj_repr):
        self.obj_repr = Variable(obj_repr)

    def render(self, context):
        try:
            obj = self.obj_repr.resolve(context)
            app_label = obj._meta.app_label
            model_name = obj._meta.model_name
            pk = obj.pk
        except VariableDoesNotExist:
            return ''
        except AttributeError:
            raise TemplateSyntaxError("%r object is not editable." % obj)
        return reverse("admin:%s_%s_change" % (app_label, model_name), args=(pk,))


def edit_link(parser, token):
    try:
        tag_name, obj_repr = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires a single argument" % token.split_contents()[0])
    return EditLinkNode(obj_repr)

register.tag(edit_link)
