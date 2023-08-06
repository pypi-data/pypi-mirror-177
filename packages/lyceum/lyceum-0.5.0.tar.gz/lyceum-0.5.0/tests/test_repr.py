#!/usr/bin/env python

"""Tests for `lyceum.repr` package."""
import pytest

from lyceum.repr import ascii2bin, bin2dec, bin2float, dec2bin, dec2hex, hex2dec


def test_bin():
    # TODO
    assert bin2dec("111") == 7


def test_ascii2bin():
    with pytest.raises(AssertionError):
        # n'accepte qu'un caractère
        ascii2bin("ab")
    with pytest.raises(AssertionError):
        # que de l'ascii
        ascii2bin("€")

    assert ascii2bin("O") == "01001111"
    assert ascii2bin("O", sep="_") == "0100_1111"


def test_bin2float():
    # double floats issus de wikipedia
    assert (
        bin2float("0 01111111111 0000000000000000000000000000000000000000000000000000")
        == 1
    )
    assert (
        bin2float("0 01111111111 0000000000000000000000000000000000000000000000000001")
        == (1 + 2**-52) * 2**0
    )
