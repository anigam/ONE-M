from settings import *
import networkx as nx
import datetime

## make network from the communication network
def makeNetwork(time_graphs, t, net):
    g = time_graphs[t]
    for ix, row in net.iterrows():
        u = row.SenderID
        v = row.ReceiverID
        #etype = row.EventType
        if g.has_edge(u,v):
            g[u][v]['weight'] +=1
            #g[u][v]['ctype'] = etype
        else:
            g.add_edge(u, v, weight=1)
            #g.add_edge(u, v, weight=1, ctype=etype)
    time_graphs[t] = g
    return time_graphs

    
## Split the network based on the start and end dates
def cutNetwork(sms_call_df, start_date, end_date):
    dt1 = datetime.datetime(year=start_date.year, month=start_date.month, day = 1)
    dt2 = datetime.datetime(year=end_date.year, month=end_date.month, day = 1)
    print "Range: >=",dt1, "and <", dt2
    network = sms_call_df[(sms_call_df.DateTime >= dt1) & (sms_call_df.DateTime < dt2)]
    return network

def buildNetwork(survey_df, sms_call_df):
    ## initialize network
    time_graphs = dict()
    for _number in survey_number:
        g = nx.DiGraph()
        time_graphs[_number] = g
    
    network_cuts = list()
    ## Cut and make network
    for _number in survey_number:
        ix = _number - 1 
        print "Study period:", _number
        #cur_d = date_cols[ix]
        cur_d = time_field + str(_number)
        start_date = survey_df[cur_d].dropna(axis=0, how='all').min()
        if ix == len(survey_number)-1:
            end_date = datetime.datetime(year=2013, month=8, day = 31)
            print "Making network from:", start_date, "to", end_date
            net = cutNetwork(sms_call_df, start_date, end_date)
            network_cuts.append(net)
            time_graphs = makeNetwork(time_graphs, _number, net)
            print "Size of network:", len(net)
            continue
        
        #next_d = date_cols[ix+1]
        next_d = time_field + str(_number + 1)
        start_date = survey_df[cur_d].dropna(axis=0, how='all').min()
        end_date = survey_df[next_d].dropna(axis=0, how='all').min()
        if ix == 0:
            start_date =  sms_call_df.DateTime.min()
        print "Making network from:", start_date, "to", end_date
        net = cutNetwork(sms_call_df, start_date, end_date)
        network_cuts.append(net)
        time_graphs = makeNetwork(time_graphs, _number, net)
        print "Number of interactions:", len(net)
        print ''
    
    ## set node attribute
    for _attr in attribute_field:
        for _number in survey_number:
            g = time_graphs[_number]
            for v in g.nodes():
                g.node[v][_attr]= survey_df[survey_df.egoid == v].iloc[0][_attr]
            time_graphs[_number] = g
        
    for _field in beliefs:
        for _number in survey_number:
            g = time_graphs[_number]
            for v in g.nodes():
                g.node[v][_field]= survey_df[survey_df.egoid == v].iloc[0][_field+str(_number)]
            time_graphs[_number] = g
    
    return time_graphs