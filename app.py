import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Smart Attendance", layout="wide")
st.title("📚 Smart Attendance - Cloud Link Version")

if 'attendance' not in st.session_state:
    st.session_state.attendance = []

# Inputs
col1, col2, col3 = st.columns(3)
with col1:
    subject = st.text_input("Subject", "aiml")
    student_name = st.text_input("Student Name", "nandu")
with col2:
    start_time = st.time_input("Class START", value=datetime.strptime("11:00 AM", "%I:%M %p").time())
with col3:
    end_time = st.time_input("Class END", value=datetime.strptime("12:00 PM", "%I:%M %p").time())

st.divider()

# CLOUD CAMERA - Works on link!
picture = st.camera_input("📸 Take Photo for Attendance")

face_percent = 0
pil_img = None

if picture:
    # Face detection on cloud photo
    image = Image.open(picture)
    pil_img = image
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x,y,w,h = faces[0]
        face_percent = min(100, int((w*h)/(img_array.shape[0]*img_array.shape[1]/1.5)*100)+60)
        cv2.rectangle(img_array, (x,y), (x+w, y+h), (0,255,0), 2)
        st.image(img_array, caption=f"Face Detected: {face_percent}%", width=400)
        st.metric("Face Match", f"{face_percent}%")
    else:
        st.warning("No face found! Try again closer")
        st.image(image, width=400)
        face_percent = 0

if st.button("✅ MARK ATTENDANCE", type="primary"):
    if pil_img is None:
        st.error("Take photo first!")
    else:
        now = datetime.now()
        now_time = now.time()
        is_late = now_time > end_time

        if is_late:
            late_mins = (datetime.combine(datetime.today(), now_time) - datetime.combine(datetime.today(), end_time)).seconds // 60
            status = "LATE - Present"
            late_text = f"{late_mins} min late"
        else:
            status = "Present - On Time"
            late_text = "On Time"

        record = {
            "Date": now.strftime("%d-%m-%Y"),
            "Time": now.strftime("%I:%M:%S %p"),
            "Class Time": f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}",
            "Subject": subject,
            "Name": student_name,
            "Status": status,
            "Late By": late_text,
            "Face %": face_percent,
            "Count": len(st.session_state.attendance)+1
        }
        st.session_state.attendance.append(record)
        st.balloons()
        if is_late:
            st.warning(f"LATE! {late_text}")
        else:
            st.success(f"On Time! Marked at {now.strftime('%I:%M:%S %p')}")

if st.session_state.attendance:
    st.divider()
    st.subheader("📋 Records")
    df = pd.DataFrame(st.session_state.attendance)
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "attendance.csv", "text/csv")
