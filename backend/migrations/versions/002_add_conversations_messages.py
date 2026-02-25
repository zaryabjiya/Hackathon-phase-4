"""Add conversations and messages tables

Revision ID: 002
Revises: 001
Create Date: 2026-02-18

"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for fast history retrieval
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('ix_messages_created_at', 'messages', ['conversation_id', 'created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_messages_created_at', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    
    # Drop tables
    op.drop_table('messages')
    op.drop_table('conversations')
