
# coding: utf-8

# In[2]:

import cufflinks as cf


# In[6]:

# オフラインモード、白基調のテーマ、リンク表示OFFをデフォルト設定に
cf.set_config_file(offline=True, theme="white", offline_show_link=False)


# オフラインモードは一度打てば今後は打たなくても良い

# In[7]:

df = pd.DataFrame(np.random.randn(10, 2), columns=["col1", "col2"])
import cufflinks as cf
df.iplot()


# In[ ]:



