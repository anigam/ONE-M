from __future__ import division
from settings import *
import math
from scipy import spatial

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
        if w > 0:
            w = 1
        else:
            w = 0
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
      
def timePredisposition(g, i, belief_field):
    if g.has_node(i) == False:
        return 0
    cur_belief = g.node[i][belief_field]
    return cur_belief

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
        
        attr_pro = (len(intersection)+add_smooth)/(len(denominator)+add_smooth)
        f *= attr_pro
    f = f*(len(denominator)/(g.number_of_nodes()-1))
    return f


def getPopulationBias(g, i, belief_field):
    if g.has_node(i) == False:
        return 0
    #Population bias: sum aj
    N = g.number_of_nodes()
    f = 0
    for j in g.nodes():
        if j == i:
            continue
        aj = g.node[j][belief_field]
        f += aj
    f = f/(N-1)
    return f

def getReciprocalBias(g, i, belief_field):
    if g.has_node(i) == False:
        return 0

    #Reciprocal: gij*gji*aj
    f = 0
    weight_sum = 0
    for j in g[i]:    #for only the valid gij links
        if g.has_edge(j,i): ## compute only for people who respond back 
            aj = g.node[j][belief_field]
            wij = g[i][j]['weight']
            wji = g[j][i]['weight']
            
            m_wij = getWeight(wij, weight_type)
            m_wji = getWeight(wji, weight_type)
            weight = getCompoundWeight([m_wij, m_wji], triad_type) #m_wij + m_wji
            #print wij,wji, m_wij, m_wji,weight
            weight_sum +=weight
            f += weight * aj
    if f > 0:
        f = f/weight_sum    
        return f
    return f

def getAttributeSim(g, i, j):
    if((g.has_node(i) == False) or (g.has_node(j) == False)):
        return 0
    
    Xi = list()
    Xj = list()
    for x in attribute_field:
        Xi.append(g.node[i][x])
        Xj.append(g.node[j][x])
    
#    f = getSimilarity(Xi, Xj)
    f = 1 - spatial.distance.cosine(Xi, Xj)
    return f

def getTriadWeights(g, i, j):
    if((g.has_node(i) == False) or (g.has_node(j) == False)):
        return 0
    #compound weight of triads
    f = 0
    
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

def getbeliefSimilarity(g, i, j):
    if g.has_node(i) == False or g.has_node(j) == False:
        return 0
    Ai = list()
    Aj = list()
    
    for belief_field in beliefs:
        Ai.append(g.node[i][belief_field])
        Aj.append(g.node[j][belief_field])
    f = 1 - spatial.distance.cosine(Ai, Aj)
    return f

def social_tie_persistence(g, i, j):
    if g.has_edge(i, j):
        f1 = getWeight(g[i][j]['weight'], weight_type)
    else:
        f1 = getWeight(0, weight_type)
        
    if g.has_edge(j, i):
        f2 = getWeight(g[j][i]['weight'], weight_type)
    else:
        f2 = getWeight(0, weight_type)

    f = [f1, f2]
    return f
