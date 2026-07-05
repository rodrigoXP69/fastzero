from sqlalchemy import select

from fastzero.models import User


def test_create_user(session):
    new_user = User(
        username='testuser', password='testpass', email='test@example.com'
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'testuser'))

    assert user.username == 'testuser'
