"""empty message

Revision ID: 36b4af1bdec0
Revises: 11dcd1db146e
Create Date: 2018-04-14 00:28:47.890795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36b4af1bdec0'
down_revision = '11dcd1db146e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dailylog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=100), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('test', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_dailylog_addtime'), 'dailylog', ['addtime'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dailylog_addtime'), table_name='dailylog')
    op.drop_table('dailylog')
    # ### end Alembic commands ###
