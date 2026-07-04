from fastzero.models import User


def test_create_user():
    user = User(
        username='testuser', password='testpass', email='test@example.com'
    )
    assert user.username == 'testuser'
    assert user.password == 'testpass'
    assert user.email == 'test@example.com'
