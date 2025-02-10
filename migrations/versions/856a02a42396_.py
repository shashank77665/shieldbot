"""empty message

Revision ID: 856a02a42396
Revises: 2732a36fe6fd
Create Date: 2025-02-11 02:54:36.556104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '856a02a42396'
down_revision = '2732a36fe6fd'
branch_labels = None
depends_on = None


def upgrade():
    # Create new user table (shieldbot_users)
    op.create_table(
        'shieldbot_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create tests table with foreign key referencing shieldbot_users
    op.create_table(
        'tests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('test_name', sa.String(length=100), nullable=False),
        sa.Column('base_url', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('logs', sa.JSON(), nullable=True),
        sa.Column('ai_insights', sa.JSON(), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['shieldbot_users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Drop the old table if it exists with CASCADE
    op.execute("DROP TABLE IF EXISTS shieldbot_user CASCADE")

    # Alter the request_log table:
    with op.batch_alter_table('request_log', schema=None) as batch_op:
        # Drop the old foreign key constraint if it exists.
        batch_op.execute(
            "ALTER TABLE request_log DROP CONSTRAINT IF EXISTS request_log_shieldbot_user_id_fkey;"
        )
        # Create new foreign key that references shieldbot_users.id with an explicit name.
        batch_op.create_foreign_key(
            "fk_request_log_shieldbot_user_id", "shieldbot_users", ['shieldbot_user_id'], ['id']
        )


def downgrade():
    # Revert the changes: remove the new foreign key first.
    with op.batch_alter_table('request_log', schema=None) as batch_op:
        batch_op.execute(
            "ALTER TABLE request_log DROP CONSTRAINT IF EXISTS fk_request_log_shieldbot_user_id;"
        )
        # Recreate the old foreign key constraint (if needed)
        batch_op.create_foreign_key(
            "request_log_shieldbot_user_id_fkey", "shieldbot_user", ['shieldbot_user_id'], ['shieldbot_user_id']
        )

    # Recreate the old shieldbot_user table.
    op.create_table(
        'shieldbot_user',
        sa.Column('shieldbot_user_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(length=50), nullable=False),
        sa.Column('email', sa.VARCHAR(length=120), nullable=False),
        sa.Column('password_hash', sa.VARCHAR(length=256), nullable=False),
        sa.Column('profile_picture', sa.VARCHAR(length=255), nullable=False),
        sa.Column('is_superuser', sa.BOOLEAN(), nullable=True),
        sa.PrimaryKeyConstraint('shieldbot_user_id', name='shieldbot_user_pkey'),
        sa.UniqueConstraint('email', name='shieldbot_user_email_key'),
        sa.UniqueConstraint('username', name='shieldbot_user_username_key')
    )

    op.drop_table('tests')
    op.drop_table('shieldbot_users')