"""empty message

Revision ID: b21eb544cb4a
Revises: 
Create Date: 2018-07-25 21:32:04.094245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b21eb544cb4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Asset',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('hostname', sa.String(length=64), nullable=True),
    sa.Column('sn', sa.String(length=64), nullable=True),
    sa.Column('buy_time', sa.DateTime(), nullable=True),
    sa.Column('expire_date', sa.DateTime(), nullable=True),
    sa.Column('ip', sa.String(length=128), nullable=True),
    sa.Column('disk', sa.String(length=128), nullable=True),
    sa.Column('model', sa.String(length=64), nullable=True),
    sa.Column('memory', sa.String(length=256), nullable=True),
    sa.Column('cpu_model', sa.String(length=128), nullable=True),
    sa.Column('cpu_processor', sa.String(length=32), nullable=True),
    sa.Column('cpu_num', sa.String(length=32), nullable=True),
    sa.Column('cpu_physical', sa.String(length=32), nullable=True),
    sa.Column('business_unit', sa.String(length=64), nullable=True),
    sa.Column('vendor', sa.String(length=64), nullable=True),
    sa.Column('os', sa.String(length=128), nullable=True),
    sa.Column('idc', sa.String(length=64), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('memo', sa.String(length=255), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hostname'),
    sa.UniqueConstraint('sn')
    )
    op.create_table('BusinessUnit',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('memo', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('IDC',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('memo', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Manufactory',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('manufactory', sa.String(length=64), nullable=True),
    sa.Column('support_num', sa.String(length=32), nullable=True),
    sa.Column('memo', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('Manufactory')
    op.drop_table('IDC')
    op.drop_table('BusinessUnit')
    op.drop_table('Asset')
    # ### end Alembic commands ###