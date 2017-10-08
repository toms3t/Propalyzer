from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Property


class PropertyAdminTest(TestCase):
    def test_access_property_admin_should_be_accessibel(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        url = '/admin/propalyzer_app/property/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
