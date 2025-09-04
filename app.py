import streamlit as st
import pandas as pd
import os

# python -m streamlit run app.py
def main():
    st.title('Upload file')

    menu = ["Home", "Dataset", "Document Files"] 
    choice = st.sidebar.selectbox('Menu', menu)
    parent_dir = r"C:\Users\esian\Desktop\Kafe\data\raw_data"

    if choice == "Home":
        st.subheader("Home")

        # File uploader outside the form for instant preview
        file_uploads = st.file_uploader("Upload Excel or CSV file", type=["csv", "xls", "xlsx"], accept_multiple_files=True)
        
        df = None
        for file_upload in file_uploads:
            if file_upload is not None:
                try:
                    if file_upload.name.endswith(('xls', 'xlsx')):
                        df = pd.read_excel(file_upload)
                    else:
                        df = pd.read_csv(file_upload)
                    
                    st.info("Preview of uploaded file:")
                    st.dataframe(df)

                except Exception as e:
                        st.error(f"Error reading file: {e}")

        # Add a separate button for saving
        if st.button("Submit"):
            if file_uploads:
                for file_upload in file_uploads:
                    file_path = os.path.join(parent_dir, file_upload.name)
                    with open(file_path, "wb") as f:
                        f.write(file_upload.getbuffer())
                st.success("All files saved successfully!")
            else:
                st.warning("Please upload at least one file before submitting.")


    elif choice == "Dataset":
        st.subheader("Dataset section coming soon!")

    else:
        st.subheader("Document Files section coming soon!")

if __name__ == "__main__":
    main()
