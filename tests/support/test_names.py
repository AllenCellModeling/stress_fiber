#!/usr/bin/end python
# -*- coding: UTF-8 -*-

"""
Test names. 
"""

import stress_fiber.support.names as names


sample_names = [names.unique_name() for i in range(20)]


def test_unique_name():
    """Check uniqueness"""
    assert len(sample_names) == len(list(set(sample_names)))


def test_name_to_uuid():
    """Check that we can roundtrip our names"""
    roundtrip = lambda name: names.unique_name(names.name_to_uuid(name))
    assert all([name == roundtrip(name) for name in sample_names])