from features.video import Video, PLVideo

video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')


def test_str():
    assert video1.__str__() == "Как устроена IT-столица мира / Russian Silicon Valley (English subs)"
    assert video2.__str__() == "Пушкин: наше все? (Литература)"


def test_init():
    assert video1.video_title == "Как устроена IT-столица мира / Russian Silicon Valley (English subs)"
    assert video1.video_views == "49404826"
    assert video1.video_likes == "976559"
    assert video2.video_title == "Пушкин: наше все?"
    assert video2.playlist_title == "Литература"
    assert video2.video_views == "514190"
    assert video2.video_likes == "18745"
