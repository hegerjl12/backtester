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
    
            #st.dataframe(numpy_data)

            start = numpy_data.iloc[0,0]
            end = numpy_data.iloc[-1, 0]

            trading = False
            profit = 0
            buy_price = 0
            sell_price = 0

            for row in numpy_data:
                if not np.isnan(row[24]):
                    buy_price = row[4]
                    trading = True
                
                if not np.isnan(row[25]):
                    sell_price = row[4]
                    trading = False
            
                if not trading:
                    #st.write(sell_price-buy_price)
                    profit += (sell_price-buy_price)
                    buy_price = 0
                    sell_price = 0
                
            st.metric("Profit", round(profit,2))
            st.metric("Days", end-start)
            
        except ValueError:
            st.warning("Upload Error")

if __name__ == "__main__":
    main()