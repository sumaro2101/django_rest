from rest_framework.pagination import PageNumberPagination

class PaginateCourses(PageNumberPagination):
    """Класс пагинации курсов
    """    
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 30
    

class PaginateLessons(PageNumberPagination):
    """Класс пагинации уроков
    """    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    