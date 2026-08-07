from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Listing
from datetime import datetime

bp = Blueprint('dashboard', __name__)


def get_subscription_context():
    """Build subscription warning/alert data for dashboard templates."""
    ctx = {}
    if current_user.user_type == 'user':
        ctx['sub_alert'] = None
        return ctx
    
    now = datetime.utcnow()
    status = current_user.subscription_status
    expiry = current_user.subscription_expiry
    grace = current_user.grace_period_end
    
    alert = None
    
    if status == 'trial':
        alert = {
            'type': 'info',
            'icon': 'fa-info-circle',
            'title': 'أنت في فترة تجريبية',
            'message': 'يمكنك نشر إعلاناتك بحرية خلال فترة التجربة. تأكد من تفعيل الاشتراك قبل انتهائها.'
        }
    elif status == 'active' and expiry:
        days_left = (expiry - now).days
        if days_left <= 0:
            alert = {
                'type': 'danger',
                'icon': 'fa-exclamation-triangle',
                'title': 'انتهى اشتراكك!',
                'message': 'لقد انتهى اشتراكك. يرجى التواصل مع الإدارة عبر الواتساب لتجديد الاشتراك.'
            }
        elif days_left <= 5:
            alert = {
                'type': 'warning',
                'icon': 'fa-bell',
                'title': f'اشتراكك على وشك الانتهاء ({days_left} يوم)',
                'message': 'اشتراكك سينتهي قريباً. تواصل مع الإدارة لتجديده واستمرار عرض إعلاناتك.'
            }
        else:
            alert = {
                'type': 'success',
                'icon': 'fa-check-circle',
                'title': f'اشتراكك نشط (متبقي {days_left} يوم)',
                'message': 'اشتراكك ساري المفعول. يمكنك إدارة إعلاناتك بشكل طبيعي.'
            }
    elif status == 'grace' and grace:
        days_left = (grace - now).days
        if days_left <= 0:
            alert = {
                'type': 'danger',
                'icon': 'fa-ban',
                'title': 'انتهت فترة السماح!',
                'message': 'لقد انتهت فترة السماح. أصبح حسابك معطلاً. تواصل مع الإدارة لتفعيل الاشتراك.'
            }
        else:
            alert = {
                'type': 'warning',
                'icon': 'fa-hourglass-half',
                'title': f'فترة سماح ({days_left} يوم متبقي)',
                'message': 'اشتراكك منتهٍ ولكن لديك فترة سماح. إعلاناتك لن تظهر في نتائج البحث. جدد الاشتراك الآن.'
            }
    elif status == 'expired':
        alert = {
            'type': 'danger',
            'icon': 'fa-ban',
            'title': 'الاشتراك منتهٍ',
            'message': 'اشتراكك منتهٍ وحسابك معطل. تواصل مع الإدارة عبر الواتساب لتجديد الاشتراك.'
        }
    
    ctx['sub_alert'] = alert
    ctx['sub_expiry'] = expiry
    ctx['sub_grace'] = grace
    ctx['sub_status'] = status
    return ctx


@bp.route('/')
@login_required
def index():
    stats = {
        'total': Listing.query.filter_by(user_id=current_user.id).count(),
        'active': Listing.query.filter_by(user_id=current_user.id, status='active').count(),
        'pending': Listing.query.filter_by(user_id=current_user.id, status='pending').count(),
        'views': db.session.query(db.func.sum(Listing.views)).filter_by(user_id=current_user.id).scalar() or 0
    }
    recent = Listing.query.filter_by(user_id=current_user.id).order_by(Listing.created_at.desc()).limit(5).all()
    ctx = get_subscription_context()
    return render_template('dashboard/index.html', stats=stats, recent=recent, **ctx)

@bp.route('/my-listings')
@login_required
def my_listings():
    listings = Listing.query.filter_by(user_id=current_user.id).order_by(Listing.created_at.desc()).all()
    ctx = get_subscription_context()
    return render_template('dashboard/my_listings.html', listings=listings, **ctx)

@bp.route('/profile')
@login_required
def profile():
    ctx = get_subscription_context()
    return render_template('dashboard/profile.html', **ctx)

@bp.route('/profile', methods=['POST'])
@login_required
def profile_update():
    current_user.name = request.form.get('name', '').strip()
    current_user.email = request.form.get('email', '').strip()
    db.session.commit()
    flash('تم تحديث الملف الشخصي', 'success')
    return redirect(url_for('dashboard.profile'))
