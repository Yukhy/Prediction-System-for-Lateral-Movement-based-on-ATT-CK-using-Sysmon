from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class noCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'private, no-store, no-cache, must-revalidate, no-transform'
        return response