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
    munged = ''.join(munged)
    assert text != munged
    return munged


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
    munged = munge_string_case(original, random_seed=SEED_NUMBER)
    return original, munged


@pytest.fixture(params=list(range(1, 11)), ids=_sample_to_fixture_id)
def two_samples(faker):
    original1 = faker.name()
    munged1 = munge_string_case(original1, random_seed=SEED_NUMBER)
    original2 = faker.name()
    munged2 = munge_string_case(original2, random_seed=SEED_NUMBER)
    assert original1 != original2
    return original1, munged1, original2, munged2


def test_repr(sample):
    text, _ = sample
    assert repr(istr(text)) == "istr({})".format(repr(text))


def test_eq_equal(sample):
    original, munged = sample
    if LOG_STRINGS:
        try:
            log.debug('original(%r) == munged(%r)',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert istr(original) == munged
    assert istr(original) == istr(munged)


def test_eq_different(two_samples):
    original1, _, _, munged2 = two_samples
    if LOG_STRINGS:
        try:
            log.debug('not original(%r) == munged(%r)',
                      original1, munged2)
        except UnicodeEncodeError:
            pass
    assert not istr(original1) == munged2
    assert not istr(original1) == istr(munged2)


def test_ne_equal(sample):
    original, munged = sample
    if LOG_STRINGS:
        try:
            log.debug('not original(%r) != munged(%r)',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert not istr(original) != munged
    assert not istr(original) != istr(munged)


def test_ne_different(two_samples):
    original1, _, _, munged2 = two_samples
    if LOG_STRINGS:
        try:
            log.debug('original(%r) != munged(%r)',
                      original1, munged2)
        except UnicodeEncodeError:
            pass
    assert istr(original1) != munged2
    assert istr(original1) != istr(munged2)


def test_lt(two_samples):
    original1, munged1, original2, munged2 = two_samples
    is_1_less = original1.casefold() < original2.casefold()
    if is_1_less:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) < munged(%r)',
                          original1, munged2)
            except UnicodeEncodeError:
                pass
        assert istr(original1) < munged2
        assert istr(original1) < istr(munged2)
    else:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) < munged(%r)',
                          original2, munged1)
            except UnicodeEncodeError:
                pass
        assert istr(original2) < munged1
        assert istr(original2) < istr(munged1)


def test_le_different(two_samples):
    original1, munged1, original2, munged2 = two_samples
    is_1_less = original1.casefold() < original2.casefold()
    if is_1_less:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) <= munged(%r)',
                          original1, munged2)
            except UnicodeEncodeError:
                pass
        assert istr(original1) <= munged2
        assert istr(original1) <= istr(munged2)
    else:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) <= munged(%r)',
                          original2, munged1)
            except UnicodeEncodeError:
                pass
        assert istr(original2) <= munged1
        assert istr(original2) <= istr(munged1)


def test_le_equal(sample):
    original, munged = sample
    if LOG_STRINGS:
        try:
            log.debug('original(%r) <= munged(%r)',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert istr(original) <= munged
    assert istr(original) <= istr(munged)


def test_gt(two_samples):
    original1, munged1, original2, munged2 = two_samples
    is_1_greater = original1.casefold() > original2.casefold()
    if is_1_greater:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) > munged(%r)',
                          original1, munged2)
            except UnicodeEncodeError:
                pass
        assert istr(original1) > munged2
        assert istr(original1) > istr(munged2)
    else:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) > munged(%r)',
                          original2, munged1)
            except UnicodeEncodeError:
                pass
        assert istr(original2) > munged1
        assert istr(original2) > istr(munged1)


def test_ge_different(two_samples):
    original1, munged1, original2, munged2 = two_samples
    is_1_greater = original1.casefold() > original2.casefold()
    if is_1_greater:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) >= munged(%r)',
                          original1, munged2)
            except UnicodeEncodeError:
                pass
        assert istr(original1) >= munged2
        assert istr(original1) >= istr(munged2)
    else:
        if LOG_STRINGS:
            try:
                log.debug('original(%r) >= munged(%r)',
                          original2, munged1)
            except UnicodeEncodeError:
                pass
        assert istr(original2) >= munged1
        assert istr(original2) >= istr(munged1)


def test_ge_equal(sample):
    original, munged = sample
    if LOG_STRINGS:
        try:
            log.debug('original(%r) >= munged(%r)',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert istr(original) >= munged
    assert istr(original) >= istr(munged)


def test_hash(sample):
    original, munged = sample
    if LOG_STRINGS:
        try:
            log.debug('hash(original(%r)) == hash(munged(%r))',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert hash(original) != hash(munged)
    assert hash(istr(original)) == hash(istr(munged))


def test_contains(sample):
    original, munged = sample
    munged_part = munged[1:-1]
    if LOG_STRINGS:
        try:
            log.debug('munged_part(%r) in original(%r)',
                      munged_part, original)
        except UnicodeEncodeError:
            pass
    assert munged_part not in original
    assert munged_part in istr(original)
    assert istr(munged_part) in istr(original)


def test_count(sample):
    original, munged = sample
    munged_other = munged[1:-1]
    if LOG_STRINGS:
        try:
            log.debug('original(%r).count(munged_other(%r))',
                      original, munged_other)
        except UnicodeEncodeError:
            pass
    assert original.count(munged_other) == 0
    assert istr(original).count(munged_other) == 1
    assert istr(original).count(istr(munged_other)) == 1


def test_find(sample):
    original, munged = sample
    pos = 2
    munged_other = munged[pos:-1]
    if LOG_STRINGS:
        try:
            log.debug('original(%r).find(munged_other(%r))',
                      original, munged_other)
        except UnicodeEncodeError:
            pass
    assert original.find(munged_other) == -1
    assert istr(original).find(munged_other) == pos
    assert istr(original).find(istr(munged_other)) == pos


def test_index(sample):
    original, munged = sample
    pos = 2
    munged_other = munged[pos:-1]
    if LOG_STRINGS:
        try:
            log.debug('original(%r).index(munged_other(%r))',
                      original, munged_other)
        except UnicodeEncodeError:
            pass
    with pytest.raises(ValueError):
        assert original.index(munged_other)
    assert istr(original).index(munged_other) == pos
    assert istr(original).index(istr(munged_other)) == pos


def test_rfind(sample):
    original, munged = sample
    pos = 2
    munged_other = munged[pos:-1]
    if LOG_STRINGS:
        try:
            log.debug('original(%r).rfind(munged_other(%r))',
                      original, munged_other)
        except UnicodeEncodeError:
            pass
    assert original.rfind(munged_other) == -1
    assert istr(original).rfind(munged_other) == pos
    assert istr(original).rfind(istr(munged_other)) == pos


def test_rindex(sample):
    original, munged = sample
    pos = 2
    munged_other = munged[pos:-1]
    if LOG_STRINGS:
        try:
            log.debug('original(%r).rindex(munged_other(%r))',
                      original, munged_other)
        except UnicodeEncodeError:
            pass
    with pytest.raises(ValueError):
        assert original.rindex(munged_other)
    assert istr(original).rindex(munged_other) == pos
    assert istr(original).rindex(istr(munged_other)) == pos


def test_startswith(sample):
    original, munged = sample
    munged_other = munged[:-1]
    if LOG_STRINGS:
        try:
            log.debug('original(%r).startswith(munged_other(%r))',
                      original, munged_other)
        except UnicodeEncodeError:
            pass
    assert not original.startswith(munged_other)
    assert istr(original).startswith(munged_other)
    assert istr(original).startswith(istr(munged_other))


def test_endswith(sample):
    original, munged = sample
    munged_other = munged[1:]
    if LOG_STRINGS:
        try:
            log.debug('original(%r).endswith(munged_other(%r))',
                      original, munged_other)
        except UnicodeEncodeError:
            pass
    assert not original.endswith(munged_other)
    assert istr(original).endswith(munged_other)
    assert istr(original).endswith(istr(munged_other))


def test_casefold(sample):
    original, munged = sample
    if LOG_STRINGS:
        try:
            log.debug('original(%r).casefold() == munged(%r))',
                      original, munged)
        except UnicodeEncodeError:
            pass
    assert original.casefold() == munged.casefold()  # !!
    assert istr(original).casefold() == munged.casefold()
    assert istr(original).casefold() == istr(munged).casefold()
