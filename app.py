import streamlit as st
import folium
from streamlit_folium import st_folium
import exifread
import sys
import os
import importlib.util

# --- CARREGAMENTO DE MÓDULOS  ---
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Caminho para os arquivos locais
base_path = os.path.dirname(os.path.abspath(__file__))
vs_path = os.path.join(base_path, "vector_store.py")

# função sem depender do sistema de importação
vector_store_mod = load_module_from_path("vector_store", vs_path)
create_or_load_vector_store = vector_store_mod.create_or_load_vector_store

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TrilhaCAR", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    [data-testid="stFileUploadDropzone"] { border: 2px dashed #1b6e41; background-color: #f8fff9; border-radius: 10px; }
    .stButton>button { background-color: #1b6e41; color: white; border-radius: 8px; }
    .stMarkdown { font-size: 18px; }
    div[data-testid="column"]:nth-of-type(2) { display: flex; justify-content: center; align-items: center; }
    </style>
""", unsafe_allow_html=True)

# HEADER
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image("Logo trilhaCar.png", width=300)
    except:
        st.title("🌿 TrilhaCAR")
        st.subheader("Seu ajudante para organizar o CAR")

st.markdown("<hr style='border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

# --- LÓGICA RAG ---
@st.cache_resource
def load_rag():
    # Certifique-se de que a pasta 'models/faiss_index' existe
    return create_or_load_vector_store(index_path="models/faiss_index")

vector_store = load_rag()

col_chat, col_mapa = st.columns([1.2, 1])

# COLUNA ESQUERDA: Chat
with col_chat:
    st.markdown("### 💬 Converse comigo")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Olá! Estou aqui para te ajudar a entender as regras do CAR. Pode me perguntar qualquer coisa sobre suas terras."}]

    chat_container = st.container(height=400, border=True)
    with chat_container:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Ex: Qual a distância certa de proteção perto do rio?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"): st.markdown(prompt)
            with st.spinner("Pensando na resposta..."):
                results = vector_store.similarity_search(prompt, k=1)
                contexto = results[0].page_content
                resposta = f"🌾 **Sobre a sua dúvida:**\n\nOlhei aqui nas regras:\n\n> *\"{contexto[:250]}...\"*\n\n**Dica:** Proteja a margem para evitar multas."
            with st.chat_message("assistant"): st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})

# COLUNA DIREITA: Mapa e Fotos
with col_mapa:
    st.markdown("### 🗺️ Minhas Fotos")
    def get_exif(f):
        try:
            f.seek(0)
            tags = exifread.process_file(f, details=False)
            if 'GPS GPSLatitude' in tags:
                d = lambda v: float(v.values[0].num)/float(v.values[0].den) + (float(v.values[1].num)/float(v.values[1].den)/60.0) + (float(v.values[2].num)/float(v.values[2].den)/3600.0)
                lat = d(tags['GPS GPSLatitude']) * (-1 if tags['GPS GPSLatitudeRef'].values == 'S' else 1)
                lon = d(tags['GPS GPSLongitude']) * (-1 if tags['GPS GPSLongitudeRef'].values == 'W' else 1)
                return lat, lon
        except: return None
        return None

    fotos = st.file_uploader("Envie as fotos da sua terra", accept_multiple_files=True, type=['jpg', 'jpeg'])
    if fotos:
        for f in fotos:
            coord = get_exif(f)
            if coord:
                st.success(f"✅ Foto '{f.name}' processada.")
                m = folium.Map(location=coord, zoom_start=18, tiles="CartoDB positron")
                folium.CircleMarker(location=coord, radius=10, color="green", fill=True).add_to(m)
                st_folium(m, width=400, height=250)
            else:
                st.error(f"⚠️ Foto '{f.name}' sem localização.")