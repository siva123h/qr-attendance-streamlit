import streamlit as st
import cv2
import pandas as pd
import numpy as np
import os
from datetime import datetime

st.set_page_config(page_title="QR Attendance System", layout="centered")

st.title("📷 QR Code Attendance System")

st.write("Scan a QR code using your camera to mark attendance.")

# Create folder for photos
if not os.path.exists("photos"):
    os.makedirs("photos")

# Function to mark attendance
def mark_attendance(student_id, frame):

    try:
        df = pd.read_csv("attendance.csv")
    except:
        df = pd.DataFrame(columns=["ID", "Time", "Image"])

    if student_id not in df["ID"].values:

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        image_name = f"photos/{student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(image_name, frame)

        df.loc[len(df)] = [student_id, now, image_name]

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

        success = mark_attendance(data, frame)

        if success:
            st.success(f"Attendance marked for ID: {data}")
            st.image(frame, caption="Stored Image")

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
