import pandas as pd
import streamlit as st
import numpy as np


def main():

    st.set_page_config(
        page_title="Back Tester",
        page_icon="📈")

    st.title("TradingView Back Tester")

    raw_data = st.file_uploader("Upload TradingView Chart Export")

    if raw_data is not None:

        try:

            panda_data = pd.read_csv(raw_data)
            numpy_data = panda_data.iloc[:,:].to_numpy()
    
            #st.dataframe(numpy_data)

            start = numpy_data[0,0]
            pd_start = pd.to_datetime(start,utc=True)
            end = numpy_data[-1, 0]
            pd_end = pd.to_datetime(end,utc=True)
            difference = pd_end - pd_start

            trading = False
            profit = 0
            buy_price = 0
            sell_price = 0
            initial_portfolio_value = st.number_input("Enter Portfolio Value at Start", min_value=1, value=5000)
            portfolio_value = initial_portfolio_value
            commission_adjustment = .003
            trade = 0
            planned_share_purchase = st.number_input('Enter Number of Shares Trading', min_value=2)

            for row in numpy_data:
                if not np.isnan(row[24]):
                    buy_price = row[4]
                    st.write(row[24])
                    st.write(buy_price)
                    trading = True
                    trade = buy_price * planned_share_purchase
                    portfolio_value -= (trade * (1+commission_adjustment))
               
                if not np.isnan(row[25]):
                    st.write(row[25])
                    sell_price = row[4]
                    trading = False
            
                if not trading:
                    #st.write(sell_price-buy_price)
                    profit += (sell_price-buy_price)
                    portfolio_value += ((sell_price * planned_share_purchase) * (1-commission_adjustment))
                    trade = 0
                    buy_price = 0
                    sell_price = 0
                
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Profit Per Share", round(profit,2), delta=round(profit,2))

            with col2:
                st.metric("Portfolio Value", round(portfolio_value,2), delta=str(str(round((portfolio_value-initial_portfolio_value),2)) + "$"))
            
            with col3:
                st.metric("Portfolio Value", round(portfolio_value,2), delta=str(str(round((((portfolio_value/initial_portfolio_value)-1)*100),0)) + "%"))

            with col4:
                st.metric("Days", str(difference))
            
        except ValueError:
            st.warning("Upload Error")

if __name__ == "__main__":
    main()
