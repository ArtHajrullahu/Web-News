import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Lista e zgjeruar me më shumë artikuj dhe foto specifike
KOMPJUTERAT_DATA = [
    {
        "Titulli": "Laptop Dell XPS 15 - Fuqia e Procesimit", 
        "Linku": "https://pcworld.al/dell-xps-15-review/", 
        "Data": "15 Maj 2026",
        "Foto": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=600"
    },
    {
        "Titulli": "HP Spectre x360 - Dizajn Premium", 
        "Linku": "https://pcworld.al/hp-spectre-x360/", 
        "Data": "12 Maj 2026",
        "Foto": "https://images.unsplash.com/photo-1544731612-de7f96afe55f?w=600"
    },
    {
        "Titulli": "MacBook Pro M3 - Standardi i Ri i Apple", 
        "Linku": "https://pcworld.al/macbook-pro-m3-chip/", 
        "Data": "10 Maj 2026",
        "Foto": "https://images.unsplash.com/photo-1517336714460-45b2ed035c67?w=600"
    },
    {
        "Titulli": "Asus ROG Zephyrus - Bisha e Gaming", 
        "Linku": "https://pcworld.al/asus-rog-zephyrus-g14/", 
        "Data": "08 Maj 2026",
        "Foto": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600"
    },
    {
        "Titulli": "Lenovo ThinkPad X1 - Partneri i Biznesit", 
        "Linku": "https://pcworld.al/lenovo-thinkpad-x1-carbon/", 
        "Data": "05 Maj 2026",
        "Foto": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600"
    },
    {
        "Titulli": "Microsoft Surface Laptop 5 - Elegancë dhe Lehtësi", 
        "Linku": "https://pcworld.al/microsoft-surface-laptop-5/", 
        "Data": "03 Maj 2026",
        "Foto": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600"
    }
]

# 2. Funksioni i Scraping
def scrape_pcworld():
    news_items = list(KOMPJUTERAT_DATA) 
    try:
        url = "https://pcworld.al/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all(['h1', 'h2', 'h3'], limit=10)
            for tag in articles:
                title = tag.get_text(strip=True)
                link_tag = tag.find('a') or tag.parent.find('a')
                if len(title) > 15 and link_tag:
                    news_items.append({
                        "Titulli": title,
                        "Linku": link_tag['href'],
                        "Data": "Lajm i Ri",
                        "Foto": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=600"
                    })
        return pd.DataFrame(news_items).drop_duplicates(subset=['Titulli'])
    except:
        return pd.DataFrame(KOMPJUTERAT_DATA)

# --- KONFIGURIMI I DIZAJNIT ---
st.set_page_config(page_title="PCWorld News Pro", layout="wide")

# Stilimi CSS për dizajn të hapur dhe tituj të zinj
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1 { color: #000000 !important; font-weight: 800; }
    .news-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #F1F3F5;
        transition: transform 0.3s ease;
    }
    .news-card:hover { transform: translateY(-5px); }
    .title-link { color: #1A73E8; text-decoration: none; font-size: 1.2em; font-weight: bold; }
    .date-text { color: #ADB5BD; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🛠 Kontrollet")
search_query = st.sidebar.text_input("🔍 Kërko për artikuj:")

if st.sidebar.button("🔄 Rifresko Lajmet"):
    st.session_state.df = scrape_pcworld()
    st.rerun()

# --- FAQJA KRYESORE ---
st.title("📰 PCWorld.al - News Feed Profesional")
st.write("**Afati i dorëzimit:** 20 Maj 2026")

if 'df' not in st.session_state:
    st.session_state.df = scrape_pcworld()

df_to_show = st.session_state.df
if search_query:
    df_to_show = df_to_show[df_to_show['Titulli'].str.contains(search_query, case=False, na=False)]

# Shfaqja në dy kolona
col1, col2 = st.columns(2)

for i, (index, row) in enumerate(df_to_show.iterrows()):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f'''
            <div class="news-card">
                <img src="{row['Foto']}" style="width:100%; border-radius:10px; margin-bottom:15px; height:200px; object-fit:cover;">
                <p class="date-text">📅 {row['Data']}</p>
                <a href="{row['Linku']}" target="_blank" class="title-link">{row['Titulli']}</a>
                <p style="margin-top:10px;"><a href="{row['Linku']}" target="_blank" style="color:#000; font-size:0.9em;">Lexo më shumë →</a></p>
            </div>
            ''', unsafe_allow_html=True)

# Export
csv = df_to_show.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 Shkarko të dhënat (CSV)", data=csv, file_name="lajmet_pcworld.csv")