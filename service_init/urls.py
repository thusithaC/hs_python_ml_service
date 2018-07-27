from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import base_view.views
import transaction_service.learning

# Examples:
# url(r'^$', 'service_init.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', base_view.views.index, name='index'),
    path('admin/', admin.site.urls),
    path('services/', transaction_service.learning.test),
    path('services/transactions', transaction_service.learning.transactions)
]
