import streamlit as st


def create_session(user):

    st.session_state.logged_in = True

    st.session_state.employee = dict(user)


def logout():

    st.session_state.logged_in = False

    st.session_state.employee = None