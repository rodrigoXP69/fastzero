from dataclasses import asdict

from sqlalchemy import select

from fastzero.models import User


def test_create_user(session, mock_db_time):

    with mock_db_time(User) as time:
        new_user = User(
            username='testuser', password='testpass', email='test@example.com'
        )

        session.add(new_user)  # pede a sessão para adicionar o novo usuário
        session.commit()  # confirma a transação

        user = session.scalar(
            select(User).where(User.username == 'testuser')
        )  # scalar transforma o resultado do banco em obj py

        assert asdict(user) == {
            'id': 1,
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com',
            'created_at': time,
            'updated_at': time,
        }
