from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class AdminUser(db.Model):
    __tablename__ = "admin_users"
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = "categories"
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(50), unique=True, nullable=False)
    slug     = db.Column(db.String(50), unique=True, nullable=False)
    icon     = db.Column(db.String(10), default="□")
    articles = db.relationship("Article", backref="category", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "slug": self.slug,
                "icon": self.icon, "count": len(self.articles)}

class Article(db.Model):
    __tablename__ = "articles"
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200), nullable=False)
    slug         = db.Column(db.String(200), unique=True, nullable=False)
    excerpt      = db.Column(db.Text)
    content      = db.Column(db.Text)
    level        = db.Column(db.Enum("Beginner","Intermediate","Advanced"), default="Beginner")
    read_time    = db.Column(db.Integer, default=5)
    is_featured  = db.Column(db.Boolean, default=False)
    views        = db.Column(db.Integer, default=0)
    category_id  = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self, full=False):
        data = {
            "id": self.id, "title": self.title, "slug": self.slug,
            "excerpt": self.excerpt, "level": self.level,
            "read_time": self.read_time, "is_featured": self.is_featured,
            "category": self.category.name if self.category else None,
            "category_slug": self.category.slug if self.category else None,
            "category_id": self.category_id,
            "views":      self.views,
            "created_at": self.created_at.isoformat(),
        }
        if full:
            data["content"] = self.content
        return data
