import pytest


from src.views import greetings

def test_greetings(afternoon_greeting):
    assert greetings('2020-03-11 20:51:36') == afternoon_greeting


@pytest.mark.parametrize(
    'date_time, result', [
        ('2020-03-11 8:15:36', 'Доброе утро'),
        ('2020-03-11 12:15:36', 'Добрый день'),
        ('2020-03-11 19:15:36', 'Добрый вечер'),
        ('2020-03-11 23:15:36', 'Доброй ночи'),
    ]
)
def test_greetings_greeting(date_time, result):
    greeting = greetings(date_time)
    assert greeting['greeting'] == result

