from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, Listing, ListingImage, Category, Governorate, SiteSetting, User
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import uuid

bp = Blueprint('listings', __name__)

PROPERTY_TYPES = [
    ('house', 'بيت'),
    ('apartment', 'شقة'),
    ('land', 'أرض'),
    ('commercial', 'تجاري'),
    ('villa', 'فيلا'),
    ('farm', 'مزرعة'),
    ('office', 'مكتب'),
]

CAR_TYPES = [
    ('sedan', 'سيدان'),
    ('suv', 'دفع رباعي'),
    ('truck', 'شاحنة'),
    ('van', 'باص صغير'),
    ('pickup', 'بيك أب'),
    ('motorcycle', 'دراجة نارية'),
    ('other', 'أخرى'),
]

LISTING_TYPES = [
    ('sale', 'للبيع'),
    ('rent', 'للإيجار'),
]

COOLING_TYPES = [
    ('split', 'مكيف سبلت'),
    ('window', 'مكيف شباك'),
    ('central', 'تكييف مركزي'),
    ('duct', 'مكيف قنوات'),
    ('cassette', 'مكيف كاست'),
    ('chiller', 'مبرد ماء'),
    ('other', 'أخرى'),
]

COOLING_SERVICE_TYPES = [
    ('install', 'تركيب جديد'),
    ('repair', 'صيانة وإصلاح'),
    ('sales', 'مبيعات فقط'),
    ('install_repair', 'تركيب وصيانة'),
]

APPLIANCE_TYPES = [
    ('refrigerator', 'ثلاجة'),
    ('washing_machine', 'غسالة'),
    ('air_conditioner', 'مكيف'),
    ('television', 'تلفزيون'),
    ('oven', 'فرن'),
    ('vacuum', 'مكنسة كهربائية'),
    ('blender', 'خلاط'),
    ('heater', 'سخان'),
    ('dishwasher', 'جلاية'),
    ('microwave', 'مايكرويف'),
    ('iron', 'مكواة'),
    ('fan', 'مروحة'),
    ('water_purifier', 'منقي مياه'),
    ('other', 'أخرى'),
]

APPLIANCE_BRANDS = [
    ('LG', 'LG'),
    ('Samsung', 'سامسونج'),
    ('Bosch', 'بوش'),
    ('Siemens', 'سيمنز'),
    ('Toshiba', 'توشيبا'),
    ('Panasonic', 'باناسونيك'),
    ('Sharp', 'شارب'),
    ('Philips', 'فيليبس'),
    ('Whirlpool', 'ويرلبول'),
    ('Candy', 'كاندي'),
    ('Midea', 'ميديا'),
    ('Gree', 'جري'),
    ('General', 'جنرال'),
    ('Unionaire', 'يونيون آير'),
    ('Kiriazi', 'كريازي'),
    ('Fresh', 'فريش'),
    ('Tornado', 'تورنادو'),
    ('Carrier', 'كارير'),
    ('Trane', 'ترين'),
    ('York', 'يورك'),
    ('Other', 'أخرى'),
]

APPLIANCE_CONDITIONS = [
    ('new', 'جديد'),
    ('used', 'مستعمل'),
    ('refurbished', 'مجدد'),
    ('slightly_used', 'استعمال خفيف'),
]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_image(file):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return f"uploads/properties/{filename}"
    return None


def check_subscription_can_post(user):
    """Check if user can post listings. Returns (can_post, message, warning)."""
    if user.user_type == 'user':
        return True, None, None
    if not user.is_subscription_valid:
        if user.subscription_status == 'grace' and user.grace_period_end and user.grace_period_end > datetime.utcnow():
            return False, 'لا يمكنك النشر خلال فترة السماح. رجاءً تواصل مع الإدارة لتجديد الاشتراك. رقم التواصل: 07833779833', 'warning'
        if user.subscription_status == 'expired':
            return False, 'انتهى اشتراكك. رجاءً تواصل مع الإدارة لتجديده. رقم التواصل: 07833779833', 'danger'
        return False, 'لا يمكنك النشر حالياً. رجاءً تواصل مع الإدارة لتفعيل اشتراكك. رقم التواصل: 07833779833', 'danger'
    days_left = user.subscription_days_left
    warning = None
    if days_left is not None and days_left <= 5 and days_left > 0:
        warning = f'تنبيه: اشتراكك ينتهي بعد {days_left} يوم/أيام. رجاءً تواصل مع الإدارة لتجديده.'
    return True, None, warning


@bp.route('/')
def search():
    category_id = request.args.get('category_id', type=int)
    query = Listing.query.filter_by(status='active')

    # Enforce own_category scope
    if current_user.is_authenticated and current_user.posting_scope == 'own_category' and current_user.user_type != 'user':
        allowed_slug = current_user.get_category_slug()
        if allowed_slug:
            allowed_cat = Category.query.filter_by(slug=allowed_slug).first()
            if allowed_cat:
                query = query.filter_by(category_id=allowed_cat.id)
                category_id = allowed_cat.id
    elif category_id:
        query = query.filter_by(category_id=category_id)
    
    # Exclude listings from users in grace period or expired (unless viewing own)
    now = datetime.utcnow()
    if current_user.is_authenticated:
        query = query.filter(
            db.or_(
                Listing.user_id == current_user.id,
                ~Listing.user_id.in_(
                    db.session.query(User.id).filter(
                        db.or_(
                            db.and_(User.subscription_status == 'grace', User.grace_period_end >= now),
                            db.and_(User.subscription_status == 'expired', User.is_active_account == False)
                        )
                    )
                )
            )
        )
    else:
        query = query.filter(
            ~Listing.user_id.in_(
                db.session.query(User.id).filter(
                    db.or_(
                        db.and_(User.subscription_status == 'grace', User.grace_period_end >= now),
                        db.and_(User.subscription_status == 'expired', User.is_active_account == False)
                    )
                )
            )
        )
    
    # Featured listings always first
    query = query.order_by(
        (Listing.featured_until >= now).desc(),
        Listing.created_at.desc()
    )
    
    # Filters
    governorate = request.args.get('governorate', '')
    listing_type = request.args.get('listing_type', '')
    property_type = request.args.get('property_type', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    rooms = request.args.get('rooms', type=int)
    search_text = request.args.get('q', '')
    
    if governorate:
        query = query.filter_by(governorate=governorate)
    if listing_type:
        query = query.filter_by(listing_type=listing_type)
    if property_type:
        query = query.filter_by(property_type=property_type)
    if min_price is not None:
        query = query.filter(Listing.price >= min_price)
    if max_price is not None:
        query = query.filter(Listing.price <= max_price)
    if rooms:
        query = query.filter(Listing.rooms >= rooms)
    if search_text:
        query = query.filter(Listing.title.contains(search_text) | Listing.description.contains(search_text))
    
    # Sorting (featured first always)
    sort = request.args.get('sort', 'newest')
    now2 = datetime.utcnow()
    if sort == 'price_asc':
        query = query.order_by((Listing.featured_until >= now2).desc(), Listing.price.asc())
    elif sort == 'price_desc':
        query = query.order_by((Listing.featured_until >= now2).desc(), Listing.price.desc())
    else:
        query = query.order_by((Listing.featured_until >= now2).desc(), Listing.created_at.desc())
    
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=12, error_out=False)
    listings = pagination.items
    
    governorates = Governorate.query.order_by(Governorate.sort_order).all()
    
    return render_template('listings/search.html', 
                         listings=listings, 
                         pagination=pagination,
                         governorates=governorates,
                         property_types=PROPERTY_TYPES,
                         listing_types=LISTING_TYPES,
                         filters=request.args)


@bp.route('/<int:id>')
def detail(id):
    listing = Listing.query.get_or_404(id)
    if listing.status != 'active' and (not current_user.is_authenticated or current_user.id != listing.user_id):
        flash('هذا الإعلان غير متاح', 'warning')
        return redirect(url_for('listings.search'))
    
    # Check if listing owner is in grace or expired (block public view)
    if current_user.is_authenticated:
        if current_user.id != listing.user_id and not current_user.is_admin:
            owner = listing.owner
            if owner and owner.user_type != 'user':
                if owner.subscription_status == 'grace' and owner.grace_period_end and owner.grace_period_end > datetime.utcnow():
                    flash('هذا الإعلان غير متاح حالياً (صاحبه في فترة سماح)', 'warning')
                    return redirect(url_for('listings.search'))
                if owner.subscription_status == 'expired':
                    flash('هذا الإعلان غير متاح حالياً (انتهى اشتراك صاحبه)', 'warning')
                    return redirect(url_for('listings.search'))
    else:
        owner = listing.owner
        if owner and owner.user_type != 'user':
            if owner.subscription_status == 'grace' and owner.grace_period_end and owner.grace_period_end > datetime.utcnow():
                flash('هذا الإعلان غير متاح حالياً', 'warning')
                return redirect(url_for('listings.search'))
            if owner.subscription_status == 'expired':
                flash('هذا الإعلان غير متاح حالياً', 'warning')
                return redirect(url_for('listings.search'))
    
    # Increment views
    listing.views += 1
    db.session.commit()
    
    # Related listings
    related = Listing.query.filter(
        Listing.id != id,
        Listing.status == 'active',
        Listing.category_id == listing.category_id,
        Listing.governorate == listing.governorate
    ).order_by(db.func.random()).limit(4).all()
    
    return render_template('listings/detail.html', listing=listing, related=related)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    can_post, message, warning = check_subscription_can_post(current_user)
    if not can_post:
        flash(message, warning or 'danger')
        return redirect(url_for('dashboard.index'))
    if warning:
        flash(warning, 'warning')
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', type=float)
        currency = request.form.get('currency', 'IQD')
        area = request.form.get('area', type=float)
        rooms = request.form.get('rooms', type=int)
        bathrooms = request.form.get('bathrooms', type=int)
        property_type = request.form.get('property_type', '')
        listing_type = request.form.get('listing_type', 'sale')
        governorate = request.form.get('governorate', '')
        district = request.form.get('district', '').strip()
        area_zone = request.form.get('area_zone', '').strip()
        address = request.form.get('address', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()
        contact_whatsapp = request.form.get('contact_whatsapp', '').strip()
        
        category_id = request.form.get('category_id', type=int)
        if not title or not description or not governorate or not category_id:
            flash('الرجاء ملء جميع الحقول المطلوبة', 'danger')
            return redirect(url_for('listings.create'))

        # Validate category for own_category scope
        if current_user.posting_scope == 'own_category' and current_user.user_type != 'user':
            allowed_slug = current_user.get_category_slug()
            selected_cat = Category.query.get(category_id)
            if not selected_cat or selected_cat.slug != allowed_slug:
                flash('يمكنك النشر في قسمك فقط.', 'danger')
                return redirect(url_for('listings.create'))
        
        if not contact_phone:
            contact_phone = current_user.phone
        
        # Car fields
        car_type = request.form.get('car_type', '').strip()
        car_year = request.form.get('car_year', type=int)
        car_mileage = request.form.get('car_mileage', type=int)
        car_fuel = request.form.get('car_fuel', '').strip()
        car_transmission = request.form.get('car_transmission', '').strip()
        
        # Cooling fields
        cooling_type = request.form.get('cooling_type', '').strip()
        cooling_capacity = request.form.get('cooling_capacity', '').strip()
        cooling_brand = request.form.get('cooling_brand', '').strip()
        cooling_service_type = request.form.get('cooling_service_type', '').strip()
        
        # Appliance fields
        appliance_type = request.form.get('appliance_type', '').strip()
        appliance_brand = request.form.get('appliance_brand', '').strip()
        appliance_condition = request.form.get('appliance_condition', '').strip()
        appliance_warranty = request.form.get('appliance_warranty', '').strip()
        
        # Handle featured listing
        is_featured = request.form.get('is_featured') == 'on'
        featured_until = None
        featured_price = None
        if is_featured:
            featured_price = SiteSetting.get_value('featured_listing_price', '5000')
            featured_duration = int(SiteSetting.get_value('featured_listing_duration', '7'))
            featured_until = datetime.utcnow() + timedelta(days=featured_duration)
        
        listing = Listing(
            user_id=current_user.id,
            category_id=category_id,
            title=title,
            description=description,
            price=price,
            currency=currency,
            area=area,
            rooms=rooms,
            bathrooms=bathrooms,
            property_type=property_type,
            listing_type=listing_type,
            car_type=car_type or None,
            car_year=car_year,
            car_mileage=car_mileage,
            car_fuel=car_fuel or None,
            car_transmission=car_transmission or None,
            cooling_type=cooling_type or None,
            cooling_capacity=cooling_capacity or None,
            cooling_brand=cooling_brand or None,
            cooling_service_type=cooling_service_type or None,
            appliance_type=appliance_type or None,
            appliance_brand=appliance_brand or None,
            appliance_condition=appliance_condition or None,
            appliance_warranty=appliance_warranty or None,
            governorate=governorate,
            district=district,
            area_zone=area_zone,
            address=address,
            contact_phone=contact_phone,
            contact_whatsapp=contact_whatsapp or contact_phone,
            status='active',
            featured_until=featured_until,
            featured_price_paid=featured_price
        )
        
        db.session.add(listing)
        db.session.flush()  # Get ID before commit
        
        # Handle images
        files = request.files.getlist('images')
        has_main = False
        for file in files:
            if file and file.filename:
                path = save_image(file)
                if path:
                    img = ListingImage(listing_id=listing.id, image_path=path, is_main=not has_main)
                    db.session.add(img)
                    has_main = True
        
        db.session.commit()
        flash('تم إضافة الإعلان بنجاح وتم نشره مباشرة', 'success')
        return redirect(url_for('listings.search', category_id=listing.category_id))
    
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    # Filter categories based on posting_scope
    if current_user.posting_scope == 'own_category' and current_user.user_type != 'user':
        allowed_slug = current_user.get_category_slug()
        if allowed_slug:
            categories = [c for c in categories if c.slug == allowed_slug]
    governorates = Governorate.query.order_by(Governorate.sort_order).all()
    featured_price = SiteSetting.get_value('featured_listing_price', '5000')
    return render_template('listings/create.html',
                         categories=categories,
                         governorates=governorates,
                         property_types=PROPERTY_TYPES,
                         listing_types=LISTING_TYPES,
                         car_types=CAR_TYPES,
                         cooling_types=COOLING_TYPES,
                         cooling_service_types=COOLING_SERVICE_TYPES,
                         appliance_types=APPLIANCE_TYPES,
                         appliance_brands=APPLIANCE_BRANDS,
                         appliance_conditions=APPLIANCE_CONDITIONS,
                         featured_price=featured_price)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    listing = Listing.query.get_or_404(id)
    if listing.user_id != current_user.id and not current_user.is_admin:
        flash('غير مصرح لك بتعديل هذا الإعلان', 'danger')
        return redirect(url_for('listings.search'))
    
    # Only check subscription for the owner (not admin)
    if listing.user_id == current_user.id and current_user.user_type != 'user':
        can_post, message, warning = check_subscription_can_post(current_user)
        if not can_post:
            flash(message, warning or 'danger')
            return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        # Validate category change for own_category scope
        new_category_id = request.form.get('category_id', type=int)
        if new_category_id and current_user.posting_scope == 'own_category' and current_user.user_type != 'user':
            allowed_slug = current_user.get_category_slug()
            selected_cat = Category.query.get(new_category_id)
            if not selected_cat or selected_cat.slug != allowed_slug:
                flash('يمكنك التعديل ضمن قسمك فقط.', 'danger')
                return redirect(url_for('listings.edit', id=listing.id))

        listing.title = request.form.get('title', '').strip()
        listing.description = request.form.get('description', '').strip()
        listing.price = request.form.get('price', type=float)
        listing.area = request.form.get('area', type=float)
        listing.rooms = request.form.get('rooms', type=int)
        listing.bathrooms = request.form.get('bathrooms', type=int)
        listing.property_type = request.form.get('property_type', '')
        listing.listing_type = request.form.get('listing_type', 'sale')
        listing.car_type = request.form.get('car_type', '').strip() or None
        listing.car_year = request.form.get('car_year', type=int)
        listing.car_mileage = request.form.get('car_mileage', type=int)
        listing.car_fuel = request.form.get('car_fuel', '').strip() or None
        listing.car_transmission = request.form.get('car_transmission', '').strip() or None
        listing.cooling_type = request.form.get('cooling_type', '').strip() or None
        listing.cooling_capacity = request.form.get('cooling_capacity', '').strip() or None
        listing.cooling_brand = request.form.get('cooling_brand', '').strip() or None
        listing.cooling_service_type = request.form.get('cooling_service_type', '').strip() or None
        listing.appliance_type = request.form.get('appliance_type', '').strip() or None
        listing.appliance_brand = request.form.get('appliance_brand', '').strip() or None
        listing.appliance_condition = request.form.get('appliance_condition', '').strip() or None
        listing.appliance_warranty = request.form.get('appliance_warranty', '').strip() or None
        listing.governorate = request.form.get('governorate', '')
        listing.district = request.form.get('district', '').strip()
        listing.area_zone = request.form.get('area_zone', '').strip()
        listing.address = request.form.get('address', '').strip()
        listing.contact_phone = request.form.get('contact_phone', '').strip()
        listing.contact_whatsapp = request.form.get('contact_whatsapp', '').strip()
        
        # Handle new images
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename:
                path = save_image(file)
                if path:
                    img = ListingImage(listing_id=listing.id, image_path=path)
                    db.session.add(img)
        
        db.session.commit()
        flash('تم تحديث الإعلان بنجاح', 'success')
        return redirect(url_for('listings.detail', id=listing.id))
    
    governorates = Governorate.query.order_by(Governorate.sort_order).all()
    return render_template('listings/edit.html', 
                         listing=listing,
                         governorates=governorates,
                         property_types=PROPERTY_TYPES,
                         listing_types=LISTING_TYPES,
                         car_types=CAR_TYPES,
                         cooling_types=COOLING_TYPES,
                         cooling_service_types=COOLING_SERVICE_TYPES,
                         appliance_types=APPLIANCE_TYPES,
                         appliance_brands=APPLIANCE_BRANDS,
                         appliance_conditions=APPLIANCE_CONDITIONS)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    listing = Listing.query.get_or_404(id)
    if listing.user_id != current_user.id and not current_user.is_admin:
        flash('غير مصرح لك بحذف هذا الإعلان', 'danger')
        return redirect(url_for('listings.search'))
    
    # Delete images
    for img in listing.images:
        try:
            os.remove(os.path.join(current_app.root_path, 'static', img.image_path))
        except:
            pass
    
    db.session.delete(listing)
    db.session.commit()
    flash('تم حذف الإعلان بنجاح', 'success')
    return redirect(url_for('listings.search', category_id=listing.category_id))


@bp.route('/<int:id>/delete-image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(id, image_id):
    listing = Listing.query.get_or_404(id)
    if listing.user_id != current_user.id and not current_user.is_admin:
        flash('غير مصرح', 'danger')
        return redirect(url_for('listings.detail', id=id))
    
    img = ListingImage.query.get_or_404(image_id)
    if img.listing_id != id:
        flash('صورة غير صالحة', 'danger')
        return redirect(url_for('listings.detail', id=id))
    
    try:
        os.remove(os.path.join(current_app.root_path, 'static', img.image_path))
    except:
        pass
    
    db.session.delete(img)
    db.session.commit()
    flash('تم حذف الصورة', 'success')
    return redirect(url_for('listings.edit', id=id))


@bp.route('/<int:id>/featured', methods=['POST'])
@login_required
def make_featured(id):
    listing = Listing.query.get_or_404(id)
    if listing.user_id != current_user.id and not current_user.is_admin:
        flash('غير مصرح', 'danger')
        return redirect(url_for('listings.detail', id=id))
    
    price = SiteSetting.get_value('featured_listing_price', '5000')
    duration = int(SiteSetting.get_value('featured_listing_duration', '7'))
    
    listing.featured_until = datetime.utcnow() + timedelta(days=duration)
    listing.featured_price_paid = price
    db.session.commit()
    
    flash(f'تم تمييز الإعلان كمميز لمدة {duration} أيام', 'success')
    return redirect(url_for('listings.detail', id=id))


@bp.route('/<int:id>/unfeatured', methods=['POST'])
@login_required
def remove_featured(id):
    listing = Listing.query.get_or_404(id)
    if not current_user.is_admin:
        flash('غير مصرح', 'danger')
        return redirect(url_for('listings.detail', id=id))
    
    listing.featured_until = None
    listing.featured_price_paid = None
    db.session.commit()
    
    flash('تم إلغاء التمييز المميز', 'success')
    return redirect(url_for('listings.detail', id=id))
