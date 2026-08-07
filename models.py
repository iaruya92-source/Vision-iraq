from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(30), default="user")
    # user, realtor, doctor, pharmacist, workshop, market_owner, car_dealer,
    # cooling, bakery, ro_water, company, trades, appliances
    user_title = db.Column(db.String(100), nullable=True)
    subscription_expiry = db.Column(db.DateTime, nullable=True)
    subscription_status = db.Column(db.String(20), default='trial')
    # trial, active, grace, expired, free
    grace_period_end = db.Column(db.DateTime, nullable=True)
    trial_end = db.Column(db.DateTime, nullable=True)
    is_active_account = db.Column(db.Boolean, default=True)
    show_in_all = db.Column(db.Boolean, default=True)
    posting_scope = db.Column(db.String(20), default='full_platform')  # own_category, full_platform
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listings = db.relationship('Listing', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_subscription_valid(self):
        """Check if user can post listings"""
        if self.user_type == 'user':
            return True
        now = datetime.utcnow()
        # Auto-activate grace period if subscription just expired and not already in grace/expired
        if self.subscription_status == 'active' and self.subscription_expiry and self.subscription_expiry <= now:
            if not self.grace_period_end or self.grace_period_end <= now:
                self.subscription_status = 'grace'
                self.grace_period_end = now + timedelta(days=10)
                db.session.commit()
        if self.subscription_status == 'trial' and self.trial_end and self.trial_end > now:
            return True
        if self.subscription_status == 'active' and self.subscription_expiry and self.subscription_expiry > now:
            return True
        return False

    @property
    def subscription_days_left(self):
        """Return days left for active subscription or trial"""
        now = datetime.utcnow()
        if self.user_type == 'user':
            return None
        if self.subscription_status == 'trial' and self.trial_end:
            days = (self.trial_end - now).days
            return max(0, days)
        if self.subscription_status == 'active' and self.subscription_expiry:
            days = (self.subscription_expiry - now).days
            return max(0, days)
        if self.subscription_status == 'grace' and self.grace_period_end:
            days = (self.grace_period_end - now).days
            return max(0, days)
        return 0

    @property
    def subscription_state_label(self):
        """Arabic label for subscription state"""
        states = {
            'trial': 'فترة تجريبية',
            'active': 'اشتراك نشط',
            'grace': 'فترة سماح',
            'expired': 'منتهي',
            'free': 'مجاني'
        }
        return states.get(self.subscription_status, self.subscription_status)

    def get_category_slug(self):
        """Map user_type to category slug for own_category scope"""
        mapping = {
            'realtor': 'real-estate',
            'doctor': 'doctors',
            'pharmacist': 'pharmacies',
            'workshop': 'workshops',
            'market_owner': 'markets',
            'car_dealer': 'cars',
            'cooling': 'services',
            'bakery': 'restaurants',
            'ro_water': 'services',
            'company': 'services',
            'trades': 'trades',
            'appliances': 'appliances',
        }
        return mapping.get(self.user_type)

    def get_user_type_display(self):
        """Arabic display name for user_type"""
        mapping = {
            'user': 'مستخدم',
            'realtor': 'عقارات',
            'doctor': 'أطباء',
            'pharmacist': 'صيادلة',
            'workshop': 'ورش',
            'market_owner': 'أسواق',
            'car_dealer': 'سيارات',
            'cooling': 'تبريد وتكييف',
            'bakery': 'مخابز',
            'ro_water': 'مياه محلاة',
            'company': 'شركات',
            'trades': 'أصحاب المهن',
            'appliances': 'أجهزة كهربائية',
        }
        return mapping.get(self.user_type, self.user_type)

    def __repr__(self):
        return f'<User {self.phone}>'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), default='grid')
    color = db.Column(db.String(20), default='#2563eb')
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    subscription_price = db.Column(db.Float, default=0)
    is_premium = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listings = db.relationship('Listing', backref='category', lazy='dynamic')
    attributes = db.relationship('CategoryAttribute', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name_ar}>'


class CategoryAttribute(db.Model):
    __tablename__ = 'category_attributes'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    name_ar = db.Column(db.String(50), nullable=False)
    attr_type = db.Column(db.String(20), default='text')
    options = db.Column(db.Text, nullable=True)
    is_required = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)


class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # Basic Info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Property / Item specifics
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='IQD')
    area = db.Column(db.Float, nullable=True)
    rooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    property_type = db.Column(db.String(50), nullable=True)
    listing_type = db.Column(db.String(20), nullable=False, default='sale')

    # Car-specific fields
    car_type = db.Column(db.String(50), nullable=True)
    car_year = db.Column(db.Integer, nullable=True)
    car_mileage = db.Column(db.Integer, nullable=True)
    car_fuel = db.Column(db.String(20), nullable=True)
    car_transmission = db.Column(db.String(20), nullable=True)

    # Cooling/AC-specific fields
    cooling_type = db.Column(db.String(50), nullable=True)
    cooling_capacity = db.Column(db.String(50), nullable=True)
    cooling_brand = db.Column(db.String(100), nullable=True)
    cooling_service_type = db.Column(db.String(50), nullable=True)

    # Electrical appliance fields
    appliance_type = db.Column(db.String(50), nullable=True)
    appliance_brand = db.Column(db.String(100), nullable=True)
    appliance_condition = db.Column(db.String(20), nullable=True)
    appliance_warranty = db.Column(db.String(100), nullable=True)

    # Featured listing
    featured_until = db.Column(db.DateTime, nullable=True)
    featured_price_paid = db.Column(db.Float, default=0)

    # Location
    governorate = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=True)
    area_zone = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)

    # Contact
    contact_phone = db.Column(db.String(20), nullable=False)
    contact_whatsapp = db.Column(db.String(20), nullable=True)

    # Status
    status = db.Column(db.String(20), default='pending')
    is_featured = db.Column(db.Boolean, default=False)
    featured_by_admin = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship('ListingImage', backref='listing', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def author(self):
        """Backward compatibility alias for owner"""
        return self.owner

    @property
    def main_image(self):
        img = self.images.filter_by(is_main=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def formatted_price(self):
        if self.price >= 1000000000:
            return f"{self.price/1000000000:.1f} مليار"
        elif self.price >= 1000000:
            return f"{self.price/1000000:.1f} مليون"
        elif self.price >= 1000:
            return f"{self.price/1000:.0f} ألف"
        return f"{self.price:.0f}"

    def __repr__(self):
        return f'<Listing {self.title[:30]}>'


class ListingImage(db.Model):
    __tablename__ = 'listing_images'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Governorate(db.Model):
    __tablename__ = 'governorates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    sort_order = db.Column(db.Integer, default=0)


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_value(cls, key, default=''):
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default

    @classmethod
    def set_value(cls, key, value, description=None):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = str(value)
        else:
            setting = cls(key=key, value=str(value), description=description)
            db.session.add(setting)
        db.session.commit()
