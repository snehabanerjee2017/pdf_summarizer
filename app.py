import streamlit as st
import os

def main():

    st.set_page_config(page_title="PDF Summarizer")

    st.title("PDF Summarizing App")
    st.write("Upload a PDF file to summarize its content.")
    st.divider()

    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    submit = st.button("Summarize")


if __name__ == "__main__":
    main()