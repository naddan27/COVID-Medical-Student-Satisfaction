display("LR tests")
display("Features to Agree or Disagree")

**************
do "/absolute/path/to/determining_cat_cont.do"

*Treat variable as continuous
display("PPE Accessibility")
logit ppe_satisfaction_binary_en c.ppe_accessibility_en, nolog
est store m1

*Treat variable as categorical
logit ppe_satisfaction_binary_en i.ppe_accessibility_en, nolog 
est store m2

*now do LR/ BIC/ AIC tests
lrtest m1 m2, stats

**************
display("PPE Training")
logit ppe_satisfaction_binary_en c.ppe_training_en, nolog
est store m1
logit ppe_satisfaction_binary_en i.ppe_training_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Comms Mental Health")
logit comms_satisfaction_binary_en i.comms_mental_health_en, nolog 
est store m2
logit comms_satisfaction_binary_en c.comms_mental_health_en, nolog
est store m1
lrtest m1 m2, stats

**************
display("Exposure Discomfort")
logit exposure_satisfaction_binary_en c.exposure_discomfort_en, nolog
est store m1
logit exposure_satisfaction_binary_en i.exposure_discomfort_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Exposure Sharing Comfort")
logit exposure_satisfaction_binary_en c.exposure_sharing_comfort_en, nolog
est store m1
logit exposure_satisfaction_binary_en i.exposure_sharing_comfort_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Time features")
display("Exposure COVID")
logit exposure_satisfaction_binary_en c.exposure_covid_en, nolog
est store m1
logit exposure_satisfaction_binary_en i.exposure_covid_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Testing Freq")
logit testing_satisfaction_binary_en c.testing_freq_en, nolog
est store m1
logit testing_satisfaction_binary_en i.testing_freq_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Comms Update Freq")
logit comms_satisfaction_binary_en c.comms_update_freq_en, nolog
est store m1
logit comms_satisfaction_binary_en i.comms_update_freq_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Satisfaction Features")
display("PPE Satisfaction")
logit general_satisfaction_binary_en c.ppe_satisfaction_en, nolog
est store m1
logit general_satisfaction_binary_en i.ppe_satisfaction_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Comms Satisfaction")
drop if comms_satisfaction_en == 5
logit general_satisfaction_binary_en c.comms_satisfaction_en, nolog
est store m1
logit general_satisfaction_binary_en i.comms_satisfaction_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Testing Satisfaction")
logit general_satisfaction_binary_en c.testing_satisfaction_en, nolog
est store m1
logit general_satisfaction_binary_en i.testing_satisfaction_en, nolog 
est store m2
lrtest m1 m2, stats

**************
display("Exposure Satisfaction")
drop if exposure_satisfaction_en == 1
logit general_satisfaction_binary_en c.exposure_satisfaction_en, nolog
est store m1
logit general_satisfaction_binary_en i.exposure_satisfaction_en, nolog 
est store m2
lrtest m1 m2, stats