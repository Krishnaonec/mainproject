from django.urls import path
from . import views 

urlpatterns = [ 
    path('oauth/', views.oauth, name = 'oauth'),
    path('contact_owner/<int:owner_id>', views.contact_owner, name='contact_owner'),
    path('create_userowner_space/<int:owner_id>', views.create_userowner_space, name='create_userowner_space'),
    path('delete_space/', views.delete_space, name= 'delete_space'),
    path('my_spaces/', views.my_spaces, name= 'my_spaces'),
    path('visit_space/', views.visit_space, name= 'visit_space'),
]