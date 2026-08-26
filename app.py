import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Gerador Autopeças", layout="centered")

st.title("📸 Gerador de Capas p/ Marketplace")
st.write("Envie a foto crua da peça. O sistema vai remover o fundo e colocar no padrão 1200x1200 branco.")

# Área de upload
arquivo_usuario = st.file_uploader("Selecione a foto da peça", type=["jpg", "jpeg", "png"])

if arquivo_usuario is not None:
    st.image(arquivo_usuario, caption="Foto Original", width=300)
    
    if st.button("✨ Criar Foto Padrão Marketplace"):
        with st.spinner("A IA está removendo o fundo. Aguarde..."):
            # 1. Lê a imagem e remove o fundo
            foto_bytes = arquivo_usuario.getvalue()
            foto_sem_fundo_bytes = remove(foto_bytes)
            peca = Image.open(io.BytesIO(foto_sem_fundo_bytes)).convert("RGBA")
            
            # 2. Cria uma tela em branco 1200 x 1200
            fundo_branco = Image.new("RGB", (1200, 1200), "WHITE")
            
            # 3. Redimensiona a peça para ocupar bem o espaço (ex: 800x800)
            peca.thumbnail((800, 800))
            
            # 4. Calcula onde colar para ficar bem no meio
            pos_x = (1200 - peca.width) // 2
            pos_y = (1200 - peca.height) // 2
            
            # Cola a peça no fundo branco
            fundo_branco.paste(peca, (pos_x, pos_y), peca)
            
            # 5. Mostra o resultado na tela
            st.success("Foto processada com sucesso!")
            st.image(fundo_branco, caption="Pronta para o Anúncio", use_column_width=True)
            
            # 6. Prepara o botão de download
            buf = io.BytesIO()
            fundo_branco.save(buf, format="JPEG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="📥 Baixar Imagem Pronta",
                data=byte_im,
                file_name="capa_1200x1200.jpg",
                mime="image/jpeg"
            )
