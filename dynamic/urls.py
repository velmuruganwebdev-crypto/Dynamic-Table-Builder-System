from django.urls import path
from .views import *

urlpatterns = [

    path('',dynamic_table, name='dynamic_table'),
    path('showtables/',showtables, name ='showtables'),
    path('insert_values/<str:table_name>/', dynamic_insert, name='dynamic_insert'),
    path('insert/<str:table_name>/', values_get, name='values_get'),
    path('tabledetails/',tabledetails, name='tabledetails'),
    path('drop_table/<str:table_name>/',drop_table,name='drop_table'),
    path('view_fields/<str:table_name>/',view_fields,name='view_fields'),
    path('values_delete/<str:table_name>/<int:id>/', values_delete, name='values_delete'),
    path('values_update/<str:table_name>/<int:id>/',values_update,name='values_update'),
    # path('csv_upload/<str:table_name>/', csv_upload, name='csv_uploadt'),
    # path('upload/', upload_csv, name='upload_csv'),
    path('insert_values/<str:table_name>/upload_file/',upload_file,name='upload_file')
]

