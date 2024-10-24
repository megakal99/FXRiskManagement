import os
from dotenv import load_dotenv
import streamlit as st
#################################################""

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'tries' not in st.session_state:
    st.session_state.tries =0
# Load environment variables from .env file
load_dotenv()

# Retrieve the variables
key = os.getenv('access_key', 'default_value')


# Function to validate the user input key
def validate_key(input_key):
    return input_key == key

def display_content():
    st.title("Welcome to Our Currency Exchange Risk Assessment Tool")

    st.subheader("Overview:")
    st.write(
        "Our application is designed to help businesses and individuals navigate the complexities of currency exchange by assessing market risks and evaluating hedging strategies. Whether you are dealing with foreign currency purchases or interested in understanding market volatility, this tool offers valuable insights."
    )

    st.subheader("How to Use the App")

    st.write("**1. Home Page:**")
    st.write(
        "Start here to familiarize yourself with the app's features and navigate to the other sections. Use the navigation bar to switch between the three pages: **Home**, **Market Risk Assessment**, and **BackTesting**."
    )

    st.write("**2. Market Risk Assessment Page:**")
    st.write(
        "Purpose: This section evaluates the risks associated with currency exchange by analyzing market fluctuations and volatility, under market rates and hedged rates."
    )
    st.write("**Key Concepts:**")
    st.write(
        "- **Value at Risk (VaR):** This metric estimates the maximum potential loss in the value of a currency position over a specific time period (days,weeks,months,quarter), at a given confidence level."
    )
    st.write(
        "- **Expected Shortfall (ES):** This measures the average loss that occurs beyond the VaR threshold, providing insight into the severity of potential losses in adverse conditions."
    )
    st.write(
        "Methodology: The assessments are based on historical data and assume that no hedging strategies are employed, as well as on scenarios where forward contract(s) hedging strategies are utilized to understand the risk mitigation associated with your hedging strategy."
    )

    st.write("**Example:**")
    st.write(
        "Suppose you are planning to exchange **£100,000** for American dollars (USD). Based on historical volatility, the VaR calculation indicates a potential loss of **1%** in the exchange rate due to market fluctuations over the next day."
    )
    st.write(
        "This means that there is a **95% confidence level** (if you choose a risk tolerance of **5%**) that you won’t lose more than **£1,000** from your currency exchange transaction if the market moves against you."
    )
    st.write(
        "If the current spot rate for GBP/USD is **1.2650**, a **1% loss** would indicate a new spot rate of **1.2524**. Therefore, your potential loss would be:"
    )
    st.write(
        "**£100,000 × (1.2650 - 1.2524) = $1,260**, meaning you would not lose more than this amount with 95% confidence."
    )
    st.write(
        "In addition, if the Expected Shortfall (ES) is **2%**, in a worst-case scenario, you might face an average loss of **£2,000** or approximately **$2,530** in value under severe market conditions."
    )

    st.write("**3. BackTesting Page:**")
    st.write(
        "Purpose: This page evaluates various hedging strategies against historical data to find the most effective approach for mitigating market risks."
    )
    st.write(
        "How It Works: By analyzing a year’s worth of historical data, you can test different forward contract strategies to see how they would have performed in past market conditions."
    )
    st.write(
        "Insights Provided: After running the tests, you will receive suggestions on the most efficient hedging strategies tailored to your currency exposure."
    )

    st.write("### Example Use Case:")
    st.write(
        "Let’s say you are a company planning to import goods from Europe, and you need to exchange USD for EUR. "
    )
    st.write(
        "1. **Start on the Market Risk Assessment page** to evaluate the potential risks associated with currency fluctuations before making any purchases."
    )
    st.write(
        "2. **Next, navigate to the BackTesting page** to test various hedging strategies, such as forward contracts, to determine which one would have minimized your risks based on past market data."
    )

    st.write("### Conclusion:")
    st.write(
        "By using our app, you can gain a comprehensive understanding of the currency exchange market and make informed decisions regarding your transactions and risk management strategies. Explore each section to maximize your insights and optimize your financial outcomes!"
    )


# Login modal functionality
def login_modal():
    if st.session_state.logged_in:
        display_content()

    else:
     if st.session_state.tries>=5:
      st.error("Too many tries. Please contact the administrator: kal.benzi25@gmail.com")
      st.stop()
     else:
      with st.form("CheckAcces", clear_on_submit=True):
        st.title("Check Acces Page")
        user_input = st.text_input("Enter the secret key:")
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            if validate_key(user_input):
                st.session_state.logged_in = True
                st.success("Access granted! Redirecting to Home...")
                display_content()
            else:
                if st.session_state.tries<5:
                    st.error("Invalid key. Please try again.")
                    st.session_state.tries+=1
                else:
                    st.error("Too many tries. Please contact the administrator: kal.benzi25@gmail.com")
                    

# Display the login modal
login_modal()


