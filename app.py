import pandas as pd
import streamlit as st
import numpy as np


def main():

    st.set_page_config(
        page_title="Back Tester",
        page_icon="🧮")

    st.title("TradingView Back Tester")

    raw_data = st.file_uploader("Upload TradingView Chart Export")

    if raw_data is not None:

        try:

            panda_data = pd.read_csv(raw_data)
            numpy_data = panda_data.iloc[:,:].to_numpy()
    
            st.dataframe(numpy_data)

            for row in numpy_data:
                if not np.isnan(row[24]):
                    st.write(row[24])
            
        except ValueError:
            st.warning("Upload Error")

if __name__ == "__main__":
    main()