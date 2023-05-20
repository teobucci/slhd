import pickle
import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
import numpy as np

# Read the model using pickle
with open('./output/pipeline_cv.pkl', 'rb') as f:
    pipeline = pickle.load(f)

# Read encoder
with open('./output/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Read imputer
with open('./output/imputer.pkl', 'rb') as f:
    imputer = pickle.load(f)

# Read scaler
with open('./output/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Read file ccolumn_info with pkl
with open('./output/column_info.pkl', 'rb') as f:
    column_info = pickle.load(f)

# Read categorical features
with open('./output/categorical_features.pkl', 'rb') as f:
    categorical_features = pickle.load(f)

# Read numerical features
with open('./output/numerical_features.pkl', 'rb') as f:
    numerical_features = pickle.load(f)

# Load the SHAP explainer
explainer = shap.TreeExplainer(pipeline['random_forest'].best_estimator_.named_steps['classifier'])

input_data = {}

def generate_sidebar(column_info: dict):
    """
    Generate the sidebar with the input fields
    """
    for column, info in column_info.items():
        st.sidebar.subheader(column)
        column_type = info['type']
        if column_type == 'binary':
            input_data[column] = st.sidebar.checkbox("Select", value=False, key=column)
        elif column_type == 'category':
            options = info['value']
            input_data[column] = st.sidebar.radio("Select", options, key=column)
        elif column_type == 'continuous' or column_type == 'integer':
            min_value, max_value = info['value']
            range_min = min_value# - abs(max_value - min_value) * 0.3
            range_max = max_value# + abs(max_value - min_value) * 0.3
            input_data[column] = st.sidebar.number_input("Enter", min_value=range_min, max_value=range_max, key=column)

# Main app
def main():
    """
    Main function of the app
    Run the app with: streamlit run app.py
    """

    # Set the title
    st.title('Heart Failure: predicting readmission after 6 months')

    # Set the subheader
    st.subheader('A Streamlit app to predict readmission after 6 months')

    # Set the text
    st.markdown('This app will predict whether a patient will be readmitted to the hospital within 6 months of their initial visit.')

    # Set the text
    st.markdown('The data used to train the model was given during the course of Statistical Learning for Healthcare Data.')

    generate_sidebar(column_info)

    # Perform prediction
    if st.sidebar.button("Predict"):
        # Create a single-row DataFrame based on the column information
        new_data = pd.DataFrame(input_data, index=['user_input'])

        # Encode
        new_data_encoded = pd.DataFrame(encoder.transform(new_data[categorical_features]), columns=encoder.get_feature_names_out(categorical_features))
        new_data = pd.concat([new_data.drop(categorical_features, axis=1).reset_index(drop=True), new_data_encoded.reset_index(drop=True)], axis=1)

        # Impute
        new_data = pd.DataFrame(imputer.transform(new_data), columns = new_data.columns)

        # Copy the data before scaling
        new_data_unscaled = new_data.copy()

        # Scale
        new_data[numerical_features] = scaler.transform(new_data[numerical_features])

        # Predict class and probabilities
        prediction = pipeline['random_forest'].best_estimator_.named_steps['classifier'].predict(new_data)
        probabilities = pipeline['random_forest'].best_estimator_.named_steps['classifier'].predict_proba(new_data)[0][1]

        # Display the prediction
        st.write("### Prediction")
        st.write("The patient will be readmitted within 6 months: ", prediction[0])

        # Display the prediction probabilities
        st.write("### Prediction probabilities")

        # Assign a string of risk based on the probability
        if probabilities < 0.3:
            output_string = "Low"
        elif probabilities < 0.7:
            output_string = "Medium"
        else:
            output_string = "High"
        
        st.write(f"Risk that the patient will be readmitted within 6 months: {output_string} ({np.round(probabilities, 2)}/1)")

        # Display the SHAP explanations
        st.write("### SHAP Explanations")

        # Generate SHAP explanations
        shap_values = explainer(new_data)

        idx = 0
        exp = shap.Explanation(
            shap_values.values[:,:,1],
            shap_values.base_values[:,1],
            shap_values.data,
            display_data=new_data_unscaled,
            feature_names=new_data.columns)

        fig = plt.figure()
        shap.plots.waterfall(exp[idx], max_display=30)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
