import streamlit as st
import paramiko
import os
import joblib
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# ✅ MUST BE FIRST
st.set_page_config(page_title="Project Dashboard", layout="wide")

# ------------------ BACKEND CONFIG ------------------
# ✅ API KEYS (Add yours here)
OPENAI_API_KEY = "AIzaSyA2eIBmI8CG0tKqXldZw0Vtoeurs1bahg8"              # Optional if using OpenAI later
GEMINI_API_KEY = "AIzaSyA2eIBmI8CG0tKqXldZw0Vtoeurs1bahg8"     # Replace with your Gemini key

# ✅ SSH CONFIG (REMOTE SERVER LOGIN)
REMOTE_IP = "10.168.195.14"            # Replace with your Linux/Docker server IP
USERNAME = "root"                      # Replace with remote username
PASSWORD = "redhat"              # Replace with password

# ✅ Configure Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-pro")
except:
    gemini_model = None

# ✅ Load model
try:
    model = joblib.load("my_salary.pkl")
except:
    model = None

# ------------------ CONNECT VIA SSH ------------------
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh_client.connect(REMOTE_IP, username=USERNAME, password=PASSWORD, timeout=5)
    ssh_connected = True
except Exception as e:
    ssh_connected = False
    ssh_error = str(e)

# ------------------ STREAMLIT UI ------------------
st.title("📊 Summer Internship 2025 Multi-Project Dashboard")
tabs = st.tabs([
    "🖥️ Linux Commands",
    "🐳 Docker Manager",
    "🧠 ML Projects",
    "🟨 JS Projects"  
])


# ------------------ TAB 1: Linux ------------------
with tabs[0]:
    st.header("🖥️ Remote Linux Commands")
    if ssh_connected:
        command = st.selectbox("Choose command", [
            "date", "cal", "uptime", "whoami", "hostname", "df -h", "free -m",
            "uname -a", "id", "top -n 1 -b", "ps aux", "ls -l", "pwd", "who",
            "users", "netstat -tulpn", "ip a", "ip r", "ping -c 2 google.com",
            "cat /etc/os-release", "lsblk", "uptime", "last"
        ])
        if st.button("Execute"):
            _, stdout, _ = ssh_client.exec_command(command)
            st.code(stdout.read().decode())
    else:
        st.error(f"SSH connection failed: {ssh_error}")

# ------------------ TAB 2: Docker ------------------
with tabs[1]:
    st.header("🐳 Docker on Remote")
    if ssh_connected:
        action = st.selectbox("Choose Action", [
            "Show Containers", "Launch Container", "Stop Container", "Remove Container",
            "Show Images", "Pull Image", "Remove Image"
        ])
       
        if action == "Launch Container":
            image = st.text_input("Image name", key="img1")
            name = st.text_input("Container name", key="name1")
            if st.button("Launch"):
                ssh_client.exec_command(f"docker run -dit --name {name} {image}")
                st.success("Container launched.")
        elif action == "Stop Container":
            name = st.text_input("Container name to stop")
            if st.button("Stop"):
                ssh_client.exec_command(f"docker stop {name}")
                st.success("Container stopped.")
        elif action == "Remove Container":
            name = st.text_input("Container name to remove")
            if st.button("Remove"):
                ssh_client.exec_command(f"docker rm {name}")
                st.success("Container removed.")
        elif action == "Pull Image":
            image = st.text_input("Image name to pull")
            if st.button("Pull"):
                ssh_client.exec_command(f"docker pull {image}")
                st.success("Image pulled.")
        elif action == "Remove Image":
            image = st.text_input("Image name to remove")
            if st.button("Remove"):
                ssh_client.exec_command(f"docker rmi {image}")
                st.success("Image removed.")
        else:
            if st.button("Show"):
                cmd = "docker ps -a" if action == "Show Containers" else "docker images"
                _, stdout, _ = ssh_client.exec_command(cmd)
                st.code(stdout.read().decode())
    else:
        st.error(f"SSH connection failed: {ssh_error}")


# ------------------ TAB 3: ML Projects ------------------
with tabs[2]:
    st.header("🧠 ML Projects")

    selected_project = st.selectbox("Choose ML Project", [
        "Salary Predictor",
        "GR Calculator",
        "MindMat (AI Psychiatrist)"
    ])

    # ------------ Salary Predictor ------------
    if selected_project == "Salary Predictor":
        st.subheader("💼 Salary Prediction (Linear Regression)")
        experience = st.number_input("Enter your years of experience", min_value=0, max_value=50, value=1)
        if st.button("Predict Salary"):
            if model:
                salary = model.predict([[experience]])
                st.success(f"Estimated Salary: ₹ {int(salary[0])}")
            else:
                st.error("Model not found. Please check 'my_salary.pkl'.")

    # ------------ GR Calculator ------------
    elif selected_project == "GR Calculator":
        st.subheader("📘 GR (Grade Ratio) Calculator")

        st.markdown("Enter marks out of 100 for each subject:")
        subjects = ["Maths", "Physics", "Chemistry", "English", "Computer Science"]
        total_marks = 0

        for subject in subjects:
            marks = st.number_input(f"{subject} Marks", min_value=0, max_value=100, key=subject)
            total_marks += marks

        if st.button("Calculate GPA"):
            percentage = total_marks / len(subjects)
            gpa = round((percentage / 10), 2)
            st.info(f"📊 Percentage: {percentage:.2f}%")
            st.success(f"🎓 Estimated GPA: {gpa}")

    # ------------ MindMate AI Psychiatrist ------------
    elif selected_project == "MindMate (AI Psychiatrist)":
        st.subheader("🧠 MindMat - AI Mental Health Companion")
        st.markdown("Powered by Gemini AI (Gradio-like AI behavior)")
        message = st.text_area("🗣️ How are you feeling today?", height=100)

        if st.button("Get AI Response"):
            if gemini_model:
                response = gemini_model.generate_content(message)
                st.markdown("### 🤖 AI Says:")
                st.write(response.text)
            else:
                st.warning("❗ Gemini API key not configured properly.")


# ------------------ TAB 3: JavaScript Projects Dashboard ------------------
with tabs[3]:
    st.header("🟨 JavaScript Projects Dashboard")

    st.markdown("This section includes various JS-based tools like webcam photo capture, email sending, and WhatsApp messaging, all embedded inside your Streamlit app.")

    st.markdown("### 📸 Project 1: Capture Photo & Download")
    with st.expander("▶️ Open Camera + Download Tool"):
        try:
            components.html(open("photo.html", "r", encoding="utf-8").read(), height=500, scrolling=True)
        except FileNotFoundError:
            st.error("photo.html file not found!")

    st.markdown("### 📧 Project 2: Send Email via EmailJS")
    with st.expander("▶️ Open EmailJS Mailer"):
        try:
            components.html(open("email.html", "r", encoding="utf-8").read(), height=500, scrolling=False)
        except FileNotFoundError:
            st.error("email.html file not found!")

    st.markdown("### 📸📧 Project 3: Take Photo & Send via Gmail")
    with st.expander("▶️ Open Capture + Email Tool"):
        try:
            components.html(open("photogml.html", "r", encoding="utf-8").read(), height=600, scrolling=False)
        except FileNotFoundError:
            st.error("photogml.html file not found!")

    st.markdown("### 💬 Project 4: Send WhatsApp Message")
    with st.expander("▶️ Open WhatsApp Web Messenger"):
        try:
            components.html(open("whtsp.html", "r", encoding="utf-8").read(), height=400, scrolling=False)
        except FileNotFoundError:
            st.error("whtsp.html file not found!")
