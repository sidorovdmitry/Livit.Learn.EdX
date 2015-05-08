from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from labster.tests.views import ViewTestMixin
from labster.tests.factories import VoucherFactory, ProductFactory
from labster_backoffice.models import Voucher


class VoucherListTest(ViewTestMixin, TestCase):

    def setUp(self):
        self.url = reverse('voucher:index')
        User.objects.create_user('username', 'user@email.com', 'password')


class VoucherPostMixin(object):

    def test_post_valid_data(self):

        self.client.login(username='username', password='password')
        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('voucher:index'))

        voucher = Voucher.objects.latest('id')
        if 'id' in self.valid_data:
            self.assertEqual(self.valid_data['id'], voucher.id)
        self.assertEqual(self.valid_data['price'], voucher.price)
        self.assertEqual(self.valid_data['limit'], voucher.limit)
        self.assertEqual(self.valid_data['week_subscription'], voucher.week_subscription)
        self.assertItemsEqual(self.valid_data['products'], [self.product.id])

    def test_post_invalid_data(self):
        self.client.login(username='username', password='password')

        for key in self.valid_data.keys():
            self._test_invalid_data(key, self.valid_data)

    def _test_invalid_data(self, key, data):
        copied_data = data.copy()
        copied_data[key] = ""
        response = self.client.post(self.url, copied_data)
        self.assertEqual(response.status_code, 200)


class VoucherCreateTest(ViewTestMixin, VoucherPostMixin, TestCase):

    def setUp(self):
        self.url = reverse('voucher:create')
        User.objects.create_user('username', 'user@email.com', 'password')

        self.product = ProductFactory()
        self.valid_data = {
            'id': '1234567890',
            'price': 1000,
            'limit': 10,
            'products': [self.product.id],
            'week_subscription': 4,
        }


class VoucherUpdateTest(ViewTestMixin, VoucherPostMixin, TestCase):

    def setUp(self):
        self.voucher = VoucherFactory(id='1234567890')

        self.url = reverse('voucher:update', args=[self.voucher.id])
        User.objects.create_user('username', 'user@email.com', 'password')

        self.product = ProductFactory()
        self.valid_data = {
            'id': '1234567890',
            'price': 1000,
            'limit': 10,
            'products': [self.product.id],
            'week_subscription': 4,
        }


class VoucherDelete(ViewTestMixin, TestCase):

    def setUp(self):
        self.voucher = VoucherFactory(id='1234567890')

        self.url = reverse('voucher:delete', args=[self.voucher.id])
        User.objects.create_user('username', 'user@email.com', 'password')

    def test_post(self):
        self.client.login(username='username', password='password')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('voucher:index'))

        self.assertFalse(Voucher.objects.filter(id='1234567890').exists())
