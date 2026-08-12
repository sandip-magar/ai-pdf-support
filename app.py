import streamlit as st
import requests

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
# Make sure this matches your FastAPI server port!
API_URL = "http://127.0.0.1:8000" 

# ==========================================
# 🔌 API HELPER FUNCTIONS
# ==========================================

def register_user(username, password):
    response = requests.post(f"{API_URL}/api/auth/register", json={"username": username, "password": password})
    return response.status_code == 200

def login_user(username, password):
    # FastAPI OAuth2 usually expects form data for login
    response = requests.post(f"{API_URL}/api/auth/login", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def upload_pdf(token, uploaded_file):
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    response = requests.post(f"{API_URL}/api/ai/upload-pdf", headers=headers, files=files)
    return response.json()

def ask_ai(token, question):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/api/ai/ask-ai", headers=headers, json={"question": question})
    if response.status_code == 200:
        return response.json().get("answer")
    return "Error: Could not get response from AI."

def clear_history(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_URL}/api/ai/chat-history", headers=headers)
    return response.status_code == 200

# ==========================================
#  MAIN APP LOGIC
# ==========================================
def main():
    st.set_page_config(page_title="AI PDF Support", page_icon="🤖", layout="wide")
    st.title("🤖 AI PDF Support System")

    # 1. INITIALIZE SESSION STATE
    if "token" not in st.session_state:
        st.session_state.token = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 2. LOGIN SCREEN (If not logged in)
    if st.session_state.token is None:
        st.subheader("🔒 Login to Continue")
        
        # Simple toggle between Login and Register
        auth_mode = st.radio("Choose an option", ["Login", "Register"], horizontal=True)
        
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button(auth_mode)
            
            if submitted:
                if auth_mode == "Register":
                    if register_user(username, password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Username might exist.")
                else:
                    token = login_user(username, password)
                    if token:
                        st.session_state.token = token
                        st.session_state.chat_history = [] # Clear chat on new login
                        st.rerun() # ️ RELOAD THE PAGE TO SHOW THE APP!
                    else:
                        st.error("Invalid username or password.")

    # 3. MAIN DASHBOARD (The part you were missing!)
    else:
        # --- SIDEBAR ---
        with st.sidebar:
            st.success(f"Logged in as: *{st.session_state.get('username', 'User')}*")
            st.divider()
            
            # File Uploader
            st.subheader(" Upload PDF")
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
            if uploaded_file is not None:
                if st.button("Upload to AI Brain"):
                    with st.spinner("Processing PDF..."):
                        result = upload_pdf(st.session_state.token, uploaded_file)
                        st.success(result.get("message", "Uploaded!"))
            
            st.divider()
            
            # Clear Chat Button
            if st.button("️ Clear Chat History"):
                clear_history(st.session_state.token)
                st.session_state.chat_history = []
                st.rerun()
                
            st.divider()
            
            # Logout Button
            if st.button("🚪 Logout"):
                st.session_state.token = None
                st.session_state.chat_history = []
                st.rerun()

        # --- MAIN CHAT AREA ---
        st.subheader("💬 Chat with your Documents")
        
        # Display Chat History
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Ask a question about your PDF..."):
            # 1. Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # 2. Display user message immediately
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 3. Get AI Response
            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    response = ask_ai(st.session_state.token, prompt)
                    st.markdown(response)
            
            # 4. Add AI response to history
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# Run the app
if __name__ == "_main_":
    main()