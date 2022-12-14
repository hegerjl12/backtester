import pandas as pd
import streamlit as st
import numpy as np
import math


def main():

    st.set_page_config(
        page_title="Back Tester",
        page_icon="📈")

    st.title("TradingView Back Tester")

    raw_data = st.file_uploader("Upload TradingView Chart Export")

    if raw_data is not None:

        try:

            panda_data = pd.read_csv(raw_data)
            
            panda_data = panda_data.filter(['time', 'close', 'BUY', 'BUY EXIT'])
            
            numpy_data = panda_data.iloc[:,:].to_numpy()
    
         #   st.dataframe(numpy_data)
        
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
            winning_trade = 0
            commission_adjustment = 0
            buy_select = st.radio("Select Buy Trigger", ("Immediate", "Bar Close"))
            sell_select = st.radio("Select Sell Trigger", ("Immediate", "Bar Close"))
            stock_or_crypto = st.radio("Select Stock or Crypto", ("Stock", "Crypto"))
            if buy_select == "Immediate":
                buy_value = 2
            if buy_select == "Bar Close":
                buy_value = 1
            if sell_select == "Immediate":
                sell_value = 3
            if sell_select == "Bar Close":
                sell_value = 1
            if stock_or_crypto == "Sock":
                commission_adjustment = 0
            if stock_or_crypto == "Crypto":
                commission_adjustment = .0025
                
            initial_portfolio_value = st.number_input("Enter Portfolio Value at Start", min_value=1, value=5000)
            portfolio_value = initial_portfolio_value
            
            trade = 0
            planned_share_purchase = st.number_input('Enter Number of Shares Trading', min_value=2)

            for row in numpy_data:
                if not np.isnan(row[2]):
                    buy_price = row[buy_value]
                   # st.write(buy_price)
                    trading = True
                    trade = buy_price * planned_share_purchase
                    adj_in = trade * (1+commission_adjustment)
                    portfolio_value -= adj_in
               
                if not np.isnan(row[3]) and trading:
                    sell_price = row[sell_value]
                   # st.write(sell_price)
                    trading = False
                    trade_count += 1
            
                if not trading:
                    trade = (sell_price * planned_share_purchase)
                    adj_out = trade * (1-commission_adjustment)
                    portfolio_value += adj_out
                    profit += (adj_out - adj_in)
                    if (adj_out-adj_in) > 0:
                        winning_trade += 1
                    adj_in = 0
                    adj_out = 0
                    trade = 0
                    buy_price = 0
                    sell_price = 0
                    
            if trading:
                adj_out = adj_in
                portfolio_value += adj_out
                st.write('test')
                
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Profit", round(profit,2), delta=round(profit,2))

            with col2:
                st.metric("Portfolio Value", round(portfolio_value,2), delta=str(str(round((((portfolio_value/initial_portfolio_value)-1)*100),0)) + "%"))
            
            with col3:
                st.metric("Number of Trades", trade_count)

            with col4:
                st.metric("Days", str(difference))

            with col5:
                st.metric("Winning Trades", str(winning_trade))
            
        except ValueError:
            st.warning("Upload Error")

if __name__ == "__main__":
    main()
