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

# ## 2. Data Cleaning
#
# ### Importing necessary libraries and dataset
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
# Graphics in retina format are more sharp and legible
# %config InlineBackend.figure_format='retina'

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import OneHotEncoder

from pathlib import Path

from statsmodels.graphics.mosaicplot import mosaic
# -

# For reproducibility purposes we load the (previously installed) `watermark` extension and print the current versions of the software.

# %load_ext watermark

# %watermark -m -v -iv

# As first step we load the data, setting the index to the first column since it's already numbered

DATA_FOLDER = Path() / "hospitalized-patients-with-heart-failure-integrating-electronic-healthcare-records-and-external-outcome-data-1.2"
df = pd.read_csv((DATA_FOLDER / "dat.csv"), index_col=0)

# ### Information about the memory usage
#
# We check the memory usage of the dataframe.

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
    're.admission.within.6.months': 'bool'
})

# and see if there has been a memory reduce

df.info(memory_usage='deep')

# We now use only 2.1 MB.
#
# Here is a recap of the columns types.

df.info(verbose=True, show_counts=False)

# Check the shape of the dataset

df.shape

# ### Handling duplicates

# Check that there are no duplicate rows.

assert df.duplicated().sum() == 0

# ### Analizing presence of missing values

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
ax.tick_params(axis='x', labelrotation=90)

plt.show()
# -

# ### Handling meaningless columns
#
# Check for the columns with all NaNs.

nan_cols = df.columns[df.isnull().all()].tolist()
print('Columns with all NaNs:', nan_cols)

# And check for columns with all the same value, which are then not significant.

same_cols = df.columns[df.apply(lambda x: len(x.unique()) == 1)].tolist()
print('Columns with all the same value:', same_cols)

# Drop the columns with all NaNs or all the same value

drop_cols = list(set(nan_cols + same_cols))
df = df.drop(drop_cols, axis=1)
print('Columns dropped:', drop_cols)

# ## 3. Exploratory Data Analysis (EDA)

# ### Descriptive statistics

# ### Data visualization

# Deep dive into the some features

col_inspect = ['Killip.grade', 'diabetes', 'ageCat']
for col_name in col_inspect:
    sns.countplot(x = col_name, data = df, palette = 'magma') # optional hue="re.admission.within.6.months"
    plt.title(col_name)
    plt.show()

# +
#df.sort_values(by=["Churn", "Total day charge"], ascending=[True, False]).head()

#pd.crosstab(df["Churn"], df["International plan"], margins=True)
# -

# **Mosaic plot** to visualize the distribution of categorical variable of type 'category' with respect to the target 

from statsmodels.graphics.mosaicplot import mosaic

# +
# Visualize the distribution of the categorical variable with respect to the target variable
target_var = 're.admission.within.6.months'
categorical_vars = [col for col in df.columns if df[col].dtype == 'category']
binary_vars = [col for col in categorical_vars if df[col].nunique()==2]
nonbinary_vars = [col for col in categorical_vars if df[col].nunique()!=2]

# Setting some parameters for mosaic function
# labelizer
def empty_labelizer(k):
    return ""

# properties
props = lambda key: {'color': 'r' if 'False' in key else 'green'}
# Create the figure and axis
fig, axs = plt.subplots(nrows=len(categorical_vars), ncols=1, figsize = (20,40))

# Iterate over categorical variables and create mosaic plots
for i, var in enumerate(categorical_vars):
    # Create the mosaic plot
    mosaic(df,index=[var, target_var], ax=axs[i], title=f'Mosaic plot of {var} by {target_var}',axes_label=True, 
           horizontal = False, gap =0.07, labelizer=empty_labelizer,properties = props)
# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
for ax in axs.flat:
    ax.set_xlabel('')
    ax.set_title('')
    ax.set_ylabel('')
plt.show()
# -

# **Stacked bar plot** to visualize categorical variable of type 'bool'

# +
binary_cat1 = [df[col].unique()[0] for col in binary_vars]
binary_cat2 = [df[col].unique()[1] for col in binary_vars]

concat = pd.DataFrame()
for i,var in enumerate(binary_vars):
    count = df[[target_var]+[var]].groupby([target_var]+[var])[var].count().unstack()
    concat = pd.concat([concat,count],axis=1)

cat1Count = concat[binary_cat1]
cat2Count = concat[binary_cat2]

bar_width = 0.25
gap = 100

fig,ax = plt.subplots(figsize =(12,6))

x = np.arange(len(binary_vars))

bars1 = ax.bar(x-bar_width/2, cat1Count.loc[True], bar_width, label ='True' ,color = 'green')
bars2 = ax.bar(x-bar_width/2, cat1Count.loc[False], bar_width, label='False',bottom =  [b.get_height() for b in bars1], color='red')

height = [x + y for x, y in zip([b.get_height() for b in bars1], [b.get_height() for b in bars2])]
for i,bar in enumerate(bars2):
    ax.text(bar.get_x() + bar.get_width()/2, height[i], str(binary_cat1[i]), ha='center', va='bottom', color='black')
ax.legend()

bars3 = ax.bar(x-bar_width/2, cat2Count.loc[True], bar_width, label ='True', 
               bottom = [x + y +gap for x, y in zip([b.get_height() for b in bars1], [b.get_height() for b in bars2])], color='green')
bars4 = ax.bar(x-bar_width/2, cat2Count.loc[False], bar_width, label='False',
               bottom = [x + y +z +gap for x, y,z in zip([b.get_height() for b in bars1], [b.get_height() for b in bars2],[b.get_height() for b in bars3])],color='red')
height = [x+y+z+w +gap for x,y,z,w in zip([b.get_height() for b in bars1], [b.get_height() for b in bars2],[b.get_height() for b in bars3],[b.get_height() for b in bars4])]
for i,bar in enumerate(bars4):
    ax.text(bar.get_x() + bar.get_width()/2, height[i], str(binary_cat2[i]), ha='center', va='bottom', color='black')
# set the labels and title
ax.set_xticks(x)
ax.set_xticklabels(binary_vars)
ax.set_ylabel('Count')
ax.set_title('Stacked Bar Plot')


# show the plot
plt.show()

plt.show()
# -

# **Swarmplot, violinplot or kdeplot** 3 opzioni per visualizzare le variabili continue

# +
fig, axs = plt.subplots(nrows= 1 , ncols=3,figsize = (10,6))
# Create grouped violin plots
sns.swarmplot(x=target_var, y='map', data=df, ax=axs[0])
sns.violinplot(x=target_var, y='map', data = df, ax= axs[1])

sns.kdeplot(df[df[target_var] == 0]['map'], shade=True, label="Target 0",ax=axs[2])
sns.kdeplot(df[df[target_var] == 1]['map'], shade=True, label="Target 1",ax=axs[2])
# -


df['all'] = ''
sns.violinplot(x='all', y='weight', hue=target_var, data = df, split=True)
plt.xlabel("")
plt.show()

# Sono 119 variabili è perciò difficile visualizzarle tutte in un unico blocco. Potremmo forse fare blocchi con una decina di variabili max che siano "simili" tra loro. 
# Come parametro per dire quanto sono simili potremmo sia usare la correlazione che vedere effettivamente cosa descrivono (i.e. weight, hight, BMI nello stesso blocco) TODO

fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize=(20,5))
continuous_vars = [col for col in df.columns if df[col].dtype == 'float64']
data = pd.melt(df, id_vars=[target_var], value_vars=continuous_vars[0:8])
sns.violinplot(x="variable", y="value", hue=target_var, data=data, split=True)

# Discrete variable visualization

discrete_vars = [col for col in df.columns if df[col].dtype == 'int64']
for var in discrete_vars:
    print('Unique values of the discrete variable',var, 'are: ',sorted(df[var].unique()))

# Create a range for each one of this value, based on medical knowledge (i.e. instead of having values for systolic.blood.pressure between 0 and 252 we can create three categories that are 'low','normal','high') TODO

# ### Correlation analysis

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
#plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
#plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)

ax.tick_params(
    axis='both',          # changes apply to both x-y-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

ax.set_aspect("equal")

# Show the plot
plt.show()
# -

# ### Feature engineering

# importante da vedere
df['NYHA.cardiac.function.classification'].unique()

# ## 4. Data Preprocessing

# ### Encoding categorical variables

# Three common encoding methods are: one-hot encoding, label encoding, and CatBoost encoding.
# Look at the advantages and disadvantages.
#
# First up is **one-hot encoding**. This technique is great for nominal or unordered categorical variables, as it keeps all the information of the categorical variable without introducing any ordinal relationship. However, one-hot encoding can result in high dimensionality, which makes it computationally expensive. Additionally, this method can lead to overfitting, especially when there are a large number of categories, and there is a loss of information about the frequency or distribution of the categories in the original feature.
#
# Next up is **label encoding**, which is simple and computationally efficient, Works well with decision tree-based models. This method is useful for categorical features that have an inherent order or ranking, but it does not capture the non-linear relationship between the categorical feature and the target variable. Label encoding can lead to biased results if the order of the labels is arbitrary, and it can result in overfitting if there is a large number of categories in the feature.
#
# Finally, we have **CatBoost encoding**, which is a powerful technique that takes into account the target variable and helps capture the non-linear relationship between the categorical feature and the target variable. CatBoost encoding can handle high cardinality categorical features with many categories, and it helps to reduce dimensionality by producing a single feature instead of multiple features like one-hot encoding. However, CatBoost encoding is computationally expensive compared to one-hot encoding and label encoding, and it requires a large amount of data to train the encoding parameters. Additionally, this method can lead to overfitting if the encoding parameters are not regularized properly.
#
# In summary, one-hot encoding is a great choice for nominal or unordered categorical variables, while label encoding can be useful for ordinal or ordered categorical variables. CatBoost encoding can be a good choice if there is a non-linear relationship between the categorical feature and the target variable, but it may not always be necessary or feasible to use, especially for small datasets or linear models. Ultimately, the choice of encoding technique depends on the nature of the data and the modeling task at hand.

# No need to encode the binary variables
cat_cols = df.select_dtypes(include=['category']).columns.tolist()
cat_cols

# #### One hot encoder

# One hot encode the categorical and boolean variables
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

# #### Label encoder

# LabelEncoder assigns a unique integer value to each category in the categorical feature, such that each category is mapped to a different integer

from sklearn.preprocessing import LabelEncoder

# +
# create LabelEncoder object
le = LabelEncoder()

# apply LabelEncoder to each categorical feature
for col in cat_cols:
    df[col] = le.fit_transform(df[col])
# -

# #### Cat boost encoder

import category_encoders as ce

encoder=ce.cat_boost.CatBoostEncoder(cols=cat_cols,
                                     random_state=None, sigma=None, a=1)
encoder.fit(df,target_var)
df = encoder.transform(df)

# ### Splitting data into training and testing sets
#
# Separate the target variable from the features

X = df_encoded.drop(['re.admission.within.6.months'], axis=1)
y = df_encoded['re.admission.within.6.months']

# Split the dataset into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ### Feature scaling
#
# Standardize the features

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

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

# ## 5. Modeling
#
# ### Training the models
#
# [`lazypredict`](https://github.com/shankarpandala/lazypredict) is a Python library that is able to quickly check through many models, without any specific fine-tuning, but is able to give an initial look at which could be the best performing models on the task.
#
# Let's begin by importing the `LazyClassifier` class.

from lazypredict.Supervised import LazyClassifier

# We now instantiate it with basic settings

clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)

# And then we fit it using our data

models, predictions = clf.fit(X_train, X_test, y_train, y_test)

# We can retrieve a dictionary of all the models trained

models

# And TODO

model_dictionary = clf.provide_models(X_train,X_test,y_train,y_test)

# ### Evaluating model performance

# Train and evaluate multiple models
models = [LogisticRegression(max_iter=100000), DecisionTreeClassifier(), RandomForestClassifier(), SVC(probability=True)]

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

# ## 6. Model Improvement
#
# ### Hyperparameter tuning
#
# ### Cross-validation
#
# ## 7. Conclusion
#
# ### Summary of findings
#
# ### Recommendations for further research
#
# ### Limitations of the analysis
