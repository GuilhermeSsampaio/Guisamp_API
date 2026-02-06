from sqlmodel import Session
from config.db import engine, create_db_and_tables

from auth.models.user import User
from auth.models.auth_provider import AuthProvider


def main():
    create_db_and_tables()
    with Session(engine) as session:

        # Criar usuário
        user = User(
            username="gui",
            email="gui@email.com"
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print("Usuário criado:", user.id)

        # Criar provider
        provider = AuthProvider(
            user_id=user.id,
            provider="password",
            password_hash="fake_hash"
        )

        session.add(provider)
        session.commit()

        print("Provider criado")

        # Testar relacionamento
        print("Providers do usuário:", user.providers)


if __name__ == "__main__":
    main()
