#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/10 3:29 PM
# @Author  : cw
import pytest


@pytest.mark.base
@pytest.mark.parametrize("name", ["小文base", "小曾base", "小s-base"])
def test_base(name):
    """我是test_base"""
    print(name)


@pytest.mark.all
@pytest.mark.parametrize("name", ["小文all", "小曾all", "小s-all"])
def test_all(name):
    """我是test_all"""
    print(name)


@pytest.mark.base
@pytest.mark.all
@pytest.mark.parametrize("name", ["小文all-base", "小曾all-base", "小s_all-base"])
def test_all_base(name):
    """我是test_all_base"""
    assert 1 == 2

@pytest.mark.base
@pytest.mark.skip
def test_skip():
    """我是test_skip"""
    assert 2 == 4
