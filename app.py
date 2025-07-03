import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont

# Set up the page
st.set_page_config(page_title="Job Application Assistant")
st.title("📄 Job Application Assistant")

st.write("Enter your personal details and upload a PDF form. The app will fill in your info and let you download the completed form.")

# Input fields
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF form", type=["pdf"])

# Function to fill PDF
def fill_pdf(base_pdf, name, email, phone):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Example positions (you can adjust these)
    can.drawString(100, 700, f"Name: {name}")
    can.drawString(100, 680, f"Email: {email}")
    can.drawString(100, 660, f"Phone: {phone}")

    can.save()
    packet.seek(0)

    # Merge with original PDF
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(base_pdf)
    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    for i in range(1, len(existing_pdf.pages)):
        output.add_page(existing_pdf.pages[i])

    output_stream = BytesIO()
    output.write(output_stream)
    output_stream.seek(0)
    return output_stream

# Process and download
if uploaded_file and name and email and phone:
    filled_pdf = fill_pdf(uploaded_file, name, email, phone)
    st.success("✅ Form filled successfully!")
    st.download_button(
        label="📥 Download Filled PDF",
        data=filled_pdf,
        file_name="filled_form.pdf",
        mime="application/pdf"
    )
elif uploaded_file:
    st.info("Please enter all your personal details to fill the form.")
