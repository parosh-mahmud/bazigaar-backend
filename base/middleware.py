from django.utils.deprecation import MiddlewareMixin
import json
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from django.http import QueryDict

class UserAchivementMiddleware(MiddlewareMixin):
    def __call__(self, request:HttpRequest):
        path=request.path
        method=request.method
        
        response:Response = self.get_response(request)
        
        return response