# # Heart Failure: predicting hospital re-admission after 6 months
#
# Project for the _Statistical Learning for Healthcare Data_ (056867) course held at Politecnico di Milano in the academic year 2022/2023 by Professor Manuela Ferrario and Professor Anna Maria Paganoni.
#
# It is recommended to [**view this notebook in nbviewer**](https://nbviewer.org/) for the best viewing experience.
#
# You can also [execute the code in this notebook on Binder](https://mybinder.org/) - no local installation required.
#
# Authors:
#
# - Teo Bucci ([@teobucci](https://github.com/teobucci))
# - Giulia Montani ([@GiuliaMontani](https://github.com/GiuliaMontani))
# - Alice Traversa ([@AliceTraversa](https://github.com/AliceTraversa))

# ## 1. Introduction
#
# ### Explanation of the problem and objective
#
#
# Heart Failure (HF) is a prevalent condition with high readmission rates: the literature states that the number of HF cases worldwide almost doubled from 33.5 million in 1990 to 64.3 million in 2017.
#
# Studies also suggest that half of the patients diagnosed with HF will be re-admitted once within a year and 20% will be re-admitted twice or more.
#
# The focus of this analysis is on predicting the readmission within 6 months for HF patients.
#
# ### Data description
#
# The data has been provided in the folder `hospitalized-patients-with-heart-failure-integrating-electronic-healthcare-records-and-external-outcome-data-1.2` and for the analysis to be reproducible it must be in the same directory as this script.

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

# ## 2. Materials and Methods
#
# ### Importing necessary libraries and dataset
#
# Here we import all the libraries we will use. For reproducibility make sure to install them with `pip install -r requirements.txt`.

# +
import pickle
import re
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
# %config InlineBackend.figure_format='retina'

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
# from sklearn.model_selection import cross_val_score, cross_val_predict
# from sklearn.experimental import enable_iterative_imputer
# from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer, KNNImputer
# from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier
# from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
from sklearn.metrics import accuracy_score, make_scorer, cohen_kappa_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import class_weight
import scipy.cluster.hierarchy as spc
from collections import Counter
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import shap

from IPython.display import Image
from mlxtend.plotting import plot_confusion_matrix
# -

# Fix the seed for reproducibility later.

SEED = 42

# Use the `pipreqs` library to produce a `requirements.txt`

# +
# #!pipreqsnb . --force
# #!pipreqs . --force
# -

# Create an output folder for pickle files and figures.

OUTPUT_FOLDER = Path() / 'output'
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# For reproducibility purposes we load the (previously installed) `watermark` extension and print the current versions of the software.

# %load_ext watermark

# %watermark -m -v -iv

# As first step we load the data, setting the index to the first column since it's already numbered

DATA_FOLDER = Path() / "hospitalized-patients-with-heart-failure-integrating-electronic-healthcare-records-and-external-outcome-data-1.2"
df = pd.read_csv((DATA_FOLDER / "dat.csv"), index_col=1)
df = df.drop(columns=df.columns[0], axis=1)

# #### Drugs integration

df_drugs = pd.read_csv((DATA_FOLDER / "dat_md.csv"), index_col=1)
df_drugs = df_drugs.drop(columns=df_drugs.columns[0], axis=1)

df_drugs.head()

# Check which patients are missing from the drugs dataframe
missing_patients = ~df.index.isin(df_drugs.index)
print('Missing patients from the drugs dataframe:')
print(df[missing_patients].index)

# Check the contrary (i.e. if there are entries in the drug dataframe that don't corresponde to any patient in the main df)
missing_drugs = ~df_drugs.index.isin(df.index)
print('Missing patients from the patients dataframe:')
print(df_drugs[missing_drugs].index)

# More drugs were given to the same patient.
#
# Let's see the unique drugs.

pd.DataFrame(df_drugs['Drug_name'].unique(), columns=['name'])

# Create a pivot table of drugs, with patients as rows and drugs as columns
drug_pivot = df_drugs.pivot_table(index='inpatient.number', columns='Drug_name', fill_value=0, aggfunc=lambda x: 1)
drug_pivot.head()

# Merge the patient dataframe with the drug pivot table
merged_df = pd.merge(df, drug_pivot, on='inpatient.number', how='left')
merged_df.head()

# Fill patients without any drug with No
for drug_name in drug_pivot.columns:
    merged_df[drug_name] = merged_df[drug_name].fillna(value=0)

INCLUDE_DRUGS = False

if INCLUDE_DRUGS:
    df = merged_df

# ### Information about the memory usage
#
# We check the memory usage of the `DataFrame`.

df.info(memory_usage='deep')

# Currently we're using 4.2 MB.

# ### Setting the correct column type
#
# To reduce the memory usage and facilitate the overall performance, let's set properly the column types, starting by investigating which types Pandas has assigned to the columns.

# +
# get the data types of each column
dtypes = df.dtypes

# count the number of columns of each type
counts = dtypes.value_counts()

# print the counts
print(counts)
# -

# Now let's look closer to which columns have which type

# +
# group the column names by type
type_dict = {}
for col, dtype in dtypes.items():
    if dtype not in type_dict:
        type_dict[dtype] = []
    type_dict[dtype].append(col)

# print the number of columns of each type
# print("Number of columns by type:")
# for dtype, cols in type_dict.items():
#     print(f"• {dtype}: {len(cols)} columns ({', '.join(cols)})")
#     print('-'*80)
# -

# Now let's dive even deeper and see the values per feature to see if the type is correct

# +
# print value counts for categorical and boolean columns
# for dtype, cols in type_dict.items():
#     if dtype == 'float64': # skip continuous
#         continue
#     if not cols:
#         continue
#     print(f"Value counts for {dtype} columns:\n")
#     for col in cols:
#         print(df[col].value_counts(), '\n')
#     print('-'*80)
# -

# Now that we know what to correct, let's perform the changes

df = df.astype({
    'DestinationDischarge': 'category',
    'admission.ward': 'category',
    'admission.way': 'category',
    'occupation': 'category',
    'discharge.department': 'category',
    'gender': 'category',
    'type.of.heart.failure': 'category',
    'NYHA.cardiac.function.classification': 'category',
    'Killip.grade': 'category',
    'type.II.respiratory.failure': 'category',
    'consciousness': 'category',
    'respiratory.support.': 'category',
    'oxygen.inhalation': 'category',
    'outcome.during.hospitalization': 'category',
    'ageCat': 'category',
    'myocardial.infarction': 'bool',
    'congestive.heart.failure': 'bool',
    'peripheral.vascular.disease': 'bool',
    'cerebrovascular.disease': 'bool',
    'dementia': 'bool',
    'Chronic.obstructive.pulmonary.disease': 'bool',
    'connective.tissue.disease': 'bool',
    'diabetes': 'bool',
    'hemiplegia': 'bool',
    'leukemia': 'bool',
    'malignant.lymphoma': 'bool',
    'solid.tumor': 'bool',
    'AIDS': 'bool',
    'acute.renal.failure': 'bool',
    'death.within.28.days': 'bool',
    're.admission.within.28.days': 'bool',
    'death.within.3.months': 'bool',
    're.admission.within.3.months': 'bool',
    'death.within.6.months': 'bool',
    're.admission.within.6.months': 'bool',
    'moderate.to.severe.chronic.kidney.disease': 'bool',
    'peptic.ulcer.disease': 'bool',
    'liver.disease': 'bool'
})

# and see if there has been a memory reduce

df.info(memory_usage='deep')

# We now use only 2.0 MB.
#
# Here is a recap of the columns types.

df.info(verbose=True, show_counts=False)

# Check the shape of the dataset

df.shape

# We have 2008 patients and 165 variables.

# ### Removing duplicates

# Remove duplicates rows if there are any.

n_duplicates = df.duplicated().sum()
if not n_duplicates == 0:
    print(f"Removing {n_duplicates} duplicate rows")
    df = df.drop_duplicates()
else:
    print("No duplicate rows found. All good!")

# ### Removing inconsistencies

# We check if there are inconsistencies by looking at two variables: `DestinationDischarge` and `outcome.during.hospitalization`, when the first is `Died` the second should be `Dead` and vice-versa, therefore we remove patients with this inconsistency.

df[(df['DestinationDischarge'] == 'Died') & (df['outcome.during.hospitalization'] != 'Dead')]

df[(df['DestinationDischarge'] != 'Died') & (df['outcome.during.hospitalization'] == 'Dead')]

df = df.drop(df[(df['DestinationDischarge'] == 'Died') & (df['outcome.during.hospitalization'] != 'Dead')].index)
df = df.drop(df[(df['DestinationDischarge'] != 'Died') & (df['outcome.during.hospitalization'] == 'Dead')].index)

# ### Removing outcome-related variables
#
# Since we're interested in predicting the re-admission at 6 months, it's important to have a look at the following features:
# - `death.within.28.days`
# - `re.admission.within.28.days`
# - `death.within.3.months`
# - `re.admission.within.3.months`
# - `death.within.6.months`
# - `re.admission.within.6.months` - this is our target
# - `time.of.death..days.from.admission.`
# - `re.admission.time..days.from.admission.`
# - `return.to.emergency.department.within.6.months`
# - `time.to.emergency.department.within.6.months`
#
# Given that some patients died before the 6 months, such patients present a target of `0` since they haven't been re-admitted, not because they're healthy, but the exact opposite. Thus keeping them together with living healthy patients doesn't make sense: we remove the dead patients.

# +
# specify the columns to check for True values
cols_to_check = [
    'death.within.28.days',
    'death.within.3.months',
    'death.within.6.months'
]

# remove rows where at least one of the specified columns is True
df = df.loc[~(df[cols_to_check] == True).any(axis=1)]
# -

# Now those columns are meaninglesse as they all have the same value, we'll remove them in the next section.

# It also makes sense that if we want to predict the re-admission at 6 months, we have no knowledge neither at 3 months nor 28 days. Therefore we can drop these features as well.

# +
drop_cols = [
    're.admission.within.28.days',
    're.admission.within.3.months',
    'time.of.death..days.from.admission.',
    're.admission.time..days.from.admission.',
    'return.to.emergency.department.within.6.months',
    'time.to.emergency.department.within.6.months',
]

df = df.drop(drop_cols, axis=1)
# -

df.shape


# Create an utility to quickly get the names of numerical and categorical features.

def get_num_cat(dataframe):
    return dataframe.select_dtypes(include=['float64', 'int64']).columns, dataframe.select_dtypes(include=['category', 'bool']).columns


# ### Removing low-variance variables

cols_numerical, cols_categorical = get_num_cat(df)

# Removing categorical variables with 95% dominance.

# +
frequencies = df[cols_categorical].apply(pd.Series.value_counts)

dominant_categories = frequencies.idxmax()

threshold = 0.95

drop_cols = []
for variable, dominant_category in dominant_categories.items():
    dominant_frequency = frequencies.loc[dominant_category, variable] / df[cols_categorical].shape[0]
    if dominant_frequency > threshold:
        drop_cols.append(variable)

drop_cols
# -

df = df.drop(drop_cols, axis=1)
cols_numerical, cols_categorical = get_num_cat(df)

# Removing numerical variables with 0 variance, i.e. constant variables.

# +
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0)
selector.fit(df[cols_numerical])

const_col = [column for column in cols_numerical 
          if column not in cols_numerical[selector.get_support()]]

const_col
# -

df = df.drop(const_col, axis=1)
cols_numerical, cols_categorical = get_num_cat(df)


# ### Checking for missing values

# Identify categorical and numerical variables

# +
def get_percentage_missing(df):
    df_na = df.isnull()
    list_vars = df_na.sum() / len(df_na.index) * 100
    list_vars = list_vars.sort_values(ascending=False)
    list_vars = list_vars[list_vars != 0]
    return list_vars

numerical_missing = get_percentage_missing(df[cols_numerical])
categorical_missing = get_percentage_missing(df[cols_categorical])

for name, features in zip(['numerical', 'categorical'], [numerical_missing, categorical_missing]):
    print(f"Among the {name} features, {len(features)} contain missing values")
# -

# #### Categorical

# The single categorical feature that contains missing values is `occupation` with 1.34% of missing values.

categorical_missing

# Given the non-clinical nature of the variable and the low percentage of missing values, we simply decide to impute it.

imputer = SimpleImputer(strategy='most_frequent')
df.occupation = imputer.fit_transform(df.occupation.values.reshape(-1,1))[:,0]

# Set its type to `category` since after imputation it's `object`.

df = df.astype({'occupation': 'category'})

cols_numerical, cols_categorical = get_num_cat(df)


# #### Numerical

# There are many more numerical features with missing values, to understand the amplitude of it, let us plot the percentage of missing values per feature.

def colors_from_values(values, palette_name):
    # normalize the values to range [0, 1]
    normalized = (values - min(values)) / (max(values) - min(values))
    # convert to indices
    indices = np.round(normalized * (len(values) - 1)).astype(np.int32)
    # use the indices to get the colors
    palette = sns.color_palette(palette_name, len(values))
    return np.array(palette).take(indices, axis=0)


# +
fig, ax = plt.subplots(figsize=(16,16))

# Plot bar charts for discrete and continuous variables
sns.barplot(orient='h', y=numerical_missing.index, x=numerical_missing, ax=ax, palette=colors_from_values(numerical_missing, "RdYlGn_r"))

# Set axis labels and titles for each subplot
ax.set_title('Percentage of Missing Values in Numerical Variables')
ax.set_ylabel('Column')
ax.set_xlabel('Percentage Missing (%)')
ax.axvline(x=50, color='k', linestyle='--')
ax.axvline(x=60, color='k', linestyle='--')
plt.savefig(str(OUTPUT_FOLDER / 'missing_values_percentages.pdf'), bbox_inches='tight')
plt.show()
# -

# We delete variables with a missing percentage higher than 60% without hesitation.

threshold = 0.60

missing_cols = numerical_missing[numerical_missing>(threshold*100)].index.tolist()
print(f'Columns with % of NaNs greater than {threshold:.0%}:')
print(missing_cols)

df = df.drop(missing_cols, axis=1)
cols_numerical, cols_categorical = get_num_cat(df)
numerical_missing = get_percentage_missing(df[cols_numerical])

# Variables with missingness between 50%-60% deserve a closer look, because they are many and we don't want to discard too much information. Let us plot their correlation matrix, clustered using hierarchical clustering to see a better block structure.

missing_cols = numerical_missing[(numerical_missing>50) & (numerical_missing<60)].index.tolist()
print(f'Columns with % of NaNs between 50% and 60%:')
print(missing_cols)




def analyze_correlation(df, columns, threshold=0.8):

    # Create a list of all the columns
    all_columns = list(df.columns)

    # Create a list of the columns that are not in the list of columns
    other_columns = [column for column in all_columns if column not in columns]
        
    # Create a dataframe with the column as index and the most correlated column and the value of the correlation as columns
    output = pd.DataFrame(index=columns, columns=['most_correlated_column', 'correlation'])

    # For each column in the list of columns
    for column in columns:
        
        # Create a list of the correlations between the column and the other columns
        correlations = [df[column].corr(df[other_column]) for other_column in other_columns]

        # Find the index of the column that is most correlated to the column
        max_index = np.argmax(np.absolute(correlations))

        # If the correlation is above a threshold
        if correlations[max_index] > threshold:
                    
            # Set the most correlated column and the value of the correlation in the dataframe
            # Round the correlation to 2 decimals
            output.loc[column, 'most_correlated_column'] = other_columns[max_index]
            output.loc[column, 'correlation'] = np.round(correlations[max_index], 2)
        
        # If the correlation is below a threshold
        else:
                        
            # Set the most correlated column to None and the value of the correlation to None
            output.loc[column, 'most_correlated_column'] = None
            output.loc[column, 'correlation'] = None
    
    # Return the dataframe
    return output


df_correlation_analysis = analyze_correlation(df_numerical,missing_cols) 
df_correlation_analysis

# Extract columns with a correlation above a threshold
columns_to_drop = df_correlation_analysis[df_correlation_analysis['most_correlated_column'].notnull()].index.tolist()
columns_to_drop

# +
# Drop columns
df = df.drop(columns=columns_to_drop)

# Update numerical df
df_numerical = df.select_dtypes(include=['float64', 'int64'])
# -

# Let's see how much we reduced the missing columns

numerical_missing = get_percentage_missing(df_numerical)
missing_cols = numerical_missing[(numerical_missing>50) & (numerical_missing<60)].index.tolist()

plot_clustered_correlation_matrix(df_numerical[missing_cols], name='clustered_correlation_matrix2')
def plot_clustered_correlation_matrix(dataframe, name='clustered_correlation_matrix'):
    
    corr_matrix = dataframe.corr()
    
    # Use correlation matrix as distance
    pdist = spc.distance.pdist(abs(corr_matrix.values))

# We see less variables and less blocks, one last thing is we can interal variables from the missing values, such as 2 out of the 3 in the upper-left block. Let us keep just `oxygen.saturation`
    linkage = spc.linkage(pdist, method='complete')
    idx = spc.fcluster(linkage, 0.5 * pdist.max(), 'distance')

# +
# Drop columns
df = df.drop(columns=['oxyhemoglobin', 'reduced.hemoglobin'])
    columns = [dataframe.columns.tolist()[i] for i in list((np.argsort(idx)))]
    dataframe = dataframe.reindex(columns, axis=1)

# Update numerical df
df_numerical = df.select_dtypes(include=['float64', 'int64'])
# -
    corr_matrix = dataframe.corr()

# ### Checking for mono-value columns
    # Create a correlation heatmap
    plt.figure(figsize=(20, 15))
    sns.heatmap(corr_matrix, annot=False, vmin=-1, vmax=1, cmap='RdBu_r') # 'bwr' 'coolwarm'
    plt.title('Correlation Heatmap')
    plt.savefig(str(OUTPUT_FOLDER / str(name+'.pdf')), bbox_inches='tight')
    plt.show()

# And check for columns with all the same value, which are then not significant.

same_cols = df.columns[df.apply(lambda x: len(x.unique()) == 1)].tolist()
print('Columns with all the same value:', same_cols)
df = df.drop(same_cols, axis=1)

# Update the categorical and numerical versions of the dataframe

# Update numerical and categorical df
df_categorical = df.select_dtypes(include=['category', 'bool'])
df_numerical = df.select_dtypes(include=['float64', 'int64'])


df.shape

# ### Data visualization

# #### Histograms of numerical variables

# Let us plot them in a big grid to have an understanding of the distribution of numerical variables.

len(df_numerical.columns)

df_numerical.hist(layout=(24,4), figsize=(15,80))
plt.show()

# #### Outlier detection

# We can immediately see that some histograms present a very wide range of values, we can leverage this knowledge to find some outliers. Let us also look at a box plot of all these features.

# +
col_inspect = [
    'respiration',
    'systolic.blood.pressure',
    'diastolic.blood.pressure',
    'map',
    'weight',
    'height',
    'BMI',
    'fio2',
    'left.ventricular.end.diastolic.diameter.LV',
    'creatinine.enzymatic.method',
    'urea',
    'cystatin',
    'white.blood.cell',
    'eosinophil.ratio',
    'basophil.count',
    'D.dimer',
    'international.normalized.ratio',
    'activated.partial.thromboplastin.time',
    'thrombin.time',
    'high.sensitivity.troponin',
    'prothrombin.time.ratio',
    'sodium',
    'potassium',
    'calcium',
    'hydroxybutyrate.dehydrogenase.to.lactate.dehydrogenase',
    'hydroxybutyrate.dehydrogenase',
    'glutamic.oxaloacetic.transaminase',
    'creatine.kinase',
    'creatine.kinase.isoenzyme',
    'lactate.dehydrogenase',
    'alkaline.phosphatase',
    'indirect.bilirubin',
    'glutamic.pyruvic.transaminase',
    'globulin',
    'direct.bilirubin',
    'total.bilirubin',
    'total.bile.acid',
    'triglyceride',
    'dischargeDay'
]

df_numerical[col_inspect].boxplot()
plt.title('Boxplot of a subset of Numerical Features')
plt.tick_params(axis='x', labelrotation=90)
plt.show()


# -

# To spot outliers, we compute their z-score and print the values. If we believe that some values are outliers, instead of discarding completely the entry, we set the value to `NaN`, to be recovered during the imputation later in the analysis.

def get_outliers(df, feature, threshold=3):

    df2 = df.copy()

    # calculate the Z-score for each value in the 'value' column
    df2['zscore'] = (df2[feature] - df2[feature].mean()) / df2[feature].std(ddof=0)

    # identify outliers as any value with a Z-score greater than threshold or less than -threshold
    outliers = (df2['zscore'] > threshold) | (df2['zscore'] < -threshold)

    return df2[[feature, 'zscore']].loc[outliers]


# Let us go through all the values which may present outliers

get_outliers(df, 'respiration', threshold=9)

# The average respiratory rate (number of respiratory acts in one minute) is recorded in a range between 16 and 20.
# 36 respiratory acts in a minute means the patient is likely to have tachypneum or polypneum.
# The only non-physical value is 0.

df.loc[df['respiration'] == 0, 'respiration'] = np.nan

get_outliers(df, 'height', threshold=3)

#df.loc[df['height'] <= 1.25, ['ageCat','height']]
df.loc[df['height'] <= 1.25, 'height'] = np.nan

get_outliers(df, 'weight', threshold=3)

df.loc[df['weight'] <= 8, 'weight'] = np.nan

get_outliers(df, 'body.temperature', threshold=6)

get_outliers(df, 'BMI', threshold=1)

# According to the World Health Organization (WHO) a healthy subject is indicated by a BMI between 18.5 and 24.9
# The threshold value of BMI in adults is 25 for overweight and 30 for obesity.
# In the underweight condition, the BMI does not reach the value of 18.5
#

df.loc[(df['BMI'] >= 100) | (df['BMI'] == 0), 'BMI'] = np.nan

get_outliers(df, 'fio2', threshold=3)

# fio2 is the fraction of inspired oxygenation (%).
#
# fiO2 is 21(%) if the patient is in spontaneous breathing without oxygen supplements.
#
# If the patient has an oxygen supplement the fiO2 is a fraction variable according to the amount of Oxygen inhaled, which depends on various factors: oxygen flows, presence or absence of reservoir, respiratory rate, total volume
#
# The fio2 can be setted by the clinician himself
#
# Even though 100% is not unfeasible, we decide to discard it to avoid numerical instabilities.

df.loc[(df['fio2'] == 100), 'fio2'] = np.nan

get_outliers(df, 'systolic.blood.pressure', threshold=3)

# In a healthy subject the systolic pressur must be around 120 mmHg
# Subjects with pressure >140 mmHg suffer of hypertension
# The patient who has a pressure equal to 50 mmHg is probably affected by hypotension
# Values = 0 or >200 are outliers

df.loc[(df['systolic.blood.pressure'] >= 200) | (df['systolic.blood.pressure'] == 0), 'systolic.blood.pressure'] = np.nan

# +
#df.loc[df['systolic.blood.pressure'] == 0, 'systolic.blood.pressure'] = np.nan
# -

get_outliers(df, 'diastolic.blood.pressure', threshold=4)

# In a healthy subject the diastolic pressur must be around 80 mmHg
# Subjects with pressure >110 mmHg suffer of hypertension

df.loc[(df['diastolic.blood.pressure'] >= 110) | (df['diastolic.blood.pressure'] == 0), 'diastolic.blood.pressure'] = np.nan

# +
#df.loc[df['diastolic.blood.pressure'] == 0, 'diastolic.blood.pressure'] = np.nan
# -

get_outliers(df, 'map', threshold=3)

# Map (Mean Arterial pressure)
# The normal MAP range is between 70 and 100 mmHg.
# Mean arterial pressures that deviate from this range for prolonged periods of time can have drastic negative effects on the body.

df.loc[df['map'] == 0, 'map'] = np.nan

get_outliers(df, 'left.ventricular.end.diastolic.diameter.LV', threshold=3)

# Left ventricular end diastolic diameter LV (cm) normal range: 3.5 - 5.6 cm
# From the histogram we can see that the values are not in cm

df['left.ventricular.end.diastolic.diameter.LV'].hist()
plt.show()

# Repeat the outlier analysis

df['left.ventricular.end.diastolic.diameter.LV'] = df['left.ventricular.end.diastolic.diameter.LV'] / 10

get_outliers(df, 'left.ventricular.end.diastolic.diameter.LV', threshold=3)

df.loc[df['left.ventricular.end.diastolic.diameter.LV'] < 0.1, 'left.ventricular.end.diastolic.diameter.LV'] = np.nan

get_outliers(df, 'creatinine.enzymatic.method', threshold=8)

# creatinine.enzymatic.method; normal range:44-110 $\mu$mol/L

df.loc[df['creatinine.enzymatic.method'] > 200, 'creatinine.enzymatic.method'] = np.nan

get_outliers(df, 'urea', threshold=4)

# urea (mmol/l), ref:1.7 - 8.3 mmol/L
# Abnormal levels of urea and creatine in the blood may be indicative of renal dysfunction.
# This means that the kidneys fail to properly eliminate toxic substances in the body

# +
#controllare il valore e fare la conversione
#df.loc[df['urea'] >10, 'urea'] = np.nan
# -

get_outliers(df, 'cystatin', threshold=6)

# cystatin (mg/L); ref:0.51–0.98
# High levels of cysteine in the blood are associated with an increased risk of cardiovascular disease, therefore more likely to suffer diseases such as heart attack, intermittent claudication, ischemic heart disease etc

df.loc[df['cystatin'] >=10, 'cystatin'] = np.nan

get_outliers(df, 'white.blood.cell', threshold=6)

# white blood cell count (*10^9/L); ref: 4 -10
# Leukocytosis, which is the increase in the number of white blood cells above 11, is often caused by the normal response of the body to fight an infection or by certain drugs such as corticosteroids
# threshold can be setted >= 11.6

df.loc[df['white.blood.cell'] >=11.6, 'white.blood.cell'] = np.nan

# `eosinophil.ratio` was probably supposed to be a percentage, as we see from the histogram, and since the data information says the ref range is 0.5-5 we multiply by 100 and check outliers.

df['eosinophil.ratio'].hist()
plt.show()

df['eosinophil.ratio'] = df['eosinophil.ratio'] * 100

get_outliers(df, 'eosinophil.ratio', threshold=8)

df.loc[df['eosinophil.ratio'] > 30, 'eosinophil.ratio'] = np.nan

get_outliers(df, 'basophil.count', threshold=8)

# basophil.count(*10^9/L); ref: 0 - 0.1
# An higher count of basophilis can be a symptom of chronic myeloid leukemia

df.loc[df['basophil.count'] > 0.280, 'basophil.count'] = np.nan

get_outliers(df, 'D.dimer', threshold=8)

# D.dimer(mg/l); ref: 0 - 0.5

df.loc[df['D.dimer'] > 48, 'D.dimer'] = np.nan

get_outliers(df, 'international.normalized.ratio', threshold=8)

# international.normalized.ratio; ref: 0.8 - 1.5

df.loc[df['international.normalized.ratio'] > 7, 'international.normalized.ratio'] = np.nan

get_outliers(df, 'activated.partial.thromboplastin.time', threshold=8)

# activated.partial.thromboplastin.time(s); ref: 20 -40

df.loc[df['activated.partial.thromboplastin.time'] > 105, 'activated.partial.thromboplastin.time'] = np.nan

get_outliers(df, 'thrombin.time', threshold=3)

# thrombin.time (s); ref: 14-21

df.loc[df['thrombin.time'] > 78, 'thrombin.time'] = np.nan

# The variable `high.sensitivity.troponin` presents an anomalous range of values and a probably wrong unit of measure since from the dataset information: `high.sensitivity.troponin` (pg/mL); ref:0-14
#
# According to [literature](https://www.reglab.org/news/new-test-high-sensitivity-troponin-i/):
#
# > The new reference range is ≤15 pg/ml for females and ≤20 pg/ml for males; results above these values indicate the possibility of myocardial infarction and require additional patient evaluation. An elevated and actionable value of hs TnI is > 100 pg/mL for males and > 75 pg/mL for females, and indicates an increased likelihood of myocardial damagewomen.

df['high.sensitivity.troponin'].hist()
plt.show()

# Given the many values set to 0 and the anomalous bins, we simply use statistics and remove some values based on z-score

get_outliers(df, 'high.sensitivity.troponin', threshold=3)

df.loc[df['high.sensitivity.troponin'] > 7, 'high.sensitivity.troponin'] = np.nan

get_outliers(df, 'prothrombin.time.ratio', threshold=6)

df.loc[df['prothrombin.time.ratio'] > 7, 'prothrombin.time.ratio'] = np.nan

get_outliers(df, 'sodium', threshold=8)

# sodium(mmol/L); ref:137 - 147

get_outliers(df, 'potassium', threshold=8)

# potassium(mmol/L); ref:3.5 - 5.3

df.loc[df['potassium'] > 11, 'potassium'] = np.nan

get_outliers(df, 'calcium', threshold=8)

get_outliers(df, 'hydroxybutyrate.dehydrogenase.to.lactate.dehydrogenase', threshold=8)

get_outliers(df, 'hydroxybutyrate.dehydrogenase', threshold=8)

# hydroxybutyrate.dehydrogenase(U/L); ref: 90 -180

df.loc[df['hydroxybutyrate.dehydrogenase'] > 1498, 'hydroxybutyrate.dehydrogenase'] = np.nan

get_outliers(df, 'glutamic.oxaloacetic.transaminase', threshold=8)

df.loc[df['glutamic.oxaloacetic.transaminase'] > 1400, 'glutamic.oxaloacetic.transaminase'] = np.nan

get_outliers(df, 'creatine.kinase', threshold=8)

df.loc[df['creatine.kinase'] > 3000, 'creatine.kinase'] = np.nan

get_outliers(df, 'creatine.kinase.isoenzyme', threshold=8)

df.loc[df['creatine.kinase.isoenzyme'] > 150, 'creatine.kinase.isoenzyme'] = np.nan

get_outliers(df, 'lactate.dehydrogenase', threshold=8)

df.loc[df['lactate.dehydrogenase'] > 1900, 'lactate.dehydrogenase'] = np.nan

get_outliers(df, 'alkaline.phosphatase', threshold=8)

df.loc[df['alkaline.phosphatase'] > 1000, 'alkaline.phosphatase'] = np.nan

get_outliers(df, 'indirect.bilirubin', threshold=8)

df.loc[df['indirect.bilirubin'] > 90, 'indirect.bilirubin'] = np.nan

get_outliers(df, 'glutamic.pyruvic.transaminase', threshold=8)

df.loc[df['glutamic.pyruvic.transaminase'] > 1800, 'glutamic.pyruvic.transaminase'] = np.nan

get_outliers(df, 'globulin', threshold=8)

df.loc[df['globulin'] > 88, 'globulin'] = np.nan

get_outliers(df, 'direct.bilirubin', threshold=8)

df.loc[df['direct.bilirubin'] > 10, 'direct.bilirubin'] = np.nan

get_outliers(df, 'total.bilirubin', threshold=8)

df.loc[df['total.bilirubin'] > 160, 'total.bilirubin'] = np.nan

get_outliers(df, 'total.bile.acid', threshold=8)

df.loc[df['total.bile.acid'] > 120, 'total.bile.acid'] = np.nan

get_outliers(df, 'triglyceride', threshold=8)

df.loc[df['triglyceride'] > 10, 'triglyceride'] = np.nan

get_outliers(df, 'dischargeDay', threshold=8)

df_numerical = df.select_dtypes(include=['float64', 'int64'])


# #### More in-depth study for some numerical features
# Control when for more than 90 percent of patients the variable takes nearly equal values

def check_histogram_bins(data, numerical_features,threshold=0.9):

    bin_counts = []
    selected_features = []

    for feature in numerical_features:
        feature_values = data[feature]
        counts, bins, _ = plt.hist(feature_values, bins=10)
        bin_counts.append(counts)

        # Check if a bin satisfies the threshold condition
        for j in range(len(counts)):
            if counts[j] >= threshold * data.shape[0]:
                selected_features.append(feature)
                print(f"Feature {feature}: Bin {j+1} - Count: {counts[j]}")

    plt.close()  # Close the figure to prevent unnecessary plots
    return selected_features


inspect_columns = check_histogram_bins(df_numerical,df_numerical.columns)

# visit.times, eye.opening, verabal.response, movement and GCS are discerete numerical variable and it's therefore reasonable that a lot of patients are characterised by the same value.
# Discard them from the suspicious columns.

inspect_columns.remove('visit.times')
inspect_columns.remove('eye.opening')
inspect_columns.remove('verbal.response')
inspect_columns.remove('movement')
inspect_columns.remove('GCS')

# Plot with more bins

df_numerical[inspect_columns].hist(layout=(3,3), figsize=(10,10), bins=20)
plt.show()

# The problem with these variables is not trivial: it's likely that part of them was inserted in a different unit of measure, however they are marked in the top important variables in many models. We decide to just keep them as is, but this range it's really likely it will affect scaling.

# #### Barplot of categorical variables

# +
col_inspect = df_categorical.columns
#col_inspect = ['Killip.grade', 'ageCat']

# Adjust subplots and figsize
fig, axes = plt.subplots(7, 5,figsize=[15,20])
axes = axes.flatten()

for idx, col_name in enumerate(col_inspect):
    plt.sca(axes[idx]) # set the current Axes
    #plt.hist(df_categorical[x],density=True)
    sns.countplot(x = col_name, data = df_categorical, palette = 'magma')
    plt.xticks(fontsize=8, rotation = 45) # Rotates X-Axis Ticks by 45-degrees
    plt.ylabel('')
    plt.title(col_name)

fig.tight_layout()
plt.show()
# -

age_counts = df_categorical.ageCat.value_counts()
age_5989 = age_counts['(59,69]']+age_counts['(69,79]']+age_counts['(79,89]']
print(f"Total and percentage in the age range 59-89: {age_5989} {age_5989/len(df.index):.2%}")

gender_counts = df_categorical.gender.value_counts()
gender_Female = gender_counts['Female']
print(f"{gender_Female/len(df.index):.2%} of females")
print(f"{1-(gender_Female)/len(df.index):.2%} of males")

hf_type_counts = df_categorical['type.of.heart.failure'].value_counts()
hf_type_right = hf_type_counts['Right']
hf_type_left = hf_type_counts['Left']
hf_type_both = hf_type_counts['Both']
print(f"{hf_type_right/len(df.index):.2%} with type Right")
print(f"{hf_type_left/len(df.index):.2%} with type Left")
print(f"{hf_type_both/len(df.index):.2%} with type Both")

diabetes_counts = df_categorical.diabetes.value_counts()
diabetes_true = diabetes_counts[True]
print(f"{diabetes_true/len(df.index):.2%} with diabetes")

# As final step, plot some numerical features distribution separately with the respect to the target to see if we have some hints in features that separate well.

target_var = 're.admission.within.6.months'

# +
#col_inspect = df_numerical.columns[:32]
col_inspect = [
    'direct.bilirubin',
    'prothrombin.activity',
    'neutrophil.ratio',
    'glomerular.filtration.rate',
    'uric.acid',
    'urea',
    'creatinine.enzymatic.method',
    'CCI.score',
    'map',
    'diastolic.blood.pressure'
]

# Adjust subplots and figsize
fig, axes = plt.subplots(2, 5,figsize=[14,7])
axes = axes.flatten()

for idx, col_name in enumerate(col_inspect):
    plt.sca(axes[idx]) # set the current Axes
    sns.kdeplot(df[df[target_var] == 0][col_name], fill=True, label="Target 0")
    sns.kdeplot(df[df[target_var] == 1][col_name], fill=True, label="Target 1")
    plt.legend(loc='lower right')
    plt.xticks(fontsize=8, rotation = 45) # Rotates X-Axis Ticks by 45-degrees
    plt.ylabel('')

fig.tight_layout()
plt.savefig(str(OUTPUT_FOLDER / 'distribution_wrt_target.pdf'), bbox_inches='tight')
plt.show()
# -

# ### Correlation analysis

# Using clinical knowledge, we inspect some groups of variables we think could be quite correlated.

corr_matrix = df_numerical.corr()


def plot_subcorrelation_matrix(corr_matrix, inspect_col, threshold=0.4):

    if not inspect_col or len(inspect_col) == 1:
        return

    if len(inspect_col) == 2:
        correlation_value = corr_matrix.values[0,1]
        if correlation_value >= threshold:
            print(f'Correlation: {correlation_value:.2f}')
        else:
            print('Correlation is below threshold')
    else:
        sub_corr_matrix = corr_matrix[inspect_col].loc[inspect_col]
        # Data will not be shown in cells where `mask` is `True`
        mask = np.triu(np.ones_like(sub_corr_matrix, dtype=bool), k=0) | (np.abs(sub_corr_matrix) <= threshold)

        # Plot the correlation matrix using seaborn
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.heatmap(sub_corr_matrix,
                    annot=True, fmt='.2f',
                    mask=mask,
                    cmap='coolwarm', center=0, cbar=True,
                    linewidths=.5,
                    ax=ax)
        ax.set_aspect("equal")
        plt.title("Correlation matrix")
        plt.show()


inspect_col = ['map', 'diastolic.blood.pressure', 'systolic.blood.pressure']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['sodium', 'chloride']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['cholesterol', 'low.density.lipoprotein.cholesterol']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['globulin', 'white.globulin.ratio', 'indirect.bilirubin', 'direct.bilirubin', 'total.bilirubin']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['cystatin', 'urea', 'creatinine.enzymatic.method', 'glomerular.filtration.rate']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['hemoglobin', 'hematocrit', 'red.blood.cell']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['basophil.count', 'basophil.ratio']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['eosinophil.count', 'eosinophil.ratio']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['white.blood.cell', 'neutrophil.count']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)

inspect_col = ['movement', 'verbal.response', 'eye.opening', 'GCS']
plot_subcorrelation_matrix(corr_matrix=corr_matrix, inspect_col=inspect_col, threshold=0.4)


# We are safe enough to do the following: write a function to discard variables correlated with others by more than a threshold we fix to 0.85.

def remove_highly_correlated(df, threshold=0.5):
    """
    Given a dataframe, removes variables that are highly correlated with the others
    Returns a dataframe with the highly correlated variables removed
    threshold is the correlation threshold to use
    Code from https://chrisalbon.com/machine_learning/feature_selection/drop_highly_correlated_features/
    """

    # Create correlation matrix
    corr_matrix = df.corr(numeric_only=True).abs()

    # Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    # Find index of feature columns with correlation greater than threshold
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    
    # Print dropped columns
    print("Dropping the following columns")
    print(to_drop)

    # Return with dropped features
    return df.drop(to_drop, axis=1)


df_shape = df.shape

df = remove_highly_correlated(df, threshold=0.85)

# We removed this number of features:

df_shape[1] - df.shape[1]

# Final shape of the dataset

df.shape

# ## 3. Modeling

# ### Feature engineering

# +
# feature engineering
#df_numerical['logduration']=df_numerical['duration'].apply(lambda x: math.log(x+1))
# -

# separate categorical and numerical features
categorical_features = df.select_dtypes(include=['category']).columns.tolist()
numerical_features = df.select_dtypes(include=[np.number]).columns.tolist()

# +
with open(str(OUTPUT_FOLDER / 'categorical_features.pkl'), 'wb') as handle:
    pickle.dump(categorical_features, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(str(OUTPUT_FOLDER / 'numerical_features.pkl'), 'wb') as handle:
    pickle.dump(numerical_features, handle, protocol=pickle.HIGHEST_PROTOCOL)
# -

# Make sure the values of categorical don't contain strange characters, because after encoding this might break XGBoost, specifically the `ageCat` variable.

df[categorical_features] = df[categorical_features].applymap(lambda x: re.sub(r'[\[\]<\(\)]', '', x))
df[categorical_features] = df[categorical_features].applymap(lambda x: re.sub(r',', '_', x))


# The following cell is needed to generate the input fields in the web app.

# +
def generate_column_info(dataframe):
    column_info = {}
    for column in dataframe.drop([target_var], axis=1).columns:
        column_type = dataframe[column].dtype
        if column_type == 'object' or pd.api.types.is_categorical_dtype(column_type):
            unique_values = dataframe[column].unique().tolist()
            column_info[column] = {"type": "category", "value": unique_values}
        elif pd.api.types.is_bool_dtype(column_type):
            unique_values = dataframe[column].unique().tolist()
            column_info[column] = {"type": "binary", "value": unique_values}
        elif pd.api.types.is_numeric_dtype(column_type):
            min_value = dataframe[column].min()
            max_value = dataframe[column].max()
            if pd.api.types.is_integer_dtype(column_type):
                column_info[column] = {"type": "integer", "value": [min_value, max_value]}
            else:
                column_info[column] = {"type": "continuous", "value": [min_value, max_value]}
    return column_info

# Generate column information dictionary
column_info = generate_column_info(df)

# Dump into file
with open(str(OUTPUT_FOLDER / 'column_info.pkl'), 'wb') as handle:
    pickle.dump(column_info, handle, protocol=pickle.HIGHEST_PROTOCOL)
# -

# ### Splitting data into training and testing sets
#
# Separate the target variable from the features

X = df.drop([target_var], axis=1)
y = df[target_var]

# Split the dataset into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.15,
                                                    stratify=y, # preserve target propotions
                                                    random_state=SEED)

# Given the reduced size of the dataset, we can simultaneously explore different models and tune them, to have the best result for each class of models.

# ### Preprocessing categorical data

# The following code is setup as a [`sklearn.pipeline.Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) object for future work, however for the `SHAP` library to work we need to be able to access the unscaled version of the data, so the preprocessing is setup outside the pipeline, but can be easily implemented inside whenever a future deployment requires so.

# +
# create preprocessor for categorical data
# cat_preprocessor = Pipeline(steps=[
#     ('onehot', OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='if_binary'))
# ])

# +
# Initialize the OneHotEncoder
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop=None)#drop='if_binary')

# Fit the encoder on the training data
encoder.fit(X_train[categorical_features])

# Transform the categorical columns in both train and test data
train_encoded = pd.DataFrame(encoder.transform(X_train[categorical_features]), columns=encoder.get_feature_names_out(categorical_features))
test_encoded = pd.DataFrame(encoder.transform(X_test[categorical_features]), columns=encoder.get_feature_names_out(categorical_features))

# Concatenate the encoded features with the original numerical columns
X_train = pd.concat([X_train.drop(categorical_features, axis=1).reset_index(drop=True), train_encoded.reset_index(drop=True)], axis=1)
X_test = pd.concat([X_test.drop(categorical_features, axis=1).reset_index(drop=True), test_encoded.reset_index(drop=True)], axis=1)

with open(str(OUTPUT_FOLDER / 'encoder.pkl'), 'wb') as handle:
    pickle.dump(encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)
# -

# ### Preprocessing numerical data
#
# #### Imputation

# +
# %%time
#imputer = IterativeImputer(max_iter=10, random_state=0, verbose=2) # Doesn't improve much but takes 10 min to run
imputer = KNNImputer(n_neighbors=5)

X_train = pd.DataFrame(imputer.fit_transform(X_train), columns = X_train.columns)
X_test = pd.DataFrame(imputer.transform(X_test), columns = X_test.columns)

with open(str(OUTPUT_FOLDER / 'imputer.pkl'), 'wb') as handle:
    pickle.dump(imputer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# +
# with open(str(OUTPUT_FOLDER / 'imputer.pkl'), 'rb') as handle:
#     imputer = pickle.load(handle)
# 
# X_train[numerical_features] = imputer.transform(X_train[numerical_features])
# X_test[numerical_features] = imputer.transform(X_test[numerical_features])
# -

# #### Imbalance

print(f'Percentage of positives in the training set: {np.round((y_train == True).sum() / len(y_train), 3):.1%}')

# Compute class weights as inversely proportional to the prevalence in the training set.

class_weights = class_weight.compute_class_weight(class_weight='balanced',
                                                  classes=np.unique(y_train),
                                                  y=y_train)
class_weights = dict(zip(np.unique(y_train), class_weights))
class_weights

# #### Scaling

# +
# create preprocessor for numerical data
# num_preprocessor = Pipeline(steps=[
#     ('imputer', KNNImputer(n_neighbors=6)),
#     ('scaler', StandardScaler())
# ])

# +
scaler = StandardScaler()

X_train[numerical_features] = scaler.fit_transform(X_train[numerical_features])
X_test[numerical_features] = scaler.transform(X_test[numerical_features])

with open(str(OUTPUT_FOLDER / 'scaler.pkl'), 'wb') as handle:
    pickle.dump(scaler, handle, protocol=pickle.HIGHEST_PROTOCOL)

# +
# with open(str(OUTPUT_FOLDER / 'imputer.pkl'), 'rb') as handle:
#     scaler = pickle.load(handle)
# 
# X_train[numerical_features] = scaler.transform(X_train[numerical_features])
# X_test[numerical_features] = scaler.transform(X_test[numerical_features])
# -

# ### Model selection

# As first step in providing the final model we test some models and do a very brief hyperparameter tuning.

# define the models and their parameter grids for grid search
models = {
    'logistic_regression': {
        'model': LogisticRegression(max_iter=10000),
        'param_grid': {
            'classifier__C': np.logspace(-3, 3, 7),
            'classifier__random_state': [SEED],
            'classifier__class_weight': [class_weights]
        }
    },
    'ada_boost': {
        'model': AdaBoostClassifier(),
        'param_grid': {
            'classifier__n_estimators': [10, 50, 100, 500],
            'classifier__random_state': [SEED],
            'classifier__learning_rate': [0.0001, 0.001, 0.01, 0.1, 1.0]
        }
    },
    'random_forest': {
        'model': RandomForestClassifier(),
        'param_grid': {
            'classifier__n_estimators': [100, 250, 450, 600],
            'classifier__max_depth': [5, 10, 15, 20],
            'classifier__max_features': ['sqrt', 'log2'],
            'classifier__criterion' :['entropy'],
            'classifier__oob_score': [True],
            'classifier__random_state': [SEED],
            'classifier__class_weight': [class_weights]
        }
    },
    'knn': {
        'model': KNeighborsClassifier(),
        'param_grid': {
            'classifier__n_neighbors': np.arange(5,80,10)
        }
    },
    'decision_tree_classifier': {
        'model': DecisionTreeClassifier(),
        'param_grid': {
            'classifier__criterion': ['entropy','gini'],
            'classifier__max_depth': [5,10],
            'classifier__min_samples_split': [5,10,20],
            'classifier__min_samples_leaf': [5,10],
            'classifier__random_state': [SEED]
        }
    },
    'mlp': {
        'model': MLPClassifier(),
        'param_grid': {
            'classifier__hidden_layer_sizes': [(10, 5),(100,20,5)],
            'classifier__max_iter': [2000],
            'classifier__alpha': [0.01],
            'classifier__random_state': [SEED]
        }
    },
    'naive_bayes': {
        'model': GaussianNB(),
        'param_grid': {}
    },
    'xgboost': {
        'model': xgb.XGBClassifier(),
        'param_grid': {
            'classifier__max_depth': [3, 6, 9],
            'classifier__learning_rate': [0.1, 0.01, 0.001],
            'classifier__n_estimators': [100, 500, 1000],
            'classifier__random_state': [SEED]
        }
    }
}

# +
# combine the preprocessors into a column transformer
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('cat', cat_preprocessor, categorical_features),
#         ('num', num_preprocessor, numerical_features)
#     ])
# -

# create the pipelines for each model
pipelines = {}
for name, model in models.items():
    pipelines[name] = Pipeline(steps=[
        #('preprocessor', preprocessor),
        ('classifier', model['model'])
    ])

# According to [the documentation](https://scikit-learn.org/stable/modules/cross_validation.html#stratified-k-fold) we choose to use the `StratifiedKFold` for doing cross-validation, choosing `n_splits=5` to have a validation set of `1/n_splits=0.20`, and `shuffle=True`.

scoring = {"AUC": "roc_auc", "Accuracy": make_scorer(accuracy_score)}
pipeline_cv = {}

# +
# # %%time
# 
# # perform grid search cross-validation for each model and output the test accuracy of the best model
# for name, pipeline in pipelines.items():
#     grid_search = GridSearchCV(
#         pipeline,
#         param_grid=models[name]['param_grid'],
#         cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED),
#         scoring=scoring,
#         refit="AUC",
#         return_train_score=True,
#         verbose=0
#     )
#     grid_search.fit(X_train, y_train)
#     pipeline_cv[name] = grid_search
#     print(f'{name:30}| train AUC = {grid_search.score(X_train, y_train):.3f} | test AUC = {grid_search.score(X_test, y_test):.3f}')
#     print('-'*80)
# -

# Save for later

# +
# with open(str(OUTPUT_FOLDER / 'pipeline_cv.pkl'), 'wb') as handle:
#     pickle.dump(pipeline_cv, handle, protocol=pickle.HIGHEST_PROTOCOL)
# -

with open(str(OUTPUT_FOLDER / 'pipeline_cv.pkl'), 'rb') as handle:
    pipeline_cv = pickle.load(handle)

# ### Training evolution

# The `GridSearchCV` objects has the following useful attributes
#
# - `.cv_results_` which contains things such as `mean_test_AUC`, `std_test_AUC`, `std_train_AUC`, `mean_train_AUC`. List all of them with `pd.DataFrame(GridSearchCV.cv_results_.keys())`
# - `.best_estimator_`
# - `.best_params_`
# - `.best_score_`
#
# For example let us analyze the evolution of one of the models

res = pipeline_cv['random_forest'].cv_results_

# +
m1 = res['mean_test_AUC']
s1 = res['std_test_AUC']
m2 = res['mean_train_AUC']
s2 = res['std_train_AUC']

axisX = list(range(len(m1)))
plt.errorbar(axisX, m1, s1, label='validation')
plt.errorbar(axisX, m2, s2, label='train')

j1 = np.argmax(m1) # maximum value of AUC in terms of mean over the CV folds

plt.plot(axisX[j1], m1[j1], 'ro', markersize=12)
plt.legend()
plt.title('Training curves for the Random Forest')
plt.savefig(str(OUTPUT_FOLDER / 'crossvalidation_curve.pdf'), bbox_inches='tight')
plt.show()
# -

res['params'][j1]

# ### AUC and confusion matrices

# +
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(16,7))#, height_ratios = [1,3])
axes = axes.flatten()

rows = []
i = 0
roc_details = {}

for name, pipeline in pipeline_cv.items():

    model = pipeline.best_estimator_.named_steps['classifier']

    # Make predictions on the testing set
    #y_pred = pipeline.predict(X_test)
    y_pred = (pipeline.predict_proba(X_test)[:,1] >= 0.44).astype(bool) # set threshold as 0.44

    # Calculate the accuracy score
    accuracy = accuracy_score(y_test, y_pred)

    # Calculate the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    #sns.heatmap(cm, annot=True, cmap='coolwarm', fmt='d', ax=axes[0,i])
    axes[i].set_title(model.__class__.__name__)
    plot_confusion_matrix(conf_mat=cm,
                          show_absolute=True,
                          show_normed=True,
                          colorbar=True, figure=fig, axis=axes[i])

    axes[i].set_xlabel('Predicted label')
    axes[i].set_ylabel('True label')

    # Calculate the ROC curve
    y_score = pipeline.predict_proba(X_test)[:,1]
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)

    # Save for later
    roc_details[model.__class__.__name__] = {
        'fpr': fpr,
        'tpr': tpr,
        'roc_auc': roc_auc
    }

    # Save for later
    row = {
        'Model': model.__class__.__name__,
        'ROC AUC': roc_auc,
        'Accuracy': accuracy,
    }

    # Append the row to the list
    rows.append(row)

    i += 1

plt.tight_layout()
plt.savefig(str(OUTPUT_FOLDER / 'confusion_matrices.pdf'), bbox_inches='tight')
plt.show()

# +
fig, ax = plt.subplots(figsize=(8,8))

model = pipeline_cv['random_forest'].best_estimator_.named_steps['classifier']

# Make predictions on the testing set
#y_pred = pipeline.predict(X_test)
y_pred = (pipeline_cv['random_forest'].predict_proba(X_test)[:,1] >= 0.44).astype(bool) # set threshold as 0.44

# Calculate the accuracy score
accuracy = accuracy_score(y_test, y_pred)

# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)
#sns.heatmap(cm, annot=True, cmap='coolwarm', fmt='d', ax=axes[0,i])
ax.set_title(model.__class__.__name__)
plot_confusion_matrix(conf_mat=cm,
                      show_absolute=True,
                      show_normed=True,
                      colorbar=True, figure=fig, axis=ax)

ax.set_xlabel('Predicted label')
ax.set_ylabel('True label')

plt.savefig(str(OUTPUT_FOLDER / 'confusion_matrix_random_forest.pdf'), bbox_inches='tight')
plt.show()

# +
# Plot the ROC curve
fig, ax = plt.subplots(figsize=(8,8))

ax.plot([0, 1], [0, 1], linestyle='--', color='gray')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')

for key, values in roc_details.items():
    ax.plot(values['fpr'], values['tpr'], label=key + ' (AUC = %0.4f)' % values['roc_auc'])

ax.set_title('ROC Curve comparison')
ax.legend(loc="lower right")
ax.set_aspect('equal')
ax.set_aspect('equal')
plt.savefig(str(OUTPUT_FOLDER / 'roc_comparison.pdf'), bbox_inches='tight')
plt.show()
# -

df_performance = pd.DataFrame(rows)
df_performance = df_performance.sort_values('ROC AUC', ascending=False)
df_performance

df_performance.to_latex(
    str(OUTPUT_FOLDER / 'performance_table.tex'),
    index=False,
    formatters={"name": str.upper},
    float_format="{:.4f}".format,
    caption="Comparison of performance.",
    label='tab:performance'
)

# ### Deep model analysis

# #### Logistic Regression

# Even though it's not the most performing model, we continue analyzing it for its simplicity and interpretability.
#
# Inspect the best configuration:

best_pipeline_logistic = pipeline_cv['logistic_regression']

best_pipeline_logistic.best_params_

# Extract the classifier
classifier = best_pipeline_logistic.best_estimator_.named_steps['classifier']

# See if the penalty discarded any variable:

len(classifier.coef_[0]) == len(X_train.columns)

# Since it didn't, let us try to reduce the model with backward selection implemented by [`SequentialFeatureSelector`](https://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/) in `mlxtend`, and then perform a second final hyperparameter tuning.

# +
from mlxtend.feature_selection import SequentialFeatureSelector

# Sequential Backward Selection
sfs = SequentialFeatureSelector(
    classifier,
    k_features=6,
    forward=False,
    floating=False,
    scoring='roc_auc',
    verbose=1,
    cv=5,
    n_jobs=-1).fit(X_train, y_train)

# +
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs

plot_sfs(sfs.get_metric_dict(), kind='std_dev',figsize=(10, 8))

plt.title('Sequential Backward Selection')
plt.xticks(np.arange(5, 138, 5.0))
plt.grid()
plt.savefig(str(OUTPUT_FOLDER / 'feature_selection_backward_logistic.pdf'), bbox_inches='tight')
plt.show()
# -

# Train it again with 15 variables to be selected, as a good tradeoff between performance and number of features.

sfs = SequentialFeatureSelector(
    classifier,
    k_features=15,
    forward=False,
    floating=False,
    scoring='roc_auc',
    verbose=2,
    cv=5,
    n_jobs=-1).fit(X_train, y_train)

print('Selected features:')
print(sfs.k_feature_names_)

important_features_lr = set(sfs.k_feature_names_)

# From 0.680109 AUC we went down to:

print(f'AUC: {sfs.k_score_:.4f}')

# Create a reduced version of the data.

X_train_sfs = pd.DataFrame(sfs.transform(X_train), columns=sfs.k_feature_names_)
X_test_sfs = pd.DataFrame(sfs.transform(X_test), columns=sfs.k_feature_names_)

# Now train again the model, performing a deeper hyperparameter tuning

# +
model = LogisticRegression(max_iter=10000)

param_grid =  {
    'C': np.logspace(-3, 3, 30),
    'random_state': [SEED],
    'class_weight': [class_weights]
}

grid_search = GridSearchCV(
     model,
     param_grid=param_grid,
     cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED),
     scoring='roc_auc',
     refit='AUC',
     return_train_score=True,
     verbose=0
)

grid_search.fit(X_train_sfs, y_train)
# -

grid_search.best_params_

print(f'AUC: {grid_search.score(X_test_sfs, y_test):.4f}')

# [This website](https://stats.oarc.ucla.edu/other/mult-pkg/faq/general/faq-how-do-i-interpret-odds-ratios-in-logistic-regression/) provides an insightful interpretation of the coefficients in a logistic regression model.

classifier = grid_search.best_estimator_

fig, ax = plt.subplots(figsize=(8,8))
coeff = pd.DataFrame()
coeff['feature'] = X_train_sfs.columns
coeff['beta'] = classifier.coef_[0]
coeff['exp_beta'] = np.exp(coeff['beta'])
coeff = coeff.sort_values(by=['beta'])
sns.barplot(data=coeff[abs(coeff.beta) > 0.05], x='beta', y='feature', color='c')
plt.title('Coefficients in Logistic Regression')
plt.savefig(str(OUTPUT_FOLDER / 'feature_importance_weightsLogisticRegression.pdf'), bbox_inches='tight')
plt.show()

var_name_scale = dict(zip(scaler.get_feature_names_out().tolist(), scaler.scale_.tolist()))
var_name_scale

coeff['unscaled_exp_beta'] = np.nan
for index, row in coeff.iterrows():    
    if row.feature in var_name_scale.keys():
        coeff.at[index,'unscaled_exp_beta'] = np.exp(row.beta / var_name_scale[row.feature])    

coeff

# +
y_pred = grid_search.predict_proba(X_test_sfs)[:,1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_pred)

# Compute the zero skill model line
# It will depend on the fraction of observations belonging to the positive class
zero_skill = len(y_test[y_test==1]) / len(y_test)

# Compute the perfect model line
perfect_precision = np.ones_like(recalls)
perfect_recall = np.linspace(0, 1, num=len(perfect_precision))

plt.plot(recalls, precisions, 'r-', label='Logistic')
plt.plot([0, 1], [zero_skill, zero_skill], 'b--', label='Zero skill')
plt.plot(perfect_recall, perfect_precision, 'g--', linewidth=2, label='Perfect model')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.axis([0, 1, 0, 1])
#plt.grid()
plt.title('Precision Recall curve in Logistic Regression')
plt.legend()
plt.show()
# -

# #### DecisionTreeClassifier

# Extract the classifier
classifier = pipeline_cv['decision_tree_classifier'].best_estimator_.named_steps['classifier']

from sklearn import tree
text_representation = tree.export_text(classifier)
with open('decistion_tree.log', 'w') as f:
    f.write(text_representation)

# The `plot_tree` returns annotations for the plot, to not show them in the notebook I assigned returned value to `_`

fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(classifier,
                   feature_names=X_train.columns,
                   class_names=['No','Yes'])

# We can export as a figure but we must use `graphviz`

export_graphviz(classifier,
                out_file=str(OUTPUT_FOLDER / 'decision_tree.dot'),
                feature_names = X_test.columns.tolist(),
                class_names=['0','1'],
                filled=True)

# !dot -Tpng output/decision_tree.dot -o output/decision_tree.png -Gdpi=600
Image(filename = str(OUTPUT_FOLDER / 'decision_tree.png'))

importance, sorted_indices = np.sort(classifier.feature_importances_), np.argsort(classifier.feature_importances_)
importance, sorted_indices = importance[-10:], sorted_indices[-10:]
importance, sorted_indices = importance[::-1], sorted_indices[::-1]
sns.barplot(x=importance, y=X_train.columns[sorted_indices], color='c')
plt.title('Feature Importance in Decision Tree')
plt.xlabel('Mean decrease in impurity')
plt.ylabel('Features')
plt.savefig(str(OUTPUT_FOLDER / 'feature_importance_DecisionTreeClassifier.pdf'), bbox_inches='tight')
plt.show()

# #### Random Forest

classifier = pipeline_cv['random_forest'].best_estimator_.named_steps['classifier']

fig, ax = plt.subplots(figsize=(8,6))
# Feature Importance
importance, sorted_indices = np.sort(classifier.feature_importances_), np.argsort(classifier.feature_importances_)
importance, sorted_indices = importance[-30:], sorted_indices[-30:]
importance, sorted_indices = importance[::-1], sorted_indices[::-1]
sns.barplot(x=importance, y=X_train.columns[sorted_indices], color='c')
plt.xlabel('Mean decrease in impurity')
plt.ylabel('Features')
plt.title('Feature Importance in Random Forest')
plt.savefig(str(OUTPUT_FOLDER / 'feature_importance_RandomForestClassifier.pdf'), bbox_inches='tight')
plt.show()

df_importance = pd.DataFrame({
    'name': X_train.columns,
    'importance': classifier.feature_importances_
})

df_importance = df_importance.sort_values(by=['importance'], ascending=False)
df_importance.head(10)

df_importance.head(10).to_latex(
    str(OUTPUT_FOLDER / 'importance_top10_rf.tex'),
    index=False,
    formatters={"name": str.upper},
    float_format="{:.4f}".format,
    caption="Top 10 feature importance.",
    label='tab:importance-rf'
)

important_features_rf = set(df_importance.head(30).name)

oob_error = 1 - classifier.oob_score_
oob_error

important_features_rf

important_features_lr

important_features_rf & important_features_lr

# ### Explaining predictions with SHAP

# +
new_data = X.iloc[0].to_frame().T
#y.iloc[0] False

# Encode
new_data_encoded = pd.DataFrame(encoder.transform(new_data[categorical_features]), columns=encoder.get_feature_names_out(categorical_features))
new_data = pd.concat([new_data.drop(categorical_features, axis=1).reset_index(drop=True), new_data_encoded.reset_index(drop=True)], axis=1)

# Impute
new_data = pd.DataFrame(imputer.transform(new_data), columns = new_data.columns)

new_data_unscaled = new_data.copy()

# Scale
new_data[numerical_features] = scaler.transform(new_data[numerical_features])

# Load the SHAP explainer
explainer = shap.TreeExplainer(pipeline_cv['random_forest'].best_estimator_.named_steps['classifier'])

shap_values = explainer(new_data)


idx = 0
exp = shap.Explanation(
    shap_values.values[:,:,1],
    shap_values.base_values[:,1],
    shap_values.data,
    display_data=new_data_unscaled,
    feature_names=new_data.columns)
shap.plots.waterfall(exp[idx], max_display=10, show=False)
plt.savefig(str(OUTPUT_FOLDER / 'shap.pdf'), bbox_inches='tight')
plt.show()
# -

pipeline_cv['random_forest'].best_estimator_.named_steps['classifier'].predict_proba(new_data)[0][1]

# +
# ensemble TODO togliere

predictions = []

# Make predictions with each model
for name, pipeline in pipeline_cv.items():

    if name in ['xgboost', 'random_forest', 'logistic_regression', 'ada_boost']:
        # Make predictions on the testing set
        y_score = pipeline.predict_proba(X_test)#[:,1]
        predictions.append(y_score)


# Take the average of predictions
ensemble_predictions = np.mean(predictions, axis=0)

# Determine the final class by taking the argmax
final_predictions = np.argmax(ensemble_predictions, axis=1)
# -

accuracy_score(y_test, final_predictions)

# +
# Plot the ROC curve
fig, ax = plt.subplots(figsize=(8,8))

fpr, tpr, _ = roc_curve(y_test, ensemble_predictions[:,1])
roc_auc = auc(fpr, tpr)

ax.plot([0, 1], [0, 1], linestyle='--', color='gray')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')


ax.plot(fpr, tpr, label='Ensemble' + ' (AUC = %0.4f)' % roc_auc)

ax.set_title('ROC Curve comparison')
ax.legend(loc="lower right")
ax.set_aspect('equal')
ax.set_aspect('equal')
plt.savefig(str(OUTPUT_FOLDER / 'roc_ensemble.pdf'), bbox_inches='tight')
plt.show()
