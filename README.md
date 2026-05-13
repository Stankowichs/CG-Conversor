# Conversor RGB para HSV

Esse projeto é um conversor simples de imagem de RGB para HSV feito com Python. A ideia dele é permitir que a pessoa envie uma imagem pelo navegador, veja a imagem original, veja a imagem convertida para HSV e também consiga mexer nos valores de matiz, saturação e brilho usando alguns sliders bem simples.

Para fazer a interface foi usado o Streamlit, porque ele facilita bastante a criação de telas simples em Python. Para a parte de processamento da imagem foi usado o OpenCV, que faz a conversão entre os espaços de cor. Também foram usadas as bibliotecas NumPy e Pillow para ajudar a abrir a imagem enviada e transformar ela em um formato que o OpenCV consegue usar.

Para instalar as bibliotecas do projeto, primeiro é recomendado criar um ambiente virtual. Depois disso, basta instalar tudo que está no arquivo `requirements.txt`. Os comandos seriam:

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Depois que as dependências estiverem instaladas, o programa pode ser executado com o Streamlit usando este comando:

```bash
streamlit run app.py
```
