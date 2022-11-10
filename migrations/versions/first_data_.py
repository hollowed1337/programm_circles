"""empty message

Revision ID: first_data
Revises: 55164c0af05b
Create Date: 2022-10-19 14:15:32.786004

"""
from alembic import op
from sqlalchemy import orm

from src.models import User, Account


# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = '55164c0af05b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind = bind)

    ivanov = User(email="ivanov@mail.ru", hashed_password = "qwe")
    petrov = User(email="petrov@mail.ru", hashed_password = "123")

    session.add_all([ivanov, petrov])
    session.flush()

    #book_eragon = Item(title = "Eragon: Brisingr", description="Book", owner_id = ivanov.id)
    #book_lowecraft = Item(title = "The Shadow over Innsmouth", description = "Book", owner_id = ivanov.id)
    #deus_ex = Item(title = "Deus Ex: Human Revolution", description = "Game", owner_id = petrov.id)
    #cartoon_rick = Item(title = "Rick and Morty", description = "Cartoon", owner_id = petrov.id)

    #session.add_all([book_eragon, book_lowecraft, deus_ex, cartoon_rick])
    #session.commit()

def downgrade() -> None:
    pass
