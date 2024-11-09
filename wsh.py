import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

def load_data():
    """Loads the GW8 data from an Excel file and returns it as a pandas dataframe."""
    df = pd.read_excel("all_matches.xlsx")
    return df

def style_dataframe(df):
    """Applies conditional formatting to the dataframe."""
    # Create a copy of the dataframe without the league column for display
    display_df = df[['fixture', 'match_xg', 'ex_bookings', 'ex_corners']].copy()
    
    def color_odds(val):
        if val > 5:
            color = 'background-color: #7A1CAC; color: white'
        elif val > 3:
            color = 'background-color: #7A1CAC; color: white'
        else:
            color = 'background-color: #7A1CAC; color: white'
        return color

    return display_df.style.applymap(color_odds, subset=['match_xg', 'ex_bookings', 'ex_corners'])

def get_statistics(df):
    """Calculates basic statistics from the dataframe."""
    stats = {
        'avg_match_xg': round(df['match_xg'].mean(), 2),
        'avg_bookings': round(df['ex_bookings'].mean(), 2),
        'avg_corners': round(df['ex_corners'].mean(), 2),
        'highest_xg_match': df.loc[df['match_xg'].idxmax(), 'fixture'],
        'highest_xg_value': round(df['match_xg'].max(), 2)
    }
    return stats

def add_search_filters(data):
    """Add search and filter options in sidebar"""
    st.sidebar.subheader("Filters")
    
    min_xg = st.sidebar.slider("Min Expected Goals", 
                              float(data['match_xg'].min()), 
                              float(data['match_xg'].max()),
                              float(data['match_xg'].min()))
    
    min_bookings = st.sidebar.slider("Min Expected Bookings",
                                    float(data['ex_bookings'].min()),
                                    float(data['ex_bookings'].max()),
                                    float(data['ex_bookings'].min()))
    
    filtered_data = data[
        (data['match_xg'] >= min_xg) &
        (data['ex_bookings'] >= min_bookings)
    ]
    
    return filtered_data

def add_insights(data):
    """Add statistical insights and analysis"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**High Impact Matches (Above Average xG)**")
        high_xg = data[data['match_xg'] > data['match_xg'].mean()]
        st.dataframe(high_xg[['fixture', 'match_xg']].sort_values('match_xg', ascending=False))
    
    with col2:
        st.markdown("**High Card Potential (Above Average Bookings)**")
        high_cards = data[data['ex_bookings'] > data['ex_bookings'].mean()]
        st.dataframe(high_cards[['fixture', 'ex_bookings']].sort_values('ex_bookings', ascending=False))

def create_visualizations(df):
    """Creates visualization charts for the data."""
    # Expected Goals Bar Chart
    fig_xg = px.bar(df, x='fixture', y='match_xg', 
                    title='Expected Goals by Match',
                    labels={'match_xg': 'Expected Goals', 'fixture': 'Match'},
                    color='match_xg',
                    color_continuous_scale='Viridis')
    fig_xg.update_layout(xaxis_tickangle=-45)
    
    # Bookings vs Corners Scatter Plot
    fig_scatter = px.scatter(df, x='ex_bookings', y='ex_corners',
                            title='Expected Bookings vs Corners',
                            text='fixture',
                            size='match_xg',
                            color='match_xg',
                            color_continuous_scale='Viridis')
    
    # Bookings Distribution
    fig_bookings = px.histogram(df, x='ex_bookings',
                               title='Distribution of Expected Bookings',
                               nbins=10)
    
    return fig_xg, fig_scatter, fig_bookings

def add_coming_soon_section():
    """Add a coming soon section with upcoming features"""
    st.sidebar.markdown("---")
    st.sidebar.header("🚀 Coming Soon")
    
    # Recommended Betslips
    with st.sidebar.expander("🎯 Recommended Betslips"):
        st.write("AI-powered betting recommendations based on our advanced prediction model.")
        st.write("- Value bet detection")
        st.write("- Confidence ratings")
        st.write("- Risk assessment")
    
    # Random Betslips
    with st.sidebar.expander("🎲 Feeling Lucky?"):
        st.write("Generate random betslips for the adventurous!")
        st.image("https://media1.tenor.com/m/ZARBViZffU4AAAAd/hd-smirk.gif", 
                caption="Coming soon...", 
                width=200)
    
    # Telegram Channel
    with st.sidebar.expander("📱 Telegram Channel"):
        st.write("Join our upcoming Telegram channel for:")
        st.write("- Live updates")
        st.write("- Instant notifications")
        st.write("- Community insights")
        st.write("- Real-time predictions")

def main():
    """Main application function that displays the GameWeek data with enhanced features."""
    st.set_page_config(layout="wide", page_title="Predictions Dashboard")
    
    st.title('Betting Odds Dashboard')
    
    # Load data
    data = load_data()
    
    # Add league filter with proper styling
    st.sidebar.header("League Filters")
    
    # Get unique leagues and sort them
    leagues = ['All'] + sorted(data['league'].unique().tolist())
    
    # Create a more prominent league selector
    selected_league = st.sidebar.selectbox(
        'Select League',
        leagues,
        index=0,  # Default to 'All'
        format_func=lambda x: f"🏆 {x}"  # Add an icon for better visibility
    )
    
    # Filter data based on league selection
    if selected_league != 'All':
        filtered_data = data[data['league'] == selected_league]
        st.sidebar.info(f"Showing {len(filtered_data)} matches from {selected_league}")
    else:
        filtered_data = data
        st.sidebar.info(f"Showing all {len(data)} matches")
        
    # Add league summary
    with st.sidebar.expander("League Summary"):
        league_counts = data['league'].value_counts()
        for league, count in league_counts.items():
            st.write(f"{league}: {count} matches")
    
    add_coming_soon_section()
    
    # Display statistics
    stats = get_statistics(filtered_data)
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
    tab1, tab2, tab3 = st.tabs(["Data View", "Visualizations", "Insights"])
    
    with tab1:
        styled_df = style_dataframe(filtered_data)
        st.dataframe(styled_df, hide_index=True, height=560, use_container_width=True)
    
    with tab2:
        fig_xg, fig_scatter, fig_bookings = create_visualizations(filtered_data)
        st.plotly_chart(fig_xg, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_scatter, use_container_width=True)
        with col2:
            st.plotly_chart(fig_bookings, use_container_width=True)
    
    with tab3:
        add_insights(filtered_data)
    
    # Download button for filtered data
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Filtered Data",
        csv,
        "filtered_odds_data.csv",
        "text/csv",
        key='download-csv'
    )
    
    # Add footer with timestamp
    st.markdown("---")
    st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()