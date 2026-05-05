#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid')

# In[ ]:


df=pd.read_csv('data/global_ai_jobs.csv')
df.info()


# In[9]:


df.drop('id',axis=1,inplace=True)


# In[10]:


# Missing Values check
missing_values=df.isnull().sum()
if missing_values.sum() > 0:
   print(missing_values[missing_values>0])
else:
   print('No missing values')


# In[ ]:


# Categorical cols
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
print(f'Categorical Columns:\n{categorical_cols}')


# In[ ]:
# top 5 category in each col
# top 5 category in each col
for col in categorical_cols:
    print(f'-----TOP 5 category in {col}------\n')
    print(df[col].value_counts().head(5))
    print('='*60)
    print('\n')


# ### **Insights**
# * **Uniform Distribution**
# * **No class impalance**
# 
# 
# 
# 
# 

# In[ ]:


numerical_cols=df.select_dtypes(include=['int','float']).columns.tolist()
print(f'Numerical Columns:\n{numerical_cols}')


# In[ ]:


#visualization of the target variable
fig,axis=plt.subplots(1,2,figsize=(15,5))
sns.histplot(df['salary_usd'],color='skyblue',bins=40,ax=axis[0],kde=True)
order=['Entry','Mid','Senior','Lead']
sns.boxplot(x='experience_level',y='salary_usd',data=df,order=order,ax=axis[1],palette='Set2')
plt.show()



# **Right skewed in salary**

# In[ ]:


job_usd=df.groupby('job_role').agg({'salary_usd':'mean'}).sort_values('salary_usd', ascending=True)
def job_role_usd(job_usd):
   plt.style.use('dark_background')
   fig=plt.figure(figsize=(8,6))
   plt.barh(job_usd.index,job_usd.salary_usd,color='magenta')
   plt.xlabel('Salary in USD')
   plt.ylabel('Job Role')
   plt.title('Average Salary by job_role')
   plt.grid(alpha=0.3)
   plt.tight_layout()
   plt.show()
   return fig


# In[ ]:


industries=df['industry'].value_counts().sort_values(ascending=True)
plt.figure(figsize=(8,6))
plt.barh(industries.index,industries.values)
plt.xlabel('Number of Jobs')
plt.ylabel('Industry')
plt.title('Number of AI Jobs by Industry')


# In[ ]:


jobs=df.groupby('year').agg({'job_openings':'sum'}).sort_values('year',ascending=True)
plt.figure(figsize=(8,6))
plt.plot(jobs.index,jobs.job_openings)
plt.title('Number of AI Jobs Around The World Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Jobs')


# In[ ]:


LayoffRisk=df.groupby('year').agg({'layoff_risk':'mean'}).sort_values('year',ascending=True)
plt.figure(figsize=(8,6))
plt.plot(LayoffRisk.index,LayoffRisk.layoff_risk)
plt.xlabel('Year')
plt.ylabel('Layoff Risk')
plt.title('Layoff Risk Over Time')


# In[ ]:


countries=df.groupby('country').agg({'salary_usd':'mean'}).sort_values('salary_usd',ascending=False)
plt.figure(figsize=(10,6))
plt.bar(countries.index,countries.salary_usd)
plt.xlabel('countries')
plt.ylabel('Salary in USD')
plt.xticks(rotation=45)
plt.title('Average Annual Salary by Country')


# In[ ]:


cuntries_jobs=df.groupby('country').agg({'job_openings':'sum'}).sort_values('job_openings').head(10)
plt.figure(figsize=(10,6))
plt.barh(cuntries_jobs.index,cuntries_jobs.job_openings)
plt.xlabel('Countries')
plt.ylabel('Number of Jobs')
plt.title('Leading Countries in AI Job Hiring (Top 10)')


# # Data Preprocessing

# ## Normalization for Numrical cols

# In[ ]:

df_pross=df.copy()
standard_scaler=StandardScaler()
df_pross[numerical_cols]=standard_scaler.fit_transform(df[numerical_cols])
df_pross[numerical_cols].head(5)


# ### Ordinal Data Encoding

# In[ ]:


mapping_experince={'Entry':0,'Mid':1,'Senior':2,'Lead':3}
df_pross['experince_level']=df['experience_level'].map(mapping_experince)
df_pross['experince_level'].head(5)


# ### One Hot Encoding for Nominal Data

# In[ ]:


#one hot encoding for nominal catogerioes
nominal_categories=categorical_cols.remove('experience_level')
df_encoded=pd.get_dummies(df_pross,columns=nominal_categories,drop_first=True)
df_encoded.shape


# # Linear Regression

# In[ ]:


x=df_encoded.drop('salary_usd',axis=1)
y=df_encoded['salary_usd']
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.2)
model=LinearRegression()
model.fit(x_train,y_train)
ypred=model.predict(x_test)
R2=r2_score(y_test,ypred)
MSE=mean_squared_error(y_test,ypred)
MAE=mean_absolute_error(y_test,ypred)
print(f'Mean Abslute Error: {MAE}')
print(f'Mean Squared Error: {MSE}')
print(f'R2 Score: {R2}')


# ## **Boxblot visualization for columns with outkliers only**

# In[ ]:


def removing_outliers(df):
  features=df.select_dtypes(include=['int','float']).columns
  result={}
  for feature in features:
    Q1=df[feature].quantile(0.25)
    Q3=df[feature].quantile(0.75)
    IQR=Q3-Q1
    lower_limit=Q1-1.5*(IQR)
    upper_limit=Q3+1.5*(IQR)
    count=((df[feature]<lower_limit)|(df[feature]>upper_limit)).sum()
    df=df[feature].clip(lower_limit,upper_limit)
    result[feature]=count
  return df,result

