import streamlit as st
import fitz  # PyMuPDF
import re
import io

st.set_page_config(page_title="PDF Markup Dashboard", page_icon="📄", layout="centered")

st.title("📄 PDF Markup Dashboard")
st.write("Upload your PDF, let the system process it, and download your marked-up copy instantly.")

# List of common merged words from your original script
MERGED_WORDS = ["tothe", "inthe", "ofthe", "forthe", "onthe", "atthe", "bythe", "fromthe", "withthe", "andthe", "isnot", "arethe"]

def process_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page in doc:
        # --- 1. LINE SPACING CHECK (Pink Highlight between lines) ---
        text_page_dict = page.get_text("dict")
        for block in text_page_dict["blocks"]:
            if "lines" not in block:
                continue
            prev_line_bottom = None
            for line in block["lines"]:
                line_rect = fitz.Rect(line["bbox"])
                if prev_line_bottom is not None:
                    line_gap = line_rect.y0 - prev_line_bottom
                    if line["spans"]:
                        font_size = line["spans"][0]["size"]
                        if font_size > 0 and not (1.35 <= (line_gap / font_size) <= 1.65):
                            spacing_rect = fitz.Rect(line_rect.x0, prev_line_bottom, line_rect.x1, line_rect.y0)
                            if not spacing_rect.is_empty:
                                annot = page.add_rect_annot(spacing_rect)
                                annot.set_colors(stroke=(1, 0.75, 0.8), fill=(1, 0.75, 0.8)) # Pink
                                annot.set_opacity(0.3)
                                annot.update()
                prev_line_bottom = line_rect.y1

                # --- 2. FONT CHECK (Red Highlight on individual span) ---
                for span in line["spans"]:
                    if "segoe" not in span["font"].lower():
                        span_rect = fitz.Rect(span["bbox"])
                        annot = page.add_highlight_annot(span_rect)
                        annot.set_colors(stroke=(1, 0.3, 0.3)) # Red
                        annot.update()

        # --- 3. WORD-SPECIFIC CHECKS (Yellow / Turquoise Highlights on EXACT words) ---
        words_list = page.get_text("words")
        
        for w in words_list:
            word_rect = fitz.Rect(w[0], w[1], w[2], w[3])
            word_str = w[4].strip()
            
            # Skip empty strings
            if not word_str:
                continue
                
            # Check for common merged words -> Turquoise Highlight
            if word_str.lower() in MERGED_WORDS:
                annot = page.add_highlight_annot(word_rect)
                annot.set_colors(stroke=(0, 0.75, 0.75)) # Turquoise
                annot.update()
                continue
            
            # --- STRICT PATTERN TO IGNORE ALL NUMERICAL POINTS ---
            is_missing_space = False
            
            # 1. First, check if the string contains a punctuation mark directly touching letters
            if re.search(r"[A-Za-z]+[, \.][A-Za-z]+", word_str) or re.search(r"[A-Za-z]+[,\.]", word_str) or re.search(r"[,\.][A-Za-z]+", word_str):
                
                # 2. Strict Filter: If the string is a date, decimal point, percentage, or mathematical code, IGNORE it.
                # This drops matches like "06.28.2025", "1.5", "45%", "7-16", "04/24/"
                if not re.search(r"\d+[\.,/\-]\d+", word_str):
                    
                    # 3. Double Check: Ensure there is actually alpha text present next to the punctuation mark
                    # (This prevents lone numbers or symbols from turning yellow)
                    if re.search(r"[A-Za-z]", word_str):
                        is_missing_space = True
            
            if is_missing_space:
                annot = page.add_highlight_annot(word_rect)
                annot.set_colors(stroke=(1, 0.85, 0)) # Yellow
                annot.update()

    output_stream = io.BytesIO()
    doc.save(output_stream)
    doc.close()
    return output_stream.getvalue()

# --- UI Dashboard ---
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.info("🔄 Processing PDF with updated pattern filtering... Please wait.")
    
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
