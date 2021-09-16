clear all
* replace with the absolute path of the csv data file after prelim analysis
import delimited "/path/to/data/Datasets/Survey_Data/preprocessed/after_prelim_analysis.csv"

* Define the Labels for one hot encoding
label define onehotencode_agreedisagree 1 "Strongly disagree" 2 "Somewhat disagree" 3 "Neither agree nor disagree" 4 "Somewhat agree" 5 "Strongly agree"
label define onehotencode_satisfied 1 "Extremely dissatisfied" 2 "Somewhat dissatisfied" 3 "Neither satisfied nor dissatisfied" 4 "Somewhat satisfied" 5 "Extremely satisfied"
label define onehotencode_bin_sat 1 "Satisfied" 0 "Dissatisfied"
label define onehotencode_daily 0 "Never" 1 "Less than monthly" 2 "Monthly" 3 "Weekly" 4 "Daily"
label define onehotencode_twice 0 "Never" 1 "Less than monthly" 2 "Once a week" 3 "Twice a week"
label define onehotencode_weekly 0 "Never" 1 "Less than monthly" 2 "Monthly" 3 "Weekly"
label define testing_results_turnover_labels 1 "Within 24 hrs" 2 "24-72 hrs" 3 "72 hrs - week" 4 "Over a week"
label define exposure_covid_pt_freq_label 0 "Never" 1 "Less than monthly" 2 "Monthly" 3 "Weekly" 4 "Daily"

*create shortened names for the variables
clonevar exposure_discomfort = exposure_discomfort_ppe_by_peers
clonevar exposure_covid = exposure_covid_pt_freq

***********************************************************************************************
*update features here
local ppe_features ppe_accessibility ppe_training
local testing_features testing_freq 
local comms_features comms_mental_health comms_update_freq 
local exposure_features exposure_covid exposure_discomfort exposure_sharing_comfort
local satisfaction_features ppe_satisfaction_binary testing_satisfaction_binary comms_satisfaction_binary exposure_satisfaction_binary general_satisfaction_binary

*Group the features by the labels they carry
local agreedisagree_features ppe_accessibility ppe_training comms_mental_health exposure_discomfort exposure_sharing_comfort 
local satisfied_features ppe_satisfaction testing_satisfaction comms_satisfaction exposure_satisfaction general_satisfaction
local bin_sat_features ppe_satisfaction_binary testing_satisfaction_binary comms_satisfaction_binary exposure_satisfaction_binary general_satisfaction_binary
local time_daily_features exposure_covid 	
local time_twice_features testing_freq
local time_weekly_features comms_update_freq
***********************************************************************************************

*Group the features together
local all_features `ppe_features' `testing_features' `comms_features' `exposure_covid_pt_freq' `satisfaction_features'

*encode the features according to the proper label mapping
foreach feature in `agreedisagree_features'{
	encode `feature', gen("`feature'_en") label(onehotencode_agreedisagree)
}
foreach feature in `satisfied_features'{
	encode `feature', gen("`feature'_en") label(onehotencode_satisfied)
}
foreach feature in `bin_sat_features'{
	encode `feature', gen("`feature'_en") label(onehotencode_bin_sat)
}
foreach feature in `time_daily_features'{
	encode `feature', gen("`feature'_en") label(onehotencode_daily)
}
foreach feature in `time_twice_features'{
	encode `feature', gen("`feature'_en") label(onehotencode_twice)
}
foreach feature in `time_weekly_features'{
	encode `feature', gen("`feature'_en") label(onehotencode_weekly)
}


*Demographics
tostring patient_ses_quartile, gen(patient_ses_quartile_str)
clonevar endowmentover900 = endowment_per_capita_thousands_o

local demographic_features year notm3 race blackmixednoneoftheabove gender ses ses_binary ///
region medschool_size_categorical endowmentover900 ///


foreach feature in `demographic_features'{
	encode `feature', gen("`feature'_en")
}

encode m1_2_tested_grouped, gen(m1_2_tested_grouped_en)
encode testing_symptoms_required_group, gen(test_symptom_required_group_en)
encode test_symptom_req_invgroup, gen(test_symptom_req_invgroup_en)
encode testing_access_if_wanted_group, gen(test_access_ifwanted_group_en)
encode testing_results_turnover, gen(testing_results_turnover_en) label(testing_results_turnover_labels)
encode exposure_covid_pt_freq, gen(exposure_covid_pt_freq_en) label (exposure_covid_pt_freq_label)
encode exposure_covid_positive_hx, gen(exposure_covid_positive_hx_en)
encode exposure_quarantine_policy_group, gen(exp_quar_policy_grp_en)
encode exposure_covid_pt_freq_bin, gen(exposure_covid_pt_freq_bin_en)

gen exp_covid_pt_freq_never_week_m = exposure_covid_pt_freq_en
recode exp_covid_pt_freq_never_week_m 2 = 1
recode exp_covid_pt_freq_never_week_m (3/4 = 2)
label define exp_covid_pt_freq_nev_week_m_lab 0 "Never" 1 "Less than weekly" 2 "Weekly or more"
label values exp_covid_pt_freq_never_week_m exp_covid_pt_freq_nev_week_m_lab

encode vaccine_simplified, gen(vaccine_simplified_en)
gen gender_simplified = gender
replace gender_simplified = "" if gender_simplified == "Non-binary/non-conforming"
replace gender_simplified = "" if gender_simplified == "Prefer not to respond"
encode gender_simplified, gen(gender_simplified_en)