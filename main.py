# # Heart Failure re-hospitalizations
#
# Project for the _Statistical Learning for Healthcare Data_ course held at Politecnico di Milano in the academic year 2022-2023 by Professor Manuela Ferrario and Professor Anna Maria Paganoni.
#
# **It is recommended to [view this notebook in nbviewer](https://nbviewer.org/) for the best viewing experience.**
#
# **You can also [execute the code in this notebook on Binder](https://mybinder.org/) - no local installation required.**
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
# The goal of this problem is to predict the readmission at 6 months from a dataset TODO scrivere bene la descrizione dell'obiettivo e in cosa consiste il dataset, cos'è ogni riga.
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

# ## 2. Data Exploration and Cleaning
#
# ### Importing necessary libraries and dataset
#
# Here we import all the libraries we will use. For reproducibility make sure to install them with `pip install -r requirements.txt`.

# +
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
# Graphics in retina format are more sharp and legible
# %config InlineBackend.figure_format='retina'

from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc, precision_recall_curve, make_scorer, cohen_kappa_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from collections import Counter
from imblearn.over_sampling import SMOTE

from pathlib import Path

from statsmodels.graphics.mosaicplot import mosaic
# -

# Fix the seed for later

SEED = 42

# Use the `pipreqs` library to produce a better `requirements.txt`

# +
# #!pipreqsnb . --force
# #!pipreqs . --force
# -

# Create an output folder for pickle files and figures

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

# Check which patients are missing from the drugs dataframe
missing_patients = ~df.index.isin(df_drugs.index)
print('Missing patients from the drugs dataframe:')
print(df[missing_patients].index)

# Check the contrary (i.e. if there are entries in the drug dataframe that don't corresponde to any patient in the main df)
missing_drugs = ~df_drugs.index.isin(df.index)
print('Missing patients from the patients dataframe:')
print(df_drugs[missing_drugs].index)

# +
#df_drugs.shape
# -

# More drugs were given to the same patient.

# +
#df_drugs.head()

# +
#df_drugs['Administration'] = df_drugs['Drug_name'].apply(lambda x: 'injection' if 'injection' in x.lower() else 'tablet')
#df_drugs['Drug_name'] = df_drugs['Drug_name'].apply(lambda x: x.replace('injection', '').replace('tablet', ''))

# +
#pd.DataFrame(df_drugs['Drug_name'].unique(), columns=['name'])
# -

# Create a pivot table of drugs, with patients as rows and drugs as columns
drug_pivot = df_drugs.pivot_table(index='inpatient.number', columns='Drug_name', fill_value='No', aggfunc=lambda x: 'Yes')
drug_pivot.head()

# Merge the patient dataframe with the drug pivot table
merged_df = pd.merge(df, drug_pivot, on='inpatient.number', how='left')
merged_df.head()

# Fill patients without any drug with No
for drug_name in drug_pivot.columns:
    merged_df[drug_name] = merged_df[drug_name].fillna(value='No')

# +
#merged_df.loc[863648]
# -

# TODO: ora bisogna fare qualcosa con sto merged

# ### Information about the memory usage
#
# We check the memory usage of the dataframe.

df.info(memory_usage='deep')

# Currently we're using 4.0 MB.

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

# We now use only 2.1 MB.
#
# Here is a recap of the columns types.

df.info(verbose=True, show_counts=False)

# Check the shape of the dataset

df.shape

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
# Given that some patients died before the 6 months, such patients present a target of `0` since they haven't been re-admitted, not because they're healthy, but the exact opposite. Thus keeping them together with living healthy patients doesn't make sense.

# Obviously, since the death within 28 days implies the death within 3 months and the non-readmission after 6 months, we can expect these variables to be highly correlated. To further prove our intuition, we can consider the binary variables (i.e. excluding the non-`time` related ones in this set) and plot a matrix with the pairwise Cohen's kappa coefficient, as a measure to the concordance of them.

# +
cols_to_check = [
    'death.within.28.days',
    're.admission.within.28.days',
    'death.within.3.months',
    're.admission.within.3.months',
    'death.within.6.months',
    're.admission.within.6.months'
]

data = df[cols_to_check] # take only binary variables

data = data.dropna()

# Create an empty table to hold the Cohen scores
score_table = pd.DataFrame(columns=data.columns, index=data.columns)

# +
# Loop over every pair of variables in the dataset
for i in range(len(data.columns)):
    for j in range(i+1, len(data.columns)):
        # Calculate the Cohen score between the ith and jth variables
        score = cohen_kappa_score(data.iloc[:,i], data.iloc[:,j])
        
        # Add the score to the score table
        score_table.iloc[i,j] = score
        score_table.iloc[j,i] = score

score_table = score_table.fillna(1)

# +
threshold = 0.3
mask = np.triu(np.ones_like(score_table, dtype=bool), k=0) | (np.abs(score_table) <= threshold)

# Print the score table
fig, ax = plt.subplots(figsize=(4, 4))
sns.heatmap(score_table,
            annot=True, fmt='.2f',
            mask=mask,
            cmap='coolwarm', center=0, cbar=True,
            linewidths=.5,
            ax=ax)
ax.set_aspect("equal")
plt.title("Agreement matrix")
plt.show()
# -

# The deaths are highly correlated for the aforementioned reason, so following the previous motivation, we remove the dead patients.

# +
# specify the columns to check for True values
cols_to_check = ['death.within.28.days', 'death.within.3.months', 'death.within.6.months']

# remove rows where at least one of the specified columns is True
df = df.loc[~(df[cols_to_check] == True).any(axis=1)]
# -

df.shape

# We have removed 57 patients.

# Now those columns are meaninglesse as they all have the same value, and we can remove them.

drop_cols = [
    'death.within.28.days',
    'death.within.3.months',
    'death.within.6.months'
]
df = df.drop(drop_cols, axis=1)

# It also makes sense that if we want to predict the re-admission at 6 months, we have no knowledge neither at 3 months nor 28 days. Therefore we can drop these features as well.

drop_cols = [
    're.admission.within.28.days',
    're.admission.within.3.months',
    'time.of.death..days.from.admission.',
    're.admission.time..days.from.admission.',
    'return.to.emergency.department.within.6.months',
    'time.to.emergency.department.within.6.months',
]
df = df.drop(drop_cols, axis=1)

# +
#TODO: ma una survival analysis? Non so se i dati sono suitable
# -

# ### Checking for duplicates

# Check if there are duplicate rows.

assert df.duplicated().sum() == 0

# ### Checking for missing values

# Identify categorical and numerical variables

df_categorical = df.select_dtypes(include=['category', 'bool'])
df_numerical = df.select_dtypes(include=['float64', 'int64'])


# +
def get_percentage_missing(df):
    df_na = df.isnull()
    list_vars = df_na.sum() / len(df_na.index) * 100
    list_vars = list_vars.sort_values(ascending=False)
    list_vars = list_vars[list_vars != 0]
    return list_vars

names = ['numerical', 'categorical']
numerical_missing = get_percentage_missing(df_numerical)
categorical_missing = get_percentage_missing(df_categorical)


for name, features in zip(names, [numerical_missing, categorical_missing]):
    print(f"Among the {name} features, {len(features)} contain missing values")


#discrete_missing_percentages = get_features_with_nans(df, discrete_vars)
#continuous_missing_percentages = get_features_with_nans(df, continuous_vars)
#categorical_missing_percentages = get_features_with_nans(df, categorical_vars)
#binary_missing_percentages = get_features_with_nans(df, binary_vars)

#print(f"List discrete_missing_percentages contains {len(discrete_missing_percentages)} elements")
#print(f"List continuous_missing_percentages contains {len(continuous_missing_percentages)} elements")
#print(f"List categorical_missing_percentages contains {len(categorical_missing_percentages)} element")
#print(f"List binary_missing_percentages contains {len(binary_missing_percentages)} element")

# -

# The single categorical feature that contains missing values is `occupation` with 1.34% of missing values.

categorical_missing


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

plt.show()
# -

# We now set a threshold for missing values and drop features that present a percentage of missing values higher than the threshold.

# +
threshold = 0.50

missing_cols = numerical_missing[numerical_missing>50].index.tolist()
print('Columns with a high percentage of NaNs:', missing_cols)

limitPer = len(df.index) * threshold
df = df.dropna(thresh=limitPer, axis=1)
# -

# ### Checking for mono-value columns

# And check for columns with all the same value, which are then not significant.

same_cols = df.columns[df.apply(lambda x: len(x.unique()) == 1)].tolist()
print('Columns with all the same value:', same_cols)
df = df.drop(same_cols, axis=1)

# Update the categorical and numerical versions of the dataframe

df_categorical = df.select_dtypes(include=['category', 'bool'])
df_numerical = df.select_dtypes(include=['float64', 'int64'])

# ### Data visualization

# We have 84 numerical features, let us plot them in a big grid to have an understanding of the distribution.

len(df_numerical.columns)

df_numerical[df_numerical.columns[:84]].hist(layout=(21,4), figsize=(15,80))
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
    # calculate the Z-score for each value in the 'value' column
    df['zscore'] = (df[feature] - df[feature].mean()) / df[feature].std(ddof=0)

    # identify outliers as any value with a Z-score greater than threshold or less than -threshold
    outliers = (df['zscore'] > threshold) | (df['zscore'] < -threshold)

    return df[[feature, 'zscore']].loc[outliers]


# Let us go through all the values which may present outliers

print(get_outliers(df, 'respiration', threshold=9))

# The only non-physical value is 0.

df.loc[df['respiration'] == 0, 'respiration'] = np.nan

print(get_outliers(df, 'height', threshold=3))

# They all come from elderly people and not from infants, so we can assume the height is wrong.

df.loc[df['height'] <= 1.25, ['ageCat','height']]

df.loc[df['height'] <= 1.25, 'height'] = np.nan

print(get_outliers(df, 'weight', threshold=4))

df.loc[df['weight'] <= 8, 'weight'] = np.nan

print(get_outliers(df, 'body.temperature', threshold=6))

print(get_outliers(df, 'BMI', threshold=1))

df.loc[(df['BMI'] >= 100) | (df['BMI'] == 0), 'BMI'] = np.nan

print(get_outliers(df, 'fio2', threshold=3))

print(get_outliers(df, 'respiration', threshold=3))
print(get_outliers(df, 'systolic.blood.pressure', threshold=3))
print(get_outliers(df, 'diastolic.blood.pressure', threshold=3))
print(get_outliers(df, 'map', threshold=3))
print(get_outliers(df, 'weight', threshold=3))
print(get_outliers(df, 'height', threshold=3))
print(get_outliers(df, 'BMI', threshold=3))
print(get_outliers(df, 'fio2', threshold=3))
print(get_outliers(df, 'left.ventricular.end.diastolic.diameter.LV', threshold=3))
print(get_outliers(df, 'creatinine.enzymatic.method', threshold=3))
print(get_outliers(df, 'urea', threshold=3))
print(get_outliers(df, 'cystatin', threshold=3))
print(get_outliers(df, 'white.blood.cell', threshold=3))
print(get_outliers(df, 'eosinophil.ratio', threshold=3))
print(get_outliers(df, 'basophil.count', threshold=3))
print(get_outliers(df, 'D.dimer', threshold=3))
print(get_outliers(df, 'international.normalized.ratio', threshold=3))
print(get_outliers(df, 'activated.partial.thromboplastin.time', threshold=3))
print(get_outliers(df, 'thrombin.time', threshold=3))
print(get_outliers(df, 'high.sensitivity.troponin', threshold=3))
print(get_outliers(df, 'prothrombin.time.ratio', threshold=3))
print(get_outliers(df, 'sodium', threshold=3))
print(get_outliers(df, 'potassium', threshold=3))
print(get_outliers(df, 'calcium', threshold=3))
print(get_outliers(df, 'hydroxybutyrate.dehydrogenase.to.lactate.dehydrogenase', threshold=3))
print(get_outliers(df, 'hydroxybutyrate.dehydrogenase', threshold=3))
print(get_outliers(df, 'glutamic.oxaloacetic.transaminase', threshold=3))
print(get_outliers(df, 'creatine.kinase', threshold=3))
print(get_outliers(df, 'creatine.kinase.isoenzyme', threshold=3))
print(get_outliers(df, 'lactate.dehydrogenase', threshold=3))
print(get_outliers(df, 'alkaline.phosphatase', threshold=3))
print(get_outliers(df, 'indirect.bilirubin', threshold=3))
print(get_outliers(df, 'glutamic.pyruvic.transaminase', threshold=3))
print(get_outliers(df, 'globulin', threshold=3))
print(get_outliers(df, 'direct.bilirubin', threshold=3))
print(get_outliers(df, 'total.bilirubin', threshold=3))
print(get_outliers(df, 'total.bile.acid', threshold=3))
print(get_outliers(df, 'triglyceride', threshold=3))
print(get_outliers(df, 'dischargeDay', threshold=3))

# TODO finire questa parte con aiuto di Alice











# Create a range for each one of this value, based on medical knowledge (i.e. instead of having values for systolic.blood.pressure between 0 and 252 we can create three categories that are 'low','normal','high') TODO

target_var = 're.admission.within.6.months'

# +
sns.lmplot(x='weight',y='height',data=df, hue=target_var,palette='Set1')
plt.show()

# TODO togliere outlier altezza e peso
# -

# Deep dive into the some features

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

pd.crosstab(df[target_var], df["gender"], margins=True)

# As final step, plot all the numerical features distribution separately in the two classes to see if we have some hints in features that separate well.

# +
col_inspect = df_numerical.columns[:32]
#col_inspect = ['Killip.grade', 'ageCat']

# Adjust subplots and figsize
fig, axes = plt.subplots(8, 4,figsize=[14,20])
axes = axes.flatten()

for idx, col_name in enumerate(col_inspect):
    plt.sca(axes[idx]) # set the current Axes
    #plt.hist(df_numerical[x],density=True)
    sns.kdeplot(df[df[target_var] == 0][col_name], fill=True, label="Target 0")
    sns.kdeplot(df[df[target_var] == 1][col_name], fill=True, label="Target 1")
    plt.legend()
    plt.xticks(fontsize=8, rotation = 45) # Rotates X-Axis Ticks by 45-degrees
    plt.ylabel('')
    #plt.grid()
    #plt.title(col_name)

fig.tight_layout()
plt.show()

# +
#df_temp = df.copy()
#df_temp['all'] = ''
#sns.violinplot(x='all', y='weight', hue=target_var, data = df_temp, split=True)
#plt.xlabel("")
#plt.show()
# -

# Sono 119 variabili è perciò difficile visualizzarle tutte in un unico blocco. Potremmo forse fare blocchi con una decina di variabili max che siano "simili" tra loro. 
# Come parametro per dire quanto sono simili potremmo sia usare la correlazione che vedere effettivamente cosa descrivono (i.e. weight, hight, BMI nello stesso blocco) TODO

# Discrete variable visualization

discrete_vars = [col for col in df.columns if df[col].dtype == 'int64']
for var in discrete_vars:
    print('Unique values of the discrete variable',var, 'are: ',sorted(df[var].unique()))

# ## 4. Data Preprocessing

# Percentage of positive observations

np.round((df[target_var] == True).sum() / len(df.index), 2)

# ### Correlation analysis

# Choose only a subset of the correlation matrix

# +
# Compute the correlation matrix
corr_matrix = df.corr(numeric_only=True, method='spearman')

#corr_matrix = corr_matrix.iloc[0:10,0:10]

inspect_col = ['urea', 'uric.acid']
# -

corr_matrix = corr_matrix[inspect_col].loc[inspect_col]

# Data will not be shown in cells where `mask` is `True`

threshold = 0.4
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=0) | (np.abs(corr_matrix) <= threshold)

# Plot the correlation matrix using seaborn
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(corr_matrix,
            annot=True, fmt='.2f',
            mask=mask,
            cmap='coolwarm', center=0, cbar=True,
            linewidths=.5,
            ax=ax)
ax.set_aspect("equal")
plt.title("Correlation matrix")
plt.show()

# ### Feature engineering

# +
# feature engineering
#df_numerical['logduration']=df_numerical['duration'].apply(lambda x: math.log(x+1))
# -

# importante da vedere
df['NYHA.cardiac.function.classification'].unique()

# ### Encoding categorical variables

# No need to encode the binary variables
cat_cols = df.select_dtypes(include=['category']).columns.tolist()

# One hot encode the categorical and boolean variables
# drop='if_binary' drops one of male/female for example
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore', drop='if_binary')
encoded_cols = pd.DataFrame(encoder.fit_transform(df[cat_cols]))

# +
encoded_cols.columns = encoder.get_feature_names_out(cat_cols)

# Replace the original categorical and boolean columns with the encoded ones
df_encoded = pd.concat([df.drop(cat_cols, axis=1).reset_index(drop=True),
                        encoded_cols.reset_index(drop=True)],
                       axis=1)
# -

df_encoded.shape

# ### Splitting data into training and testing sets
#
# Separate the target variable from the features

X = df_encoded.drop([target_var], axis=1)
y = df_encoded[target_var]

# Split the dataset into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    stratify=y, # preserve target propotions
                                                    random_state=SEED)

X_train.columns = X.columns
X_test.columns = X.columns

# ### Feature scaling
#
# Standardize the features

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the scaler

import pickle
with open(str(OUTPUT_FOLDER / 'scaler.pkl'), 'wb') as handle:
    pickle.dump(scaler, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Load it back

with open(str(OUTPUT_FOLDER / 'scaler.pkl'), 'rb') as handle:
    scaler = pickle.load(handle)

# ### Feature selection

# +
## Select the top k features using the ANOVA F-value
#k_best = SelectKBest(f_classif, k=10)
#X_train = k_best.fit_transform(X_train, y_train)
#X_test = k_best.transform(X_test)
# -

# ### Imputing missing values
#
# Since we only need to impute numerical features, let us use the mean with a KNNImputer

# Impute missing values using the mean strategy
imputer = KNNImputer(n_neighbors=5)
X_train = pd.DataFrame(imputer.fit_transform(X_train))
X_test = pd.DataFrame(imputer.transform(X_test)) # TODO a volte dà un warning

# TODO qualcosa su https://www.kaggle.com/code/residentmario/simple-techniques-for-missing-data-imputation

# ### Principal Component Analysis

# +
# Instantiate PCA
pca = PCA()

# Fit and transform the data to the new coordinate system
pca.fit(X_train)

X_train_transformed = pca.transform(X_train) # scores
X_test_transformed = pca.transform(X_test)

vars_names = X_train.columns
p = X_train.columns.size
comp_names = ["PC " + str(i) for i in range(1, p+1)]

# +
plt.subplot(221)
plt.bar(vars_names, np.var(X, axis=0))
plt.xticks(rotation=90)
plt.title('Original variables')
plt.ylabel('Variances')
plt.ylim([0, 5])

plt.subplot(223)
plt.bar(comp_names, np.var(X_train_transformed, axis=0))
plt.title('Principal components')
plt.ylabel('Variances')
plt.ylim([0, 10])

plt.subplot(122)
plt.plot(np.cumsum(pca.explained_variance_ratio_), '-o')
plt.xlabel('Number of components')
plt.ylabel('Contribution to total variability')
plt.ylim([0, 1.1])
plt.axhline(y=1, lw=0.5)
plt.axhline(y=0.8, linestyle='--', lw=0.5)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xticks(np.arange(0,p), np.arange(1,p+1))
plt.title('Cumulative explained variance')

plt.tight_layout()
plt.show()

# +
loadings = pca.components_

fig, ax = plt.subplots(1, 2, figsize=(8, 3))

ax[0].bar(range(p), loadings[:, 0], align='center')
ax[1].bar(range(p), loadings[:, 1], align='center')

ax[0].set_title('Factor loading onto PC1')
ax[1].set_title('Factor loading onto PC2')

ax[0].set_xticks(range(p))
ax[1].set_xticks(range(p))
ax[0].set_xticklabels(vars_names, rotation=45)
ax[1].set_xticklabels(vars_names, rotation=45)
plt.tight_layout()
# -

# Visualize the data in the new coordinate system
plt.scatter(X_train_transformed[:, 0], X_train_transformed[:, 1], c=y_train)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

# ## 5. Modeling

# ### Training the models
#
# [`lazypredict`](https://github.com/shankarpandala/lazypredict) is a Python library that is able to quickly check through many models, without any specific fine-tuning, but is able to give an initial look at which could be the best performing models on the task.
#
# Let's begin by importing the `LazyClassifier` class.

from lazypredict.Supervised import LazyClassifier

# We now instantiate it with basic settings

clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)

# And then we fit it using our data

models, predictions = clf.fit(X_train, X_test, y_train, y_test)

# We can retrieve a dictionary of all the models trained

models

# And TODO

model_dictionary = clf.provide_models(X_train,X_test,y_train,y_test)

# +
# The scorers can be either one of the predefined metric strings or a scorer
# callable, like the one returned by make_scorer

scoring = {"AUC": "roc_auc", "Accuracy": make_scorer(accuracy_score)}

# Setting refit='AUC', refits an estimator on the whole dataset with the
# parameter setting that has the best cross-validated AUC score.
# That estimator is made available at ``gs.best_estimator_`` along with
# parameters like ``gs.best_score_``, ``gs.best_params_`` and
# ``gs.best_index_``
gs = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid={"min_samples_split": range(2, 403, 10)},
    scoring=scoring,
    refit="AUC",
    return_train_score=True
)
gs.fit(X_train, y_train)
R = gs.cv_results_
# -

gs.best_estimator_

gs.best_params_

gs.best_score_

pd.DataFrame(R.keys())

# +
m1=R['mean_test_AUC']
s1=R['std_test_AUC']
s2=R['std_train_AUC']
m2=R['mean_train_AUC']

axisX = list(range(len(m1)))
plt.errorbar(axisX, m1, s1, label='test')
plt.errorbar(axisX, m2, s2, label='train')

j1=np.argmax(m1) # maximum value of AUC in terms of mean over the CV folds

plt.plot(axisX[j1],m1[j1], 'ro', markersize=12)
plt.legend()
plt.show()

print(R['params'][j1])
# -

# ### Evaluating model performance

# Train and evaluate multiple models
models = [LogisticRegression(max_iter=100000),
          DecisionTreeClassifier(),
          RandomForestClassifier(),
          SVC(probability=True)]

from mlxtend.plotting import plot_confusion_matrix

# +
fig, axes = plt.subplots(nrows=2, ncols=len(models), figsize=(20,8))#, height_ratios = [1,3])


for i, model in enumerate(models):
    # Train the model on the training set
    model.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = model.predict(X_test)

    # Calculate the accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    print(model.__class__.__name__, 'Accuracy:', accuracy)

    # Calculate the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    #sns.heatmap(cm, annot=True, cmap='coolwarm', fmt='d', ax=axes[0,i])
    axes[0,i].set_title(model.__class__.__name__ + ' Confusion Matrix')
    plot_confusion_matrix(conf_mat=cm,
                                show_absolute=True,
                                show_normed=True,
                                colorbar=True, figure=fig, axis=axes[0,i])

    axes[0,i].set_xlabel('Predicted label')
    axes[0,i].set_ylabel('True label')

    # Calculate the ROC curve
    y_score = model.predict_proba(X_test)[:,1]
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)

    # Plot the ROC curve
    axes[1,i].plot(fpr, tpr, label=model.__class__.__name__ + ' (AUC = %0.2f)' % roc_auc)
    axes[1,i].plot([0, 1], [0, 1], linestyle='--', color='gray')
    axes[1,i].set_xlim([0.0, 1.0])
    axes[1,i].set_ylim([0.0, 1.05])
    axes[1,i].set_xlabel('False Positive Rate')
    axes[1,i].set_ylabel('True Positive Rate')
    axes[1,i].set_title(model.__class__.__name__ + ' ROC Curve')
    axes[1,i].legend(loc="lower right")
    axes[1,i].set_aspect('equal')
    axes[0,i].set_aspect('equal')

plt.tight_layout()
plt.show()
# -

# #### Logistic Regression

# coeff logistic
classifier = LogisticRegression()
classifier.fit(X_train,y_train)
coeff=pd.DataFrame()
coeff["feature"]=X_train.columns
coeff["w"]=classifier.coef_[0]
coeff = coeff.sort_values(by=['w'])
sns.barplot(data=coeff, y="feature", x="w", palette="Blues_d", orient="h")
plt.show()

# +
y_pred = classifier.predict(X_test)
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
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.axis([0, 1, 0, 1])
#plt.grid()
plt.title("Precision Recall curve")
plt.legend()
plt.show()
# -

# #### DecisionTreeClassifier

classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

from sklearn import tree
text_representation = tree.export_text(classifier)
with open("decistion_tree.log", "w") as f:
    f.write(text_representation)

# The `plot_tree` returns annotations for the plot, to not show them in the notebook I assigned returned value to `_`

fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(classifier,
                   feature_names=X_train.columns,
                   class_names=['No','Yes'])

# We can export as a figure but we must use `graphviz`

from sklearn.tree import export_graphviz
export_graphviz(classifier, out_file=str(OUTPUT_FOLDER / 'decision_tree.dot'), feature_names = X_test.columns.tolist(),class_names=['0','1'],
                   filled=True)

# !dot -Tpng decision_tree.dot -o output/decision_tree.png -Gdpi=600
from IPython.display import Image
Image(filename = str(OUTPUT_FOLDER / 'decision_tree.png'))

GiniScore, j = np.sort(classifier.feature_importances_), np.argsort(classifier.feature_importances_)
GiniScore, j = GiniScore[-10:],j[-10:]
sns.barplot(y=X.columns[j], x=GiniScore, color='g')
plt.title('Feature importances using MDI')
plt.xlabel('Mean decrease in impurity')
plt.show()

# Out of bag score.
#
# It permits to have an overview without the cv validation test, of course the results should be then tested on the test set.

bag_clf = BaggingClassifier(DecisionTreeClassifier(), n_estimators=500, bootstrap=True,
                            oob_score=True, n_jobs=-1,random_state=42)
bag_clf.fit(X_train, y_train)

bag_clf.oob_score_

# ## 6. Model Improvement
#
# ### Hyperparameter tuning
#
# ### Cross-validation
#
# ### Final model pipeline

# +
# separate categorical and numerical features
categorical_features = ['categorical_feature_1', 'categorical_feature_2']
numerical_features = ['numerical_feature_1', 'numerical_feature_2']


# create preprocessor for categorical data
cat_preprocessor = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# create preprocessor for numerical data
num_preprocessor = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    #('pca', PCA(n_components=2))
])

# combine the preprocessors into a column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', cat_preprocessor, categorical_features),
        ('num', num_preprocessor, numerical_features)
    ])

# define the models and their parameter grids for grid search
models = {
    'logistic_regression': {
        'model': LogisticRegression(max_iter=10000),
        'param_grid': {'classifier__C': np.logspace(-3, 3, 7)}
    },
    'svm': {
        'model': SVC(),
        'param_grid': {'classifier__C': np.logspace(-3, 3, 7),
                       'classifier__gamma': ['scale', 'auto'],
                       'classifier__kernel': ['linear','rbf']}
    },
    'random_forest': {
        'model': RandomForestClassifier(),
        'param_grid': {'classifier__n_estimators': [100, 200, 300],
                       'classifier__max_depth': [5, 10]}
    },
    'knn': {
        'model': KNeighborsClassifier(),
        'param_grid': {'classifier__n_neighbors': np.arange(10,500,20)}
    },
    'decision_tree_classifier': {
        'model': DecisionTreeClassifier(),
        'param_grid': {'classifier__criterion': ['entropy','gini'], 
                       'classifier__max_depth': [4,5,6,8,10],
                       'classifier__min_samples_split': [5,10,20],
                       'classifier__min_samples_leaf': [5,10,20]}
    },
    'mlp': {
        'model': MLPClassifier(),
        'param_grid': {'classifier__hidden_layer_sizes': [(10, 5),(100,20,5)],
                       'classifier__max_iter': [2000],
                       'classifier__alpha': [0.001,0.1]}
    },
    'naive_bayes': {
        'model': GaussianNB(),
        'param_grid': {}
    }
}

# create the pipelines for each model
pipelines = {}
for name, model in models.items():
    pipelines[name] = Pipeline(steps=[
        #('preprocessor', preprocessor),
        ('classifier', model['model'])
    ])

# split the data into training and testing sets
#X_train, X_test, y_train, y_test = train_test_split(data.drop('target', axis=1), data['target'], test_size=0.2, random_state=42)

scoring = {"AUC": "roc_auc", "Accuracy": make_scorer(accuracy_score)}

# perform grid search cross-validation for each model and output the test accuracy of the best model
for name, pipeline in pipelines.items():
    grid_search = GridSearchCV(
        pipeline,
        param_grid=models[name]['param_grid'],
        cv=5,
        scoring=scoring,
        refit="AUC",
        return_train_score=True
    )
    grid_search.fit(X_train, y_train)
    print(f'{name}: test accuracy = {grid_search.score(X_test, y_test):.3f}')
# -

# ## 7. Conclusion
#
# ### Summary of findings
#
# ### Recommendations for further research
#
# ### Limitations of the analysis

# # Extras

# ## Imbalance

# +
# #!pip install imbalanced-learn
# -

oversample = SMOTE(random_state=45)
X_ov, y_ov = oversample.fit_resample(X_train, y_train)
oversample.get_params()

Counter(y_train)

Counter(y_ov)
