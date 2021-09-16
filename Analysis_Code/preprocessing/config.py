preprocess = True

#preprocessing parameters (delete the first row in the raw data)
params = {}
params["raw_data_file_path"] = "/path/to/csv/file/from/survey"
params["output_base_directory"] = "/path/to/where/to/save/the/preprocessed/csv/data"
params["county_income_data"] = "./../../Datasets/Hospital/county_income.csv" #data to extract the income of the county of the hospital; indirect measurement of county income
params["state_abbrev_fp"] = "./../../Datasets/Hospital/state_abbreviations.csv"
params["time_cutoff_seconds"] = 30 # if student answers survey took quickly, then remove
params["raw_data_question_dictionary"] = {
    #Response Date
    "Date": "Recorded Date",

    #Demographics
    "Email": 'What is your email? Please use your school email containing ".edu" Why am I being asked this?We will be using email addresses to filter duplicate responses. The ".edu" email address will be used as our validation criteria for medical student enrollment. Email addresses will be deidentified during data collection, and inputted emails will NOT be used for contact',
    "Year": "What class are you? Note: This is ONLY for clinical medical students",
    "Age": "What is your age?",
    "Race": "What race do you identify with?",
    "Gender": "What gender do you identify as?",
    "SES": "What is your perceived socioeconomic status?",
    "Hospital_State": "What hospital are you currently working at?\nState, District, Territory",
    "Hospital": "Select hospital (if not in list, pick OTHER):",

    #PPE
    "PPE_accessibility": "Please indicate the extent to which you agree with the following statement: I am able to obtain appr",
    "PPE_training": "To what extent do you agree with the following: I was properly prepared/provided adequate training for how to use PPE.",
    "PPE_satisfaction": "How satisfied are you with the training and availability of PPE at your hospital?",

    #Testing
    "Testing_freq": "How often are you tested while on rotations?",
    "Testing_results_turnover": "If you get regularly tested, how long does it take to receive your results?",
    "M1_2_tested": "Are the M1/M2s in your school being regularly tested?",
    "Testing_access_if_wanted": "Do you have access to COVID-19 testing if you wanted to?",
    "Testing_symptoms_required": "Do you have to be symptomatic to receive a COVID-19 test?",
    "Testing_satisfaction": "How satisfied are you with your school's current testing system?",

    #Communication
    "Comms_update_freq": "How often do you receive updates by your school on COVID-19?",
    "Comms_update_composition": "If you receive updates, what is included in these messages? (Optional)",
    "Comms_student_worker": "Does your school categorize you as a student or healthcare worker in terms of COVID-19 policies?",
    "Comms_vaccine": "What has your school communicated with you about the upcoming vaccine?",
    "Comms_mental_health": "To what extent do you agree with the following: My mental health improved since the start of the pandemic.",
    "Comms_satisfaction": "How satisfied are you with how your school has communicated with you about COVID-19?",
    
    #Exposure
    "Exposure_COVID_positive_hx": "Have you tested positive for COVID-19 during your clinical rotations?",
    "Exposure_COVID_pt_freq": "How often do you see COVID-19 patients?",
    "Exposure_quarantine_policy": "Is there a policy in place regarding rotations if you have to quarantine because of COVID-19?",
    "Exposure_discomfort_PPE_by_peers": "To what extent do you agree with the following: I experience discomfort in the workplace due to improper PPE usage by others.",
    "Exposure_sharing_comfort": "One of the reasons schools do not want to share COVID-19 cases is due to fear of loss of anonymity on behalf of the students. To what extent do you agree with the following: If I were to test positive for COVID-19, I would be comfortable communicating my results with my school",
    "Exposure_satisfaction": "How satisfied are you with your safety concerning exposures?",

    #General
    "General_satisfaction": "In general, how satisfied are you with your school's response and policy to COVID-19 in regards to your clinical experience?",

    #Free response
    "FR: If there is a policy in place, what details are you aware of?": "If there is a policy in place, what details are you aware of?",
    "FR: What, if anything, could your school have done better to handle the pandemic? (Optional)": "What, if anything, could your school have done better to handle the pandemic? (Optional)",
    "FR: What, if anything, has your school done well in terms of the pandemic? (Optional)": "What, if anything, has your school done well in terms of the pandemic? (Optional)",

}
params["continuous_features"] = ["Age"]
params["school_csv_path"] = "./../../Datasets/School_data/school_list.csv"
params["school_data_dictionary"] = {
    #name used in code (key), name used in excel
    "Medschool": "School",
    "Domain": "Email_domain",
    "State": "State",
    "Region": "Region, based on US Census Bureau (LINK)",
    "MedSchool_size": "Med Student Population Size (LINK)",
    "University_size": "University Student Population Size ",
    "Endowment_billions": "Endowment (billions)",
    "Endowment_for_med_school": "Medical school endowment? T/F",
}
params["Income_Brackets"] = [48000, 61000, 82000]