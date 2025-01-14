from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}"
        with open('requests.log', 'a') as log_file:
            log_file.write(log_message + '\n')
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = datetime.strptime('21:00', '%H:%M').time()
        end_time = datetime.strptime('18:00', '%H:%M').time()

        if current_time >= start_time or current_time <= end_time:
            return HttpResponseForbidden("Access to the messaging app is restricted during these hours.")

        response = self.get_response(request)
        return response