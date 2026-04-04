

from django.http import HttpRequest


def set_useragent_on_request_middleware(get_responce):
    print("initial call")
    def middleware(request: HttpRequest):
        print("before get responce")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        responce = get_responce(request)
        print("after get responce")

        return responce
    return middleware

class  CountRequestsMiddleware:
    def __init__(self, get_responce):
        self.get_responce = get_responce
        self.requests_count = 0
        self.responces_count = 0
        self.exceptions_count = 0


    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests count", self.requests_count)

        responce = self.get_responce(request)

        print("responces count", self.responces_count)
        self.responces_count += 1

        return responce

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")
