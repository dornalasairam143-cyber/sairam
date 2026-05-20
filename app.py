import streamlit as st
import fitz  # PyMuPDF
import re
import io

st.set_page_config(page_title="PDF Markup Dashboard", page_icon="📄", layout="centered")

st.title("📄 PDF Markup Dashboard")
st.write("Upload your PDF, let the system process it, and download your marked-up copy instantly.")

def process_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page in doc:
        # Get detailed text layout blocks (includes fonts and line positions)
        text_page = page.get_text("dict")
        
        for block in text_page["blocks"]:
            if "lines" not in block:
                continue
                
            prev_line_bottom = None
            
            for line in block["lines"]:
                line_rect = fitz.Rect(line["bbox"])
                
                # --- 1. LINE SPACING CHECK (Pink Highlight) ---
                # Calculate spacing if there's a previous line in the same block
                if prev_line_bottom is not None:
                    line_gap = line_rect.y0 - prev_line_bottom
                    # Estimate line spacing multiplier based on font size
                    if line["spans"]:
                        font_size = line["spans"][0]["size"]
                        # Standard 1.5 spacing usually results in a baseline gap roughly 1.4 to 1.6 times font size
                        if font_size > 0 and not (1.35 <= (line_gap / font_size) <= 1.65):
                            # Draw a pink background highlight block between the lines
                            spacing_rect = fitz.Rect(line_rect.x0, prev_line_bottom, line_rect.x1, line_rect.y0)
                            if not spacing_rect.is_empty:
                                annot = page.add_rect_annot(spacing_rect)
                                annot.set_colors(stroke=(1, 0.75, 0.8), fill=(1, 0.75, 0.8)) # Pink
                                annot.set_opacity(0.4)
                                annot.update()
                                
                prev_line_bottom = line_rect.y1
                
                for span in line["spans"]:
                    span_rect = fitz.Rect(span["bbox"])
                    font_name = span["font"]
                    text_content = span["text"]
                    
                    # --- 2. FONT CHECK (Red Highlight) ---
                    # If font name does not match Segoe UI, mark it Red
                    if "segoe" not in font_name.lower():
                        annot = page.add_highlight_annot(span_rect)
                        annot.set_colors(stroke=(1, 0, 0)) # Red
                        annot.update()
                        
                    # --- 3. MISSING OR EXTRA SPACING CHECK (Yellow Highlight) ---
                    # Match missing space after comma/period: e.g., ",word" or ".word"
                    # Match extra consecutive spaces: e.g., "  "
                    if re.search(r"[,\.][A-Za-z0-9]", text_content) or "  " in text_content:
                        annot = page.add_highlight_annot(span_rect)
                        annot.set_colors(stroke=(1, 0.85, 0)) # Yellow
                        annot.update()

    output_stream = io.BytesIO()
    doc.save(output_stream)
    doc.close()
    return output_stream.getvalue()

# --- UI Dashboard ---
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.info("🔄 Processing PDF with new rules... Please wait.")
    
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
