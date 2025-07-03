import streamlit as st
import json
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

st.set_page_config(page_title="Smart Job Application Assistant")
st.title("📄 Smart Job Application Assistant")

# Load user profile
try:
    with open("user_profile.json", "r") as f:
        user_profile = json.load(f)
    st.success("✅ Personal info loaded from profile.")
except FileNotFoundError:
    st.error("❌ user_profile.json not found. Please upload it to your GitHub repo.")
    user_profile = {}

# Display stored info
if user_profile:
    st.subheader("Your Stored Information")
    for key, value in user_profile.items():
        st.write(f"**{key}**: {value}")

# Upload document
st.subheader("Upload a Job Application Form")
uploaded_file = st.file_uploader("Upload a PDF form with fillable fields", type=["pdf"])

# Fill form fields using stored info
def fill_pdf_form_fields(pdf_file, data):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.update_page_form_field_values(writer.pages[0], fields=data)

    output_stream = BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

# Match fields (basic version)
def match_fields(profile):
    # Map common field names to profile keys
    field_map = {
        "Name": "Full Name",
        "Email": "Email Address",
        "Phone": "Phone Number",
        "Address": "Address",
        "City": "City",
        "Postcode": "Postcode",
        "Country": "Country"
    }
    return {form_field: profile.get(profile_key, "") for form_field, profile_key in field_map.items()}

# Process and download
if uploaded_file and user_profile:
    field_data = match_fields(user_profile)
    filled_pdf = fill_pdf_form_fields(uploaded_file, field_data)
    st.success("✅ Form fields filled using your stored info!")
    st.download_button(
        label="📥 Download Filled PDF",
        data=filled_pdf,
        file_name="filled_form.pdf",
        mime="application/pdf"
    )
