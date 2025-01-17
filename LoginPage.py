import streamlit as st
import pyrebase
from datetime import datetime
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

st.set_page_config(initial_sidebar_state="collapsed")
#Configuration key
firebaseConfig = {
    'apiKey': "AIzaSyCZPtwe0V9lMRTqUEqDcPKFALHwlefAmho",
    'authDomain': "courserecsystem-9a84c.firebaseapp.com",
    'projectId': "courserecsystem-9a84c",
    'databaseURL': "https://courserecsystem-9a84c-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "courserecsystem-9a84c.appspot.com",
    'messagingSenderId': "149618883518",
    'appId': "1:149618883518:web:0d6c9b123973bf5e1cd7ef",
    'measurementId': "G-YCFDDD2VLR"
}


# Check if the Firebase app is already initialized

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()  

db = firebase.database()
storage = firebase.storage()



st.markdown(
    """
    <style>
 
    
    .button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #b153ea;
        color: #fff;
        text-align: center;
        text-decoration: none;
        border-radius: 5px;
        cursor: pointer;
    }
   
    </style>
    """,
    unsafe_allow_html=True
)

# Display the shape using markdown
# st.markdown(shape_html, unsafe_allow_html=True)

def is_user_logged_in():
    try:
        user = auth.current_user
        return user is not None
    except:
        return False

def app():
    
    st.markdown("<h1 style='text-align: center; font-size:80px ; font-weight:30px;margin:0px;padding:0px; color: #6f07bb;'>Course Dekho.com</h1><br> <center><p style='font-size:25px;font-weight: normal; font-style:italic;color: #fffff'> ""Where learning meets personalisation""</center>", unsafe_allow_html=True)
    if not is_user_logged_in():
        # Select login or signup
        choice = option_menu(None,["Login", "Signup"],orientation='horizontal')


        if choice == "Signup":
            st.subheader("Signup")
            
            email = st.text_input("Email:")
            create_password = st.text_input("Create Password:", type="password")
            confirm_password = st.text_input("Confirm Password:", type="password")
            username = st.text_input('Username', value='Default')

            if create_password != confirm_password:
                st.error("Passwords do not match")
            if st.button("Signup"):
                try:
                    user = auth.create_user_with_email_and_password(email, confirm_password)
                    st.success('Your account is created sucessfully!')
                    st.title('Welcome' + username)
                    # Sign in
                    user = auth.sign_in_with_email_and_password(email, confirm_password)

                    # # Store the user's local ID in session_state
                    st.session_state.user_local_id = user['localId']
                    st.session_state.user = user

                    db.child(user['localId']).child("Username").set(username)
                    db.child(user['localId']).child("ID").set(user['localId'])
                   
                    # st.info('Login via login drop down selection')
                except Exception as e:
                    st.error(f"Signup Failed: {str(e)}")



        elif choice == "Login":
            
            st.subheader("Login")
            
            email = st.text_input("Email:")
            password = st.text_input("Password:", type="password")

            if st.button('Login'):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)

                    # user = auth.get_user_by_email(email)
                    # auth.get_user(user.uid)
                    # console.log(user)
                    st.success("Login Successful")
                    # st.markdown(f'<a href="Dashboard?user_id={user["localId"]}" target="_self">Get Started</a>', unsafe_allow_html=True)
                    st.markdown(f'<a href="Dashboard?{user["localId"]}" target="_self" class="button">Get Started</a>',unsafe_allow_html=True)
                    st.markdown( """
    <style>
    .button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #FFFFFF; 
        color: #FFFFFF;
        text-align: center;
        text-decoration: none;
        border-radius: 5px;
        cursor: pointer;
        font-color:white;
        text-decoration:none;
        border:1px solid #C88EE6;
    }
    .button:hover {
        background-color: #CDBFEC;
        text-decoration:none;
    }
    .button a {
        color: #fff; 
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
                except Exception as e:
                    st.error(f"Login Failed: {str(e)}")



if __name__ == "__main__":
    app()