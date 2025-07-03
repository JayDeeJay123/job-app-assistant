
import streamlit as st

st.set_page_config(page_title="Job Application Assistant")

st.title("📄 Job Application Assistant")

st.write("Welcome! This app lets you upload a job application form and enter your personal details.")

# Input fields for user information
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

# File uploader for PDF form
uploaded_file = st.file_uploader("Upload a PDF job application form", type=["pdf"])

# Display success message if all fields are filled
if uploaded_file and name and email and phone:
    st.success("✅ Form uploaded and details entered!")
    st.write("In the next version, this app will fill the form and let you download it.")
elif uploaded_file:
    st.info("Please enter all your personal details to proceed.")
