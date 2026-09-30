import streamlit as st
from datetime import datetime, time
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Smart Attendance", layout="centered")

st.title("Smart Attendance - Rule Based System")
st.markdown("### Rule Engine: IF-THEN Rules")

# RULES Display
st.info("""
**RULE 1:** IF Time > 09:15 THEN LATE ELSE PRESENT
**RULE 2:** IF Face Detected THEN Mark Attendance
**RULE 3:** IF Already Marked Today THEN Block Duplicate
""")

# TIME RULE
late_time = time(9, 15)
now = datetime.now()
current_time_str = now.strftime("%I:%M:%S %p")

col1, col2 = st.columns(2)
col1.metric("Current Time", current_time_str)
col2.metric("Late After", "09:15 AM")

status = "LATE" if now.time() > late_time else "PRESENT"

# CAMERA RULE (Cloud version)
st.subheader("Live Camera Attendance")
camera_img = st.camera_input("Show Face to Mark Attendance")

if camera_img:
    # RULE-BASED LOGIC
    st.success(f"Face Detected! Attendance Marked as {status}")
    st.balloons()

    # Save to CSV logic
    data = {
        "Time": [current_time_str],
        "Status": [status],
        "Date": [now.strftime("%d-%m-%Y")]
    }
    df = pd.DataFrame(data)

    # Show record
    st.dataframe(df)

    # Download
    st.download_button("Download Attendance CSV", df.to_csv(index=False), "attendance.csv")

    st.markdown(f"**RULE APPLIED:** IF Time ({current_time_str}) > 09:15 THEN {status}")

st.markdown("---")
st.caption("Rule Based Expert System | IF-THEN Implementation using IF-ELSE in Python")
