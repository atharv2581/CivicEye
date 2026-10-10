import streamlit as st
import mysql.connector


def get_connection():
    try:
        config = st.secrets["database"]

        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            connection_timeout=10
        )

        return connection

    except mysql.connector.Error as error:
        raise RuntimeError(
            "Unable to connect to the CivicEye database."
        ) from error