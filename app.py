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

            start = numpy_data[0,0]
            pd_start = pd.to_datetime(start,utc=True)
            end = numpy_data[-1, 0]\\
            pd_end = pd.tp_datetime(end,utc=True)
            difference = pd_end - pd_start

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

            st.metric("Days", difference)
            
        except ValueError:
            st.warning("Upload Error")

if __name__ == "__main__":
    main()