import pandas as pd

from settings import *
from mappings import *
from datanetwork import *

def processData():
    #load communication data
    print "Loading communication data..."
    sms_call_df = pd.read_csv(datapath + communication_file)
    print "Fixing data format..."
    sms_call_df.DateTime =  pd.to_datetime(sms_call_df.DateTime, format='%Y-%m-%d %H:%M:%S',errors='ignore')
    print "Shape of sms-call data:", sms_call_df.shape
    
    print "Dropping instances where sender and receiver match..."
    sms_call_df = sms_call_df[sms_call_df.SenderID != sms_call_df.ReceiverID]
    print "Shape of sms-call data:", sms_call_df.shape
    
    print sms_call_df.head()
    
    #load survey data
    print ''
    print "Loading survey data..."
    all_survey_df = pd.read_csv(datapath + survey_file)
    print "Fixing data format..."
    for i in survey_number:
        _cname = 'completed_'+str(i)
        if i ==1:
            all_survey_df.loc[:,_cname] =  pd.to_datetime(all_survey_df.loc[:,_cname], format='%m/%d/%Y %H:%M',errors='coerce')
        else:
            all_survey_df.loc[:,_cname] =  pd.to_datetime(all_survey_df.loc[:,_cname], format='%Y-%m-%d %H:%M:%S',errors='coerce')

    print "Shape of survey dataframe", all_survey_df.shape        
#    print "All survey columns:", all_survey_df.columns
    print all_survey_df.head()
    
    ## preprocessing
    print ''
    print "Beginning preprocessing..."
    print "Number of users who participated in the survey:", all_survey_df.shape[0]

    survey_df = all_survey_df.dropna(subset=belief_cols, how='any', inplace=False)
    print "Number of users who answered all surveys for all beliefs:", survey_df.shape[0]
    
    print "Mapping categorical data to numerical data..."
    # Encode the beliefs
    survey_df = mapData(survey_df)
    
    #Encode the user attributes
    survey_df = exo_attr_mapping(survey_df)
    
    # Select communication data only amongst users for whom survey data is available
    selected_users = list(survey_df.egoid.unique())
   
    print ''
    print "Extracting corresponding communication network..."
    sms_call_df = sms_call_df[sms_call_df.SenderID.isin(selected_users) & sms_call_df.ReceiverID.isin(selected_users)]
    print "Number of interactions amongst selected users:", sms_call_df.shape[0]
    print "Interactions date range:", sms_call_df.DateTime.min(),"-", sms_call_df.DateTime.max()
    
    print ''
    print "Building network..."
    time_graphs = buildNetwork(survey_df, sms_call_df)
    
    return survey_df, sms_call_df, time_graphs
