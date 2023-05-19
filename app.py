# this is the commad to run the app
# streamlit run app.py

import streamlit as st
import pandas as pd
import shap
import pickle

# Read the model using pickle
with open('./output/pipeline_cv.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the SHAP explainer
explainer = shap.Explainer(model)

# Helper function to get SHAP explanations
def get_shap_explanations(inputs):

    #set the tree explainer as the model of the pipeline
    explainer = shap.TreeExplainer(pipeline['classifier'])

    #apply the preprocessing to x_test
    observations = pipeline['imputer'].transform(x_test)

    #get Shap values from preprocessed data
    shap_values = explainer.shap_values(observations)

    #plot the feature importance
    shap.summary_plot(shap_values, x_test, plot_type="bar")


    shap_values = explainer.shap_values(inputs)
    return shap_values

def generate_sidebar(column_info):
    for column, info in column_info.items():
        st.sidebar.subheader(column)
        column_type = info['type']
        if column_type == 'binary':
            value = st.sidebar.checkbox("Select", value=False, key=column)
        elif column_type == 'category':
            options = info['value']
            value = st.sidebar.radio("Select", options, key=column)
        elif column_type == 'continuous' or column_type == 'integer':
            min_value, max_value = info['value']
            range_min = min_value# - abs(max_value - min_value) * 0.3
            range_max = max_value# + abs(max_value - min_value) * 0.3
            value = st.sidebar.number_input("Enter", min_value=range_min, max_value=range_max, key=column)
        st.sidebar.write("Selected value:", value)

    # Button to compute prediction on click
    #st.sidebar.button("Compute prediction", on_click=pred())

# Main app
def main():

    # Set the title
    st.title('Heart Failure: predicting readmission after 6 months')

    # Set the subheader
    st.subheader('A Streamlit app to predict readmission after 6 months')

    # Set the text
    st.markdown('This app will predict whether a patient will be readmitted to the hospital within 6 months of their initial visit.')

    # Set the text
    st.markdown('The data used to train the model was given during the course of Statistical Learning for Healthcare Data.')

    # Collect user inputs
    feature_1 = st.number_input("Feature 1", value=0.0)
    feature_2 = st.number_input("Feature 2", value=0.0)
    feature_3 = st.number_input("Feature 3", value=0.0)
    user_inputs = [feature_1, feature_2, feature_3]


    # Read file ccolumn_info with pkl
    with open('./output/column_info.pkl', 'rb') as f:
        column_info = pickle.load(f)

    generate_sidebar(column_info)

    # Perform prediction
    if st.sidebar.button("Predict"):
        # Create a single-row DataFrame based on the column information
        input_data = {}
        for column in column_info.keys():
            if column_info[column]['type'] == 'binary':
                input_data[column] = [st.sidebar.checkbox(column)]
            elif column_info[column]['type'] == 'category':
                input_data[column] = [st.sidebar.radio(column, column_info[column]['value'])]
            elif column_info[column]['type'] in ['continuous', 'integer']:
                min_value, max_value = column_info[column]['value']
                range_min = min_value - abs(max_value - min_value) * 0.3
                range_max = max_value + abs(max_value - min_value) * 0.3
                input_data[column] = [st.sidebar.number_input(column, min_value=range_min, max_value=range_max)]
        
        input_df = pd.DataFrame(input_data)

        # Predict class and probabilities
        prediction = model.predict(processed_inputs)[0]
        probabilities = model.predict_proba(processed_inputs)[0]

        # Generate SHAP explanations
        shap_values = get_shap_explanations(user_inputs)

        st.write("### SHAP Explanations")
        # Display the SHAP values as a force plot
        shap.force_plot(
            explainer.expected_value[1],  # Use the class index for binary classification
            shap_values[1][0, :],  # Use the SHAP values for the positive class
            processed_inputs.iloc[0, :],  # Display the feature values for the current instance
            matplotlib=True
        )

if __name__ == "__main__":
    main()








