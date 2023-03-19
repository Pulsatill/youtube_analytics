import datetime
import pytest

from features.video import Video, PLVideo, PlayList

video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
playlist1 = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')


def test_str():
    assert video1.__str__() == "Как устроена IT-столица мира / Russian Silicon Valley (English subs)"
    assert video2.__str__() == "Пушкин: наше все? (Литература)"


def test_init():
    assert video1.video_title == "Как устроена IT-столица мира / Russian Silicon Valley (English subs)"
    assert video1.video_views == "49417177"
    assert video1.video_likes == "976642"
    assert video2.video_title == "Пушкин: наше все?"
    assert video2.playlist_title == "Литература"
    assert video2.video_views == "515567"
    assert video2.video_likes == "18787"


def test_get_pl_title():
    assert playlist1.pl_title == "Редакция. АнтиТревел"
    with pytest.raises(Exception):
        PlayList("play")


def test_get_data():
    assert playlist1.get_data('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb') == ['4jRSy-_CLFg',
                                                                        'XG6pQ9n4kr0',
                                                                        'cIs7N8B300M',
                                                                        'S7Ri5-9WHQY',
                                                                        '9Bv2zltQKQA'
                                                                        ]


def test_total_duration():
    assert video1.duration == datetime.timedelta(seconds=11253)
    duration = playlist1.total_duration()
    assert duration.total_seconds() == 13261.0


def test_show_best_video():
    assert playlist1.show_best_video() == "https://youtu.be/9Bv2zltQKQA"
