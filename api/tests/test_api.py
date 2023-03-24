from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from .utils import (
 valid_uuid, valid_name, valid_username, 
 valid_url, gen_token_str, valid_token_str,
 pal,
)
from .serializers import (
    PlatformUserSerializer, PlatformSerializer, UserTokenSerializer
)
from .models import (
    PlatformUser, Platform, UserToken
)
import logging

lgr = logging.getLogger(__name__)


class TestUtils(TestCase):
    """ tests for utils.py """
    def test_valid_uuid(self):
        valid = '123e4567-e89b-12d3-a456-426614174000'
        invalid = '123e4567-e89b-12d3-a456-42661417400g'
        short = '123'
        nodash = '123e4567e89b12d3a45642661417400g'
        self.assertTrue(valid_uuid(valid))
        self.assertFalse(valid_uuid(invalid))
        self.assertFalse(valid_uuid(short))
        self.assertFalse(valid_uuid(nodash))

    def test_valid_name(self):
        valid = 'ExampleName'
        invalid = 'Example@Name'
        longname = 'TOOLONG' * 50
        empty = ''
        digits = '123132123123123'
        chars = 'aaaaaaaaaaaa'
        spchars = 'äæ3áa6ãäæ3áa6ã'

        self.assertTrue(valid_name(valid))
        self.assertFalse(valid_name(invalid))
        self.assertFalse(valid_name(longname))
        self.assertFalse(valid_name(empty))
        self.assertTrue(valid_name(digits))

        self.assertFalse(valid_name(spchars))

        self.assertFalse(valid_name(spchars))

    def test_valid_username(self):
        invalids = ['username', 'user@', '@user', '@', ' @ ', '#@', '#@#', 'user name']
        valids = ['u@u', 'username@platform', '1@1', 'u@1']

        for iv in invalids: self.assertFalse(valid_username(iv))
        for i in valids: self.assertTrue(valid_username(i))


    def test_valid_url(self):
        valids = ['https://www.example.com', 'http://google.com', 'google.com']

        invalids = ['htp://example', '//example.com', 'p://example.com',
                   'http://example', 'https://example.', 'http://example./']
        
        for v in valids:
            print(v, valids.index(v))
            self.assertTrue(valid_url(v))

        for iv in invalids:
            self.assertFalse(valid_url(iv))


    def test_ptoken_str(self):
        ptoken = gen_token_str()

        self.assertIsNotNone(ptoken)
        self.assertTrue(ptoken.startswith('fdr-'))
        self.assertEqual(len(ptoken), 47)

        self.assertTrue(valid_token_str(ptoken))

        pal(ptoken + 'l')
        self.assertFalse(valid_token_str(ptoken + 'l'))

        self.assertFalse(valid_token_str(ptoken[1:]))
        self.assertFalse(valid_token_str(ptoken[:-1]))

        badtoken = str(ptoken)
        badtoken[0] = '#'
        self.assertFalse(valid_token_str(badtoken))


class TestModels(TestCase):
    """ tests for models.py """
    def setUp(self):
        self.user = PlatformUser.objects.create_user(
            username='testuser', password='testpassword')
        self.platform_user = PlatformUser.objects.create_user(
            username='testplatformuser', password='testpassword')
        self.platform = Platform.objects.create(name='Test Platform')
        self.user_token = UserToken.objects.create(
            user=self.platform_user, platform=self.platform)

    def test_platform_user_creation(self):
        self.assertIsNotNone(self.platform_user)
        self.assertEqual(self.platform_user.username,
                         'testplatformuser@{}'.format(Platform.get_or_create_host().name))

    def test_platform_creation(self):
        self.assertIsNotNone(self.platform)
        self.assertEqual(self.platform.name, 'Test Platform')

    def test_user_token_creation(self):
        self.assertIsNotNone(self.user_token)
        self.assertEqual(self.user_token.user, self.platform_user)
        self.assertEqual(self.user_token.platform, self.platform)

    def tearDown(self):
        self.user.delete()
        self.platform_user.delete()
        self.platform.delete()
        self.user_token.delete()


# Serializer tests
class TestSerializers(APITestCase):
    def setUp(self):
        self.platform_user = PlatformUser.objects.create_user(
            username='testplatformuser', password='testpassword')
        self.platform = Platform.objects.create(name='Test Platform')
        self.user_token = UserToken.objects.create(
            user=self.platform_user, platform=self.platform)

    def test_platform_user_serializer(self):
        serializer = PlatformUserSerializer(self.platform_user)
        self.assertIsNotNone(serializer)
        self.assertEqual(
            serializer.data['username'], 'testplatformuser@{}'.format(Platform.get_or_create_host().name))

    def test_platform_serializer(self):
        serializer = PlatformSerializer(self.platform)
        self.assertIsNotNone(serializer)
        self.assertEqual(serializer.data['name'], 'Test Platform')

    def test_user_token_serializer(self):
        serializer = UserTokenSerializer(self.user_token)
        self.assertIsNotNone(serializer)
        self.assertEqual(serializer.data['user']['username'],
                         'testplatformuser@{}'.format(Platform.get_or_create_host().name))
        self.assertEqual(serializer.data['platform']['name'], 'Test Platform')

    def tearDown(self):
        self.platform_user.delete()
        self.platform.delete()
        self.user_token.delete()


# View tests
class TestViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform_user = PlatformUser.objects.create_user(
            username='testplatformuser', password='testpassword')
        self.platform = Platform.objects.create(name='Test Platform')
        self.user_token = UserToken.objects.create(
            user=self.platform_user, platform=self.platform)

    def test_create_usertoken_view(self):
        # replace 'usertoken-create_usertoken' with the correct URL name
        url = reverse('usertoken-create_usertoken')
        response = self.client.post(url, {'user_id': self.platform_user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        self.platform_user.delete()
        self.platform.delete()
        self.user_token.delete()
