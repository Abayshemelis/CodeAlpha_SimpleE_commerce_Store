from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views # Needed if you keep individual paths here

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. The fix for your 'social' namespace error
    path('social-auth/', include('social_django.urls', namespace='social')), 
    
    # 2. Your Store App URLs
    path('', include('store.urls')), 

    # NOTE: If these three paths are already inside store/urls.py, 
    # you can delete them from this file to keep it clean:
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.cart_add, name='cart_add'),
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)