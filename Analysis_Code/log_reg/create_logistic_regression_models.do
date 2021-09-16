do "/absolute/path/to/determining_cat_cont.do"

set cformat %9.3f

***************************************************************************************
*PPE Satisfaction
logit ppe_satisfaction_binary_en ppe_accessibility_en ppe_training_en, nolog or
cvauroc ppe_satisfaction_binary_en ppe_accessibility_en ppe_training_en

***************************************************************************************
*Testing Satisfaction 
*includes non-signifcant testing results turnover 
logit testing_satisfaction_binary_en testing_freq_en i.m1_2_tested_grouped_en i.test_symptom_req_invgroup_en i.test_access_ifwanted_group_en testing_results_turnover_en, nolog or

*final model
logit testing_satisfaction_binary_en testing_freq_en i.m1_2_tested_grouped_en i.test_symptom_req_invgroup_en i.test_access_ifwanted_group_en, nolog or
cvauroc testing_satisfaction_binary_en testing_freq_en m1_2_tested_grouped_en test_symptom_req_invgroup_en test_access_ifwanted_group_en

***************************************************************************************
*Comms Satisfaction
*important messages
logit comms_satisfaction_binary_en comms_update_supportivemessages comms_update_informationontestin comms_update_numberofcovid19case comms_update_covid19protocolchan comms_update_statusonppeinventor, nolog or
lroc, nograph

*includes non-significant comms update frequency
logit comms_satisfaction_binary_en i.comms_mental_health_en i.comms_update_freq_en comms_nimportant_messages, nolog or
test 1.comms_update_freq_en 2.comms_update_freq_en 3.comms_update_freq_en

*final model
logit comms_satisfaction_binary_en i.comms_mental_health_en comms_nimportant_messages, nolog or
cvauroc comms_satisfaction_binary_en comms_mental_health_en comms_nimportant_messages

***************************************************************************************
*Exposure Satisfaction
*includes non significant covid hx
logit exposure_satisfaction_binary_en exp_quar_policy_grp_en exposure_sharing_comfort_en exp_covid_pt_freq_never_week_m exposure_discomfort_en exposure_covid_positive_hx_en, nolog or

*final model
logit exposure_satisfaction_binary_en exp_quar_policy_grp_en exposure_sharing_comfort_en exp_covid_pt_freq_never_week_m exposure_discomfort_en, nolog or
cvauroc exposure_satisfaction_binary_en exp_quar_policy_grp_en exposure_sharing_comfort_en exp_covid_pt_freq_never_week_m exposure_discomfort_en

***************************************************************************************
*General satisfaction
*final model
logit general_satisfaction_binary_en ppe_satisfaction_binary_en testing_satisfaction_binary_en comms_satisfaction_binary_en exposure_satisfaction_binary_en, nolog or
cvauroc general_satisfaction_binary_en ppe_satisfaction_binary_en testing_satisfaction_binary_en comms_satisfaction_binary_en exposure_satisfaction_binary_en

*adjusted model
logit general_satisfaction_binary_en ppe_satisfaction_binary_en testing_satisfaction_binary_en comms_satisfaction_binary_en exposure_satisfaction_binary_en i.year_en i.gender_simplified_en i.region_en i.vaccine_simplified_en medschool_size, nolog or
firthlogit general_satisfaction_binary_en ppe_satisfaction_binary_en testing_satisfaction_binary_en comms_satisfaction_binary_en exposure_satisfaction_binary_en i.year_en i.gender_simplified_en i.region_en i.vaccine_simplified_en medschool_size, nolog or
test 2.year_en 3.year_en
test 2.region 3.region 4.region 

