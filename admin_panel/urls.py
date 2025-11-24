from django.urls import path
from admin_panel import views

urlpatterns=[
    path('index_page/',views.index_page,name="index_page"),
    path('add_service_category/',views.add_service_category,name="add_service_category"),
    path('save_category/',views.save_category,name="save_category"),
    path('display_service_category/',views.display_service_category,name="display_service_category"),
    path('display_service_category/',views.display_service_category,name="display_service_category"),
    path('edit_service_category/<int:c_id>/',views.edit_service_category,name="edit_service_category"),
    path('update_service_category/<int:c_id>/',views.update_service_category,name="update_service_category"),
    path('delete_service_category/<int:c_id>/',views.delete_service_category,name="delete_service_category"),
    path('admin_login_page/',views.admin_login_page,name="admin_login_page"),
    path('admin_login/',views.admin_login,name="admin_login"),
    path('admin_logout/',views.admin_logout,name="admin_logout"),
    path('display_donors/',views.display_donors,name="display_donors"),
    path('delete_donors/<int:d_id>/',views.delete_donors,name="delete_donors"),
]