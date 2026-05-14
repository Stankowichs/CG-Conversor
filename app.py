import cv2
import numpy as np
import streamlit as st
from PIL import Image


st.set_page_config(page_title="Conversor RGB para HSV", layout="centered")


if "imagem_rgb" not in st.session_state:
    st.session_state.imagem_rgb = None

if "chave_upload" not in st.session_state:
    st.session_state.chave_upload = 0

def remover_imagem():
    st.session_state.imagem_rgb = None
    st.session_state.chave_upload += 1

    for nome in ["matiz", "saturacao", "brilho"]:
        st.session_state[nome] = 0
        st.session_state[f"{nome}_zerado"] = False
        st.session_state[f"{nome}_valor_anterior"] = 0

def download(imagem_rgb):
    imagem_bgr = cv2.cvtColor(imagem_rgb, cv2.COLOR_RGB2BGR)
    sucesso, buffer = cv2.imencode(".png", imagem_bgr)
    if sucesso:
        return buffer.tobytes()
    return None

for nome in ["matiz", "saturacao", "brilho"]:
    if nome not in st.session_state:
        st.session_state[nome] = 0

    if f"{nome}_zerado" not in st.session_state:
        st.session_state[f"{nome}_zerado"] = False

    if f"{nome}_valor_anterior" not in st.session_state:
        st.session_state[f"{nome}_valor_anterior"] = 0 

def resetar_ajustes():
    for nome in ["matiz", "saturacao", "brilho"]:
        st.session_state[nome] = 0
        st.session_state[f"{nome}_zerado"] = False
        st.session_state[f"{nome}_valor_anterior"] = 0

def alternar_zero(nome):
    chave_slider = nome
    chave_checkbox = f"{nome}_zerado"
    chave_anterior = f"{nome}_valor_anterior"

    if st.session_state[chave_checkbox]:
        st.session_state[chave_anterior] = st.session_state[chave_slider]
        st.session_state[chave_slider] = 0
    else:
        st.session_state[chave_slider] = st.session_state[chave_anterior]

st.title("RGB para HSV")

arquivo_enviado = st.file_uploader(
    "Enviar imagem",
    type=["png", "jpg", "jpeg"],
    key=f"upload_imagem_{st.session_state.chave_upload}",
)


if arquivo_enviado is not None:
    imagem_pil = Image.open(arquivo_enviado).convert("RGB")
    st.session_state.imagem_rgb = np.array(imagem_pil)


if st.session_state.imagem_rgb is not None:
    imagem_rgb = st.session_state.imagem_rgb

    imagem_hsv = cv2.cvtColor(imagem_rgb, cv2.COLOR_RGB2HSV)

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.image(imagem_rgb, caption="Original", use_container_width=True)

    with coluna2:
        st.image(imagem_hsv, caption="HSV", use_container_width=True)

    col_m1, col_m2 = st.columns([3, 1])

    with col_m1:
        ajuste_matiz = st.slider(
            "Matiz",
            min_value=-179,
            max_value=179,
            value=0,
            key="matiz",
            disabled=st.session_state.matiz_zerado
        )

    with col_m2:
        st.checkbox(
            "Zerar",
            key="matiz_zerado",
            on_change=alternar_zero,
            args=("matiz",)
        )
    
    col_s1, col_s2 = st.columns([3, 1])

    with col_s1:
        ajuste_saturacao = st.slider(
            "Saturação",
            min_value=-255,
            max_value=255,
            value=0,
            key="saturacao",
            disabled=st.session_state.saturacao_zerado
        )
    
    with col_s2:
        st.checkbox(
            "Zerar ",
            key="saturacao_zerado",
            on_change=alternar_zero,
            args=("saturacao",)
        )

    col_b1, col_b2 = st.columns([3, 1])

    with col_b1:
        ajuste_brilho = st.slider(
            "Brilho",
            min_value=-255,
            max_value=255,
            value=0,
            key="brilho",
            disabled=st.session_state.brilho_zerado
        )

    with col_b2:
        st.checkbox(
            "Zerar  ",
            key="brilho_zerado",
            on_change=alternar_zero,
            args=("brilho",)
        )

    hsv_ajustado = imagem_hsv.astype(np.int16)

    hsv_ajustado[:, :, 0] = (hsv_ajustado[:, :, 0] + ajuste_matiz) % 180

    hsv_ajustado[:, :, 1] = np.clip(
        hsv_ajustado[:, :, 1] + ajuste_saturacao, 0, 255
    )
    hsv_ajustado[:, :, 2] = np.clip(
        hsv_ajustado[:, :, 2] + ajuste_brilho, 0, 255
    )

    hsv_ajustado = hsv_ajustado.astype(np.uint8)

    imagem_ajustada = cv2.cvtColor(hsv_ajustado, cv2.COLOR_HSV2RGB)

    st.image(imagem_ajustada, caption="Resultado", use_container_width=True)

    st.button("Resetar ajustes", on_click=resetar_ajustes)

    dados_download = download(imagem_ajustada)

    if dados_download is not None:
        st.download_button(
            label="Baixar imagem ajustada",
            data=dados_download,
            file_name="imagem_hsv_ajustada.png",
            mime="image/png"
        )

    st.button("Remover imagem", on_click=remover_imagem)