import pytest

from features.YouTube import YouTube

channel1 = YouTube('UCkJhWA2SEYbVYnE2Y2FWryA')
channel2 = YouTube('UCml3DQJIJSCr9YGpVRFIvgQ')


def test_str():
    assert channel1.__str__() == "Youtube-канал: hhwang - кто молодец?!"
    assert channel2.__str__() == "Youtube-канал: КРИПЕРС"


def test_add():
    assert channel1 + channel2 == "81200051300"


def test_lt():
    assert channel1.__lt__(channel2) == False
    assert channel2.__lt__(channel1) == True


def test_gt():
    assert channel1.__gt__(channel2) == True
    assert channel2.__gt__(channel1) == False
