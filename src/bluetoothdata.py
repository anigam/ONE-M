from settings import *
import pandas as pd
import networkx as nx

def makeNetwork(net, t, survey_df):
    g = nx.DiGraph()
    for ix, row in net.iterrows():
        u = row.SenderID
        v = row.ReceiverID
        w = row.weight
        
        g.add_edge(u, v, weight=w)
    
    ## set node attribute
    for _attr in attribute_field:
        for v in g.nodes():
            g.node[v][_attr]= survey_df[survey_df.egoid == v].iloc[0][_attr]
            
    for _field in beliefs:
        for v in g.nodes():
            g.node[v][_field]= survey_df[survey_df.egoid == v].iloc[0][_field+str(t)]
            
    return g

def loadBluetoothnetwork(bnet_dir, base_name, survey_df):
    bluetooth_time_graphs = dict()
    for t in survey_number:    
        fname = bnet_dir + base_name + str(t) + '.txt'
        df = pd.read_csv(fname,header=None)
        df.columns = ['SenderID', 'ReceiverID', 'weight']
        g = makeNetwork(df, t, survey_df)
        bluetooth_time_graphs[t] = g
        
    return bluetooth_time_graphs

def getBluetoothNetworks(survey_df):
    bluetooth_time_graphs = loadBluetoothnetwork(bnet_dir, base_name, survey_df)
    weekend_bluetooth_time_graphs = loadBluetoothnetwork(weekend_bnet_dir, weekend_base_name, survey_df)

    return bluetooth_time_graphs, weekend_bluetooth_time_graphs