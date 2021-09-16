import os
from glob import glob
from matplotlib import pyplot as plt 
import numpy as np
import pandas as pd
from collections import Counter
from prettytable import PrettyTable
from scipy.stats import chi2_contingency
from scipy.stats import ranksums


def percentage(number, subset):
    if len(subset) > 0:
        proportion = round(float(number) / len(subset) * 100, 1)
        return str(proportion) + "%, (n=" + str(number) + ")"
    return "0% (n=0)"

def create_pie_chart(response_df, categorical_demographic_features, nhorizontal, nvertical, startangle, annotationLocation):
    for i, categorical_feature in enumerate(categorical_demographic_features):
        plt.subplot(nhorizontal,nvertical,i+1)
        subset = response_df[response_df[categorical_feature] == response_df[categorical_feature]]
        count = Counter(subset[categorical_feature])
        labels = [x for x in count]
        count_indiv = [count[x] for x in count]
        plt.pie(count_indiv, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=startangle, textprops = {'fontsize': 7})
        plt.annotate(categorical_feature, annotationLocation, weight = 'bold')
        plt.axis('equal')

def conditional_agree_disagree_table(response_df, categorical_features):
    print("Generating Conditional Tables...")
    agree_choices = ['Strongly agree', 'Somewhat agree', 'Extremely satisfied', 'Somewhat satisfied']
    disagree_choices = ['Strongly disagree', 'Somewhat disagree', 'Extremely dissatisfied', 'Somewhat dissatisfied']
    satisfied_choices = ['Extremely satisfied', 'Somewhat satisfied']
    dissatisfied_choices = ['Extremely dissatisfied', 'Somewhat dissatisfied']
    neither_choice = "Neither satisfied nor dissatisfied"
    
    independent_variables = categorical_features[:-1]
    dependent_variable = categorical_features[-1]
    
    for iv in independent_variables:
        agree_subset = response_df[response_df[iv].isin(agree_choices)]
        disagree_subset = response_df[response_df[iv].isin(disagree_choices)]
        
        given_agree_satisfied = np.sum(agree_subset[dependent_variable].isin(satisfied_choices))
        given_agree_dissatisfied = np.sum(agree_subset[dependent_variable].isin(dissatisfied_choices))
        given_agree_neither = np.sum(agree_subset[dependent_variable] == neither_choice)
        given_disagree_satisfied = np.sum(disagree_subset[dependent_variable].isin(satisfied_choices))
        given_disagree_dissatisfied = np.sum(disagree_subset[dependent_variable].isin(dissatisfied_choices))
        given_disagree_neither = np.sum(disagree_subset[dependent_variable] == neither_choice)
        
        df = pd.DataFrame(data = {iv: ["Agree", "Disagree"]})
        df["Satisfied"] = [percentage(given_agree_satisfied, agree_subset), percentage(given_disagree_satisfied, disagree_subset)]
        df["Dissatisfied"] = [percentage(given_agree_dissatisfied, agree_subset), percentage(given_disagree_dissatisfied, disagree_subset)]
        df["Neither"] = [percentage(given_agree_neither, agree_subset), percentage(given_disagree_neither, disagree_subset)]
        df["Total"] = [
            percentage(given_agree_satisfied + given_agree_dissatisfied + given_agree_neither, agree_subset),
            percentage(given_disagree_satisfied + given_disagree_dissatisfied + given_disagree_neither, disagree_subset)
                      ]
        display(df)
        
def create_conditional_matrix(response_df, categorical_features):
    print("Generating conditional tables...")
    independent_variables = categorical_features[:-1]
    dependent_variable = categorical_features[-1]
    satisfied_choices = ['Extremely satisfied', 'Somewhat satisfied']
    dissatisfied_choices = ['Extremely dissatisfied', 'Somewhat dissatisfied']
    neither_choice = "Neither satisfied nor dissatisfied"
    
    matrix_dict = dict()
    for iv in independent_variables:
        answer_choices = []
        for x in Counter(response_df[iv]).keys():
            if x==x:
                answer_choices.append(x)
        
        answer_choices = sorted(answer_choices)
        
        df = pd.DataFrame(data = {iv: answer_choices})
        stats = []
        for answer_choice in answer_choices:
            answer_true_subset = response_df[response_df[iv] == answer_choice]
            
            given_answer_satisfied = np.sum(answer_true_subset[dependent_variable].isin(satisfied_choices))
            given_answer_dissatisfied = np.sum(answer_true_subset[dependent_variable].isin(dissatisfied_choices))
            given_answer_neither = np.sum(answer_true_subset[dependent_variable] == neither_choice)
            
            stats.append([
                percentage(given_answer_satisfied, answer_true_subset),
                percentage(given_answer_dissatisfied, answer_true_subset),
                percentage(given_answer_neither, answer_true_subset),
                percentage(given_answer_satisfied + given_answer_dissatisfied + given_answer_neither, answer_true_subset)
            ])
            
        stats = np.array(stats)
        df["Satisfied"] = stats[:,0]
        df["Dissatisfied"] = stats[:,1]
        df["Neither"] = stats[:,2]
        df["Total"] = stats[:,3]
        display(df)

def highlight_significant_rows(value):
    color = 'abb2bf'
    if value == "<0.001":
        color = 'red'
    elif float(value) < 0.05:
        color = 'red'
    elif float(value) < 0.1:
        color = 'blue'
    else:
        color = 'gray'

    return 'color: %s' % color

def get_chi_square_table(response_df, header, independent_variables, dependent_variables):
    print(header)
    independent_column = []
    dependent_column = []
    p_values = []
    
    for dv in dependent_variables:
        for iv in independent_variables:
            satisfied_choices = ['Extremely satisfied', 'Somewhat satisfied']
            dissatisfied_choices = ['Extremely dissatisfied', 'Somewhat dissatisfied']
            agree_choices = ['Extremely agree', 'Somewhat agree']
            disagree_choices = ['Extremely disagree', 'Somewhat disagree']

            binary_satisfaction = []
            for x in response_df[dv]:
                if x in satisfied_choices:
                    binary_satisfaction.append("Satisfied")
                elif x in dissatisfied_choices:
                    binary_satisfaction.append("Dissatisfied")
                else:
                    binary_satisfaction.append(np.nan)
            response_df[dv+"_binary"] = binary_satisfaction

            subset = response_df[[iv, dv+"_binary"]].copy()
            subset.dropna(inplace = True)
            contigency = pd.crosstab(subset[iv], subset[dv+"_binary"])
            c, p, dof, expected = chi2_contingency(contigency, correction = False) 
            
            if p < 0.001:
                p = "<0.001"
            else:
                p = round(p, 3)
            independent_column.append(iv)
            dependent_column.append(dv+"_binary")
            p_values.append(p)

            #if the independent variable can be binary
            if any([x in satisfied_choices + dissatisfied_choices + agree_choices + disagree_choices for x in Counter(response_df[iv]).keys()]):
                binary_iv = []
                for x in response_df[iv]:
                    if x in satisfied_choices:
                        binary_iv.append("Satisfied")
                    elif x in dissatisfied_choices:
                        binary_iv.append("Dissatisfied")
                    elif x in agree_choices:
                        binary_iv.append("Agree")
                    elif x in disagree_choices:
                        binary_iv.append("Disagree")
                    else:
                        binary_iv.append(np.nan)
                response_df[iv + "_binary"] = binary_iv
                subset = response_df[[iv+"_binary", dv+"_binary"]].copy()
                subset.dropna(inplace = True)
                contigency = pd.crosstab(subset[iv+"_binary"], subset[dv+"_binary"])
                c, p, dof, expected = chi2_contingency(contigency) 
                independent_column.append(iv+"_binary")
                dependent_column.append(dv+"_binary")
                
                if p < 0.001:
                    p = "<0.001"
                else:
                    p = round(p, 3)
                p_values.append(p)

    df = pd.DataFrame(data = {
        "Independent Variable": independent_column,
        "Dependent Variable": dependent_column,
        "P_Values": p_values
    })
    display(df.style.applymap(highlight_significant_rows, subset = ["P_Values"]).set_precision(3))

def get_ranksums(response_df, name, independent_variables, dependent_variables):
    print(name)
    independent_column = []
    dependent_column = []
    p_values = []
    
    for dv in dependent_variables:
        for iv in independent_variables:
            sample1 = response_df[response_df[dv] == "Satisfied"][iv]
            sample2 = response_df[response_df[dv] == "Dissatisfied"][iv]
            
            independent_column.append(iv)
            dependent_column.append(dv)
            p = ranksums(sample1, sample2)[1]
            if p < 0.001:
                p = "<0.001"
            else:
                p = round(p, 3)
            p_values.append(p)
    
    ranksum_df = pd.DataFrame(data = {
        "Independent Variable": independent_column,
        "Dependent Variable": dependent_column,
        "P_Values": p_values
    }
    )
    display(ranksum_df.style.applymap(highlight_significant_rows, subset = ["P_Values"]).set_precision(3))

def make_vaccine_groups(response_df):
    vacc_faster_than_gen_pop = []
    for x in response_df["Comms_vaccine"]:
        if x == 'I have already received the vaccine' or x == 'I will receive the vaccine by the school earlier than the general population':
            vacc_faster_than_gen_pop.append(1)
        else:
            vacc_faster_than_gen_pop.append(0)

    vaccinated = []
    for x in response_df["Comms_vaccine"]:
        if x == 'I have already received the vaccine':
            vaccinated.append(1)
        else:
            vaccinated.append(0)

    vaccinated_faster_else = []
    for x in response_df["Comms_vaccine"]:
        if x == 'I have already received the vaccine':
            vaccinated_faster_else.append('I have already received the vaccine')
        elif x == 'I will receive the vaccine by the school earlier than the general population':
            vaccinated_faster_else.append('I will receive the vaccine by the school earlier than the general population')
        else:
            vaccinated_faster_else.append("Else")

    response_df["vacc_faster_than_gen_pop"] = vacc_faster_than_gen_pop
    response_df["vaccinated"] = vaccinated
    response_df['vaccinated_faster_else'] = vaccinated_faster_else

def count_important_messages_comms(response_df):
    number_important = []
    for i, response in response_df.iterrows():
        num = response["Comms_update_Supportive messages"] + response["Comms_update_Number of COVID-19 cases in your school"] + response["Comms_update_Status on PPE inventory/availability"]
        number_important.append(num)
    response_df["Comms_nImportant_Messages"] = number_important

def group_unsure_and_no_responses_testing(response_df):
    m1_2_tested_group = []
    for response in response_df["M1_2_tested"]:
        if response == "Yes":
            m1_2_tested_group.append("Yes")
        else:
            m1_2_tested_group.append("No/Unsure")
    response_df["M1_2_tested_grouped"] = m1_2_tested_group

    testing_symptoms_required_group = []
    for response in response_df["Testing_symptoms_required"]:
        if response == "Yes":
            testing_symptoms_required_group.append("Yes")
        else:
            testing_symptoms_required_group.append("No/Unsure")
    response_df["testing_symptoms_required_group"] = testing_symptoms_required_group

    testing_symptoms_required_invgroup = []
    for response in response_df["Testing_symptoms_required"]:
        if response == "No":
            testing_symptoms_required_invgroup.append("No")
        else:
            testing_symptoms_required_invgroup.append("Yes/Unsure")
    response_df["test_symptom_req_invgroup"] = testing_symptoms_required_invgroup

    testing_access_if_wanted_group = []
    for response in response_df["Testing_access_if_wanted"]:
        if response == "Yes":
            testing_access_if_wanted_group.append("Yes")
        else:
            testing_access_if_wanted_group.append("No/Unsure")
    response_df["testing_access_if_wanted_group"] = testing_access_if_wanted_group

def group_unsure_and_no_responses_exposure(response_df):
    exposure_quarantine_policy_grouped = []
    for response in response_df["Exposure_quarantine_policy"]:
        if response == "Yes":
                exposure_quarantine_policy_grouped.append("Yes")
        else:
            exposure_quarantine_policy_grouped.append("No/Unsure")
    response_df["exposure_quarantine_policy_grouped"] = exposure_quarantine_policy_grouped

    exposure_quarantine_policy_grouped = []
    for response in response_df["Exposure_quarantine_policy"]:
        if response == "No":
                exposure_quarantine_policy_grouped.append("No")
        else:
            exposure_quarantine_policy_grouped.append("Yes/Unsure")
    response_df["expos_quaran_policy_invgroup"] = exposure_quarantine_policy_grouped

    exposure_covid_pt_binary = []
    for response in response_df["Exposure_COVID_pt_freq"]:
        if response == "Weekly" or response == "Daily":
            exposure_covid_pt_binary.append("Weekly or More Frequently")
        else:
            exposure_covid_pt_binary.append("Less than Weekly")
    response_df["exposure_covid_pt_freq_bin"] = exposure_covid_pt_binary

def group_comms_update_freq(response_df):
    weekly_else = []
    for x in response_df["Comms_update_freq"]:
        if x == "Weekly":
            weekly_else.append("Weekly")
        else:
            weekly_else.append("Else")
    response_df["Comms_update_freq_weekly"] = weekly_else

    monthly_or_freq_else = []
    for x in response_df["Comms_update_freq"]:
        if x == "Weekly" or x == "Monthly":
            monthly_or_freq_else.append("Monthly or more freq")
        else:
            monthly_or_freq_else.append("Else")
    response_df["Comms_update_freq_monthly"] = monthly_or_freq_else

    monthly_less_else_freq = []
    for x in response_df["Comms_update_freq"]:
        if x == "Weekly" or x == "Monthly":
            monthly_less_else_freq.append("Monthly or more freq")
        elif x == "Less than monthly":
            monthly_less_else_freq.append("Less than monthly")
        else:
            monthly_less_else_freq.append("Never")
    response_df["Comms_update_freq_mle"] = monthly_less_else_freq