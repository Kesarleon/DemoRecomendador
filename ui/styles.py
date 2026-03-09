"""ui/styles.py — CSS de branding de Rosa Oliva."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

c = config.BRAND_COLORS

CSS_STYLES = f"""
<style>
    .stApp {{
        background-color: {c['cream']};
    }}

    [data-testid="stSidebar"] {{
        background-color: {c['olive']};
    }}

    .stButton>button {{
        background-color: {c['jade']};
        color: #FFFFFF;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        background-color: {c['jade_dark']};
        color: #FFFFFF;
    }}

    h1, h2, h3 {{
        color: {c['charcoal']};
        font-family: 'Helvetica Neue', sans-serif;
    }}

    .metric-card {{
        background-color: white;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid {c['jade']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 8px;
    }}

    .product-card {{
        background-color: white;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border-top: 3px solid {c['gold']};
    }}

    .badge-oferta {{
        background-color: #FF6B35;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78em;
        font-weight: 700;
        display: inline-block;
        margin-top: 4px;
    }}

    .badge-material {{
        background-color: {c['cream']};
        color: {c['charcoal']};
        border: 1px solid {c['gold']};
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.78em;
        display: inline-block;
        margin-right: 4px;
    }}

    div[data-testid="stNotification"][kind="success"] p {{
        color: white;
    }}
</style>
"""
