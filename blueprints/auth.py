from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from models import db, User
from datetime import datetime, timedelta
import re

bp = Blueprint('auth', __name__)


def is_valid_phone(phone):
    return re.match(r'^07\d{9}$', phone) is not None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        
        if not phone or not password:
            flash('الرجاء إدخال رقم الهاتف وكلمة المرور', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(phone=phone).first()
        if user and user.check_password(password):
            if not getattr(user, 'is_active_account', True):
                flash('الحساب محظور. تواصل مع الإدارة', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, remember=True)
            flash('تم تسجيل الدخول بنجاح', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('رقم الهاتف أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()
        user_type = request.form.get('user_type', 'user').strip()
        user_title = request.form.get('user_title', '').strip()
        posting_scope = request.form.get('posting_scope', 'full_platform').strip()
        
        # Validation
        if not name or not phone or not password:
            flash('الرجاء ملء جميع الحقول المطلوبة', 'danger')
            return redirect(url_for('auth.register'))
        
        if not is_valid_phone(phone):
            flash('رقم الهاتف غير صحيح. يجب أن يبدأ بـ 07 ويتكون من 11 رقماً', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm:
            flash('كلمات المرور غير متطابقة', 'danger')
            return redirect(url_for('auth.register'))

        if posting_scope not in ('own_category', 'full_platform'):
            flash('نطاق النشر غير صالح.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(phone=phone).first():
            flash('هذا الرقم مسجل مسبقاً. استخدم تسجيل الدخول', 'warning')
            return redirect(url_for('auth.login'))
        
        # Create user with trial
        user = User(
            phone=phone,
            name=name,
            user_type=user_type,
            user_title=user_title if user_title else None,
            posting_scope=posting_scope,
            trial_end=datetime.utcnow() + timedelta(days=7)
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user, remember=True)
        flash('تم إنشاء الحساب بنجاح. لديك تجربة مجانية لمدة أسبوع', 'success')
        return redirect(url_for('main.index'))
    
    # Title options mapped by user_type
    title_options = {
        'user': ['فرد', 'مستخدم عادي'],
        'realtor': ['مسوق عقاري', 'صاحب مكتب عقارات', 'وسيط عقاري'],
        'doctor': ['طبيب', 'أخصائي', 'جراح', 'استشاري'],
        'pharmacist': ['صيدلاني', 'مساعد صيدلاني', 'صاحب صيدلية'],
        'workshop': ['صاحب ورشة', 'فني', 'ميكانيكي', 'كهربائي سيارات'],
        'market_owner': ['صاحب سوق', 'صاحب محل', 'تاجر'],
        'car_dealer': ['تاجر سيارات', 'معرض سيارات', 'وسيط سيارات'],
        'cooling': ['صاحب محل تبريد', 'فني تبريد', 'مقاول تكييف', 'صاحب معرض مكيفات'],
        'bakery': ['صاحب مخبز', 'خباز', 'صاحب فرن', 'معجنات وحلويات'],
        'ro_water': ['صاحب محطة مياه', 'فني تركيب فلاتر', 'موزع مياه معبأة'],
        'company': ['مدير شركة', 'صاحب مؤسسة', 'مسؤول مبيعات', 'مسؤول تسويق'],
        'trades': ['نجار', 'حداد', 'كهربائي', 'سباك', 'بلاط', 'صباغ', 'جبس بورد', 'ألومنيوم وبي في سي', 'نجار أثاث', 'فني تركيب', 'صيانة عامة', 'مقاول بناء', 'حداد أبواب وشبابيك', 'فني سيراميك', 'فني ديكور', 'مبلط', 'فني تصليحات', 'صاحب ورشة'],
        'appliances': ['تاجر أجهزة كهربائية', 'فني صيانة أجهزة', 'صاحب محل أجهزة', 'موزع معتمد', 'وكيل شركة', 'صاحب معرض أجهزة منزلية'],
    }
    return render_template('auth/register.html', title_options=title_options)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج', 'info')
    return redirect(url_for('main.index'))
