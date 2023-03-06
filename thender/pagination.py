from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):

    page_query_param = "p"
    page_size = 10
    max_page_size = 25
    page_size_query_param = "s"
