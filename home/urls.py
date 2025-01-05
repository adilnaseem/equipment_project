from django.urls import path, include
from . import views
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
router = DefaultRouter()
router.register('equipment', views.ItemViewSet)
router.register('employees', views.EmployeeViewSet,basename='employees')
router.register('eqpttype',views.EqptTypeViewSet)
handler403 = 'home.views.custom_permission_denied_view'
# urlpatterns
urlpatterns = [
    path('send-email/', views.send_test_email, name='send-email'),
    path('',views.home, name='home'),
    path('eqp/',views.eqp, name='eqp'),
    path('eqp/details/<int:id>',views.eqp_details,name='details'),
    path('eqp/details/<int:id>/edit/', views.equipment_update, name='equipment_update'),
    path('eqp/<int:id>/delete/', views.equipment_delete, name='equipment_delete'),
    path('staff/',views.staff,name='staff'),
    path('stafform/',views.staff_form,name='staff_form'),
    path('airportform/',views.airport_form,name='airport_form'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    # path('eqptform/',views.eptFormView,name='eqptform'),
    path('eqptform/',views.data_entry_view,name='eqptdata'),
    path('repairs/',views.repairs,name='repairs'),
    path('form_repairs/',views.repair_form,name='formrepairs'),
    
    path('search/', views.search_view, name='search_view'),
    path('search/results/', views.search_results_view, name='search_results_view'),
    path('api/',include(router.urls)),
    # path('apipost/',views..apiPost,name = 'apipost'),
    path('hello/', TemplateView.as_view(template_name='employees.html')),
    path('hello-webpack/', TemplateView.as_view(template_name='hello_webpack.html')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI:
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('logs/', views.log_list, name='log_list'),
]+ debug_toolbar_urls()