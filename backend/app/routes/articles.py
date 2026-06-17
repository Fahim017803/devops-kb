from flask import Blueprint, jsonify, request
from app import db
from app.models import Article, Category

bp = Blueprint("articles", __name__, url_prefix="/api")

# ── Health check ──────────────────────────────────────────
@bp.route("/health")
def health():
    return jsonify({"status": "ok"})

# ── Categories ────────────────────────────────────────────
@bp.route("/categories")
def get_categories():
    cats = Category.query.all()
    return jsonify([c.to_dict() for c in cats])

# ── Articles (list) ───────────────────────────────────────
@bp.route("/articles")
def get_articles():
    category = request.args.get("category")   # ?category=cicd
    featured  = request.args.get("featured")  # ?featured=true
    page      = int(request.args.get("page", 1))
    per_page  = int(request.args.get("per_page", 9))

    q = Article.query
    if category:
        q = q.join(Category).filter(Category.slug == category)
    if featured == "true":
        q = q.filter(Article.is_featured == True)

    paginated = q.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "articles": [a.to_dict() for a in paginated.items],
        "total":    paginated.total,
        "pages":    paginated.pages,
        "page":     page,
    })

# ── Article (single) ──────────────────────────────────────
@bp.route("/articles/<slug>")
def get_article(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    return jsonify(article.to_dict(full=True))

# ── Search ─────────────────────────────────────────────────
@bp.route("/search")
def search():
    q = request.args.get("q", "").strip()
    if not q or len(q) < 2:
        return jsonify({"results": [], "query": q})

    pattern = f"%{q}%"
    results = Article.query.filter(
        db.or_(
            Article.title.ilike(pattern),
            Article.excerpt.ilike(pattern),
        )
    ).limit(8).all()

    return jsonify({
        "results": [a.to_dict() for a in results],
        "query":   q,
        "count":   len(results),
    })
