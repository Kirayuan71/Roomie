"""Streamlit deployment wrapper for the bundled Roomie React application."""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Roomie · 室友搭子", page_icon="🏡", layout="wide", initial_sidebar_state="collapsed")
# Keep the Streamlit host stationary. Only the React document scrolls.
# CSS owns the frame height, so its size cannot grow with its own contents.
st.markdown("""<style>
[data-testid="stHeader"],footer{display:none}
html,body,[data-testid="stApp"],[data-testid="stAppViewContainer"],
[data-testid="stMain"]{height:100dvh;overflow:hidden!important}
.block-container,[data-testid="stMainBlockContainer"]{
 padding:0!important;max-width:none!important;height:100dvh;
}
[data-testid="stVerticalBlock"]{gap:0!important}
[data-testid="stElementContainer"]:has(.stMarkdown){display:none}
iframe{border:0;width:100%;height:100dvh!important;display:block}
</style>""", unsafe_allow_html=True)

dist = Path(__file__).parent / "dist"
if not (dist / "index.html").exists():
    st.error("缺少前端构建产物，请先运行 npm ci && npm run build，并将 dist 目录一同部署。")
    st.stop()
# A component serves the built files on the same stable Streamlit origin.
roomie = components.declare_component("roomie_app", path=str(dist))
roomie(default=None, key="roomie")
