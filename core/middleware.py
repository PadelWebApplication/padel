import threading

_thread_locals = threading.local()


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            _thread_locals.user_id = request.user.id
        else:
            _thread_locals.user_id = None
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_user_id():
        return getattr(_thread_locals, 'user_id', None)
