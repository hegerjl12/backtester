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
            adj_in = 0
            adj_out = 0
            buy_price = 0
            sell_price = 0
            trade_count = 0
            buy_select = st.radio("Select Buy Trigger", ("Immediate", "Bar Close"))
            sell_select = st.radio("Select Sell Trigger", ("Immediate", "Bar Close"))
            if buy_select == "Immediate":
                buy_value = 24
            if buy_select == "Bar Close":
                buy_value = 3
            if sell_select == "Immediate":
                sell_value = 25
            if sell_select == "Bar Close":
                sell_value = 4
            initial_portfolio_value = st.number_input("Enter Portfolio Value at Start", min_value=1, value=5000)
            portfolio_value = initial_portfolio_value
            commission_adjustment = .0025
            trade = 0
            planned_share_purchase = st.number_input('Enter Number of Shares Trading', min_value=2)

            for row in numpy_data:
                if row[24] != 'nan':
                    buy_price = row[buy_value]
                    st.write(row)
                    st.write(buy_price)
                    trading = True
                    trade = buy_price * planned_share_purchase
                    adj_in = trade * (1+commission_adjustment)
                    portfolio_value -= adj_in
               
                if row[25] != 'nan':
                    sell_price = row[sell_value]
                    st.write(sell_price)
                    trading = False
                    trade_count += 1
            
                if not trading:
                    adj_out = ((sell_price * planned_share_purchase) * (1-commission_adjustment))
                    portfolio_value += adj_out
                    profit += (adj_out - adj_in)
                    adj_in = 0
                    adj_out = 0
                    trade = 0
                    buy_price = 0
                    sell_price = 0
                    
                
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Profit", round(profit,2), delta=round(profit,2))

            with col2:
                st.metric("Portfolio Value", round(portfolio_value,2), delta=str(str(round((((portfolio_value/initial_portfolio_value)-1)*100),0)) + "%"))
            
            with col3:
                st.metric("Number of Trades", trade_count)

            with col4:
                st.metric("Days", str(difference))
            
        except ValueError:
            st.warning("Upload Error")

if __name__ == "__main__":
    main()
