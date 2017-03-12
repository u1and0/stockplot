
# coding: utf-8

# # ランダムウォークのシリーズを作成

# In[1]:

n = 1000
se = pd.Series(np.random.randint(-1, 2, n)).cumsum()
se.plot()


# ## 特定期間で買い

# In[3]:

freq = 5 


# ## 前日より値が低かったら買い、高かったら見過ごし

# In[7]:

position = np.zeros(len(se))  # seと同じ長さの配列を作成
for i in se.index:
    try: 
        if se[i+1] - se[i] > 0:
            position[i]=1
    except:
        
position


# In[ ]:



