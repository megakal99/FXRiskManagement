import streamlit as st
import plotly.graph_objects as go
from datetime import date,timedelta


###################################################################""

def GraphDaily(Column,percHedge):
 # Create figure
 fig = go.Figure()
 fig.add_trace(go.Scatter(
    x=dailyDataHedge['Date'],
    y=round(dailyDataHedge[Column],4),
    mode='lines',#'lines+markers'
    name='hedged exchange rate',
    line=dict(color='blue'),
    hoverinfo='text',
    hovertext=dailyDataHedge.apply(lambda row: f"Date: {row['Date']}<br>Hedge Rate: {round(row[Column],4)}", axis=1)
))

 fig.add_trace(go.Scatter(
    x=dailyDataHedge['Date'],
    y=dailyDataHedge['Close'],
    mode='lines',#'lines+markers'
    name='Market exchange rate',
    line=dict(color='red'),
    hoverinfo='text',
    hovertext=dailyDataHedge.apply(lambda row: f"Date: {row['Date']}<br>Market Rate: {row['Close']}", axis=1)
))

 fig.add_trace(go.Scatter(
    x=dailyDataHedge['Date'],
    y=dailyDataHedge[Column],
    fill='tonexty',
    mode='none',
    name='Fill Areas between hedge rate and market rate',
    fillcolor='blue', # blue when hedgeRate0 is above Close
    visible='legendonly'
))
 if percHedge==0:
  # Customize layout
  fig.update_layout(
    title=f"Hedged Rate Covering {st.session_state.hedgePercent*100}% of Exposure vs Market Exchange Rate",
    xaxis_title="Date",
    yaxis_title="Exchange Rate",
    legend_title="Legend",
    template="plotly_white"
  )
 else:
  # Customize layout
  fig.update_layout(
    title=f"Hedged Rate Covering {(1-st.session_state.hedgePercent)*100}% of Exposure vs Market Exchange Rate",
    xaxis_title="Date",
    yaxis_title="Exchange Rate",
    legend_title="Legend",
    template="plotly_white"
  ) 
 # Show figure in Streamlit
 st.plotly_chart(fig)

def GraphPeriod(Column,percHedge):
 # Create figure
 fig = go.Figure()
 fig.add_trace(go.Scatter(
    x=frequentDataHedge['Date'],
    y=round(frequentDataHedge[Column],4),
    mode='lines',#'lines+markers'
    name='hedged exchange rate',
    line=dict(color='blue'),
    hoverinfo='text',
    hovertext=frequentDataHedge.apply(lambda row: f"Date: {row['Date']}<br>Hedge Rate: {round(row[Column],4)}", axis=1)
))

 fig.add_trace(go.Scatter(
    x=frequentDataHedge['Date'],
    y=frequentDataHedge['Close'],
    mode='lines',#'lines+markers'
    name='Market exchange rate',
    line=dict(color='red'),
    hoverinfo='text',
    hovertext=frequentDataHedge.apply(lambda row: f"Date: {row['Date']}<br>Market Rate: {row['Close']}", axis=1)
))

 fig.add_trace(go.Scatter(
    x=frequentDataHedge['Date'],
    y=frequentDataHedge[Column],
    fill='tonexty',
    mode='none',
    name='Fill Areas between hedge rate and market rate',
    fillcolor='blue', # blue when hedgeRate0 is above Close
    visible='legendonly'
))
 if percHedge==0:
  # Customize layout
  fig.update_layout(
    title=f"Hedged Rate Covering {st.session_state.hedgePercent*100}% of Exposure vs Market Exchange Rate",
    xaxis_title="Date",
    yaxis_title="Exchange Rate",
    legend_title="Legend",
    template="plotly_white"
  )
 else:
  # Customize layout
  fig.update_layout(
    title=f"Hedged Rate Covering {(1-st.session_state.hedgePercent)*100}% of Exposure vs Market Exchange Rate",
    xaxis_title="Date",
    yaxis_title="Exchange Rate",
    legend_title="Legend",
    template="plotly_white"
  ) 

 # Show figure in Streamlit
 st.plotly_chart(fig)

def Recap(percHedge):
  if percHedge==0:
    # Calculate the count of cases where hedgedRate >= Close
    count_hitting_market = (dailyDataHedge['hedgedRate0'] >= dailyDataHedge['Close']).sum()
    # Total number of data points
    total_cases = dailyDataHedge.shape[0]
    # Calculate percentage
    percentage_beating_market = (count_hitting_market / total_cases) * 100 if total_cases > 0 else 0
    # Format the percentage to two decimal places
    percentage_beating_market = round(percentage_beating_market, 2)
    # Generate a professional conclusion
    if percentage_beating_market >= 50:
        conclusion = "The hedging strategy has successfully outperformed the market exchange rate in over {:.2f}% of cases. This suggests a strong performance in mitigating risk and capitalizing on favorable market conditions.".format(percentage_beating_market)
    else:
        conclusion = "The hedging strategy has only managed to beat the market exchange rate in {:.2f}% of cases. This indicates a need for further evaluation of the hedging approach to improve its effectiveness.".format(percentage_beating_market)
    # Display the percentage and conclusion in Streamlit
    st.write(f"Percentage of Cases Beating Market Rate on daily basis: **{percentage_beating_market}%**")
    st.write(conclusion)

    # Calculate the count of cases where hedgedRate >= Close
    count_hitting_market = (frequentDataHedge['hedgedRate0'] >= frequentDataHedge['Close']).sum()
    # Total number of data points
    total_cases = frequentDataHedge.shape[0]
    # Calculate percentage
    percentage_beating_market = (count_hitting_market / total_cases) * 100 if total_cases > 0 else 0
    # Format the percentage to two decimal places
    percentage_beating_market = round(percentage_beating_market, 2)
    # Generate a professional conclusion
    if percentage_beating_market >= 50:
        conclusion = "The hedging strategy has successfully outperformed the market exchange rate in over {:.2f}% of cases. This suggests a strong performance in mitigating risk and capitalizing on favorable market conditions.".format(percentage_beating_market)
    else:
        conclusion = "The hedging strategy has only managed to beat the market exchange rate in {:.2f}% of cases. This indicates a need for further evaluation of the hedging approach to improve its effectiveness.".format(percentage_beating_market)
    # Display the percentage and conclusion in Streamlit
    st.write(f"Percentage of Cases Beating Market Rate on {st.session_state.period}ly basis: **{percentage_beating_market}%**")
    st.write(conclusion)
  else:
    # Calculate the count of cases where hedgedRate >= Close
    count_hitting_market = (dailyDataHedge['hedgedRate1'] >= dailyDataHedge['Close']).sum()
    # Total number of data points
    total_cases = dailyDataHedge.shape[0]
    # Calculate percentage
    percentage_beating_market = (count_hitting_market / total_cases) * 100 if total_cases > 0 else 0
    # Format the percentage to two decimal places
    percentage_beating_market = round(percentage_beating_market, 2)
    # Generate a professional conclusion
    if percentage_beating_market >= 50:
        conclusion = "The hedging strategy has successfully outperformed the market exchange rate in over {:.2f}% of cases. This suggests a strong performance in mitigating risk and capitalizing on favorable market conditions.".format(percentage_beating_market)
    else:
        conclusion = "The hedging strategy has only managed to beat the market exchange rate in {:.2f}% of cases. This indicates a need for further evaluation of the hedging approach to improve its effectiveness.".format(percentage_beating_market)
    # Display the percentage and conclusion in Streamlit
    st.write(f"Percentage of Cases Beating Market Rate on daily basis: **{percentage_beating_market}%**")
    st.write(conclusion)

    # Calculate the count of cases where hedgedRate >= Close
    count_hitting_market = (frequentDataHedge['hedgedRate1'] >= frequentDataHedge['Close']).sum()
    # Total number of data points
    total_cases = frequentDataHedge.shape[0]
    # Calculate percentage
    percentage_beating_market = (count_hitting_market / total_cases) * 100 if total_cases > 0 else 0
    # Format the percentage to two decimal places
    percentage_beating_market = round(percentage_beating_market, 2)
    # Generate a professional conclusion
    if percentage_beating_market >= 50:
        conclusion = "The hedging strategy has successfully outperformed the market exchange rate in over {:.2f}% of cases. This suggests a strong performance in mitigating risk and capitalizing on favorable market conditions.".format(percentage_beating_market)
    else:
        conclusion = "The hedging strategy has only managed to beat the market exchange rate in {:.2f}% of cases. This indicates a need for further evaluation of the hedging approach to improve its effectiveness.".format(percentage_beating_market)
    # Display the percentage and conclusion in Streamlit
    st.write(f"Percentage of Cases Beating Market Rate on {st.session_state.period}ly basis: **{percentage_beating_market}%**")
    st.write(conclusion)
    
####################################################################""

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'risk_assessment' not in st.session_state:
    st.session_state.risk_assessment=None
    

if st.session_state.logged_in:
  if st.session_state.risk_assessment is not None:
     # Sidebar for date input
     st.sidebar.header("Backtesting Date Range")
     start_date = st.sidebar.date_input("Start Date", value=date(2019, 1, 1), min_value=date(2019, 1, 1), max_value=date.today() - timedelta(days=30))
     end_date = st.sidebar.date_input("End Date (yyyy-mm-dd)", min_value=date(2019, 2, 1), max_value=date.today(),value=date(2024, 1, 1))
     dailyDataHedge=st.session_state.dailyDataHedge[(st.session_state.dailyDataHedge['Date']>=str(start_date)) & (st.session_state.dailyDataHedge['Date']<=str(end_date))]
     frequentDataHedge=st.session_state.frequentDataHedge[(st.session_state.frequentDataHedge['Date']>=str(start_date)) & (st.session_state.frequentDataHedge['Date']<=str(end_date))]

     st.title(f'FX Backtesting of your hedging strategy for the following currency pair: {st.session_state.localCurrency}/{st.session_state.foreignCurrency} ')
     # Footer information
     st.write("💡 Use this tool to test your hedging strategy after using risk assessment tool!")
     st.title(f"Evaluate Hedging Strategy ({st.session_state.hedgePercent *100}%) on a Daily Basis")
     GraphDaily('hedgedRate0',0)
     st.title(f"Evaluate Hedging Strategy ({st.session_state.hedgePercent *100}%) on a {st.session_state.period}ly Basis")
     GraphPeriod('hedgedRate0',0)
     st.title("Conclusion 1")
     Recap(0)
     st.title(f"Evaluate Hedging Strategy ({(1-st.session_state.hedgePercent)*100}%) on a Daily Basis")
     GraphDaily('hedgedRate1',1)
     st.title(f"Evaluate Hedging Strategy ({(1-st.session_state.hedgePercent)*100}%) on a {st.session_state.period}ly Basis")
     GraphPeriod('hedgedRate1',1)
     st.title("Conclusion 2")
     Recap(1)
     st.title("Advice")
     st.write(f"👨‍💼 Choose the best strategy based on your objectives: whether to maximize potential earnings or to minimize risks in a worst-case scenario. If your goal is to achieve the highest possible profit, analyze the graphs of the two strategies and focus on those that show a greater area of difference between the hedged rate and the market rate. Conversely, if you aim to mitigate risk in adverse conditions, prioritize the hedging strategy that offers a lower value of Value at Risk (VaR) or Expected Shortfall (ES), depending on your chosen timeframe (daily or {st.session_state.period}).")

    

  else:
    st.warning("👆 Please use firstly risk assessment tool (MarketRiskAssessment)")
    st.stop()
else:
     st.warning("Denied Access")












