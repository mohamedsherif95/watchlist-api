from rest_framework.pagination import PageNumberPagination,CursorPagination

class WatchlistPagination(PageNumberPagination):
       page_size= 5
       max_page_size = 10
       page_size_query_param='size'
      
class WatchlistCursorPagination(CursorPagination):
       page_size= 4
       cursor_query_param='recoed'
       ordering ='-created'
    
