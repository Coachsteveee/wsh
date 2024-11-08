import pandas as pd
import streamlit as st

def load_data():
    """Loads the GW4 data from a CSV file and returns it as a pandas dataframe.
    
    Returns:
        A pandas dataframe containing the GW4 data.
    """

    df = pd.read_excel("GW8.xlsx").drop(columns=['Unnamed: 0'])
    return df

def main():
    """Loads the GameWeek data from an excel file and displays it
    in a Streamlit dataframe. The dataframe is displayed with its
    index hidden and a fixed height of 900px, and it is allowed
    to use the full width of the Streamlit app."""
    st.title('Game Week 8')
    
    data = load_data()
    st.dataframe(data, hide_index=True, height=560, use_container_width=True)
    
if __name__ == '__main__':
    main()