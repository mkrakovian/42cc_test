from contact.models import Request


class RequestSaveMiddleware(object):
    def process_request(self, request):

        Request.objects.create(
            path=request.path, method=request.method,
            encoding=request.META.get('HTTP_ACCEPT_ENCODING', 'N/A'),
            user_agent=request.META.get('HTTP_USER_AGENT', 'N/A'),
            ip=request.META.get('REMOTE_ADDR', 'N/A')
        )

