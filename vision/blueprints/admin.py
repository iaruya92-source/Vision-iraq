from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user
from functools import wraps
from models import db, Listing, User, ListingImage, Category, Governorate, SiteSetting
from datetime import datetime, timedelta
import os
from flask import current_app

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('غير مصرح بالوصول', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        
        user = User.query.filter_by(phone=phone).first()
        if user and user.check_password(password) and user.is_admin:
            login_user(user, remember=True)
            flash('تم تسجيل الدخول للوحة الإدارة', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة أو ليس لديك صلاحية الإدارة', 'danger')
    
    return render_template('admin/login.html')

@bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'listings': Listing.query.count(),
        'pending': Listing.query.filter_by(status='pending').count(),
        'active': Listing.query.filter_by(status='active').count(),
        'rejected': Listing.query.filter_by(status='rejected').count(),
        'total_views': db.session.query(db.func.sum(Listing.views)).scalar() or 0
    }
    pending = Listing.query.filter_by(status='pending').order_by(Listing.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, pending_listings=pending, recent_users=recent_users)

@bp.route('/listings')
@login_required
@admin_required
def listings():
    status = request.args.get('status', '')
    query = Listing.query.order_by(Listing.created_at.desc())
    if status:
        query = query.filter_by(status=status)
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/listings.html', listings=pagination.items, pagination=pagination, status=status)

@bp.route('/listings/<int:id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_listing(id):
    listing = Listing.query.get_or_404(id)
    listing.status = 'active'
    db.session.commit()
    flash('تم قبول الإعلان', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))

@bp.route('/listings/<int:id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_listing(id):
    listing = Listing.query.get_or_404(id)
    listing.status = 'rejected'
    db.session.commit()
    flash('تم رفض الإعلان', 'warning')
    return redirect(request.referrer or url_for('admin.dashboard'))

@bp.route('/listings/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_listing(id):
    listing = Listing.query.get_or_404(id)
    for img in listing.images:
        try:
            os.remove(os.path.join(current_app.root_path, 'static', img.image_path))
        except:
            pass
    db.session.delete(listing)
    db.session.commit()
    flash('تم حذف الإعلان', 'success')
    return redirect(request.referrer or url_for('admin.listings'))

@bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=pagination.items, pagination=pagination)

@bp.route('/users/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('لا يمكنك تعديل صلاحياتك', 'danger')
        return redirect(url_for('admin.users'))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('تم تحديث الصلاحيات', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/categories')
@login_required
@admin_required
def categories():
    cats = Category.query.order_by(Category.sort_order).all()
    return render_template('admin/categories.html', categories=cats)

@bp.route('/categories/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_category(id):
    cat = Category.query.get_or_404(id)
    cat.is_active = not cat.is_active
    db.session.commit()
    flash('تم تحديث القسم', 'success')
    return redirect(url_for('admin.categories'))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    if request.method == 'POST':
        for cat in Category.query.all():
            price_key = f'price_{cat.id}'
            premium_key = f'premium_{cat.id}'
            if price_key in request.form:
                cat.subscription_price = float(request.form[price_key] or 0)
            cat.is_premium = premium_key in request.form
        # Site settings
        featured_price = request.form.get('featured_price', '').strip()
        trial_days = request.form.get('trial_days', '').strip()
        if featured_price:
            SiteSetting.set_value('featured_price', featured_price)
        if trial_days:
            SiteSetting.set_value('trial_days', trial_days)
        db.session.commit()
        flash('تم حفظ الإعدادات', 'success')
        return redirect(url_for('admin.settings'))
    categories = Category.query.order_by(Category.sort_order).all()
    featured_price = SiteSetting.get_value('featured_price', '25000')
    trial_days = SiteSetting.get_value('trial_days', '7')
    return render_template('admin/settings.html', categories=categories, featured_price=featured_price, trial_days=trial_days)

@bp.route('/governorates')
@login_required
@admin_required
def governorates():
    govts = Governorate.query.order_by(Governorate.sort_order).all()
    return render_template('admin/governorates.html', governorates=govts)

@bp.route('/governorates/add', methods=['POST'])
@login_required
@admin_required
def add_governorate():
    name = request.form.get('name', '').strip()
    name_ar = request.form.get('name_ar', '').strip()
    if name and name_ar:
        g = Governorate(name=name, name_ar=name_ar, sort_order=Governorate.query.count()+1)
        db.session.add(g)
        db.session.commit()
        flash('تم إضافة المحافظة', 'success')
    return redirect(url_for('admin.governorates'))

@bp.route('/governorates/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_governorate(id):
    g = Governorate.query.get_or_404(id)
    db.session.delete(g)
    db.session.commit()
    flash('تم حذف المحافظة', 'success')
    return redirect(url_for('admin.governorates'))

@bp.route('/users/<int:id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('لا يمكنك تعديل حالة حسابك', 'danger')
        return redirect(url_for('admin.users'))
    user.is_active_account = not user.is_active_account
    db.session.commit()
    flash('تم تحديث حالة الحساب', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('لا يمكنك حذف حسابك', 'danger')
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    flash('تم حذف المستخدم', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/users/<int:id>/toggle-show-all', methods=['POST'])
@login_required
@admin_required
def toggle_show_all(id):
    user = User.query.get_or_404(id)
    user.show_in_all = not user.show_in_all
    db.session.commit()
    flash('تم تحديث الإعداد', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/listings/<int:id>/feature', methods=['POST'])
@login_required
@admin_required
def feature_listing(id):
    listing = Listing.query.get_or_404(id)
    if listing.is_featured:
        listing.featured_until = None
        listing.featured_price_paid = None
        listing.featured_by_admin = False
        flash('تم إلغاء تمييز الإعلان', 'warning')
    else:
        listing.featured_until = datetime.utcnow() + timedelta(days=30)
        listing.featured_price_paid = 0
        listing.featured_by_admin = True
        flash('تم تمييز الإعلان لمدة 30 يوم', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('admin.listings'))


@bp.route('/users/<int:id>/subscription', methods=['POST'])
@login_required
@admin_required
def update_subscription(id):
    """Admin can activate or extend subscription for a user."""
    user = User.query.get_or_404(id)
    if user.user_type == 'user':
        flash('المستخدمون العاديون لا يحتاجون اشتراك', 'info')
        return redirect(url_for('admin.users'))
    
    days = request.form.get('days', type=int)
    action = request.form.get('action', 'activate')
    
    if not days or days <= 0:
        flash('الرجاء إدخال عدد أيام صحيح', 'danger')
        return redirect(url_for('admin.users'))
    
    now = datetime.utcnow()
    
    if action == 'activate':
        # Fresh activation
        user.subscription_expiry = now + timedelta(days=days)
        user.subscription_status = 'active'
        user.grace_period_end = None
        user.is_active_account = True
        flash(f'تم تفعيل اشتراك المستخدم لمدة {days} يوم', 'success')
    elif action == 'extend':
        # Extend from current expiry or now
        base = user.subscription_expiry if user.subscription_expiry and user.subscription_expiry > now else now
        user.subscription_expiry = base + timedelta(days=days)
        user.subscription_status = 'active'
        user.grace_period_end = None
        user.is_active_account = True
        flash(f'تم تمديد الاشتراك بـ {days} يوم. ينتهي في {user.subscription_expiry.strftime("%Y-%m-%d")}', 'success')
    elif action == 'cancel':
        user.subscription_expiry = None
        user.subscription_status = 'expired'
        user.grace_period_end = None
        user.is_active_account = False
        flash('تم إلغاء الاشتراك', 'warning')
    
    db.session.commit()
    return redirect(url_for('admin.users'))


@bp.route('/users/<int:id>/start-grace', methods=['POST'])
@login_required
@admin_required
def start_grace_period(id):
    """Manually start grace period for a user (usually auto, but admin can trigger)."""
    user = User.query.get_or_404(id)
    if user.user_type == 'user':
        flash('المستخدمون العاديون لا يحتاجون فترة سماح', 'info')
        return redirect(url_for('admin.users'))
    
    days = request.form.get('grace_days', 10, type=int)
    user.subscription_status = 'grace'
    user.grace_period_end = datetime.utcnow() + timedelta(days=days)
    user.is_active_account = True
    db.session.commit()
    flash(f'تم تفعيل فترة سماح {days} يوم للمستخدم', 'warning')
    return redirect(url_for('admin.users'))


@bp.route('/users/<int:id>/expire', methods=['POST'])
@login_required
@admin_required
def expire_subscription(id):
    """Immediately expire subscription and disable account."""
    user = User.query.get_or_404(id)
    user.subscription_expiry = None
    user.subscription_status = 'expired'
    user.grace_period_end = None
    user.is_active_account = False
    db.session.commit()
    flash('تم إنهاء الاشتراك وتعطيل الحساب', 'danger')
    return redirect(url_for('admin.users'))
