from django.test import TestCase
from api.utils import (
 valid_uuid, valid_name, valid_username, valid_url, gen_token_str, valid_token_str
)


class TestUtils(TestCase):
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
        self.assertTrue(valid_name(spchars))
        self.assertFalse(valid_name(spchars))

    def test_valid_username(self):
        valid = 'ExampleName'
        invalid = 'Example@Name'
        longname = 'TOOLONG' * 50
        empty = ''
        digits = '123132123123123'
        chars = 'aaaaaaaaaaaa'
        spchars = 'äæ3áa6ãäæ3áa6ã'

        self.assertTrue(valid_username(valid))
        self.assertFalse(valid_username(invalid))
        self.assertFalse(valid_username(longname))
        self.assertFalse(valid_username(empty))
        self.assertTrue(valid_username(digits))
        self.assertTrue(valid_username(spchars))
        self.assertFalse(valid_username(spchars))


    def test_valid_url(self):
        valids = ['https://www.example.com', 'http://google.com', 'google.com']

        invalids = ['htp://example', '//example.com', 'p://example.com',
                   'http://example', 'https://example.', 'http://example./']
        
        for v in valids:
            self.assertTrue(valid_url(v))

        for iv in invalids:
            self.assertFalse(valid_url(iv))


    def test_ptoken_str(self):
        ptoken = gen_token_str()

        self.assertIsNotNone(ptoken)
        self.assertTrue(ptoken.startswith('fdr-'))
        self.assertEqual(len(ptoken), 47)

        self.assertTrue(valid_token_str(ptoken))
        self.assertFalse(valid_token_str(ptoken + 'l'))
        self.assertFalse(valid_token_str(ptoken[1:]))
        self.assertFalse(valid_token_str(ptoken[:-1]))

        badtoken = str(ptoken)
        badtoken[0] = '#'
        self.assertFalse(valid_token_str(badtoken))
