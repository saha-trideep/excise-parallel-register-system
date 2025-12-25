import streamlit as st

def check_password():
    """Returns True if the user has entered the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "admin089":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.markdown("""
            <style>
            .login-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 3rem;
                background: linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%);
                border-radius: 20px;
                border: 2px solid #f4b942;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                max-width: 450px;
                margin: auto;
                margin-top: 100px;
            }
            .login-title {
                color: #f4b942;
                font-size: 2rem;
                font-weight: 800;
                margin-bottom: 20px;
                text-align: center;
            }
            .stTextInput > div > div > input {
                background-color: #1a1f2e !important;
                color: white !important;
                border: 1px solid #f4b942 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">🔐 Secure Access</div>', unsafe_allow_html=True)
        st.text_input(
            "Enter Password to Access Registers", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Password incorrect. Please try again.")
        st.info("System protected by Admin Security.")
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

def login_required():
    if not check_password():
        st.stop()
