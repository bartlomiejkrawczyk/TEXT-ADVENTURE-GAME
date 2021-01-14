from utils.format import format_stats


def test_format_stats():
    assert format_stats(
        'Ala', 90, 100) == 'Ala: [===================90/100=================----]\n'
