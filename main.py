import pandas as pd
import streamlit as st

from classes.analyst import Insight

headers = {
    'authorization': st.secrets['OPENAI_API_KEY'],
    'content-type': 'application/json'
}

def main():
    
    analyst = Insight()
    st.title('HB BK-Umfrage (2024)')
    st.divider()

    uploaded_file = st.file_uploader('Choose a CSV file', type='csv')

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())

        columns = df.columns.to_list()
        selected_columns = st.selectbox('Select column to filter by', columns)
        unique_values = df[selected_columns].unique()
        selected_value = st.selectbox('Select value', unique_values)

        filtered_df = df[df[selected_columns] == selected_value]
        st.write(filtered_df)

        relevenat_columns = st.multiselect('Select relevant columns only', filtered_df.columns, default=filtered_df.columns[:3])
        relevant_df = filtered_df[relevenat_columns]
        st.write(relevant_df)


        question = st.text_area('Ask a question')

        if question:
            insight = analyst.generate_insight(relevant_df, question)
        
        if st.button('Generate Insights'):
            st.write(insight.insight)

    else:
        st.write('No file uploaded')

if __name__ == '__main__':
    main()
