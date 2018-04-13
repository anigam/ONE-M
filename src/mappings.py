##mappings.py
from settings import *
from collections import Counter

##Codings
political_coding = {"Slightly conservative":1, 
                    "Extremely conservative":1, 
                    "Conservative":1, 
                    "Moderate":2, 
                    "Not sure":2, 
                    "Slightly liberal":3, 
                    "Liberal":3, 
                    "Extremely liberal":3}

abortion_coding = {'By law, abortion should never be permitted': 1,
       "Law should permit only in rape, incest, or woman's life in danger": 1,
       'Not sure':2,
       'Law should permited in other cases, but only after need is established': 3,
       'By law, should always be able to obtain abortion': 3}

deathpen_coding = {'Oppose':1,
                   'Not sure':2,
                   'Favor':3}

homosexual_coding = {'Always wrong':1, 
                     'Almost always wrong' :1,
                     'Not sure':2,
                     'Sometimes wrong':3,
                    'Not wrong at all':3}

gaymarriage_coding = {'Strongly disagree':1, 
                      'Disagree':1, 
                      'Neither agree nor disagree':2, 
                      'Not Sure':2, 
                      'Agree': 3,
                      'Strongly agree':3}

premaritalsex_coding = {'Always wrong':1, 
                     'Almost always wrong' :1,
                     'Not sure':2,
                     'Sometimes wrong':3,
                    'Not wrong at all':3}

euthanasia_coding = {'No':1, 
                     'Not sure':2,
                     'Yes':3}

marijuana_coding = {'Not Legal':1, 
                    'Not Sure':2,
                    'Legal':3}

coding = {'political_':political_coding,
         'marijuana_':marijuana_coding,
         'abortion_': abortion_coding,
          'deathpen_':deathpen_coding,
          'homosexual_': homosexual_coding,
          'gaymarriage_': gaymarriage_coding,
          'premaritalsex_': premaritalsex_coding,
          'euthanasia_': euthanasia_coding
         }

attr_mapping = {"age_1":     {17.0: 1, 18.0: 1, 19: 2},
                "hometown_1": {6.0: 1, 5.0: 2, 4.0: 3, 1.0: 3, 0.0:1},
               "ethnicity_1": {'White/Caucasian': 1, 'Asian American/Asian': 2, 'African American/Black': 3, 
                    'Mexican American/Chicano': 4, 'Other Latino': 4, 'Other': 4, 'American Indian/Alaska Native': 4},
               "gender_1":{'Male': 1, 'Female': 2}}


## Encode beliefs
def mapData(survey_df):
    print "map" 
    mapping = dict()
    for _number in survey_number:
        for _field in beliefs:
            _cname = _field+str(_number)
            _mapping = _field+"coding"
            mapping[_cname] = coding[_field]
    print "after this"
    survey_df.replace(mapping,inplace=True)
    return survey_df

#Encode user attributes
def exo_attr_mapping(survey_df):  
    print "Before:"
#    ## encode for the exogenous attributes
#    for attr in attribute_field:
#        print attr, Counter(survey_df[attr])

    for attr in attribute_field:
        #survey_df.loc[:,attr] = survey_df[attr].fillna(0)
        survey_df[attr].fillna(0,inplace=True)
        survey_df.loc[:,attr] = survey_df.loc[:,attr].map(attr_mapping[attr])

#    print "After:"
#    for attr in attribute_field:
#        print attr, Counter(survey_df[attr])
    return survey_df