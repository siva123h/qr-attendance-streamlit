import streamlit as st
import cv2
import pandas as pd
import numpy as np
from datetime import datetime

st.title("📷 QR Code Attendance System")

st.write("Scan a QR code using your camera to mark attendance.")

# Function to mark attendance
def mark_attendance(student_id):
    try:
        df = pd.read_csv("attendance.csv")
    except:
        df = pd.DataFrame(columns=["ID","Time"])

    if student_id not in df["ID"].values:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.loc[len(df)] = [student_id, now]
        df.to_csv("attendance.csv", index=False)
        return True
    return False


# Camera input
image = st.camera_input("Scan QR Code")

if image is not None:

    bytes_data = image.getvalue()
    np_img = np.frombuffer(bytes_data, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(frame)

    if data:
        success = mark_attendance(data)

        if success:
            st.success(f"Attendance marked for ID: {data}")
        else:
            st.warning("Attendance already marked")

    else:
        st.error("No QR Code detected")


st.subheader("📋 Attendance Records")

if st.button("Show Attendance"):
    try:
        df = pd.read_csv("attendance.csv")
        st.dataframe(df)
    except:
        st.warning("No attendance records found")