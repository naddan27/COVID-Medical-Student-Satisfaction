# COVID-Medical-Student-Satisfaction
COVID-19 has affected institutions worldwide, including medical schools. Medical schools had to rapidly adapt their curriculum to deliver a safe learning environment for their students who are in the front-lines of the pandemic. Despite numerous research on the effects of the pandemic on healthcare professionals, such as residents, healthcare personnel, and physicians, there has been limited research on its effect on medical students in their clinical years, who are generally in the same hospital environment during their rotations. The purpose of this study was to assess the satisfaction of clinical medical students to their schools' response to the COVID-19 pandemic and the various specific components that influenced their satisfaction.

For the purposes of student confidentiality, the data is not available. However, the code to generate the results are present here.

| Table of Contents |
| ----------------- |
|[1. Data Preprocessing](#data-preprocessing) |
|[2. Preliminary Analysis with Chi2 and RankSum](#preliminary-analysis-with-chi2-and-ranksum)|
|[3. Logistic Regression Analysis](#logistic-regression-analysis)|

## Data Preprocessing
In order to analyze the data, the data from the survey must be preprocessed. Preprocessing steps include deriving features from survey data, removing student identifiers, removing duplicates.

To preprocess the data, open the notebook at
```bash
./Analysis_Code/preprocessing/functions_preprocessing.ipynb
```

First, set the config file to the correct paths and settings. Then, run the notebook.

## Preliminary Analysis with Chi2 and RankSum
Now, we will perform chi2 and ranksum analysis for the categorical and continuous features, respectively. The distribution of the answers are also shown with pie charts. Conditional distributions are shown via tables.

To perform preliminary analysis, open and run the notebook at
```bash
./Analysis_Code/prelim_analysis/Visual Distributions.ipynb
```

## Logistic Regression Analysis
The final analysis using logistic regression is in Stata. Satisfaction features in the survey distributed had Likert scale answer choices (e.g. strongly disagree, slightly disagree, neither disagree or agree, slightly agree, strongly agree). First, we need to see if these answer choices should be coded continuously or categorically. Categorical coding removes the inherent order of the Likert scale answer choices. Continuous would assign each answer choice a consecutive integer in the logical order (e.g. strongly disagree = 1, strongly disagree = 2, neither = 3, slightly agree, = 4, strongly agree = 5). This assumes that each of the answer choices are equally spaced in the logistic regression analysis.

Open Stata, and run the do file at
```bash
./Analysis_Code/log_reg/LR_and_BIC_test.do
```

Check for which model (continuous or categorical encoding) has the lower BIC score. Furthermore, check if the coefficients in the categorical encoding have a linear relationship in the expected order. If so and if the continuous model has the lower BIC score, the continuous model is preferred. Else, categorical model is preferred.

Now, let us create logistic regression model to assess the odds a component of a school's response affected a student's satisfaction. Run the do file at 
```bash
./Analysis_Code/log_reg/create_logistic_regression_models.do
```
