import avpkg
import streamlit as st

def main():
    st.set_page_config(page_title="Resumen de Visitas",
                       page_icon="🌴",
                       layout="centered",
                       initial_sidebar_state="auto",
                       menu_items=None)

    st.write("## Resumen de Visitas de Campo")

    uploaded_files = st.file_uploader("Subir el archivo",
                                     type=["m4a", "ogg"
                                           ],
                                     accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            try:
                fname = avpkg.get_summary(uploaded_file)
    
                with open(fname, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
    
                # Create a download button
                st.download_button(
                    label="Descargar: " + fname[5:],
                    data=pdf_bytes,
                    file_name=fname,
                    mime="application/pdf",  # PDFs
                )
    
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # os.remove("converted_audio.wav")

if __name__ == "__main__":
    main()