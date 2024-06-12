from dependancies import *
from src.database_operations import Database
from src.utils import send_email

# conn = psycopg2.connect(host="localhost", dbname="user_database", user="postgres", password="postgres", port="5432")

# cur = conn.cursor()
db = Database()
db.connect()

# cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id SERIAL PRIMARY KEY,
#         first_name TEXT,
#         last_name TEXT,
#         dob TEXT,
#         email TEXT UNIQUE,
#         password TEXT,
#         reset_token TEXT,
#         reset_expiration TIMESTAMP
#     );
# """)

# conn.commit()

db.create_table()

def get_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    user_input = st.radio('Please select an option:', options=['Sign In', 'Sign Up'], horizontal=True)
    
    if user_input == 'Sign In':
        sign_in()
        if get_session_state().user:
            user_dashboard()
    
    elif user_input == 'Sign Up':
        sign_up()

def generate_reset_token():
    return secrets.token_urlsafe(32)

def send_reset_email(email, token):
    
    # smtp_server = "smtp.office365.com"
    # smtp_port = 587
    # smtp_username = "cognimindai@gmail.com"
    # smtp_password = ""

    
    # sender_email = "cognimindai@gmail.com"
    # recipient_email = email
    # subject = "Password Reset Request"
    # body = f'''
    #     To reset your password, click the following link:
    #     [Reset Link](http://localhost:8501/?page=reset&token={token})

    #     If you did not make this request, please ignore this email.
    # '''

    # try:
    #     with smtplib.SMTP(smtp_server, smtp_port) as server:
    #         server.starttls()
    #         server.login(smtp_username, smtp_password)

    #         msg = MIMEText(body)
    #         msg["Subject"] = subject
    #         msg["From"] = sender_email
    #         msg["To"] = recipient_email

    #         server.sendmail(sender_email, recipient_email, msg.as_string())

    #     st.success("Password reset link sent to your email. Check your inbox or spam.")
    # except Exception as e:
    #     st.error(f"Error sending email: {e}")
    if(send_email(email, token)):
        st.success("Password reset link sent to your email. Check your inbox or spam.")
    else:
        st.error(f"Error sending email")


def user_dashboard():
    st.title("User Dashboard")
    st.subheader("User Details")

    user = st.session_state.user
    st.write(f"First Name: {user[1]}")
    st.write(f"Last Name: {user[2]}")
    st.write(f"Email: {user[4]}")
    st.write(f"Date of Birth: {user[3]}")

    st.subheader("Update User Details")

    change_first_name = st.checkbox("Want to change your First Name?")

    if change_first_name:
        changefname = st.text_input("Enter your new First Name")
        
        changeb = st.button("Change First Name")
        if changeb:
            # cur.execute('''
            # UPDATE users
            # SET first_name = %s
            # WHERE id = %s
            # ''', (changefname,st.session_state.user[0]))
            # conn.commit()
            db.update_first_name(changefname, st.session_state.user[0])
            st.success("Updated Successfully")

    change_last_name = st.checkbox("Want to change your Last Name?")

    if change_last_name:
        changelname = st.text_input("Enter your new Last Name")
        changel = st.button("Change Last Name")
        if changel:
            # cur.execute('''
            # UPDATE users
            # SET last_name = %s
            # WHERE id = %s
            # ''', (changelname,st.session_state.user[0]))
            # conn.commit()
            db.update_last_name(changelname, st.session_state.user[0])
            st.success("Updated Successfully")

    change_first_name = st.checkbox("Want to change your DOB?")

    if change_first_name:
        changedob = st.text_input("Enter your new Date of Birth (YYYY-MM-DD)")
        
        changed = st.button("Change DOB")
        if changed:
            # cur.execute('''
            # UPDATE users
            # SET dob = %s
            # WHERE id = %s
            # ''', (changedob,st.session_state.user[0]))
            # conn.commit()
            db.update_dob(changedob, st.session_state.user[0])
            st.success("Updated Successfully")


    st.subheader("Actions")
    passbutton = st.checkbox("Change Password")

    if passbutton:
        oldpass = st.text_input("Enter your old password", type="password")
        newpass = st.text_input("Enter your new password", type="password")
        connpass = st.text_input("Confirm your new password", type="password")
        changep = st.button("Change")
        if changep:
            if hash_password(oldpass) != st.session_state.user[5]:
                st.error("Old password doesn't match")
            else:
                if newpass != connpass:
                    st.error("New and Confirm password don't match")
                else:
                    hashpass = hash_password(newpass)
                    # cur.execute('''
                    # UPDATE users
                    # SET password = %s
                    # WHERE id = %s
                    # ''', (hashpass,st.session_state.user[0]))
                    # conn.commit()
                    db.update_password(hashpass, st.session_state.user[0])
                    st.success("Password Updated Successfully")

    # if st.button("Log Out"):
    #     get_session_state().user = None
    #     st.success("Logged out successfully.")
    #     login()


def sign_in():
    st.header('User Login')
    email_login = st.text_input('Enter your email:', placeholder="abc123@email.com")
    password_login = st.text_input('Enter your Password:', placeholder="Password", type="password")

    forgot_password = st.checkbox("Forgot Password")

    if forgot_password:
        email_forgot = st.text_input("Enter your registered Gmail account:")
        if st.button("Reset Password"):
            
            #cur.execute('SELECT * FROM users WHERE email = %s', (email_forgot,))
            #user = cur.fetchone()
            user = db.select_user(email_forgot)

            if user:
                
                reset_token = generate_reset_token()
                reset_expiration = datetime.now() + timedelta(hours=1)

                # cur.execute('''
                #     UPDATE users
                #     SET reset_token = %s, reset_expiration = %s
                #     WHERE email = %s
                # ''', (reset_token, reset_expiration, email_forgot))
                # conn.commit()
                db.update_reset_token(reset_token, reset_expiration, email_forgot)

                
                send_reset_email(email_forgot, reset_token)

                st.session_state.user = user

            else:
                st.error("Email not found. Please enter a registered Gmail account.")
    else:
        if st.button("Login"):
        
            hashed_login_password = hash_password(password_login)

            # cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email_login, hashed_login_password))
            # user = cur.fetchone()
            user = db.login(email_login, hashed_login_password)

            if user:
                st.session_state.user = user
                st.success("Login successful.")
                return user
            else:
                st.error("Invalid email or password.")
                return None
            
def sign_up():
    st.header('Create a new Account')
    first_name = st.text_input('Enter your First Name:')
    last_name = st.text_input("Enter your Last Name:")
    dob = st.text_input('Enter your DOB(YYYY-MM-DD):', placeholder="01/01/1980")
    email_reg = st.text_input('Enter your email account:', placeholder="abc123@gmail.com")
    password_reg = st.text_input('Enter your password:', type="password")
    confirm_password = st.text_input('Confirm your password:', type="password")
    register=st.button('Register')

    if register == True:
        if password_reg != confirm_password:
            st.error('Passwords do not match. Please try again.')
        
        elif not email_reg.endswith('@gmail.com'):
            st.error('Please register with a Gmail account.')
        else:
            hashed_password = hash_password(password_reg)

            try:
                parameters = (first_name, last_name, dob, email_reg, hashed_password)
                # cur.execute("""
                #     INSERT INTO users (first_name, last_name, dob, email, password)
                #     VALUES (%s, %s, %s, %s, %s);
                #     """, parameters)
                
                # conn.commit()
                db.insert_user(first_name, last_name, dob, email_reg, hashed_password)

                st.success(f"Registration successful for {email_reg}!")
            
            except IntegrityError:
                    st.error(f"Email {email_reg} is already registered. Please use a different email.")