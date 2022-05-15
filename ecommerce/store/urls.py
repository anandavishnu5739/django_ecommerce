from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
urlpatterns = [
path('', views.store, name="store"),
path('cart/', views.cart, name="cart"),
path('checkout/', views.checkout, name="checkout"),
path('update_item/', views.updateItem, name="update_item"),
path('process_order/', views.processOrder, name="process_order"),
path('dashboard/', views.dashboard, name="dashboard"),
path('logout/', views.logout_page, name="logout"),
path('settings/', views.settings, name="settings"),
path('navbar/', views.navbar, name="navbar"),
path('view_product/<str:pk_test>/', views.product_view, name="view_product"),
path('add_product/', views.add_products, name="add_product"),
path('login/', views.login, name="login"),


path('product_dashboard/', views.dashboard_product_view, name="product_dashboard"),


path('category/<str:cats>/', views.product_category, name="product_category"),
path('edit_products/<str:edit_products>/', views.edit, name="edit_products"),
path('delete_products/<str:delete_products>/', views.delete, name="delete_products"),
path('delete_category/<str:delete_category>/', views.delete_cat, name="delete_category"),

]
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





    
