import streamlit as st
import fitz  # PyMuPDF
import re
import io

st.set_page_config(page_title="PDF Markup Dashboard", page_icon="📄", layout="centered")

st.title("📄 PDF Markup Dashboard")
st.write("Upload your PDF, let the system process it, and download your marked-up copy instantly.")

# List of merged words from your VBA script
MERGED_WORDS = ["tothe", "inthe", "ofthe", "forthe", "onthe", "atthe", "bythe", "fromthe", "withthe", "andthe", "isnot", "arethe"]

def process_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page in doc:
        # Get all words on the page with coordinates
        text_page = page.get_text("words") 
        
        for w in text_page:
            word_str = w[4]
            rect = fitz.Rect(w[0], w[1], w[2], w[3])
            
            # Check merged words -> Turquoise Highlight
            if word_str.lower() in MERGED_WORDS:
                annot = page.add_highlight_annot(rect)
                annot.set_colors(stroke=(0, 0.7, 0.7)) 
                annot.update()
                
            # Check for missing spaces after punctuation (e.g., ",a" or ".b") -> Yellow Highlight
            if re.search(r"[,\.][A-Za-z0-9]", word_str):
                annot = page.add_highlight_annot(rect)
                annot.set_colors(stroke=(1, 0.8, 0)) 
                annot.update()

    output_stream = io.BytesIO()
    doc.save(output_stream)
    doc.close()
    return output_stream.getvalue()

# --- UI Dashboard ---
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.info("🔄 Processing PDF... Please wait.")
    
    try:
        processed_pdf_bytes = process_pdf(uploaded_file.read())
        st.success("✅ Work Complete!")
        
        original_name = uploaded_file.name.rsplit('.', 1)[0]
        output_filename = f"{original_name}_MARKUP.pdf"
        
        st.download_button(
            label="📥 Download Marked-up PDF",
            data=processed_pdf_bytes,
            file_name=output_filename,
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
