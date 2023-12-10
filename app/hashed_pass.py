import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Putu Pradnya A", "Asido Saputra"]
usernames = ["putupradnya", "asidosaputra"]
passwords = ["tgitera@2023", "tgitera@2023"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)