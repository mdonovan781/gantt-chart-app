import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
import chardet
import textwrap

def import_csv(file):
    try:
        # Detect encoding
        raw_data = file.read()
        detected = chardet.detect(raw_data)
        encoding = detected['encoding']
        
        # Load CSV
        file.seek(0)  # Reset file pointer
        df = pd.read_csv(file, encoding=encoding)
        df = df.dropna(how='all')
        st.success(f"Successfully loaded CSV with encoding: {encoding}")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return None

def parse_date(date_str):
    date_formats = ['%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d', '%m-%d-%Y', '%d-%m-%Y']
    for date_format in date_formats:
        try:
            return pd.to_datetime(date_str, format=date_format)
        except ValueError:
            continue
    return pd.to_datetime(date_str, errors='coerce')

def generate_colors_from_csv(df):
    unique_dimensions = df['Dimension'].unique()
    color_palette = px.colors.qualitative.Set2
    return {dimension: color_palette[i % len(color_palette)] for i, dimension in enumerate(unique_dimensions)}

def create_gantt_chart(df):
    try:
        df['Start'] = df['Start'].apply(parse_date)
        df['Finish'] = df['Finish'].apply(parse_date)
        colors = generate_colors_from_csv(df)
        
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Resource", color="Dimension",
                          text="Task", color_discrete_map=colors)
        fig.update_yaxes(categoryorder="total ascending")
        return fig
    except Exception as e:
        st.error(f"Error creating Gantt chart: {str(e)}")
        return None

def main():
    st.title("Interactive Gantt Chart Generator")
    
    # File Upload
    uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])
    
    if uploaded_file:
        df = import_csv(uploaded_file)
        if df is not None:
            st.dataframe(df.head())  # Show a preview of the DataFrame
            
            # Create Gantt Chart
            fig = create_gantt_chart(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
