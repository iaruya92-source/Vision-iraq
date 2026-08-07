from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import Listing, Category, Governorate
from sqlalchemy import desc

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Get active listings from all categories
    featured = Listing.query.filter_by(status='active').order_by(desc(Listing.is_featured), desc(Listing.created_at)).limit(6).all()
    latest = Listing.query.filter_by(status='active').order_by(desc(Listing.created_at)).limit(8).all()

    # Stats
    total_listings = Listing.query.filter_by(status='active').count()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()

    # Filter for own_category scope
    if current_user.is_authenticated and current_user.posting_scope == 'own_category' and current_user.user_type != 'user':
        allowed_slug = current_user.get_category_slug()
        if allowed_slug:
            categories = [c for c in categories if c.slug == allowed_slug]
            featured = [f for f in featured if f.category and f.category.slug == allowed_slug]
            latest = [l for l in latest if l.category and l.category.slug == allowed_slug]
            total_listings = len(latest)

    return render_template('index.html', featured=featured, latest=latest, total_listings=total_listings, categories=categories)

@bp.route('/category/<slug>')
def category_detail(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    if not cat.is_active:
        flash('هذا القسم غير متاح حالياً', 'warning')
        return redirect(url_for('main.index'))
    
    # Redirect to listings search with category filter
    return redirect(url_for('listings.search', category_id=cat.id))

@bp.route('/coming-soon')
def coming_soon():
    return render_template('coming_soon.html')
