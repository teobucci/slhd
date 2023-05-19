# this is the commad to run the app
# streamlit run app.py

import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import shap

# Set up imputer and scaler
imputer = SimpleImputer(strategy='median')
scaler = StandardScaler()

# Load the pre-trained model
model = RandomForestClassifier()  # Replace with your own model

# Load the SHAP explainer
explainer = shap.Explainer(model)

# Helper function to preprocess user inputs
def preprocess_inputs(inputs):
    # Convert inputs to DataFrame
    df = pd.DataFrame(inputs, index=[0])
    df.columns = ['feature_1', 'feature_2', 'feature_3']  # Replace with your own feature names

    # Impute missing values
    df = pd.DataFrame(imputer.transform(df), columns=df.columns)

    # Scale the features
    df = pd.DataFrame(scaler.transform(df), columns=df.columns)

    return df

# Helper function to get SHAP explanations
def get_shap_explanations(inputs):
    processed_inputs = preprocess_inputs(inputs)
    shap_values = explainer.shap_values(processed_inputs)
    return shap_values

# Main app
def main():
    st.title("Binary Classification App")

    # Collect user inputs
    feature_1 = st.number_input("Feature 1", value=0.0)
    feature_2 = st.number_input("Feature 2", value=0.0)
    feature_3 = st.number_input("Feature 3", value=0.0)
    user_inputs = [feature_1, feature_2, feature_3]

    # Set the page title and favicon
    st.set_page_config(page_title='Predicting Credit Card Fraud',
                        page_icon='💳')

    # Set the title
    st.title('Heart Failure: predicting readmission after 6 months')

    # Set the subheader
    st.subheader('A Streamlit app to predict readmission after 6 months')

    # Set the text
    st.text('This app will predict whether a patient will be readmitted to the hospital within 6 months of their initial visit.')

    # Set the text
    st.text('The data used to train the model was given during the course of Statistical Learning for Healthcare Data.')

    # Create UI
    st.sidebar.header('User Input Parameters')

    # Create function to get user input
    def get_user_input():
        # Create dictionary to store user input
        user_input = {}

        # Create slider for time
        user_input['time'] = st.sidebar.slider('Time', 0, 300, 150)

        # Create slider for anaemia
        user_input['anaemia'] = st.sidebar.selectbox('Anaemia', ('No', 'Yes'))


    

    # Perform prediction
    if st.button("Predict"):
        # Preprocess user inputs
        processed_inputs = preprocess_inputs(user_inputs)

        # Predict class and probabilities
        prediction = model.predict(processed_inputs)[0]
        probabilities = model.predict_proba(processed_inputs)[0]

        # Compute score segments
        segment_1 = round(probabilities[0], 2)  # 0 to 0.3
        segment_2 = round(probabilities[1], 2)  # 0.3 to 0.6
        segment_3 = round(probabilities[2], 2)  # 0.6 to 1

        st.write("### Prediction")
        st.write(f"Class: {prediction}")
        st.write("### Probability Segments")
        st.write(f"0 to 0.3: {segment_1}")
        st.write(f"0.3 to 0.6: {segment_2}")
        st.write(f"0.6 to 1: {segment_3}")

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








