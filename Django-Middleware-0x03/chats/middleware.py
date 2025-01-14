from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
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
    
class OffensiveLanguageMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = {}
        self.time_window = timedelta(minutes=1)
        self.message_limit = 5

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            current_time = datetime.now()

            if ip not in self.message_counts:
                self.message_counts[ip] = []

            # Remove messages outside the time window
            self.message_counts[ip] = [timestamp for timestamp in self.message_counts[ip] if current_time - timestamp < self.time_window]

            if len(self.message_counts[ip]) >= self.message_limit:
                return HttpResponseForbidden("You have exceeded the message limit. Please wait before sending more messages.")

            self.message_counts[ip].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated or not (user.is_staff or user.is_superuser):
            return HttpResponseForbidden("You do not have permission to perform this action.")
        
        response = self.get_response(request)
        return response