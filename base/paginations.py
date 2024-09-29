from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings
from collections import OrderedDict, namedtuple
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 100  # Number of items per page
    page_size_query_param = 'page_size'  # The query parameter to specify the page size (e.g., ?page_size=20)
    max_page_size = 1000  # Maximum page size allowed
    page_query_param="page"

    def get_paginated_response(self, data,other_dic={}):
        page_no=1
        try:
            page_no=self.request.GET[self.page_query_param]
        except:
            page_no=1
        res=[
            ('page_no',page_no),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]
        dic=OrderedDict(res)
        dic.update(other_dic)
        return Response(dic)
