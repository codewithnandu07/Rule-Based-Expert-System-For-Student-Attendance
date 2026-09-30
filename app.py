import streamlit as st
from datetime import datetime, time
import pandas as pd
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Smart Attendance - Rule Based", layout="centered")
st.title("Smart Attendance - Rule Based System")

st.info("**RULE 1:** IF Time > 09:15 THEN LATE ELSE PRESENT\n**RULE 2:** IF Face Detected THEN Allow\n**RULE 3:** IF Subject Selected THEN Mark")

# --- MANUAL INPUTS ---
col1, col2 = st.columns(2)

with col1:
    manual_subject = st.selectbox("Select Subject (Manual)", 
        ["Maths", "Science", "English", "Computer", "AI", "Python", "Other"])

with col2:
    manual_time = st.time_input("Select Time (Manual)", value=datetime.now().time())

late_time = time(9, 15)

# Show what rule will apply
st.metric("Selected Time", manual_time.strftime("%I:%M %p"))
st.metric("Late After", "09:15 AM")

# RULE 1 LOGIC for MANUAL TIME
if manual_time > late_time:
    status_preview = "LATE"
else:
    status_preview = "PRESENT"

st.warning(f"Selected: {manual_subject} | If you mark now, you will be marked **{status_preview}**")

# --- CAMERA ---
st.subheader("Live Camera Attendance")
camera_img = st.camera_input("Show Face to Mark Attendance")

if camera_img:
    img = Image.open(camera_img)
    img_array = np.array(img)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        st.error("❌ No Face Detected! Show face properly. Attendance NOT Marked.")
        st.stop()

    # FINAL MARKING WITH MANUAL VALUES
    if manual_time > late_time:
        status = "LATE"
        rule_text = f"IF Manual Time ({manual_time.strftime('%I:%M %p')}) > 09:15 THEN LATE"
    else:
        status = "PRESENT"
        rule_text = f"IF Manual Time ({manual_time.strftime('%I:%M %p')}) <= 09:15 THEN PRESENT"

    st.success(f"✅ Face Detected! Attendance Marked as {status} for {manual_subject}")
    st.balloons()

    df = pd.DataFrame([{
        "Subject": manual_subject,
        "Time": manual_time.strftime("%I:%M %p"),
        "Status": status,
        "Date": datetime.now().strftime("%d-%m-%Y"),
        "Face": f"{len(faces)} Detected"
    }])

    st.dataframe(df)
    st.download_button("Download Attendance CSV", df.to_csv(index=False), "attendance.csv", use_container_width=True)
    st.markdown(f"**RULE APPLIED:** {rule_text}")
    st.markdown(f"**RULE APPLIED:** IF Subject = {manual_subject} THEN Mark Attendance")

st.caption("Rule Based System | Manual Time + Manual Subject + Face Rule")
