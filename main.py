# # Statistical Learning for Healthcare Data
#
# Authors:
#
# - Teo Bucci ([@teobucci](https://github.com/teobucci))
# - Giulia Montani ([@GiuliaMontani](https://github.com/GiuliaMontani))
# - Alice Traversa ([@AliceTraversa](https://github.com/AliceTraversa))
#
# For the analysis to be reproducible the folder `hospitalized-patients-with-heart-failure-integrating-electronic-healthcare-records-and-external-outcome-data-1.2` provided must be in the same directory as this script.
#
# ## Project Goal
#
# The goal of this problem is to predict the readmission at 6 months from a dataset TODO scrivere bene la descrizione dell'obiettivo e in cosa consiste il dataset, cos'è ogni riga.

# # Import external libraries
#
# Here we import all the libraries we will use.
#
# TODO qualcosa sull'environment

# +
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
# %config InlineBackend.figure_format='retina'

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc

from pathlib import Path
# -

# # Load data

# Load the dataset
DATA_FOLDER = Path() / "hospitalized-patients-with-heart-failure-integrating-electronic-healthcare-records-and-external-outcome-data-1.2"
df = pd.read_csv((DATA_FOLDER / "dat.csv"), index_col=0)
df

# # Data exploration
#
# ## Information about the 

# Check the shape of the dataset
df.shape

# Display the first five rows of the dataset
df.head()

# Check the summary statistics of the dataset
df.describe()

# ## Missing values

df.dtypes.unique()

# Identify discrete and continuous variables
discrete_vars = [col for col in df.columns if df[col].dtype == 'int64']
continuous_vars = [col for col in df.columns if df[col].dtype == 'float64']
categorical_vars = [col for col in df.columns if df[col].dtype == 'O']


# +
def process_var_list(df, list_vars):
    df_na = df[list_vars].isnull()
    list_vars = df_na.sum() / len(df_na.index) * 100
    list_vars = list_vars.sort_values(ascending=False)
    list_vars = list_vars[list_vars != 0]
    return list_vars

discrete_missing_percentages = process_var_list(df, discrete_vars)
continuous_missing_percentages = process_var_list(df, continuous_vars)
categorical_missing_percentages = process_var_list(df, categorical_vars)

print(f"List discrete_missing_percentages contains {len(discrete_missing_percentages)} elements")
print(f"List continuous_missing_percentages contains {len(continuous_missing_percentages)} elements")
print(f"List categorical_missing_percentages contains {len(categorical_missing_percentages)} element")
# -

# importante da vedere
df['NYHA.cardiac.function.classification'].unique()

# +
# Create subplots for discrete and continuous variables
fig, ax = plt.subplots(figsize=(10,20))

palette = sns.color_palette("RdYlGn",n_colors=len(continuous_missing_percentages))
# https://r02b.github.io/seaborn_palettes/
# palette.reverse()
# in realtà meglio l'approccio con la norma perché così tanti alla stessa lunghezza sono di colore diverso (sbagliato)

# Plot bar charts for discrete and continuous variables
sns.barplot(orient='h', y=continuous_missing_percentages.index, x=continuous_missing_percentages, ax=ax, palette=palette)

# Set axis labels and titles for each subplot
ax2.set_title('Percentage of Missing Values in Continuous Variables')
ax2.set_xlabel('Column')
ax2.set_ylabel('Percentage Missing (%)')
ax2.tick_params(axis='x', labelrotation=90)

plt.show()
# -

# ## Correlation

# prepare confronto tra distribuzioni di variabili discrete, continue, categoriche con kde

# Compute the correlation matrix
corr_matrix = df.corr(numeric_only=True)

# +
# Plot the correlation matrix using seaborn
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(corr_matrix,
            annot=False, fmt='.2f',
            cmap='coolwarm', center=0, cbar=True,
            linewidths=.5,
            ax=ax,
            mask=np.tril(corr_matrix, k=-1))


# Add x-axis and y-axis labels
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)

# Show the plot
plt.show()
# -

# ## Visualizations of continuous and discrete data distributions

# Visualize the distribution of the target variable
sns.countplot(data=df) # TODO capire

# # Preprocessing

# +
# Separate the target variable from the features
X = df.drop(['target'], axis=1)
y = df['target']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Select the top k features using the ANOVA F-value
k_best = SelectKBest(f_classif, k=10)
X_train = k_best.fit_transform(X_train, y_train)
X_test = k_best.transform(X_test)
# -

# # Imputing missing values

# Impute missing values using the mean strategy
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# # Model selection and performance analysis

# +
# Train and evaluate multiple models
models = [LogisticRegression(), DecisionTreeClassifier(), RandomForestClassifier(), SVC()]

for model in models:
    # Train the model on the training set
    model.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = model.predict(X_test)

    # Calculate the accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    print(model.__class__.__name__, 'Accuracy:', accuracy)

    # Calculate the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, cmap='coolwarm')
    plt.title(model.__class__.__name__ + ' Confusion Matrix')
    plt.show()

    # Calculate the ROC curve
    y_score = model.predict_proba(X_test)[:,1]
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)

    # Plot the ROC curve
    plt.plot(fpr, tpr, label=model.__class__.__name__ + ' (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(model.__class__.__name__ + ' ROC Curve')
    plt.legend(loc="lower right")

plt.show()
# -

# |     | Variables                                                     | Description                                                                                                                                                                                                                                                                                                         |
# |-------|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
# | 1   | inpatient.number                                              | The patient unique ID                                                                                                                                                                                                                                                                                               |
# | 2   | DestinationDischarge                                          | Destination of hospital discharge, recorded after discharge                                                                                                                                                                                                                                                         |
# | 3   | admission.ward                                                | first admission ward                                                                                                                                                                                                                                                                                                |
# | 4   | admission.way                                                 | possible ways of admission are Emergency vs. non-emergency                                                                                                                                                                                                                                                          |
# | 5   | occupation                                                    | occupation                                                                                                                                                                                                                                                                                                          |
# | 6   | discharge.department                                          | the patient discharged from                                                                                                                                                                                                                                                                                         |
# | 7   | visit.times                                                   | the number of hospital admissions before this hospitalization                                                                                                                                                                                                                                                       |
# | 8   | gender                                                        | gender: Male, Female                                                                                                                                                                                                                                                                                                |
# | 9   | body.temperature                                              | body temperature in degrees celsius                                                                                                                                                                                                                                                                                 |
# | 10  | pulse                                                         | pulse rate (beats per minute)                                                                                                                                                                                                                                                                                       |
# | 11  | respiration                                                   | respiratory rate (breaths/min)                                                                                                                                                                                                                                                                                      |
# | 12  | systolic.blood.pressure                                       | systolic blood pressure (mmHg)                                                                                                                                                                                                                                                                                      |
# | 13  | diastolic.blood.pressure                                      | diastolic blood pressure (mmHg)                                                                                                                                                                                                                                                                                     |
# | 14  | map                                                           | mean arterial pressure (mmHg)                                                                                                                                                                                                                                                                                       |
# | 15  | weight                                                        | weight (kg)                                                                                                                                                                                                                                                                                                         |
# | 16  | height                                                        | height (m)                                                                                                                                                                                                                                                                                                          |
# | 17  | BMI                                                           | BMI (kg/m^2)                                                                                                                                                                                                                                                                                                        |
# | 18  | type.of.heart.failure                                         | type of heart failure (left, right, both)                                                                                                                                                                                                                                                                           |
# | 19  | NYHA.cardiac.function.classification                          | NYHA.cardiac.function.classification                                                                                                                                                                                                                                                                                |
# | 20  | Killip.grade                                                  | Killip.grade: Class 1 No rales, no 3rd heart sound; Class 2 Rales in <1⁄2 lung field or presence of a 3rd heart sound; Class 3 Rales in >1⁄2 lung field–pulmonary edema;Class 4 Cardiogenic shock–determined clinically                                                                                             |
# | 21  | myocardial.infarction                                         | myocardial.infarction                                                                                                                                                                                                                                                                                               |
# | 22  | congestive.heart.failure                                      | congestive heart failure (e.g., A minority of patients were not coded as having the diagnosis of “congestive heart failure” in the comorbidity list because they did not have past history of congestive heart failure on admission. They were diagnosed with HF for the first time in this index hospitalization.) |
# | 23  | peripheral.vascular.disease                                   | peripheral.vascular.disease                                                                                                                                                                                                                                                                                         |
# | 24  | cerebrovascular.disease                                       | cerebrovascular.disease                                                                                                                                                                                                                                                                                             |
# | 25  | dementia                                                      | dementia                                                                                                                                                                                                                                                                                                            |
# | 26  | Chronic.obstructive.pulmonary.disease                         | Chronic.obstructive.pulmonary.disease                                                                                                                                                                                                                                                                               |
# | 27  | connective.tissue.disease                                     | connective.tissue.disease                                                                                                                                                                                                                                                                                           |
# | 28  | peptic.ulcer.disease                                          | peptic.ulcer.disease                                                                                                                                                                                                                                                                                                |
# | 29  | diabetes                                                      | diabetes                                                                                                                                                                                                                                                                                                            |
# | 30  | moderate.to.severe.chronic.kidney.disease                     | moderate to severe chronic kidney disease with Glomerular filtration rate < 60 ml/min                                                                                                                                                                                                                               |
# | 31  | hemiplegia                                                    | hemiplegia                                                                                                                                                                                                                                                                                                          |
# | 32  | leukemia                                                      | leukemia                                                                                                                                                                                                                                                                                                            |
# | 33  | malignant.lymphoma                                            | malignant.lymphoma                                                                                                                                                                                                                                                                                                  |
# | 34  | solid.tumor                                                   | solid.tumor                                                                                                                                                                                                                                                                                                         |
# | 35  | liver.disease                                                 | liver.disease                                                                                                                                                                                                                                                                                                       |
# | 36  | AIDS                                                          | AIDS                                                                                                                                                                                                                                                                                                                |
# | 37  | CCI.score                                                     | Charlson Comorbidity Index score                                                                                                                                                                                                                                                                                    |
# | 38  | type.II.respiratory.failure                                   | type.II.respiratory.failure                                                                                                                                                                                                                                                                                         |
# | 39  | consciousness                                                 | consciousness                                                                                                                                                                                                                                                                                                       |
# | 40  | eye.opening                                                   | eye.opening                                                                                                                                                                                                                                                                                                         |
# | 41  | verbal.response                                               | verbal.response                                                                                                                                                                                                                                                                                                     |
# | 42  | movement                                                      | movement                                                                                                                                                                                                                                                                                                            |
# | 43  | respiratory.support.                                          | respiratory support defined as the use of either invasive or non-invasive mechanical ventilation                                                                                                                                                                                                                    |
# | 44  | oxygen.inhalation                                             | oxygen.inhalation                                                                                                                                                                                                                                                                                                   |
# | 45  | fio2                                                          | fraction of inspired oxygenation (%)                                                                                                                                                                                                                                                                                |
# | 46  | acute.renal.failure                                           | presence of acute kidney injury defined as Increase of serum creatinine ≥ 0.3 mg per dL (26.52 μmol per L) or ≥ 1.5- to twofold from baseline, or urine output < 0.5 mL per kg per hour for more than six hours                                                                                                     |
# | 47  | LVEF                                                          | Left Ventricular Ejection Fraction (%), normal range: 55% - 70%                                                                                                                                                                                                                                                     |
# | 48  | left.ventricular.end.diastolic.diameter.LV                    | left.ventricular.end.diastolic.diameter.LV (cm), normal range: 3.5 - 5.6 cm                                                                                                                                                                                                                                         |
# | 49  | mitral.valve.EMS                                              | maximum velocity of the mitral.valve E wave (m/s)                                                                                                                                                                                                                                                                   |
# | 50  | mitral.valve.AMS                                              | maximum velocity of the mitral.valve A wave (m/s)                                                                                                                                                                                                                                                                   |
# | 51  | EA                                                            | E/A ratio, normal range: 0.6-1.32                                                                                                                                                                                                                                                                                   |
# | 52  | tricuspid.valve.return.velocity                               | tricuspid.valve.return.velocity (m/s)                                                                                                                                                                                                                                                                               |
# | 53  | tricuspid.valve.return.pressure                               | tricuspid.valve.return.pressure (mmHg)                                                                                                                                                                                                                                                                              |
# | 54  | outcome.during.hospitalization                                | outcome during hospitalization, recorded after the decision of discharge was made ( living vs. died in the hospital)                                                                                                                                                                                                |
# | 55  | death.within.28.days                                          | death.within.28.days                                                                                                                                                                                                                                                                                                |
# | 56  | re.admission.within.28.days                                   | re.admission.within.28.days                                                                                                                                                                                                                                                                                         |
# | 57  | death.within.3.months                                         | death.within.3.months                                                                                                                                                                                                                                                                                               |
# | 58  | re.admission.within.3.months                                  | re.admission.within.3.months                                                                                                                                                                                                                                                                                        |
# | 59  | death.within.6.months                                         | death.within.6.months                                                                                                                                                                                                                                                                                               |
# | 60  | re.admission.within.6.months                                  | re.admission.within.6.months                                                                                                                                                                                                                                                                                        |
# | 61  | time.of.death..days.from.admission.                           | time.of.death..days.from.admission.                                                                                                                                                                                                                                                                                 |
# | 62  | re.admission.time..days.from.admission.                       | re.admission.time..days.from.admission.                                                                                                                                                                                                                                                                             |
# | 63  | return.to.emergency.department.within.6.months                | return.to.emergency.department.within.6.months                                                                                                                                                                                                                                                                      |
# | 64  | time.to.emergency.department.within.6.months                  | time.to.emergency.department.within.6.months                                                                                                                                                                                                                                                                        |
# | 65  | creatinine.enzymatic.method                                   | creatinine (enzymatic method, umol/l); normal range:44-110 umol/L                                                                                                                                                                                                                                                   |
# | 66  | urea                                                          | urea (mmol/l), ref:1.7 - 8.3 mmol/L                                                                                                                                                                                                                                                                                 |
# | 67  | uric.acid                                                     | uric.acid (umol/L); ref: 150 - 440 umol/L                                                                                                                                                                                                                                                                           |
# | 68  | glomerular.filtration.rate                                    | glomerular.filtration.rate (mL/min/1.73 m^2); ref: 90 -120                                                                                                                                                                                                                                                          |
# | 69  | cystatin                                                      | cystatin (mg/L); ref:0.51–0.98                                                                                                                                                                                                                                                                                      |
# | 70  | white.blood.cell                                              | white blood cell count (*10^9/L); ref: 4 -10                                                                                                                                                                                                                                                                        |
# | 71  | monocyte.ratio                                                | monocyte.ratio (%); ref: 3 -11.4                                                                                                                                                                                                                                                                                    |
# | 72  | monocyte.count                                                | monocyte.count (*10^9/L); ref:0.2 - 0.8                                                                                                                                                                                                                                                                             |
# | 73  | red.blood.cell                                                | red blood cell count (*10^12/L); ref: 3.5 - 5.5                                                                                                                                                                                                                                                                     |
# | 74  | coefficient.of.variation.of.red.blood.cell.distribution.width | coefficient of variation of.red.blood.cell.distribution.width(%); ref: 0 -15                                                                                                                                                                                                                                        |
# | 75  | standard.deviation.of.red.blood.cell.distribution.width       | standard.deviation.of.red.blood.cell.distribution.width (fL); ref: 40 - 53                                                                                                                                                                                                                                          |
# | 76  | mean.corpuscular.volume                                       | mean.corpuscular.volume (fL); ref: 82 - 96                                                                                                                                                                                                                                                                          |
# | 77  | hematocrit                                                    | hematocrit(%); ref: 35 - 50                                                                                                                                                                                                                                                                                         |
# | 78  | lymphocyte.count                                              | lymphocyte.count (*10^9/L); ref:0.8 - 4                                                                                                                                                                                                                                                                             |
# | 79  | mean.hemoglobin.volume                                        | mean.hemoglobin.content(pg); ref: 27 - 35                                                                                                                                                                                                                                                                           |
# | 80  | mean.hemoglobin.concentration                                 | mean.hemoglobin.concentration (g/L); ref: 320 - 360                                                                                                                                                                                                                                                                 |
# | 81  | mean.platelet.volume                                          | mean.platelet.volume(fL); ref: 6.5 - 12                                                                                                                                                                                                                                                                             |
# | 82  | basophil.ratio                                                | basophil.ratio; ref: 0 -1                                                                                                                                                                                                                                                                                           |
# | 83  | basophil.count                                                | basophil.count(*10^9/L); ref: 0 - 0.1                                                                                                                                                                                                                                                                               |
# | 84  | eosinophil.ratio                                              | eosinophil.ratio; ref: 0.5 -5                                                                                                                                                                                                                                                                                       |
# | 85  | eosinophil.count                                              | eosinophil.count(*10^9/L); ref: 0.02-0.5                                                                                                                                                                                                                                                                            |
# | 86  | hemoglobin                                                    | hemoglobin (g/L); ref: 110 - 160                                                                                                                                                                                                                                                                                    |
# | 87  | platelet                                                      | platelet(*10^9/L); ref:100 - 300                                                                                                                                                                                                                                                                                    |
# | 88  | platelet.distribution.width                                   | platelet.distribution.width (fL); ref: 9 -17                                                                                                                                                                                                                                                                        |
# | 89  | platelet.hematocrit                                           | platelet.hematocrit(%); ref: 0.108 - 0.282                                                                                                                                                                                                                                                                          |
# | 90  | neutrophil.ratio                                              | neutrophil.ratio; ref: 0.5 -0.7                                                                                                                                                                                                                                                                                     |
# | 91  | neutrophil.count                                              | neutrophil.count(*10^9/L); 2 -7                                                                                                                                                                                                                                                                                     |
# | 92  | D.dimer                                                       | D.dimer(mg/l); ref: 0 - 0.55                                                                                                                                                                                                                                                                                        |
# | 93  | international.normalized.ratio                                | international.normalized.ratio; ref: 0.8 - 1.5                                                                                                                                                                                                                                                                      |
# | 94  | activated.partial.thromboplastin.time                         | activated.partial.thromboplastin.time(s); ref: 20 -40                                                                                                                                                                                                                                                               |
# | 95  | thrombin.time                                                 | thrombin.time (s); ref: 14-21                                                                                                                                                                                                                                                                                       |
# | 96  | prothrombin.activity                                          | prothrombin.activity(%); ref: 70 -120                                                                                                                                                                                                                                                                               |
# | 97  | prothrombin.time.ratio                                        | prothrombin.time.ratio                                                                                                                                                                                                                                                                                              |
# | 98  | fibrinogen                                                    | fibrinogen (g/L); ref: 2 -4                                                                                                                                                                                                                                                                                         |
# | 99  | high.sensitivity.troponin                                     | high.sensitivity.troponin (pg/mL); ref:0 -14                                                                                                                                                                                                                                                                        |
# | 100 | myoglobin                                                     | myoglobin (ng/ml); ref: 28 - 72                                                                                                                                                                                                                                                                                     |
# | 101 | carbon.dioxide.binding.capacity                               | carbon.dioxide.binding.capacity (mmol/L); ref: 22 -30                                                                                                                                                                                                                                                               |
# | 102 | calcium                                                       | calcium (mmol/L); ref: 2.11 - 2.52                                                                                                                                                                                                                                                                                  |
# | 103 | potassium                                                     | potassium(mmol/L); ref:3.5 - 5.3                                                                                                                                                                                                                                                                                    |
# | 104 | chloride                                                      | chloride(mmol/L); ref:99 - 110                                                                                                                                                                                                                                                                                      |
# | 105 | sodium                                                        | sodium(mmol/L); ref:137 - 147                                                                                                                                                                                                                                                                                       |
# | 106 | Inorganic.Phosphorus                                          | Inorganic.Phosphorus (mmol/L); ref: 0.85-1.51                                                                                                                                                                                                                                                                       |
# | 107 | serum.magnesium                                               | serum.magnesium (mmol/L); ref:0.75-1.02                                                                                                                                                                                                                                                                             |
# | 108 | creatine.kinase.isoenzyme.to.creatine.kinase                  | creatine.kinase.isoenzyme.to.creatine.kinase; ref: 0 -0.05                                                                                                                                                                                                                                                          |
# | 109 | hydroxybutyrate.dehydrogenase.to.lactate.dehydrogenase        | hydroxybutyrate.dehydrogenase.to.lactate.dehydrogenase; ref: 0.2-0.8                                                                                                                                                                                                                                                |
# | 110 | hydroxybutyrate.dehydrogenase                                 | hydroxybutyrate.dehydrogenase(U/L); ref: 90 -180                                                                                                                                                                                                                                                                    |
# | 111 | glutamic.oxaloacetic.transaminase                             | glutamic.oxaloacetic.transaminase(IU/L); ref: 15 -40                                                                                                                                                                                                                                                                |
# | 112 | creatine.kinase                                               | creatine.kinase (IU/L); ref: 22 -270                                                                                                                                                                                                                                                                                |
# | 113 | creatine.kinase.isoenzyme                                     | creatine.kinase.isoenzyme (IU/L); ref: 0-32                                                                                                                                                                                                                                                                         |
# | 114 | lactate.dehydrogenase                                         | lactate.dehydrogenase(IU/L); ref: 90 -282                                                                                                                                                                                                                                                                           |
# | 115 | brain.natriuretic.peptide                                     | brain.natriuretic.peptide (pg/ml); ref: 0 -100                                                                                                                                                                                                                                                                      |
# | 116 | high.sensitivity.protein                                      | high.sensitivity.C reactive protein (mg/L); ref: 0- 5                                                                                                                                                                                                                                                               |
# | 117 | nucleotidase                                                  | nucleotidase(U/L); ref: 0-10                                                                                                                                                                                                                                                                                        |
# | 118 | fucosidase                                                    | fucosidase(U/L); ref: 0-40                                                                                                                                                                                                                                                                                          |
# | 119 | albumin                                                       | albumin (g/L); ref: 40-55                                                                                                                                                                                                                                                                                           |
# | 120 | white.globulin.ratio                                          | white.globulin.ratio; ref: 1.2-2.4                                                                                                                                                                                                                                                                                  |
# | 121 | cholinesterase                                                | cholinesterase(U/L); ref:3000-13000                                                                                                                                                                                                                                                                                 |
# | 122 | glutamyltranspeptidase                                        | glutamyltranspeptidase(U/L); ref:10-60                                                                                                                                                                                                                                                                              |
# | 123 | glutamic.pyruvic.transaminase                                 | glutamic.pyruvic.transaminase(U/L); ref: 9-50                                                                                                                                                                                                                                                                       |
# | 124 | glutamic.oxaliplatin                                          | AST/ALT ratio; ref: <0.8                                                                                                                                                                                                                                                                                            |
# | 125 | indirect.bilirubin                                            | indirect.bilirubin (umol/L); ref: 0-16                                                                                                                                                                                                                                                                              |
# | 126 | alkaline.phosphatase                                          | alkaline.phosphatase (U/L); ref: 45-125                                                                                                                                                                                                                                                                             |
# | 127 | globulin                                                      | globulin (g/L); ref: 20-40                                                                                                                                                                                                                                                                                          |
# | 128 | direct.bilirubin                                              | direct.bilirubin (umol/L); ref: 0-6.8                                                                                                                                                                                                                                                                               |
# | 129 | total.bilirubin                                               | total.bilirubin(umol/l); ref: 2-20.4                                                                                                                                                                                                                                                                                |
# | 130 | total.bile.acid                                               | total.bile.acid(umol/l); ref: 0-20                                                                                                                                                                                                                                                                                  |
# | 131 | total.protein                                                 | total.protein(g/l); ref: 65-85                                                                                                                                                                                                                                                                                      |
# | 132 | erythrocyte.sedimentation.rate                                | erythrocyte.sedimentation.rate(mm/h); ref: 0-43                                                                                                                                                                                                                                                                     |
# | 133 | cholesterol                                                   | cholesterol(mmol/l); ref:2.9-5.68                                                                                                                                                                                                                                                                                   |
# | 134 | low.density.lipoprotein.cholesterol                           | low.density.lipoprotein.cholesterol(mmol/l); ref:0-3.36                                                                                                                                                                                                                                                             |
# | 135 | triglyceride                                                  | triglyceride(mmol/l); ref:0.22-2.26                                                                                                                                                                                                                                                                                 |
# | 136 | high.density.lipoprotein.cholesterol                          | high.density.lipoprotein.cholesterol(mmol/l); ref:0.9-2.19                                                                                                                                                                                                                                                          |
# | 137 | homocysteine                                                  | homocysteine(umol/l); ref: 0-15                                                                                                                                                                                                                                                                                     |
# | 138 | apolipoprotein.A                                              | apolipoprotein.A(g/l); ref: 1.2-1.8                                                                                                                                                                                                                                                                                 |
# | 139 | apolipoprotein.B                                              | apolipoprotein.B (g/l); ref:0.6-1.14                                                                                                                                                                                                                                                                                |
# | 140 | lipoprotein                                                   | lipoprotein(mg/l); ref: 0-300                                                                                                                                                                                                                                                                                       |
# | 141 | pH                                                            | pH; ref: 7.35-7.45                                                                                                                                                                                                                                                                                                  |
# | 142 | standard.residual.base                                        | standard base excess(mmol/l); ref: -3 - 3                                                                                                                                                                                                                                                                           |
# | 143 | standard.bicarbonate                                          | standard.bicarbonate (mmol/l); ref: 21.8-26.9                                                                                                                                                                                                                                                                       |
# | 144 | partial.pressure.of.carbon.dioxide                            | partial.pressure.of.carbon.dioxide (mmHg); 35-45                                                                                                                                                                                                                                                                    |
# | 145 | total.carbon.dioxide                                          | total.carbon.dioxide(mmol/l); ref:24-32                                                                                                                                                                                                                                                                             |
# | 146 | methemoglobin                                                 | methemoglobin (%); ref: 0-6                                                                                                                                                                                                                                                                                         |
# | 147 | hematocrit.blood.gas                                          | hematocrit.blood.gas(%); ref: 37-49                                                                                                                                                                                                                                                                                 |
# | 148 | reduced.hemoglobin                                            | reduced.hemoglobin (%); ref: 0-5                                                                                                                                                                                                                                                                                    |
# | 149 | potassium.ion                                                 | potassium.ion(mmol/l); ref:3.5-4.5                                                                                                                                                                                                                                                                                  |
# | 150 | chloride.ion                                                  | chloride.ion(mmol/l); ref:98-106                                                                                                                                                                                                                                                                                    |
# | 151 | sodium.ion                                                    | sodium.ion(mmol/l); ref:136-146                                                                                                                                                                                                                                                                                     |
# | 152 | glucose.blood.gas                                             | glucose.blood.gas(mmol/l); ref: 3.9-6.1                                                                                                                                                                                                                                                                             |
# | 153 | lactate                                                       | lactate(mmol/l); ref: 0.5-2.2                                                                                                                                                                                                                                                                                       |
# | 154 | measured.residual.base                                        | measured base excess(mmol/L); ref: -3 - +3                                                                                                                                                                                                                                                                          |
# | 155 | measured.bicarbonate                                          | measured.bicarbonate mmol/L); ref: 22-30                                                                                                                                                                                                                                                                            |
# | 156 | carboxyhemoglobin                                             | carboxyhemoglobin(%); ref: 0-1.6                                                                                                                                                                                                                                                                                    |
# | 157 | body.temperature.blood.gas                                    | body.temperature.blood.gas (℃)                                                                                                                                                                                                                                                                                      |
# | 158 | oxygen.saturation                                             | oxygen.saturation(%); ref: 93-98                                                                                                                                                                                                                                                                                    |
# | 159 | partial.oxygen.pressure                                       | partial.oxygen.pressure(mmHg); ref: 83-108                                                                                                                                                                                                                                                                          |
# | 160 | oxyhemoglobin                                                 | oxyhemoglobin(%); ref:94-97                                                                                                                                                                                                                                                                                         |
# | 161 | anion.gap                                                     | anion.gap(mmol/l); ref:12-16                                                                                                                                                                                                                                                                                        |
# | 162 | free.calcium                                                  | free.calcium(mmol/l); ref:1.15-1.29                                                                                                                                                                                                                                                                                 |
# | 163 | total.hemoglobin                                              | total.hemoglobin(g/L); ref: 130-175                                                                                                                                                                                                                                                                                 |
# | 164 | GCS                                                           | Glasgow Coma Scale: range 3-15                                                                                                                                                                                                                                                                                      |
# | 165 | dischargeDay                                                  | dischargeDay: days from admission to hospital discharge                                                                                                                                                                                                                                                             |
# | 166 | ageCat                                                        | ageCat:the age is categorized in decades                                                                                                                                                                                                                                                                            |
#
