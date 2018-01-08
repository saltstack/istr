# -*- coding: utf-8 -*-
'''
    tests.test_match
    ~~~~~~~~~~~~~~~~

    iStr unit tests
'''

# Import python libs
import os
import logging
from random import Random

# Import pytest libs
import pytest

# Import 3rd-party libs
from faker import Factory

# Import raas libs
from istr import istr

log = logging.getLogger(__name__)

SEED_NUMBER = 12345

LOCALES = (
    'en_US',
    # Now come the Unicode interesting locales
    'bg_BG',  # Bulgarian'
    'cs_cZ',  # Czech
    'de_DE',  # German
    'el_GR',  # Greek
    'fi_FI',  # Finish
    'lv_LV',  # Latvian
    'ru_RU',  # Russian
    'sv_SE',  # Swedish
    'tr_TR',  # Turkish
    'uk_UA',  # Ukrainian
    # The following would be interesting but apparently there's no
    # lower/upper case
    # 'fa_IR',  # Persian, Iran
    # 'hi_IN',  # Hindi
    # 'ja_JP',  # Japanese
    # 'ko_KR',  # Korean
    # 'ne_NP',  # Nepali
    # 'zh_CN',  # Chinese, China
    # 'zh_TW',  # Chinese, Taiwan
)

LOG_STRINGS = 'CI_RUN' not in os.environ


def munge_string_case(text, random_seed=None):
    random = Random(random_seed)
    munged = list(text)
    size = len(text)
    choices = list(range(size))
    while size >= 0:
        char_index = random.choice(choices)
        if char_index % 2 == 0:
            munged[char_index] = munged[char_index].upper()
        else:
            munged[char_index] = munged[char_index].lower()
        size -= 1
    return ''.join(munged)


def _locale_to_fixture_id(value):
    return 'Locale({})'.format(value)


@pytest.fixture(params=LOCALES, ids=_locale_to_fixture_id)
def locale(request):
    return request.param


@pytest.fixture
def faker(locale):
    faker_instance = Factory.create(locale)
    # We want random, but expectable randomness
    faker_instance.random.seed(SEED_NUMBER)
    return faker_instance


def _sample_to_fixture_id(value):
    return 'Sample({})'.format(value)


@pytest.fixture(params=list(range(1, 11)), ids=_sample_to_fixture_id)
def sample(faker):
    original = faker.name()
    return original, munge_string_case(original, random_seed=SEED_NUMBER)


def test_equality(sample):
    original, munged = sample
    if LOG_STRINGS:
        try:
            log.debug('Comparing original(%s) and munged(%s)',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert original != munged
    assert istr(original) == munged


def test_startswith(sample):
    original, munged = sample
    munged = munged[:-1]
    if LOG_STRINGS:
        try:
            log.debug('original(%s).startswith(munged(%s))',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert not original.startswith(munged)
    assert istr(original).startswith(munged)


def test_endswith(sample):
    original, munged = sample
    munged = munged[1:]
    if LOG_STRINGS:
        try:
            log.debug('original(%s).endswith(munged(%s))',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert not original.endswith(munged)
    assert istr(original).endswith(munged)
