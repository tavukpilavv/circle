"""initial schema with extensions and seed data

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2024-08-30
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS btree_gist;')
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
    op.execute('CREATE EXTENSION IF NOT EXISTS citext;')

    op.create_table(
        "universities",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("slug", sa.String(length=64), nullable=False, unique=True),
        sa.Column("name", sa.String(length=128), nullable=False),
    )

    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("label", sa.String(length=128), nullable=False),
    )

    op.create_table(
        "visibility_types",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("label", sa.String(length=128), nullable=False),
    )

    op.create_table(
        "event_statuses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("label", sa.String(length=128), nullable=False),
    )

    op.create_table(
        "signup_statuses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("label", sa.String(length=128), nullable=False),
    )

    op.create_table(
        "venue_types",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("label", sa.String(length=128), nullable=False),
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("university_id", sa.String(length=36), nullable=False),
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"], name="fk_tags_uni"),
        sa.UniqueConstraint("university_id", "key", name="uq_tag_uni_key"),
    )

    op.create_table(
        "campuses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("university_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"], name="fk_campuses_university"),
        sa.UniqueConstraint("university_id", "name", name="uq_campus_name_uni"),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("university_id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"], name="fk_users_university"),
        sa.UniqueConstraint("university_id", "email", name="uq_user_uni_email"),
    )

    op.create_table(
        "clubs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("university_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"], name="fk_clubs_university"),
        sa.UniqueConstraint("university_id", "slug", name="uq_clubs_uni_slug"),
    )

    op.create_table(
        "venues",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("university_id", sa.String(length=36), nullable=False),
        sa.Column("campus_id", sa.String(length=36), nullable=True),
        sa.Column("venue_type_id", sa.String(length=36), nullable=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"], name="fk_venues_university"),
        sa.ForeignKeyConstraint(["campus_id"], ["campuses.id"], name="fk_venues_campus"),
        sa.ForeignKeyConstraint(["venue_type_id"], ["venue_types.id"], name="fk_venues_type"),
        sa.UniqueConstraint("university_id", "name", name="uq_venues_uni_name"),
    )

    op.create_table(
        "user_roles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column("university_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_roles_user"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_user_roles_role"),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"], name="fk_user_roles_uni"),
        sa.UniqueConstraint("user_id", "role_id", "university_id", name="uq_user_role"),
    )

    op.create_table(
        "club_memberships",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("club_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"], name="fk_club_memberships_club"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_club_memberships_user"),
        sa.UniqueConstraint("club_id", "user_id", name="uq_club_member"),
    )

    op.create_table(
        "venue_blocks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("venue_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("start_at", sa.DateTime(), nullable=False),
        sa.Column("end_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"], name="fk_venue_blocks_venue"),
        sa.UniqueConstraint("venue_id", "name", name="uq_venue_block_name"),
    )

    op.create_table(
        "events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("university_id", sa.String(length=36), nullable=False),
        sa.Column("club_id", sa.String(length=36), nullable=False),
        sa.Column("venue_id", sa.String(length=36), nullable=True),
        sa.Column("status_id", sa.String(length=36), nullable=False),
        sa.Column("visibility_type_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_at", sa.DateTime(), nullable=False),
        sa.Column("end_at", sa.DateTime(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column("banner_url", sa.String(length=512), nullable=True),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"], name="fk_events_uni"),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"], name="fk_events_club"),
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"], name="fk_events_venue"),
        sa.ForeignKeyConstraint(["status_id"], ["event_statuses.id"], name="fk_events_status"),
        sa.ForeignKeyConstraint(["visibility_type_id"], ["visibility_types.id"], name="fk_events_visibility"),
        sa.CheckConstraint("end_at > start_at", name="ck_event_time"),
    )

    op.create_table(
        "event_tags",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("tag_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], name="fk_event_tags_event"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], name="fk_event_tags_tag"),
        sa.UniqueConstraint("event_id", "tag_id", name="uq_event_tag"),
    )

    op.create_table(
        "event_signups",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("status_id", sa.String(length=36), nullable=False),
        sa.Column("waitlist_position", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], name="fk_event_signups_event"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_event_signups_user"),
        sa.ForeignKeyConstraint(["status_id"], ["signup_statuses.id"], name="fk_event_signups_status"),
        sa.UniqueConstraint("event_id", "email", name="uq_event_signup_email"),
    )

    op.create_table(
        "waitlist_promotions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("signup_id", sa.String(length=36), nullable=False),
        sa.Column("promoted_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["signup_id"], ["event_signups.id"], name="fk_waitlist_promotions_signup"),
    )

    op.create_table(
        "checkins",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("signup_id", sa.String(length=36), nullable=False),
        sa.Column("checked_in_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["signup_id"], ["event_signups.id"], name="fk_checkins_signup"),
    )

    op.create_table(
        "media",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("event_id", sa.String(length=36), nullable=True),
        sa.Column("url", sa.String(length=512), nullable=False),
        sa.Column("content_type", sa.String(length=128), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], name="fk_media_event"),
    )

    op.create_table(
        "email_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("event_id", sa.String(length=36), nullable=True),
        sa.Column("recipient", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], name="fk_email_logs_event"),
    )

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("event_id", sa.String(length=36), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], name="fk_audit_events_event"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_audit_events_user"),
    )

    op.create_index("idx_events_start_at", "events", ["start_at"])
    op.create_index("idx_events_search_trgm", "events", [sa.text("title gin_trgm_ops")], postgresql_using="gin")

    op.execute(
        """
        ALTER TABLE events
          ADD CONSTRAINT events_no_room_overlap EXCLUDE USING gist (
            venue_id WITH =,
            tstzrange(start_at, end_at) WITH &&
          )
          WHERE (venue_id IS NOT NULL);
        """
    )

    op.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_public_events AS
        SELECT e.id, e.university_id, e.title, e.description, e.start_at, e.end_at, e.banner_url,
               c.name AS club_name, v.name AS venue_name
        FROM events e
        JOIN clubs c ON c.id = e.club_id
        LEFT JOIN venues v ON v.id = e.venue_id
        WHERE e.deleted_at IS NULL
          AND e.status_id = (SELECT id FROM event_statuses WHERE key='published');
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_mv_public_events_time ON mv_public_events(start_at);")

    op.execute(
        """
        INSERT INTO roles (id, created_at, updated_at, key, label) VALUES
        (uuid_generate_v4(), now(), now(), 'org_admin', 'Organization Admin'),
        (uuid_generate_v4(), now(), now(), 'club_admin', 'Club Admin'),
        (uuid_generate_v4(), now(), now(), 'venue_admin', 'Venue Admin'),
        (uuid_generate_v4(), now(), now(), 'staff', 'Staff'),
        (uuid_generate_v4(), now(), now(), 'student', 'Student')
        ON CONFLICT (key) DO NOTHING;
        """
    )
    op.execute(
        """
        INSERT INTO visibility_types (id, created_at, updated_at, key, label) VALUES
        (uuid_generate_v4(), now(), now(), 'public', 'Public'),
        (uuid_generate_v4(), now(), now(), 'private', 'Private'),
        (uuid_generate_v4(), now(), now(), 'campus', 'Campus Only')
        ON CONFLICT (key) DO NOTHING;
        """
    )
    op.execute(
        """
        INSERT INTO event_statuses (id, created_at, updated_at, key, label) VALUES
        (uuid_generate_v4(), now(), now(), 'draft', 'Draft'),
        (uuid_generate_v4(), now(), now(), 'published', 'Published'),
        (uuid_generate_v4(), now(), now(), 'cancelled', 'Cancelled')
        ON CONFLICT (key) DO NOTHING;
        """
    )
    op.execute(
        """
        INSERT INTO signup_statuses (id, created_at, updated_at, key, label) VALUES
        (uuid_generate_v4(), now(), now(), 'confirmed', 'Confirmed'),
        (uuid_generate_v4(), now(), now(), 'waitlist', 'Waitlist'),
        (uuid_generate_v4(), now(), now(), 'cancelled', 'Cancelled')
        ON CONFLICT (key) DO NOTHING;
        """
    )
    op.execute(
        """
        INSERT INTO venue_types (id, created_at, updated_at, key, label) VALUES
        (uuid_generate_v4(), now(), now(), 'indoor', 'Indoor'),
        (uuid_generate_v4(), now(), now(), 'outdoor', 'Outdoor')
        ON CONFLICT (key) DO NOTHING;
        """
    )
    op.execute(
        """
        INSERT INTO universities (id, created_at, updated_at, slug, name) VALUES
        (uuid_generate_v4(), now(), now(), 'aybu', 'AYBU')
        ON CONFLICT (slug) DO NOTHING;
        """
    )


def downgrade():
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_public_events;")
    op.drop_index("idx_mv_public_events_time", table_name=None, if_exists=True)
    op.drop_constraint("events_no_room_overlap", "events", type_="exclude", if_exists=True)
    op.drop_index("idx_events_search_trgm", table_name="events")
    op.drop_index("idx_events_start_at", table_name="events")

    for table in [
        "audit_events",
        "email_logs",
        "media",
        "checkins",
        "waitlist_promotions",
        "event_signups",
        "event_tags",
        "events",
        "venue_blocks",
        "club_memberships",
        "user_roles",
        "venues",
        "clubs",
        "users",
        "campuses",
        "tags",
        "venue_types",
        "signup_statuses",
        "event_statuses",
        "visibility_types",
        "roles",
        "universities",
    ]:
        op.drop_table(table)
