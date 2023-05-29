import pickle
import streamlit as st
import pandas as pd
import numpy as np

classification_threshold = 0.5

# Read the model using pickle
with open('./output/final_model.pkl', 'rb') as f:
    final_model = pickle.load(f)

# Read encoder
with open('./output/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Read file ccolumn_info with pkl
with open('./output/column_info.pkl', 'rb') as f:
    column_info = pickle.load(f)

# Read categorical features
with open('./output/cols_categorical.pkl', 'rb') as f:
    cols_categorical = pickle.load(f)

# Read numerical features
with open('./output/cols_numerical.pkl', 'rb') as f:
    cols_numerical = pickle.load(f)

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
        new_data_encoded = pd.DataFrame(encoder.transform(new_data[cols_categorical]), columns=encoder.get_feature_names_out(cols_categorical))
        new_data = pd.concat([new_data.drop(cols_categorical, axis=1).reset_index(drop=True), new_data_encoded.reset_index(drop=True)], axis=1)

        # Predict class and probabilities
        y_score = final_model.predict_proba(new_data)[0][1]
        y_pred = (y_score >= classification_threshold).astype(bool)

        # Display the prediction
        st.write("### Prediction")
        st.write("The patient will be readmitted within 6 months: ", y_pred)

        # Display the prediction probabilities
        st.write("### Prediction probabilities")

        # Assign a string of risk based on the probability
        if y_score < 0.3:
            output_string = "Low"
        elif y_score < 0.7:
            output_string = "Medium"
        else:
            output_string = "High"
        
        st.write(f"Risk that the patient will be readmitted within 6 months: {output_string} ({np.round(y_score, 2)}/1)")

if __name__ == "__main__":
    main()
