import streamlit as st
from profile_stalker import summarize_linkedin


st.title("Linkedin Profile Stalker")

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "facts" not in st.session_state:
    st.session_state.facts = []

form_values = {
    "name": "",
}


def summarize_linkedin_wrapper(name: str):
    print(f"Checking {name} linkedin profile...")
    response = summarize_linkedin(name)
    st.session_state.summary = (
        response.summary if hasattr(response, "summary") else ""
    )
    st.session_state.facts = (response.facts if hasattr(response, "facts") else [])
    st.rerun(scope="app")


with st.form(key="linkedin_form"):
    form_values["name"] = st.text_input("Enter a name")
    submitted = st.form_submit_button("Check Profile")
    if submitted:
        if not all(form_values.values()):
            st.warning("Please enter a name!")
        else:
            summarize_linkedin_wrapper(form_values["name"])

if st.session_state.summary != "":
    print("found profile, writing summary...")
    st.subheader("Summary")
    st.write(st.session_state.summary)
    st.session_state.summary = ""
    st.subheader("Interesting Facts:")
    for fact in st.session_state.facts:
        st.write(fact)
