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
    st.rerun()


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
    hsv_em_rgb = cv2.cvtColor(imagem_hsv, cv2.COLOR_HSV2RGB)

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.image(imagem_rgb, caption="Original", use_container_width=True)

    with coluna2:
        st.image(hsv_em_rgb, caption="HSV", use_container_width=True)

    ajuste_matiz = st.slider("Matiz", min_value=-179, max_value=179, value=0)
    ajuste_saturacao = st.slider("Saturação", min_value=-255, max_value=255, value=0)
    ajuste_brilho = st.slider("Brilho", min_value=-255, max_value=255, value=0)

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

    if st.button("Remover imagem"):
        remover_imagem()
