import os

css = """/* ===== Vision Platform - Complete CSS ===== */
/* RTL Civilized Design - Dark Blue & Gold */

:root {
    --primary: #0B1B2B;
    --primary-light: #162A3D;
    --accent: #D4A853;
    --accent-light: #E8C67A;
    --accent-dark: #B88D3E;
    --text: #F0F2F5;
    --text-muted: #8A9AAF;
    --success: #28A745;
    --warning: #F39C12;
    --danger: #E74C3C;
    --info: #3498DB;
    --bg: #0A0F1A;
    --card: #0F1624;
    --card-hover: #131B2D;
    --border: #1E2A40;
    --gradient-primary: linear-gradient(135deg, #0B1B2B 0%, #162A3D 100%);
    --gradient-accent: linear-gradient(135deg, #D4A853 0%, #B88D3E 100%);
    --shadow: 0 8px 32px rgba(0,0,0,0.4);
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.2);
    --radius: 12px;
    --radius-sm: 6px;
    --font-main: 'Tajawal', 'Noto Sans Arabic', 'Segoe UI', sans-serif;
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
    font-family: var(--font-main);
    background: var(--bg);
    color: var(--text);
    direction: rtl;
    line-height: 1.7;
    min-height: 100vh;
}
a { text-decoration: none; color: var(--accent); transition: 0.3s; }
a:hover { color: var(--accent-light); }
img { max-width: 100%; display: block; }
button { cursor: pointer; font-family: inherit; border: none; background: none; }
input, textarea, select { font-family: inherit; direction: rtl; }

.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.text-center { text-align: center; }
.mt-4 { margin-top: 24px; }

/* ===== Header ===== */
.main-header {
    background: var(--primary);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}
.header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 0;
    gap: 16px;
}
.logo {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 22px;
    font-weight: 800;
    color: var(--text);
}
.logo i { color: var(--accent); font-size: 24px; }
.header-nav { display: flex; gap: 28px; align-items: center; }
.header-nav a {
    color: var(--text-muted);
    font-size: 15px;
    font-weight: 500;
    position: relative;
    padding: 4px 0;
}
.header-nav a:hover, .header-nav a.active { color: var(--accent); }
.header-nav a.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    right: 0;
    width: 100%;
    height: 2px;
    background: var(--accent);
    border-radius: 2px;
}
.header-actions { display: flex; align-items: center; gap: 10px; }

/* Buttons */
.btn-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 22px;
    background: var(--gradient-accent);
    color: var(--primary);
    font-weight: 700;
    font-size: 14px;
    border-radius: var(--radius-sm);
    transition: 0.3s;
    border: none;
    cursor: pointer;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(212,168,83,0.3); }
.btn-outline {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border: 1px solid var(--border);
    color: var(--text);
    font-weight: 600;
    font-size: 14px;
    border-radius: var(--radius-sm);
    transition: 0.3s;
    background: transparent;
    cursor: pointer;
}
.btn-outline:hover { border-color: var(--accent); color: var(--accent); }
.btn-white {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 28px;
    background: #fff;
    color: var(--primary);
    font-weight: 700;
    font-size: 15px;
    border-radius: var(--radius-sm);
    transition: 0.3s;
    cursor: pointer;
}
.btn-white:hover { background: var(--accent-light); color: var(--primary); }
.btn-block { width: 100%; justify-content: center; }
.btn-sm { padding: 6px 14px; font-size: 13px; }
.btn-lg { padding: 14px 32px; font-size: 16px; }
.btn-icon {
    width: 36px; height: 36px;
    display: inline-flex; align-items: center; justify-content: center;
    border-radius: var(--radius-sm); background: var(--primary-light);
    color: var(--text); border: 1px solid var(--border); cursor: pointer; transition: 0.3s;
}
.btn-icon:hover { background: var(--accent); color: var(--primary); border-color: var(--accent); }

/* ===== Hero ===== */
.hero {
    background: var(--gradient-primary);
    padding: 80px 0 60px;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.hero-bg {
    position: absolute;
    top: -50%; right: -20%;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(212,168,83,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-content { position: relative; z-index: 1; max-width: 720px; margin: 0 auto; }
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(212,168,83,0.12);
    color: var(--accent);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 20px;
    border: 1px solid rgba(212,168,83,0.2);
}
.hero-badge i { font-size: 12px; }
.hero h1 {
    font-size: 40px;
    font-weight: 800;
    line-height: 1.3;
    margin-bottom: 16px;
}
.gradient-text { background: var(--gradient-accent); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-desc { font-size: 17px; color: var(--text-muted); max-width: 560px; margin: 0 auto 32px; }
.hero-shapes { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
.shape { position: absolute; border-radius: 50%; opacity: 0.06; background: var(--accent); }
.shape-1 { width: 300px; height: 300px; top: 10%; left: 5%; }
.shape-2 { width: 200px; height: 200px; bottom: 15%; right: 8%; }
.shape-3 { width: 150px; height: 150px; top: 40%; right: 20%; }

.hero-stats { display: flex; justify-content: center; gap: 40px; margin-top: 36px; }
.stat-item { text-align: center; }
.stat-num { display: block; font-size: 28px; font-weight: 800; color: var(--accent); }
.stat-label { font-size: 13px; color: var(--text-muted); }

/* Search box inside hero */
.hero-search { margin-top: 32px; }
.search-box {
    display: flex;
    align-items: center;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 6px 6px 6px 6px;
    box-shadow: var(--shadow);
    max-width: 640px;
    margin: 0 auto;
}
.search-box i { color: var(--text-muted); padding: 0 14px; font-size: 16px; }
.search-box input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text);
    padding: 12px 8px;
    font-size: 15px;
    outline: none;
}
.search-box button { border-radius: var(--radius-sm); padding: 10px 24px; }

/* ===== Sections & Tags ===== */
.section { padding: 60px 0; }
.section-header { margin-bottom: 32px; text-align: center; }
.section-tag {
    display: inline-block;
    background: rgba(212,168,83,0.1);
    color: var(--accent);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
    border: 1px solid rgba(212,168,83,0.2);
}
.section-header h2 { font-size: 28px; font-weight: 700; margin-bottom: 6px; }
.section-header p { color: var(--text-muted); font-size: 15px; }

/* ===== Categories ===== */
.categories-section { padding: 60px 0; background: var(--bg); }
.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 20px;
}
.category-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 20px;
    text-align: center;
    transition: 0.3s;
    display: block;
    color: var(--text);
    position: relative;
}
.category-card:hover { transform: translateY(-6px); border-color: var(--accent); box-shadow: var(--shadow); }
.category-icon {
    width: 56px; height: 56px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 14px;
    font-size: 22px;
}
.category-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.category-card p { font-size: 13px; color: var(--text-muted); margin-bottom: 10px; line-height: 1.5; }
.active-badge {
    display: inline-block;
    background: rgba(40,167,69,0.12);
    color: var(--success);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid rgba(40,167,69,0.2);
}

/* ===== Listings ===== */
.listings-section { padding: 60px 0; }
.listings-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }
.listing-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: 0.3s;
}
.listing-card:hover { transform: translateY(-4px); border-color: var(--accent); box-shadow: var(--shadow); }
.listing-image { display: block; position: relative; height: 200px; background: var(--primary-light); overflow: hidden; }
.listing-image img { width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }
.listing-card:hover .listing-image img { transform: scale(1.05); }
.no-image {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    color: var(--text-muted); font-size: 40px;
}
.listing-category {
    position: absolute;
    top: 12px; right: 12px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    z-index: 2;
}
.listing-type {
    position: absolute;
    top: 12px; left: 12px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    z-index: 2;
}
.listing-type.sale { background: var(--danger); color: #fff; }
.listing-type.rent { background: var(--info); color: #fff; }
.featured-badge {
    position: absolute;
    bottom: 12px; left: 12px;
    background: var(--accent);
    color: var(--primary);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: flex; align-items: center; gap: 4px;
}
.listing-body { padding: 20px; }
.listing-price { margin-bottom: 8px; }
.listing-price .price { font-size: 18px; font-weight: 800; color: var(--accent); }
.listing-price .price small { font-size: 13px; font-weight: 600; }
.listing-title { font-size: 16px; font-weight: 700; margin-bottom: 8px; line-height: 1.4; }
.listing-title a { color: var(--text); }
.listing-title a:hover { color: var(--accent); }
.listing-location { font-size: 13px; color: var(--text-muted); margin-bottom: 12px; display: flex; align-items: center; gap: 6px; }
.listing-location i { color: var(--accent); }
.listing-meta { display: flex; gap: 16px; font-size: 13px; color: var(--text-muted); }
.listing-meta span { display: flex; align-items: center; gap: 4px; }
.listing-meta i { color: var(--accent); font-size: 13px; }

/* ===== CTA ===== */
.cta-section { padding: 60px 0; }
.cta-box {
    background: var(--gradient-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    flex-wrap: wrap;
    position: relative;
    overflow: hidden;
}
.cta-box::before {
    content: '';
    position: absolute;
    top: -50%; left: -20%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(212,168,83,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.cta-content { position: relative; z-index: 1; }
.cta-content h2 { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.cta-content p { color: var(--text-muted); font-size: 15px; }
.cta-box .btn-white { position: relative; z-index: 1; }

/* ===== How It Works ===== */
.how-it-works { padding: 60px 0; background: var(--bg); }
.steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; }
.step-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 32px 24px;
    text-align: center;
    transition: 0.3s;
    position: relative;
}
.step-card:hover { border-color: var(--accent); transform: translateY(-4px); }
.step-num {
    position: absolute;
    top: 16px; left: 16px;
    font-size: 32px;
    font-weight: 800;
    color: rgba(212,168,83,0.12);
    line-height: 1;
}
.step-icon {
    width: 56px; height: 56px;
    border-radius: 50%;
    background: rgba(212,168,83,0.1);
    color: var(--accent);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    margin: 0 auto 16px;
}
.step-card h3 { font-size: 17px; font-weight: 700; margin-bottom: 8px; }
.step-card p { font-size: 14px; color: var(--text-muted); line-height: 1.6; }

/* ===== Auth Pages ===== */
.auth-section {
    min-height: calc(100vh - 140px);
    display: flex; align-items: center; justify-content: center;
    padding: 40px 0;
    background: var(--gradient-primary);
    position: relative; overflow: hidden;
}
.auth-section::before {
    content: '';
    position: absolute; top: -50%; left: -20%;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(212,168,83,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.auth-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 40px 36px;
    width: 100%; max-width: 440px;
    position: relative; z-index: 1;
    box-shadow: var(--shadow);
}
.auth-logo { text-align: center; margin-bottom: 28px; }
.auth-logo i { font-size: 42px; color: var(--accent); }
.auth-logo h1 { font-size: 22px; font-weight: 800; margin-top: 8px; }
.auth-logo p { color: var(--text-muted); font-size: 14px; margin-top: 4px; }
.auth-subtitle { text-align: center; color: var(--text-muted); font-size: 14px; margin-bottom: 24px; }
.form-group { margin-bottom: 18px; }
.form-group label { font-size: 13px; font-weight: 600; color: var(--text-muted); margin-bottom: 6px; display: block; }
.form-group input, .form-group select, .form-group textarea {
    width: 100%; padding: 12px 16px;
    background: var(--primary-light); border: 1px solid var(--border);
    border-radius: var(--radius-sm); color: var(--text); font-size: 15px;
    transition: 0.3s;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
    outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(212,168,83,0.15);
}
.form-group input::placeholder, .form-group textarea::placeholder { color: var(--text-muted); opacity: 0.5; }
.input-icon { position: relative; display: flex; align-items: center; }
.input-icon i { position: absolute; left: 14px; color: var(--text-muted); font-size: 14px; pointer-events: none; }
.input-icon input { padding-left: 38px !important; }
.checkbox-label { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--text-muted); cursor: pointer; }
.checkbox-label input[type=checkbox] { width: 18px; height: 18px; accent-color: var(--accent); cursor: pointer; }
.form-hint { display: block; font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.auth-links { text-align: center; margin-top: 20px; font-size: 14px; color: var(--text-muted); }
.auth-links a { color: var(--accent); font-weight: 600; }
.auth-footer { text-align: center; margin-top: 20px; font-size: 14px; }
.auth-footer a { color: var(--accent); font-weight: 600; }
.auth-footer i { margin-left: 6px; }

/* Alerts */
.alert { padding: 10px 14px; border-radius: var(--radius-sm); font-size: 14px; margin-bottom: 16px; border: 1px solid transparent; }
.alert-success { background: rgba(40,167,69,0.12); color: #28A745; border-color: rgba(40,167,69,0.25); }
.alert-danger  { background: rgba(231,76,60,0.12); color: #E74C3C; border-color: rgba(231,76,60,0.25); }
.alert-warning { background: rgba(243,156,18,0.12); color: #F39C12; border-color: rgba(243,156,18,0.25); }
.alert-info    { background: rgba(52,152,219,0.12); color: #3498DB; border-color: rgba(52,152,219,0.25); }

/* ===== Dashboard / Admin ===== */
.dashboard-section { padding: 40px 0; background: var(--bg); min-height: calc(100vh - 140px); }
.admin-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; flex-wrap: wrap; gap: 16px; }
.admin-header h1 { font-size: 24px; font-weight: 700; display: flex; align-items: center; gap: 10px; }
.admin-header h1 i { color: var(--accent); }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; margin-bottom: 28px; }
.stat-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 20px;
    transition: 0.3s;
}
.stat-card:hover { border-color: var(--accent); }
.stat-card .stat-label { font-size: 13px; color: var(--text-muted); margin-bottom: 6px; }
.stat-card .stat-value { font-size: 26px; font-weight: 800; color: var(--accent); }
.admin-table-wrap { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; margin-bottom: 24px; }
.admin-table-wrap table { width: 100%; border-collapse: collapse; }
.admin-table-wrap th, .admin-table-wrap td { padding: 12px 16px; text-align: right; font-size: 14px; border-bottom: 1px solid var(--border); }
.admin-table-wrap th { background: var(--primary-light); color: var(--accent); font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
.admin-table-wrap tr:last-child td { border-bottom: none; }
.admin-table-wrap tr:hover td { background: var(--primary-light); }
.status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-left: 6px; }
.status-dot.active { background: var(--success); }
.status-dot.pending { background: var(--warning); }
.status-dot.rejected { background: var(--danger); }
.actions-cell { white-space: nowrap; }
.actions-cell a, .actions-cell button { padding: 4px 10px; border-radius: var(--radius-sm); font-size: 12px; margin-left: 4px; border: 1px solid var(--border); color: var(--text); background: var(--primary-light); transition: 0.2s; cursor: pointer; }
.actions-cell a:hover, .actions-cell button:hover { border-color: var(--accent); color: var(--accent); }

/* ===== Footer ===== */
.main-footer { background: var(--primary); border-top: 1px solid var(--border); padding: 48px 0 0; }
.footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 32px; margin-bottom: 32px; }
.footer-brand h2 { font-size: 20px; font-weight: 800; display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.footer-brand h2 i { color: var(--accent); }
.footer-brand p { font-size: 14px; color: var(--text-muted); line-height: 1.7; }
.footer-links h4 { font-size: 15px; font-weight: 700; margin-bottom: 14px; color: var(--text); }
.footer-links ul { list-style: none; }
.footer-links li { margin-bottom: 8px; }
.footer-links a { font-size: 14px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }
.footer-links a:hover { color: var(--accent); }
.footer-bottom { border-top: 1px solid var(--border); padding: 20px 0; text-align: center; font-size: 13px; color: var(--text-muted); }

/* ===== Toast / Flash ===== */
.toast {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 18px; border-radius: var(--radius-sm);
    font-size: 14px; font-weight: 600;
    box-shadow: var(--shadow); animation: slideIn 0.4s ease;
    min-width: 280px; max-width: 400px;
}
.toast.success { background: var(--success); color: #fff; }
.toast.danger { background: var(--danger); color: #fff; }
.toast.warning { background: var(--warning); color: #fff; }
.toast.info { background: var(--info); color: #fff; }
@keyframes slideIn { from { transform: translateX(-20px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

/* ===== Scrollbar ===== */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ===== Responsive ===== */
@media (max-width: 1024px) {
    .footer-grid { grid-template-columns: 1fr 1fr; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .cta-box { flex-direction: column; text-align: center; }
}
@media (max-width: 768px) {
    .header-inner { flex-wrap: wrap; }
    .header-nav { display: none; }
    .hero h1 { font-size: 28px; }
    .hero-stats { gap: 24px; }
    .search-box { flex-direction: column; padding: 12px; }
    .search-box input { width: 100%; text-align: center; }
    .categories-grid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }
    .listings-grid { grid-template-columns: 1fr; }
    .steps-grid { grid-template-columns: 1fr; }
    .footer-grid { grid-template-columns: 1fr; }
    .auth-box { padding: 28px 20px; }
    .admin-header { flex-direction: column; text-align: center; }
    .admin-table-wrap { overflow-x: auto; }
    .admin-table-wrap table { min-width: 600px; }
}
@media (max-width: 480px) {
    .container { padding: 0 16px; }
    .hero-stats { flex-direction: column; gap: 16px; }
    .categories-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
    .stats-grid { grid-template-columns: 1fr; }
}
"""
with open("/nfs/102295708/temp/vision/static/css/main.css", "w", encoding="utf-8") as f:
    f.write(css)
print("CSS written", len(css.splitlines()), "lines")
