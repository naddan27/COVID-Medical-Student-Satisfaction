from uszipcode import SearchEngine
import numpy as np
import pandas as pd
from collections import Counter
from datetime import datetime

def check_for_duplicates(df, params):
    """
    Checks for survey answers from the same student by verifying that
    all of the emails are unique

    Parameters
    ----------
    df : pd.DataFrame
        The data to which to check for duplicates. The dataframe must contain
        a header called 'Email' as this is the values it will check for
        duplicates
    params : dict
        The keys from the config file
    """
    #check duplicate emails
    unique_emails = set()
    for i, email in enumerate(df["Email"]):
        processed_email = str(email).lower().strip()

        duplicate_emails_found = False
        if processed_email in unique_emails:
            duplicate_emails_found = True
            print("Duplicate email found at index ", i, ": ", email)
            input("Continue?")
        else:
            unique_emails.add(processed_email)
        
        if duplicate_emails_found == False:
            print("No duplicate emails found")
            
        return duplicate_emails_found

def extract_features(df, params):
    """
    Extracts the answers from the survey data and saves it into a new 
    dataframe, replacing the headers with shorter header names designated in the
    config file.

    Parameters
    ----------
    df : pd.DataFrame
        The Dataframe containing the data from the raw survey data
    params : dict
        The parameters designated in the config file
    
    Returns
    -------
    df : pd.DataFrame
        The Dataframe with headers renamed to the short names
    """
    extracted_df = df[["Duration (in seconds)"]].copy()

    #extract appropriate fetures into new df with headers renamed according to params dictionary
    for param_dict_key in params["raw_data_question_dictionary"].keys():
        if param_dict_key != "Hospital":
            header_in_raw_df = params["raw_data_question_dictionary"][param_dict_key]
            extracted_df.insert(len(extracted_df.columns), param_dict_key, df[header_in_raw_df])

    #add the hospital data
    hospital_state_ix = extracted_df.columns.get_loc("Hospital_State")
    hospital_features_of_all_states = []

    for header in df.columns: #find the features that match ones that would contain hospital data
        hospital_header_name = params["raw_data_question_dictionary"]["Hospital"]
        if header[:len(hospital_header_name)] == hospital_header_name:
            hospital_features_of_all_states.append(header)
    extracted_df.insert(hospital_state_ix + 1, "Hospital", df[hospital_features_of_all_states].bfill(axis = 1).iloc[:, 0])
    
    return extracted_df

def drop_responses_completed_too_quickly(input_df, params):
    df = input_df.copy()
    response_too_quick_ix = []
    for i, time in enumerate(df["Duration (in seconds)"]):
        if time < params["time_cutoff_seconds"]:
            response_too_quick_ix.append(i)
    df.drop(response_too_quick_ix)

    print(len(response_too_quick_ix), " responses were under the time cutoff and therefore dropped.")

    return df

def preprocess_school_list(school_df):
    """
        Preprocesses the school data  by adding an endowment per capita column
    
    Parameters
    ----------
    school_df : pd.DataFrame
        The Dataframe containing the data from the school csv
    
    Returns
    -------
    None
    """
    #create an endowment per capita column
    endowment_per_capita = []
    for ix, school in school_df.iterrows():
        endowment = school["Endowment_billions"]
        if school["Endowment_for_med_school"] == "T": #divide by the med school size
            epc = endowment / float(school["MedSchool_size"])
            if epc == epc: #check if one of the values are null or empty
                endowment_per_capita.append(epc)
            else:
                raise AssertionError("Check ", school["Medschool"], "endowment")
        elif school["Endowment_for_med_school"] == "F": #divide by the university size
            epc = endowment / float(school["University_size"])
            if epc == epc:
                endowment_per_capita.append(epc)
            else:
                raise AssertionError("Check ", school["Medschool"], "endowment")
        else: #if T/F is missing
            #check if the endowment is missing
            if endowment == endowment:
                raise AssertionError("Check ", school["Medschool"], "T/F")
            else:
                endowment_per_capita.append(np.nan)

    school_df["Endowment_per_capita"] = endowment_per_capita

def derive_hospital_zipcode_county(response_df):
    """
    Based on the hospital name, get the zipcode and the county of the hospital.
    This will be used to generate the income of the neighborhood the hospital
    is located in

    Parameters
    ----------
    response_df : pd.DataFrame
        The data to derive the hospital data from

    Returns
    -------
    None
    """
    hospital_zipcode = []
    for hospital in response_df["Hospital"]:
        if hospital != hospital: #if hospital is nan
            hospital_zipcode.append(np.nan)
        elif hospital == "OTHER":
            hospital_zipcode.append(np.nan)
        else:
            hospital_zipcode.append(hospital[-5:]) #extract the last five digits which represent the zip code
    response_df["Hospital_Zipcode"] = hospital_zipcode

    #find the hospital county
    search = SearchEngine(simple_zipcode=True)
    hospital_county = []
    for zipcode in response_df["Hospital_Zipcode"]:
        if zipcode != zipcode:
            hospital_county.append(np.nan)
        else:
            zc = search.by_zipcode(zipcode)
            hospital_county.append(zc.to_dict()["county"])
    response_df["Hospital_county"] = hospital_county

def derive_patient_ses(response_df, params):
    """
    Get the socioeconomic status of the patient population the hospital serves.
    This is estimated by the median household income of the county of the
    hospital.

    Parameters
    ----------
    response_df : pd.DataFrame
        The data that contain the hospital data to which to add the patient SES
    
    Returns
    -------
    None
    """
    state_abbreviations_df = pd.read_csv(params["state_abbrev_fp"])

    #get Dataframe mapping county to income
    income_df = pd.read_csv(params["county_income_data"])[["Geographic Area Name", "Estimate!!Households!!Median income (dollars)"]]
    income_county = []
    income_state = []
    for ic in income_df["Geographic Area Name"]:
        income_county.append(ic.split(",")[0].strip())
        state = ic.split(",")[1].strip()
        try:
            income_state.append(state_abbreviations_df[state_abbreviations_df["State"] == state]["Postal"].values[0])
        except:
            print(state)
        
    income_df["County"] = income_county
    income_df["State"] = income_state 

    #map each hospital to the income
    response_hospital_income = []
    for ix, response in response_df.iterrows():
        id_county = response["Hospital_county"]
        id_state = response["Hospital_State"]
        if id_county != id_county:
            response_hospital_income.append(np.nan)
            continue
        
        subset_in_state = income_df[income_df["State"] == id_state]
        subset = subset_in_state[subset_in_state["County"].str.lower() == id_county.lower().strip()]

        if len(subset) > 1:
            print(id_state, id_county, ":More than one county found")
        elif len(subset) == 0:
            print(id_state, id_county, response["Hospital"], ": No county found")
            response_hospital_income.append(np.nan)
        else:
            response_hospital_income.append(subset["Estimate!!Households!!Median income (dollars)"].values[0])
    response_df["Patient_Median_Income"] = response_hospital_income

    #map each hospital to quartile
    quartiles = []
    for pmi in response_df["Patient_Median_Income"]:
        if pmi != pmi:
            quartiles.append(np.nan)
            continue
        if pmi < params["Income_Brackets"][0]:
            quartiles.append("1")
        elif pmi < params["Income_Brackets"][1]:
            quartiles.append("2")
        elif pmi < params["Income_Brackets"][2]:
            quartiles.append("3")
        else:
            quartiles.append("4")
    response_df["Patient_SES_Quartile"] = quartiles

def drop_hospital_name_county_zipcode(response_df):
    """
    Removes potential identifiers that are associated to a student based on the
    hospital they work in

    Parameters
    ----------
    response_df : pd.DataFrame
        The dataframe to remove the identifying hospital data
    """
    response_df.drop(columns = ["Hospital_State", "Hospital", "Hospital_Zipcode", "Hospital_county"], inplace = True)

def add_school_data_to_responses(response_df, school_df):
    """
    Append to the dataframe the region, medical school student size,
    endowment per capita based on the information provided in the 'school_df'

    Parameters
    ----------
    response_df : pd.DataFrame
        The data to which to add the school data
    school_df : pd.DataFrame
        The data from which the school data is derived from
    """
    respondent_school_data = []

    for email in response_df["Email"]:
        at_ix = email.index("@")
        domain = str(email[at_ix+1:]).lower().strip()

        #find the school based on the domain
        school_information = school_df[school_df["Domain"] == domain]
    

        if len(school_information) > 1:
            print(domain, " has more than one schools it can refer to")
            raise Exception("Can't have more than one school as reference")
        elif len(school_information) == 0:
            print(domain, " does not correlate to a school")
            respondent_school_data.append(["delete", "delete", "delete", "delete"])
            continue
        
        school = school_information["Medschool"].item()
        region = school_information["Region"].item()
        medschool_size = school_information["MedSchool_size"].item()
        endowment = school_information["Endowment_per_capita"].item()

        respondent_school_data.append([school, region, medschool_size, endowment])

    respondent_school_data_np = np.array(respondent_school_data)
    
    response_df["Medschool"] = respondent_school_data_np[:, 0]
    response_df["Region"] = respondent_school_data_np[:, 1]
    response_df["MedSchool_size"] = respondent_school_data_np[:, 2]
    response_df["Endowment_per_capita"] = respondent_school_data_np[:, 3]

def delete_inappropriate_schools(response_df):
    """
    Deletes the responses where the school data is not known

    Parameters
    ----------
    response_df : pd.DataFrame
        The data to which to remove the responses with unknown school data
    
    Returns
    -------
    None
    """
    response_df.reset_index(drop = True, inplace = True)
    ix = response_df.index[response_df["Medschool"] == "delete"]
    print("deleted: ", response_df.iloc[ix]["Email"].tolist())
    response_df.drop(ix, inplace = True)
    response_df.reset_index(drop = True, inplace = True)

def drop_school_email_data(response_df):
    """
    Remove identifiers related to school

    Parameters
    ----------
    response_df : pd.DataFrame
        The data to drop the identifying information

    Returns
    -------
    None
    """
    response_df.drop(columns = ["Email", "Medschool"], inplace = True)

def make_fr_free_version(response_df):
    """
    Returns a version of the data that does not have the free response data

    Parameters
    ----------
    response_df : pd.DataFrame
        The data to remove the free responses
    
    Returns
    -------
    pd.DataFrame
        The Dataframe containing the data without the free responses
    """
    fr_free_df = response_df.copy()

    fr_headers = []
    for header in response_df.columns:
        if header[:3] == "FR:":
            fr_headers.append(header)
    
    fr_free_df.drop(columns = fr_headers, inplace = True)

    return fr_free_df

def one_hot_encode_comms_update_composition(response_df):
    """
    One-hot encodes (make dummy variable) the feature regarding the composition
    of the communication update messages. From the survey, this is combined into
    one column. This method separates this one column into T/F for each possible
    answer choice.

    Parameters
    ----------
    response_df : pd.DataFrame
        The Dataframe to one-hot encode the update message composition feature
    
    Returns
    -------
    None
    """
    answer_choices = set()
    for answer in response_df["Comms_update_composition"]:
        if answer == answer:
            for choice in answer.split(","):
                answer_choices.add(choice)
    answer_choices

    answer_choices_dict = dict()
    for ac in answer_choices:
        answer_choices_dict[ac] = []

    for user_response in response_df["Comms_update_composition"]:
        if user_response == user_response:
            user_response_breakdown = user_response.split(",")
            for possible_answer_choice in answer_choices:
                if possible_answer_choice in user_response_breakdown:
                    answer_choices_dict[possible_answer_choice].append(1)
                else:
                    answer_choices_dict[possible_answer_choice].append(0)
        else:
            for possible_answer_choice in answer_choices:
                answer_choices_dict[possible_answer_choice].append(0)

    for possible_answer_choice in answer_choices:
        response_df["Comms_update_" + possible_answer_choice] = answer_choices_dict[possible_answer_choice]
    
    response_df.drop(columns = ["Comms_update_composition"], inplace = True)

def drop_incomplete(response_df):
    """
    Drops responses that are incomplete. Columns that are okay to be not complete
    are not dropped

    Parameters
    ----------
    response_df : pd.DataFrame
        The data to which to drop the incomplete responses
    
    Returns
    -------
    None
    """
    before_size = len(response_df)
    dropping_copy = response_df.copy()
    dropping_copy.drop(columns = [
        "Testing_results_turnover",
        "Patient_Median_Income",
        "Patient_SES_Quartile",
        "SES",
        "General_satisfaction",
        "Exposure_COVID_positive_hx",
        "FR: If there is a policy in place, what details are you aware of?",
        "FR: What, if anything, could your school have done better to handle the pandemic? (Optional)",
        "FR: What, if anything, has your school done well in terms of the pandemic? (Optional)","Email", "Medschool"
        ], inplace = True)
    response_df.drop(response_df[dropping_copy.isna().any(axis=1)].index, inplace = True)
    after_size = len(response_df)
    print(before_size - after_size, " incompletes removed")

