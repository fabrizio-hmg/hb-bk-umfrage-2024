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
    st.markdown('''
        1. Upload the provided dataset in CSV format.  
        2. Filter the data based on your criteria.  
        3. Select only the most relevant column(s) for your question.  
        4. Ask ChatGPT your question.  
    ''')
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

        relevenat_columns = st.multiselect('Select only relevant columns', filtered_df.columns[2:])
        relevant_df = filtered_df[relevenat_columns]
    
        if relevenat_columns:
            st.write(relevant_df)

        prompt = st.text_area('Ask a question')

        if prompt:
            insight = analyst.generate_insight(relevant_df, prompt)
        
        if st.button('Generate Insights'):
            st.write(insight.insight)

    else:
        st.write('No file uploaded')

if __name__ == '__main__':
    main()
