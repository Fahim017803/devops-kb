from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import Article, Category
import re

bp = Blueprint("admin_articles", __name__, url_prefix="/api/admin")

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

# ── List all articles ──────────────────────────────────────
@bp.route("/articles")
@jwt_required()
def list_articles():
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 15))
    q        = request.args.get("q", "")

    query = Article.query
    if q:
        query = query.filter(Article.title.ilike(f"%{q}%"))

    paginated = query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "articles": [a.to_dict() for a in paginated.items],
        "total": paginated.total,
        "pages": paginated.pages,
        "page": page,
    })

# ── Create article ─────────────────────────────────────────
@bp.route("/articles", methods=["POST"])
@jwt_required()
def create_article():
    data = request.get_json()
    required = ["title", "category_id"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"{f} is required"}), 400

    slug = data.get("slug") or slugify(data["title"])
    if Article.query.filter_by(slug=slug).first():
        slug = f"{slug}-{int(__import__('time').time())}"

    article = Article(
        title       = data["title"],
        slug        = slug,
        excerpt     = data.get("excerpt", ""),
        content     = data.get("content", ""),
        level       = data.get("level", "Beginner"),
        read_time   = int(data.get("read_time", 5)),
        is_featured = bool(data.get("is_featured", False)),
        category_id = int(data["category_id"]),
    )
    db.session.add(article)
    db.session.commit()
    return jsonify(article.to_dict(full=True)), 201

# ── Get single article ─────────────────────────────────────
@bp.route("/articles/<int:article_id>")
@jwt_required()
def get_article(article_id):
    a = db.get_or_404(Article, article_id)
    return jsonify(a.to_dict(full=True))

# ── Update article ─────────────────────────────────────────
@bp.route("/articles/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    a    = db.get_or_404(Article, article_id)
    data = request.get_json()

    a.title       = data.get("title",       a.title)
    a.slug        = data.get("slug",        a.slug)
    a.excerpt     = data.get("excerpt",     a.excerpt)
    a.content     = data.get("content",     a.content)
    a.level       = data.get("level",       a.level)
    a.read_time   = int(data.get("read_time", a.read_time))
    a.is_featured = bool(data.get("is_featured", a.is_featured))
    a.category_id = int(data.get("category_id", a.category_id))

    db.session.commit()
    return jsonify(a.to_dict(full=True))

# ── Delete article ─────────────────────────────────────────
@bp.route("/articles/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    a = db.get_or_404(Article, article_id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({"deleted": article_id})

# ── Categories (admin) ─────────────────────────────────────
@bp.route("/categories")
@jwt_required()
def list_categories():
    return jsonify([c.to_dict() for c in Category.query.all()])

@bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()
    cat  = Category(
        name = data["name"],
        slug = data.get("slug") or slugify(data["name"]),
        icon = data.get("icon", "□"),
    )
    db.session.add(cat)
    db.session.commit()
    return jsonify(cat.to_dict()), 201

@bp.route("/categories/<int:cat_id>", methods=["DELETE"])
@jwt_required()
def delete_category(cat_id):
    cat = db.get_or_404(Category, cat_id)
    if cat.articles:
        return jsonify({"error": "Cannot delete a category that still has articles"}), 400
    db.session.delete(cat)
    db.session.commit()
    return jsonify({"deleted": cat_id})
