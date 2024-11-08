import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

def load_data():
    """Loads the GW8 data from an Excel file and returns it as a pandas dataframe.
   
    Returns:
        A pandas dataframe containing the GW8 data.
    """
    df = pd.read_excel("GW8.xlsx").drop(columns=['Unnamed: 0'])
    return df

def style_dataframe(df):
    """Applies conditional formatting to the dataframe.
    
    Args:
        df: The dataframe to style.
    
    Returns:
        A styled dataframe.
    """
    def color_odds(val):
        if val > 5:
            color = 'background-color: #1e3a8a; color: white'
        elif val > 3:
            color = 'background-color: #1e40af; color: white'
        else:
            color = 'background-color: #3b82f6; color: white'
        return color

    return df.style.applymap(color_odds, subset=['match_xg', 'ex_bookings', 'ex_corners'])

def get_statistics(df):
    """Calculates basic statistics from the dataframe.
    
    Args:
        df: The dataframe to analyze.
    
    Returns:
        Dict containing key statistics.
    """
    stats = {
        'avg_match_xg': df['match_xg'].mean(),
        'avg_bookings': df['ex_bookings'].mean(),
        'avg_corners': df['ex_corners'].mean(),
        'highest_xg_match': df.loc[df['match_xg'].idxmax(), 'fixture'],
        'highest_xg_value': df['match_xg'].max()
    }
    return stats

def create_visualizations(df):
    """Creates visualization charts for the data.
    
    Args:
        df: The dataframe to visualize.
    """
    # Bar chart for match_xg
    fig_xg = px.bar(df, x='fixture', y='match_xg', 
                    title='Expected Goals by Match',
                    labels={'match_xg': 'Expected Goals', 'fixture': 'Match'})
    fig_xg.update_layout(xaxis_tickangle=-45)
    
    # Scatter plot comparing bookings and corners
    fig_scatter = px.scatter(df, x='ex_bookings', y='ex_corners',
                            title='Expected Bookings vs Corners',
                            text='fixture')
    
    return fig_xg, fig_scatter

def main():
    """Main application function that displays the GameWeek data with enhanced features."""
    st.set_page_config(layout="wide", page_title="Betting Odds Dashboard")
    
    st.title('Game Week 8 Analysis')
    
    # Load data
    data = load_data()
    
    # Add league filter if 'league' column exists
    if 'league' in data.columns:
        leagues = ['All'] + list(data['league'].unique())
        selected_league = st.selectbox('Select League', leagues)
        if selected_league != 'All':
            data = data[data['league'] == selected_league]
    
    # Display statistics
    stats = get_statistics(data)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Expected Goals", f"{stats['avg_match_xg']:.2f}")
    with col2:
        st.metric("Avg Expected Bookings", f"{stats['avg_bookings']:.2f}")
    with col3:
        st.metric("Avg Expected Corners", f"{stats['avg_corners']:.2f}")
    
    # Display highest XG match
    st.info(f"Highest XG Match: {stats['highest_xg_match']} ({stats['highest_xg_value']:.2f})")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Data View", "Visualizations"])
    
    with tab1:
        # Display styled dataframe
        styled_df = style_dataframe(data)
        st.dataframe(styled_df, hide_index=True, height=560, use_container_width=True)
    
    with tab2:
        # Display visualizations
        fig_xg, fig_scatter = create_visualizations(data)
        st.plotly_chart(fig_xg, use_container_width=True)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Add footer with timestamp
    st.markdown("---")
    st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()