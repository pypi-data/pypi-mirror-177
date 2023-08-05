#!/usr/bin/env python
# coding: utf-8

# In[14]:


# import libraries
import pandas as pd
import string
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import random
import warnings
import networkx as nx
from cdlib import algorithms
warnings.filterwarnings('ignore')

def random_comention_df():
    '''
    Creating a dataframe containing an article column and a firm list column
    return dataframe
    '''
    articles = list(range(100))
    firms = list(string.ascii_lowercase)
    df = pd.DataFrame([[article,random.choices(firms,k=random.randint(2,10))] for article in articles],columns=['article','firms'])
    return df

def comention_similarity(df):
    '''
    Calculate the co-mention similarity between firms in the list
    df: dataframe, a dataframe with two columns (an article column and a firm list column)
    return dataframe, dataframe with three columns (firm1, firm2 and similarity score)
    '''

    # converting the co-mention dataframe into a feature matrix: rows are firms and columns are articles
    feature_df = pd.get_dummies(df['firms'].apply(pd.Series).stack()).sum(level=0).transpose()
    feature_sparse_df = sparse.csr_matrix(feature_df)

    # calculate the cosine similarity based on the feature matrix
    simi_vec = cosine_similarity(feature_sparse_df)
    simi_vec = pd.DataFrame(index=feature_df.index,columns=feature_df.index,data=simi_vec)
    simi_vec = pd.DataFrame(simi_vec.unstack())

    # convert the format of the similarity matrix
    simi_vec = simi_vec.reset_index(0).rename(columns={'level_0':'level_1'}).reset_index()
    simi_vec.columns = ['firm1','firm2','similarity']
    simi_vec = simi_vec[simi_vec['similarity']!=0].reset_index(drop=True)
    simi_vec = simi_vec[simi_vec['firm1']!=simi_vec['firm2']]
    return simi_vec

def community_detection(df):
    '''
    Categorizing the firms based on their co-mention-based similarity by using community detection
    df: dataframe, a dataframe with three columns (firm1, firm2 and similarity score)
    return dataframe, dataframe with two columns (firm and group label)
    '''

    G = nx.from_pandas_edgelist(df,'firm1','firm2','similarity')

    #get the optimal partrition solution by Surpise
    coms = algorithms.surprise_communities(G,weights='similarity')

    #label firms according to the group solution and generate a dataframe containing the info
    group_df = pd.DataFrame({'firm':coms.communities,'group':range(len(coms.communities))})
    group_df = group_df.explode('firm')
    return group_df


# In[ ]:




