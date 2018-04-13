# settings.py

datapath = "../../data/"
figure_folder = "/Users/aastha/Google Drive File Stream/My Drive/Projects/cmu/nd-netsense/src/all_beliefs/figures/"

survey_file = 'survey-data.csv'
communication_file = 'sms-call-data-eventtype.csv'

bnet_dir = '/Users/aastha/Google Drive File Stream/My Drive/Projects/cmu/nd-netsense/src/all_beliefs/bluetooth-data/Wholenetworks/'
base_name = 'BTnet'

weekend_bnet_dir = "/Users/aastha/Google Drive File Stream/My Drive/Projects/cmu/nd-netsense/src/all_beliefs/bluetooth-data/Weekendnetworks/"
weekend_base_name = 'BTWeekEndnet'

id_field = ['egoid']
attribute_field = ['age_1','hometown_1','ethnicity_1','gender_1']
base_field = id_field + attribute_field
time_field = 'completed_'
beliefs = ['premaritalsex_', 'euthanasia_', 'deathpen_', 'gaymarriage_', 'marijuana_', 'political_', 'abortion_', 'homosexual_']
survey_number = list(range(1, 7))

belief_cols = list()
for _belief in beliefs:
    for _number in survey_number:
        belief_cols.append(_belief+str(_number))

#belief_field = 'marijuana_'

weight_type = 'log'
triad_type = 'sum'