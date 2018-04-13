from __future__ import division
from settings import *
import math

def getSimilarity(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    assert len(s1) == len(s2)
    sim = sum(c1 == c2 for c1, c2 in zip(s1, s2))
    return sim/len(s1)

def getWeight(w, options = 'log'):
    if options == 'log':
        w = math.log(w+1)
    elif options == 'linear':
        w = w
    elif options == 'binary':
        w = 1
    return w
    
def getCompoundWeight(weights, options = 'sum'):
    if options == 'sum':
        compound_weight = 0
        for w in weights:
            compound_weight += w
    elif options == 'product':
        compound_weight = 1
        for w in weights:
            compound_weight *= w
    return compound_weight
      
def timePredisposition(prev_g, t, i, belief_field):
    if prev_g.has_node(i) == False:
        return 0

#    prev_g = time_graphs[t-1]
    prev_belief = prev_g.node[i][belief_field]
    return prev_belief

def populationPredisposition(g, i, belief_field):
    if g.has_node(i) == False:
        return 0
    ai = g.node[i][belief_field]
    add_smooth = 1
    f = 1
    for attr in attribute_field:
        xi = g.node[i][attr]
        intersection = [x for x,y in g.nodes(data=True) if y[attr] == xi and y[belief_field]==ai]
        denominator = [x for x,y in g.nodes(data=True) if y[belief_field]==ai]
        
        if i in intersection:
            intersection.remove(i)
        if i in denominator:
            denominator.remove(i)
        
        #attr_pro = (len(intersection)+add_smooth)/(len(denominator)+len(attribute_field)+add_smooth)
        attr_pro = (len(intersection)+add_smooth)/(len(denominator)+add_smooth)
        f *= attr_pro
        #print f
    f = f*(len(denominator)/(g.number_of_nodes()-1))
    #print f
#    f = ai * f
    #print f
    return f
      

def getPopulationBias(g, i, belief_field):
    if g.has_node(i) == False:
        return 0
    #Population bias: sum aj
    ai = g.node[i][belief_field]
    f = 0
    for j in g.nodes():
        if j == i:
            continue
        aj = g.node[j][belief_field]
        f += aj
    f = ai*f
    return f

def getReciprocalBias(g, i, belief_field):
    if g.has_node(i) == False:
        return 0
    ai = g.node[i][belief_field]
    #Reciprocal: gij*gji*aj
    f = 0
    for j in g[i]:    #for only the valid gij links
        wij = g[i][j]['weight']
        if g.has_edge(j,i):
            aj = g.node[j][belief_field]
            wji = g[j][i]['weight']
            
            m_wij = getWeight(wij, weight_type)
            m_wji = getWeight(wji, weight_type)
            weight = getCompoundWeight([m_wij, m_wji], triad_type)
            #print wij,wji, m_wij, m_wji,weight
            
            f += weight * aj
    f = ai * f    
    return f

def getAttributeSim(g,i):
    if g.has_node(i) == False:
        return 0
    f = 0
    for j in g[i]:
        X_i = list()
        X_j = list()
        for x in attribute_field:
            xi = g.node[i][x]
            xj = g.node[j][x]
            X_i.append(xi)
            X_j.append(xj)
        
        sim = getSimilarity(X_i, X_j)
        wij = g[i][j]['weight']
        m_wij = getWeight(wij, weight_type)
        
        f += m_wij * sim
    return f
    
def getReciprocalWeight(g,i):
    if g.has_node(i) == False:
        return 0
    #compound weight of reciprocal links
    f = 0
    for j in g[i]:
        wij = g[i][j]['weight']
        if g.has_edge(j,i):
            wji = g[j][i]['weight']
      
            m_wij = getWeight(wij, weight_type)
            m_wji = getWeight(wji, weight_type)
            weight = getCompoundWeight([m_wij, m_wji], triad_type)
            f += weight
    return f

def getTriadWeights(g,i):
    if g.has_node(i) == False:
        return 0
    #compound weight of triads
    f = 0
    for j in g[i]: #gij
        for k in g[j]: 
            if g.has_edge(i,j) and g.has_edge(j,k) and g.has_edge(k,i):
                if i!=j and j!=k and k!=i:
                    wij = g[i][j]['weight']
                    wjk = g[j][k]['weight']
                    wki = g[k][i]['weight']
                
                    m_wij = getWeight(wij, weight_type)
                    m_wjk = getWeight(wjk, weight_type)
                    m_wki = getWeight(wki, weight_type)
                
                    weight = getCompoundWeight([m_wij,m_wjk,m_wki], triad_type)
                    f += weight
    return f