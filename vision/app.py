from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User, Category, Governorate, SiteSetting
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from blueprints.main import bp as main_bp
    from blueprints.auth import bp as auth_bp
    from blueprints.listings import bp as listings_bp
    from blueprints.dashboard import bp as dashboard_bp
    from blueprints.admin import bp as admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(listings_bp, url_prefix='/listings')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Health check for Render/Railway
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'vision-classifieds'}, 200
    
    # Template globals
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        categories = Category.query.order_by(Category.sort_order).all()
        governorates = Governorate.query.order_by(Governorate.sort_order).all()
        listing_types = [
            ('sale', 'بيع'), ('rent', 'إيجار'), ('investment', 'استثمار')
        ]
        return dict(categories=categories, governorates=governorates, listing_types=listing_types, now=datetime.utcnow)
    
    # Create tables and seed data
    with app.app_context():
        db.create_all()
        seed_data()
    
    return app

def seed_data():
    """Seed initial data if not exists"""
    # Seed categories - ALL ACTIVE
    categories_data = [
        {'slug':'real-estate','name':'Real Estate','name_ar':'العقارات','description':'بيع وشراء وإيجار العقارات','icon':'home','color':'#2563eb','sort_order':1},
        {'slug':'restaurants','name':'Restaurants','name_ar':'المطاعم','description':'مطاعم وكافيهات','icon':'utensils','color':'#ea580c','sort_order':2},
        {'slug':'pharmacies','name':'Pharmacies','name_ar':'الصيدليات','description':'صيدليات وخدمات صحية','icon':'capsules','color':'#16a34a','sort_order':3},
        {'slug':'markets','name':'Markets','name_ar':'الأسواق','description':'أسواق ومحلات تجارية','icon':'store','color':'#9333ea','sort_order':4},
        {'slug':'workshops','name':'Workshops','name_ar':'الورش','description':'ورش صيانة وخدمات','icon':'wrench','color':'#ca8a04','sort_order':5},
        {'slug':'internet','name':'Internet','name_ar':'شركات الإنترنت','description':'مزودي خدمة الإنترنت','icon':'wifi','color':'#0ea5e9','sort_order':6},
        {'slug':'doctors','name':'Doctors','name_ar':'الأطباء','description':'أطباء وعيادات','icon':'user-md','color':'#dc2626','sort_order':7},
        {'slug':'services','name':'Services','name_ar':'الخدمات','description':'خدمات متنوعة','icon':'hands-helping','color':'#059669','sort_order':8},
        {'slug':'cars','name':'Cars','name_ar':'السيارات','description':'بيع وشراء السيارات والمركبات','icon':'car','color':'#3b82f6','sort_order':9},
        {'slug':'cooling-ac','name':'Cooling & AC','name_ar':'التبريد والمكيفات','description':'مكيفات وخدمات التبريد والصيانة','icon':'snowflake','color':'#06b6d4','sort_order':10},
        {'slug':'bakery','name':'Bakery','name_ar':'المخابز','description':'مخابز ومعجنات وحلويات','icon':'bread-slice','color':'#d97706','sort_order':11},
        {'slug':'ro-water','name':'RO Water','name_ar':'محطات المياه','description':'محطات تنقية المياه وتوصيل المياه المعبأة','icon':'tint','color':'#0ea5e9','sort_order':12},
        {'slug':'companies','name':'Companies','name_ar':'الشركات','description':'شركات ومؤسسات تجارية','icon':'building','color':'#4f46e5','sort_order':13},
        {'slug':'trades','name':'Trades & Professions','name_ar':'أصحاب المهن','description':'جميع المهن والحرف اليدوية والخدمات المتنوعة','icon':'tools','color':'#8b5cf6','sort_order':14},
        {'slug':'appliances','name':'Electrical Appliances','name_ar':'الأجهزة الكهربائية','description':'أجهزة منزلية كهربائية - ثلاجات، غسالات، مكيفات، تلفزيونات','icon':'plug','color':'#ec4899','sort_order':15},
    ]
    for cdata in categories_data:
        if Category.query.filter_by(slug=cdata['slug']).first() is None:
            db.session.add(Category(
                slug=cdata['slug'], name=cdata['name'], name_ar=cdata['name_ar'],
                description=cdata['description'], icon=cdata['icon'], color=cdata['color'],
                is_active=True, sort_order=cdata['sort_order']
            ))
    
    # Seed governorates (Iraq)
    if Governorate.query.count() == 0:
        governorates = [
            Governorate(name='Baghdad', name_ar='بغداد', sort_order=1),
            Governorate(name='Basra', name_ar='البصرة', sort_order=2),
            Governorate(name='Mosul', name_ar='الموصل', sort_order=3),
            Governorate(name='Erbil', name_ar='أربيل', sort_order=4),
            Governorate(name='Sulaymaniyah', name_ar='السليمانية', sort_order=5),
            Governorate(name='Duhok', name_ar='دهوك', sort_order=6),
            Governorate(name='Najaf', name_ar='النجف', sort_order=7),
            Governorate(name='Karbala', name_ar='كربلاء', sort_order=8),
            Governorate(name='Kirkuk', name_ar='كركوك', sort_order=9),
            Governorate(name='Anbar', name_ar='الأنبار', sort_order=10),
            Governorate(name='Babil', name_ar='بابل', sort_order=11),
            Governorate(name='Dhi Qar', name_ar='ذي قار', sort_order=12),
            Governorate(name='Diyala', name_ar='ديالى', sort_order=13),
            Governorate(name='Wasit', name_ar='واسط', sort_order=14),
            Governorate(name='Muthanna', name_ar='المثنى', sort_order=15),
            Governorate(name='Qadisiyah', name_ar='القادسية', sort_order=16),
            Governorate(name='Maysan', name_ar='ميسان', sort_order=17),
            Governorate(name='Saladin', name_ar='صلاح الدين', sort_order=18),
        ]
        db.session.add_all(governorates)
    
    # Seed admin user
    if User.query.filter_by(phone='07833779833').count() == 0:
        admin = User(phone='07833779833', name='مدير المنصة', is_admin=True, is_active_account=True)
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Seed site settings
    if SiteSetting.query.filter_by(key='featured_listing_price').count() == 0:
        db.session.add(SiteSetting(key='featured_listing_price', value='25000', description='سعر الإعلان المميز (د.ع)'))
    if SiteSetting.query.filter_by(key='featured_listing_duration').count() == 0:
        db.session.add(SiteSetting(key='featured_listing_duration', value='7', description='مدة الإعلان المميز (أيام)'))
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
