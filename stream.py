import streamlit as st
import os
import json
from PIL import Image, UnidentifiedImageError

# Directories for storing images and data
PROFILE_FOLDER = 'profile_pictures'
UPLOADS_FOLDER = 'uploaded_photos'
DATA_FILE = 'bio_data.json'

# Create folders if they don't exist
os.makedirs(PROFILE_FOLDER, exist_ok=True)
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# Default data structure for biography
default_data = {
    "name": "Ma. Kishie Nicole C. Abian",
    "address": "Bagong Silang 1, Kaskag Village, Surigao City",
    "birthday": "September 17, 2005",
    "gender": "Female",
    "age": 19,
    "mother": "Catherine C. Abian",
    "father": "Nixon C. Abian",
    "sister": "Kiziah Nica C. Abian",
    "early_life": "I was born on September 17, 2005, in Surigao City...",
    "education": "I am currently attending Surigao del Norte State University...",
    "hobbies": "I enjoy reading books, listening to music, and singing...",
    "favorites": {
        "artists": ["Coldplay", "Paramore", "Hozier"],
        "books": ["A Walk To Remember", "The Chronicles of Narnia"]
    },
    "achievements": "Consistently received honors during high school...",
    "contact": {
        "instagram": "Waoozzzz",
        "facebook": "Kishie Abian",
        "gmail": "kishienicoleabian@gmail.com",
        "contact_number": "09262261633"
    }
}

# Load data from JSON file or initialize with default data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
else:
    data = default_data
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Save data to JSON file
def save_data(updated_data):
    with open(DATA_FILE, "w") as file:
        json.dump(updated_data, file, indent=4)

# App title and sidebar menu
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>Kishie's Dashboard</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("Navigation", ["About Me", "Upload Pictures"])

# "About Me" section
if menu == "About Me":
    st.markdown("<h2 style='text-align: center; background-color: #ffcccb; padding: 10px; border-radius: 10px;'>✨ Welcome To My Biography ✨</h2>", unsafe_allow_html=True)

    # Profile Picture Upload
    st.sidebar.header("Upload Profile Picture")
    profile_picture = st.sidebar.file_uploader("Choose a picture", type=["jpg", "jpeg", "png"])
    profile_path = os.path.join(PROFILE_FOLDER, "profile_picture.jpg")

    if profile_picture:
        with open(profile_path, "wb") as f:
            f.write(profile_picture.getbuffer())
        st.sidebar.success("Profile picture uploaded successfully!")

    # Display profile picture and editable biography
    col1, col2 = st.columns([1, 2])
    with col1:
        if os.path.exists(profile_path):
            try:
                img = Image.open(profile_path)
                st.image(img, caption="Profile Picture", use_container_width=True)
            except UnidentifiedImageError:
                st.warning("Invalid profile picture format.")
        else:
            st.write("No profile picture uploaded yet.")

    with col2:
        st.subheader("Edit Your Details")
        data["name"] = st.text_input("Name", data["name"])
        data["address"] = st.text_input("Address", data["address"])
        data["birthday"] = st.text_input("Birthday", data["birthday"])
        data["gender"] = st.text_input("Gender", data["gender"])
        data["age"] = st.number_input("Age", value=data["age"], step=1)
        data["mother"] = st.text_input("Mother's Name", data["mother"])
        data["father"] = st.text_input("Father's Name", data["father"])
        data["sister"] = st.text_input("Sister's Name", data["sister"])

    # Additional sections
    st.subheader("Biography")
    data["early_life"] = st.text_area("Early Life", data["early_life"])
    data["education"] = st.text_area("Education", data["education"])
    data["hobbies"] = st.text_area("Hobbies", data["hobbies"])
    data["achievements"] = st.text_area("Achievements", data["achievements"])

    # Contact Info
    st.subheader("Contact Information")
    data["contact"]["instagram"] = st.text_input("Instagram", data["contact"]["instagram"])
    data["contact"]["facebook"] = st.text_input("Facebook", data["contact"]["facebook"])
    data["contact"]["gmail"] = st.text_input("Gmail", data["contact"]["gmail"])
    data["contact"]["contact_number"] = st.text_input("Contact Number", data["contact"]["contact_number"])

    # Save Button
    if st.button("Save Changes"):
        save_data(data)
        st.success("Your changes have been saved!")

# "Upload Pictures" section
elif menu == "Upload Pictures":
    st.markdown("<h2 style='text-align: center; background-color: #d0f0c0; padding: 10px; border-radius: 20px;'>📷 Upload Your Pictures 📷</h2>", unsafe_allow_html=True)

    uploaded_file = st.sidebar.file_uploader("Upload a Picture", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        upload_path = os.path.join(UPLOADS_FOLDER, uploaded_file.name)
        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    # Display uploaded photos
    st.header("Photo Collection")
    uploaded_files = os.listdir(UPLOADS_FOLDER)
    if uploaded_files:
        for filename in uploaded_files:
            file_path = os.path.join(UPLOADS_FOLDER, filename)
            try:
                img = Image.open(file_path)
                st.image(img, caption=filename, use_container_width=True)
            except UnidentifiedImageError:
                st.warning(f"Cannot display {filename}. Unsupported format.")
    else:
        st.write("No photos uploaded yet.")
