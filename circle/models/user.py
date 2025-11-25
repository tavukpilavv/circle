from circle.extensions import db
from circle.models.base import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash


class User(BaseModel):
    __tablename__ = "users"

    university_id = db.Column(
        db.String(36),
        db.ForeignKey("universities.id"),
        nullable=False,
        index=True,
    )
    email = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    __table_args__ = (
        db.UniqueConstraint(
            "university_id", "email", name="uq_user_uni_email"
        ),
    )

    roles = db.relationship("UserRole", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False
    )
    role_id = db.Column(
        db.String(36), db.ForeignKey("roles.id"), nullable=False
    )
    university_id = db.Column(
        db.String(36), db.ForeignKey("universities.id"), nullable=False
    )
    role = db.relationship("Role")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "role_id", "university_id", name="uq_user_role"
        ),
    )
