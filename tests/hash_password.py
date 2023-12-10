import streamlit_authenticator as stauth

hashed_pass = stauth.Hasher(['tgitera@2023']).generate()
print(hashed_pass)