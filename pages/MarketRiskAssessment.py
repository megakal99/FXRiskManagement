import streamlit as st
import pandas as pd
import os
import yfinance as yf
from datetime import date, timedelta
####################################################################""

# Define your functions here
def GetData(UserCurrency, TargetCurrency, firstDate):
    forex_data = yf.download(f'{UserCurrency}{TargetCurrency}=X', start=firstDate, end=str(date.today()), interval='1d')
    forex_data=pd.DataFrame(forex_data)
    forex_data.index = pd.to_datetime(forex_data.index)
    forex_data['Date'] = forex_data.index.strftime('%Y-%m-%d')
    forex_data = forex_data.reset_index(drop=True)
    forex_data = forex_data[['Date','Close']]
    forex_data.columns=['Date','Close']
    forex_data['Close'] = forex_data['Close'].round(4)
    forex_data['Pct_Change'] = round(forex_data['Close'].pct_change() * 100, 4)  
    return forex_data

def LoadData(UserCurrency, TargetCurrency):
    if UserCurrency == TargetCurrency:
       st.warning("You can't use the same currency for getting spot (market) rate")
       st.stop()
    else:
     current_dir = os.getcwd()  # This should point to the 'pages' folder
     
     file_name = f"{UserCurrency}_{TargetCurrency}.xlsx"
     file_path = os.path.join(current_dir,"data", file_name)
     
     try:
        data = pd.read_excel(file_path)
        data = data.iloc[:, 1:]
        firstDate = data.loc[len(data) - 1, 'Date']
        firstDate = pd.to_datetime(firstDate) + timedelta(days=1)
        firstDate = firstDate.strftime('%Y-%m-%d')
        forex_data = GetData(UserCurrency, TargetCurrency, str(firstDate))
        
        if forex_data.shape[0]: 
            data = pd.concat([data, forex_data], ignore_index=True)
            data['Pct_Change'] = round(data['Close'].pct_change() * 100, 4) 
            data.to_excel(file_path)
     except Exception:
        forex_data = GetData(UserCurrency, TargetCurrency, '2019-01-01')
        forex_data.to_excel(file_path)

def GetDatafrequently(UserCurrency, TargetCurrency,frequent):
    if frequent=='week':
       frequent='1wk'
    elif frequent=='quarter':
       frequent='3mo'
    elif frequent=='month':
       frequent='1mo'
    else:
       pass
    forex_data_freq = yf.download(f'{UserCurrency}{TargetCurrency}=X', start='2019-01-01', end=str(date.today()), interval=frequent)
    forex_data_freq=pd.DataFrame(forex_data_freq)
    forex_data_freq.index = pd.to_datetime(forex_data_freq.index)
    forex_data_freq['Date'] = forex_data_freq.index.strftime('%Y-%m-%d')
    forex_data_freq = forex_data_freq.reset_index(drop=True)
    forex_data_freq = forex_data_freq[['Date','Close']] 
    forex_data_freq.columns=['Date','Close']
    forex_data_freq['Close'] = forex_data_freq['Close'].round(4)
    forex_data_freq['Pct_Change'] = round(forex_data_freq['Close'].pct_change() * 100, 4)  
    return forex_data_freq

def Var_calculation(UserCurrency, TargetCurrency, risktolerance,frequent):
    current_dir = os.getcwd()
    file_name = f"{UserCurrency}_{TargetCurrency}.xlsx"
    file_path = os.path.join(current_dir, "data", file_name)
    data = pd.read_excel(file_path)
    data = data.iloc[:, 1:]
    
    riskrate = data['Pct_Change'].quantile(risktolerance)
    returns = data['Pct_Change']
    losses_beyond_var = returns[returns <= riskrate]
    expected_shortfall = losses_beyond_var.mean()
    # freq data
    forex_data_freq=GetDatafrequently(UserCurrency, TargetCurrency,frequent)
    riskrate_ = forex_data_freq['Pct_Change'].quantile(risktolerance)
    returns_ = forex_data_freq['Pct_Change']
    losses_beyond_var_ = returns_[returns_ <= riskrate_]
    expected_shortfall_ = losses_beyond_var_.mean()

    risk_assessment = pd.DataFrame({
        'CurrencyPair':[f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}'],
        'RiskToleranceRate':[f'{risktolerance*100}%',f'{risktolerance*100}%',f'{risktolerance*100}%',f'{risktolerance*100}%'],
        'Risk Assessment': [f'{round(riskrate,2)}%', f'{round(expected_shortfall,2)}%',f'{round(riskrate_,2)}%', f'{round(expected_shortfall_,2)}%'],
        'Interpretation': [
            f"The Value at Risk (VaR) is {round(riskrate,2)}%, meaning there is a {(1 - risktolerance) * 100}% chance that your losses related to fluctuations in the exchange market will not exceed {-round(riskrate,2)}% of your exposure over the next day.",
            f"The Expected Shortfall (ES) is {round(expected_shortfall,2)}%, meaning that if you experience losses beyond the VaR threshold, you can expect, on average, to incur a loss of about {-round(expected_shortfall,2)}% of your exposure in those worst-case scenarios over the next day.",
            f"The Value at Risk (VaR) is {round(riskrate_,2)}%, meaning there is a {(1 - risktolerance) * 100}% chance that your losses related to fluctuations in the exchange market will not exceed {-round(riskrate_,2)}% of your exposure over the next {frequent}.",
            f"The Expected Shortfall (ES) is determined to be a rate of {round(expected_shortfall_,2)}%, meaning that if you experience losses beyond the VaR threshold, you can expect, on average, to incur a loss of about {-round(expected_shortfall_,2)}% of your exposure in those worst-case scenarios over the next {frequent}."
        
        ]
    },index=['Daily VAR','Daily ES',f'{frequent}ly VAR',f'{frequent}ly ES'])
    
    return risk_assessment


def HedgeVarES(UserCurrency,TargetCurrency,Fxdata,period,forwardRate,hedgePercent):
      datax=pd.DataFrame({'Date':[],'Close':[],'hedgedRate0':[],'hedgedRate1':[]})
      if period=='week':
       period='1wk'
      elif period=='quarter':
       period='3mo'
      elif period=='month':
       period='1mo'
      else:
       pass
      forex_data_freq = yf.download(f'{UserCurrency}{TargetCurrency}=X', start='2019-01-01', end=str(date.today()), interval=period)
      forex_data_freq=pd.DataFrame(forex_data_freq)
      forex_data_freq.index = pd.to_datetime(forex_data_freq.index)
      forex_data_freq['Date'] = forex_data_freq.index.strftime('%Y-%m-%d')
      forex_data_freq = forex_data_freq.reset_index(drop=True)
      forex_data_freq = forex_data_freq[['Date','Close']]
      forex_data_freq.columns=['Date','Close']
      forex_data_freq['Close'] = forex_data_freq['Close'].round(4)
      aux=0
      for i in range(forex_data_freq.shape[0]):
          if aux==len(forwardRate):
            aux=0
          forex_data_freq.loc[i,'hedgedRate0']=forwardRate[aux]*hedgePercent + forex_data_freq.loc[i,'Close']*(1-hedgePercent)
          forex_data_freq.loc[i,'hedgedRate1']=forwardRate[aux]*(1-hedgePercent) + forex_data_freq.loc[i,'Close']*hedgePercent
          aux+=1
      # Calculate the percentage change
      forex_data_freq['Pct_Change_hedge0'] = round((forex_data_freq['hedgedRate0'] - forex_data_freq['Close'].shift(1)) / forex_data_freq['Close'].shift(1) * 100,4)
      forex_data_freq['Pct_Change_hedge1'] = round((forex_data_freq['hedgedRate1'] - forex_data_freq['Close'].shift(1)) / forex_data_freq['Close'].shift(1) * 100,4)
      aux=0
      for j,i in zip(list(forex_data_freq['Date']),list(forex_data_freq['Date'])[1:]):
            if aux==len(forwardRate):
               aux=0
            dd=Fxdata[(Fxdata['Date']>=j) & (Fxdata['Date']<i)]
            dd['hedgedRate0']=forwardRate[aux]*hedgePercent + dd['Close']*(1-hedgePercent)
            dd['hedgedRate1']=forwardRate[aux]*(1-hedgePercent) + dd['Close']*hedgePercent
            datax=pd.concat([datax,dd], ignore_index=True)
            aux+=1
      # Calculate the percentage change
      datax['Pct_Change_hedge0'] = round((datax['hedgedRate0'] - datax['Close'].shift(1)) / datax['Close'].shift(1) * 100,4)
      datax['Pct_Change_hedge1'] = round((datax['hedgedRate1'] - datax['Close'].shift(1)) / datax['Close'].shift(1) * 100,4)
        
      return forex_data_freq,datax
    
        
def ExecHedgeVarES(UserCurrency,TargetCurrency,period,forwardRate,hedgePercent,risktolerance):
       current_dir = os.getcwd() 
       file_name = f"{UserCurrency}_{TargetCurrency}.xlsx"
       file_path = os.path.join(current_dir,"data", file_name)
       data = pd.read_excel(file_path)
       data = data.iloc[:, 1:]
       frequentDataHedge,dailyDataHedge=HedgeVarES(UserCurrency,TargetCurrency,data,period,forwardRate,hedgePercent)
       st.session_state.frequentDataHedge=frequentDataHedge
       st.session_state.dailyDataHedge=dailyDataHedge
       st.session_state.hedgePercent=hedgePercent
       st.session_state.period=period
       riskrateHedge0 = dailyDataHedge['Pct_Change_hedge0'].quantile(risktolerance)
       riskrateHedge1 = dailyDataHedge['Pct_Change_hedge1'].quantile(risktolerance)
       riskrateHedge0_ = frequentDataHedge['Pct_Change_hedge0'].quantile(risktolerance)
       riskrateHedge1_ = frequentDataHedge['Pct_Change_hedge1'].quantile(risktolerance)
       if riskrateHedge0>=0 or riskrateHedge0_>=0 :
           if riskrateHedge0>=0:
            st.success(f"This hedging strategy of hedging {hedgePercent*100}% of the exposure is efficient 100%, because it generate a positive daily value at risk, which means there is no daily expected loss by following this strategy.")
            st.stop()
           elif riskrateHedge0_>=0:
            st.success(f"This hedging strategy of hedging {hedgePercent*100}% of the exposure is efficient 100%, because it generate a positive {period}ly value at risk, which means there is no {period}ly expected loss by following this strategy.")
            st.stop() 
           else:
            st.success(f"This hedging strategy of hedging {hedgePercent*100}% of the exposure is efficient 100%, because it generate a positive value at risk, which means there is no daily or {period}ly expected loss by following this strategy.")
            st.stop()  
       elif riskrateHedge1 >=0 or riskrateHedge1_>=0:
           if riskrateHedge1>=0:
            st.success(f"This hedging strategy of hedging {(1-hedgePercent)*100}% of the exposure is efficient 100%, because it generate a positive daily value at risk, which means there is no daily expected loss by following this strategy.")
            st.stop()
           elif riskrateHedge1_>=0:
            st.success(f"This hedging strategy of hedging {(1-hedgePercent)*100}% of the exposure is efficient 100%, because it generate a {period}ly positive value at risk, which means there is no {period}ly expected loss by following this strategy.")
            st.stop() 
           else:
            st.success(f"This hedging strategy of hedging {(1-hedgePercent)*100}% of the exposure is efficient 100%, because it generate a positive value at risk, which means there is no daily or {period}ly expected loss by following this strategy.")
            st.stop()
       else:
        returnsHedge0 = dailyDataHedge['Pct_Change_hedge0']
        losses_beyond_varhedge0 = returnsHedge0[returnsHedge0 <= riskrateHedge0]
        expected_shortfallhedge0 = losses_beyond_varhedge0.mean()
        returnsHedge0_ = frequentDataHedge['Pct_Change_hedge0']
        losses_beyond_varhedge0_ = returnsHedge0_[returnsHedge0_ <= riskrateHedge0_]
        expected_shortfallhedge0_ = losses_beyond_varhedge0_.mean()
        returnsHedge1 = dailyDataHedge['Pct_Change_hedge1']
        losses_beyond_varhedge1 = returnsHedge1[returnsHedge1 <= riskrateHedge1]
        expected_shortfallhedge1 = losses_beyond_varhedge1.mean()
        returnsHedge1_ = frequentDataHedge['Pct_Change_hedge1']
        losses_beyond_varhedge1_ = returnsHedge1_[returnsHedge1_ <= riskrateHedge1_]
        expected_shortfallhedge1_ = losses_beyond_varhedge1_.mean()
        risk_assessment = pd.DataFrame({
        'CurrencyPair':[f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}'],
        'RiskToleranceRate':[f'{risktolerance*100}%',f'{risktolerance*100}%',f'{risktolerance*100}%',f'{risktolerance*100}%'],
        'Risk Assessment': [f'{round(riskrateHedge0,2)}%', f'{round(expected_shortfallhedge0,2)}%',f'{round(riskrateHedge0_,2)}%', f'{round(expected_shortfallhedge0_,2)}%'],
        'Interpretation': [
            f"The Value at Risk (VaR) is {round(riskrateHedge0,2)}%, meaning there is a {(1 - risktolerance) * 100}% chance that your losses from exchange rate fluctuations, with a hedging strategy covering {hedgePercent*100}% of exposure, will not exceed {-round(riskrateHedge0,2)}% of your exposure over the next day.",
            f"The Expected Shortfall (ES) is {round(expected_shortfallhedge0,2)}%, which means that if you experience losses beyond the VaR threshold, you can expect, on average, to incur a loss of about {-round(expected_shortfallhedge0,2)}% of your exposure in those worst-case scenarios over the next day, with a hedging strategy covering {hedgePercent*100}% of your exposure.",
            f"The Value at Risk (VaR) is {round(riskrateHedge0_,2)}%, meaning there is a {(1 - risktolerance) * 100}% chance that your losses from exchange rate fluctuations, with a hedging strategy covering {hedgePercent*100}% of exposure, will not exceed {-round(riskrateHedge0_,2)}% of your exposure over the next {period}.",
            f"The Expected Shortfall (ES) is {round(expected_shortfallhedge0_,2)}%, which means that if you experience losses beyond the VaR threshold, you can expect, on average, to incur a loss of about {-round(expected_shortfallhedge0_,2)}% of your exposure in those worst-case scenarios over the next {period}, with a hedging strategy covering {hedgePercent*100}% of your exposure.",]},index=['Daily VAR','Daily ES',f'{period}ly VAR',f'{period}ly ES'])
        risk_assessment_ = pd.DataFrame({
        'CurrencyPair':[f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}',f'{st.session_state.localCurrency}/{st.session_state.foreignCurrency}'],
        'RiskToleranceRate':[f'{risktolerance*100}%',f'{risktolerance*100}%',f'{risktolerance*100}%',f'{risktolerance*100}%'],
        'Risk Assessment': [f'{round(riskrateHedge1,2)}%', f'{round(expected_shortfallhedge1,2)}%',f'{round(riskrateHedge1_,2)}%', f'{round(expected_shortfallhedge1_,2)}%'],
        'Interpretation': [
          f"The Value at Risk (VaR) is {round(riskrateHedge1,2)}%, meaning there is a {(1 - risktolerance) * 100}% chance that your losses from exchange rate fluctuations, with a hedging strategy covering {(1-hedgePercent)*100}% of exposure, will not exceed {-round(riskrateHedge1,2)}% of your exposure over the next day.",
          f"The Expected Shortfall (ES) is {round(expected_shortfallhedge1,2)}%, which means that if you experience losses beyond the VaR threshold, you can expect, on average, to incur a loss of about {-round(expected_shortfallhedge1,2)}% of your exposure in those worst-case scenarios over the next day, with a hedging strategy covering {(1-hedgePercent)*100}% of your exposure.",
          f"The Value at Risk (VaR) is {round(riskrateHedge1_,2)}%, meaning there is a {(1 - risktolerance) * 100}% chance that your losses from exchange rate fluctuations, with a hedging strategy covering {(1-hedgePercent)*100}% of exposure, will not exceed {-round(riskrateHedge1_,2)}% of your exposure over the next {period}.",
          f"The Expected Shortfall (ES) is determined to be a rate of {round(expected_shortfallhedge1_,2)}%, which means that if you experience losses beyond the VaR threshold, you can expect, on average, to incur a loss of about {-round(expected_shortfallhedge1_,2)}% of your exposure in those worst-case scenarios over the next {period}, with a hedging strategy covering {(1-hedgePercent)*100}% of your exposure."]},index=['Daily VAR','Daily ES',f'{period}ly VAR',f'{period}ly ES'])
        return risk_assessment,risk_assessment_
   
#######################################################################################Run app

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'risk_assessment' not in st.session_state:
    st.session_state.risk_assessment=None
if 'hedgePercent' not in st.session_state:
    st.session_state.hedgePercent=None
if 'risk_assessment0' not in st.session_state:
    st.session_state.risk_assessment0=None
if 'risk_assessment1' not in st.session_state:
    st.session_state.risk_assessment1=None


if st.session_state.logged_in:
  try:
    # Streamlit App
    st.title("Currency Exchange Risk Assessment Tool")
    # Footer information
    st.write("💡 Use this tool to evaluate and get insight about the risk associated with currency exchange Market!")
    # Sidebar for navigation
    st.sidebar.header("Navigation")
    user_currency = st.sidebar.selectbox("Select Your Currency", ["GBP", "USD", "EUR","JPY","CAD","CHF","AUD","NZD","MAD","RUB","PHP","INR","SGD","HKD","CNY","HUF","SEK","MYR","THB","ZAR"])
    target_currency = st.sidebar.selectbox("Select Target Currency", ["GBP", "USD", "EUR","JPY","CAD","CHF","AUD","NZD","MAD","RUB","PHP","INR","SGD","HKD","CNY","HUF","SEK","MYR","THB","ZAR"])
    Frequent = st.sidebar.selectbox("Select The period of your Exchange", ["week","month","quarter"])
    hedgePercent = st.sidebar.selectbox("Select The hedged percentage of your exposure",[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
    forwardRate= st.sidebar.text_input("Enter the forward rate(s) (e.g., 1.2548,1.2241,etc):", None)
    risk_tolerance = st.sidebar.slider("Select Risk Tolerance (%)", min_value=1, max_value=10, value=5) / 100
    # Assess Risk button
    if st.sidebar.button("Assess Risk"):
        if forwardRate:
            forwardRate=forwardRate.split(',')
            forwardRate = [float(num) for num in forwardRate]
            print(forwardRate,'*****************')
        else:
            st.warning("👆 Please enter the exchange rates for the forward contract(s). If you will use different forward contracts for each specific period, please enter the agreed exchange rates (forward rates) and separate them with a comma (,). If you plan to use one forward contract, enter the agreed forward rate.")
            st.stop()
        
        st.session_state.localCurrency=user_currency
        st.session_state.foreignCurrency=target_currency
        LoadData(user_currency, target_currency)  # Load the data
        risk_assessment = Var_calculation(user_currency, target_currency, risk_tolerance,Frequent)
        risk_assessmenthedging0,risk_assessmenthedging1=ExecHedgeVarES(user_currency,target_currency,Frequent,forwardRate,hedgePercent,risk_tolerance)
        # Store the result in session state
        st.session_state.risk_assessment=risk_assessment
        st.session_state.risk_assessment0=risk_assessmenthedging0
        st.session_state.risk_assessment1=risk_assessmenthedging1
        
        st.header("Risk Assessment Results")
        st.write("🔍 **Value at Risk (VaR) and Expected Shortfall (ES) without any hedging strategy:**")
        st.table(st.session_state.risk_assessment)
        st.write(f"🔍 **Value at Risk (VaR) and Expected Shortfall (ES) with a forward contract hedging strategy covering {st.session_state.hedgePercent * 100}% of exposure:**")
        st.table(st.session_state.risk_assessment0)
        st.write(f"🔍 **Value at Risk (VaR) and Expected Shortfall (ES) with a forward contract hedging strategy covering {(1-st.session_state.hedgePercent)*100}% of exposure:**")
        st.table(st.session_state.risk_assessment1)

    elif st.session_state.risk_assessment is not None:
        st.header("Risk Assessment Results")
        st.write("🔍 **Value at Risk (VaR) and Expected Shortfall (ES) without any hedging strategy:**")
        st.table(st.session_state.risk_assessment)
        st.write(f"🔍 **Value at Risk (VaR) and Expected Shortfall (ES) with a forward contract hedging strategy covering {st.session_state.hedgePercent * 100}% of exposure:**")
        st.table(st.session_state.risk_assessment0)
        st.write(f"🔍 **Value at Risk (VaR) and Expected Shortfall (ES) with a forward contract hedging strategy covering {(1-st.session_state.hedgePercent)*100}% of exposure:**")
        st.table(st.session_state.risk_assessment1)
    else:
       pass
    
  except Exception as e:
   st.error(str(e))
   st.stop()
else:
    st.warning("Denied Access")






    

