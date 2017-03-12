
# coding: utf-8

# # ランダムウォークのシリーズを作成

# In[2]:

n = 1000
se = pd.Series(np.random.randint(-1, 2, n)).cumsum()
se.plot()


# ## 前日より値が低かったら買い、高かったら見過ごし

# In[14]:

position = np.zeros(len(se))  # seと同じ長さの配列を作成
for i in se.index[:-1]:
    if se[i+1] - se[i] > 0:
        position[i]=se[i]
position


# In[23]:

fig, ax = plt.subplots()
se.plot(ax=ax)
pd.DataFrame(position).cumsum().plot(ax=ax, secondary_y=True)  # ポジションのcum sumをプロット
plt.grid(True)


# 

# ## 特定期間で買い

# In[3]:

freq = 5 

