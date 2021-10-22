#!/usr/bin/env python
# coding: utf-8

# In[16]:


get_ipython().system('pip install boto3')


# In[17]:


import boto3


# In[18]:


#In the first section, Python will check if you need to install Pscycopg2 library and install it.
import subprocess
import sys

def install(package):
    #if pip doesn't work, try pip3 in the following statement
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("boto3")

import boto3


# In[19]:


s3 = boto3.resource('s3',
 aws_access_key_id='AKIA5SUXCFMO2QNUR3XT',
 aws_secret_access_key='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')


# In[21]:


try:
 s3.create_bucket(Bucket='mingruo', CreateBucketConfiguration={
 'LocationConstraint': 'us-west-2'})
except Exception as e:
 print (e)


# In[22]:


bucket = s3.Bucket("mingruo")


# In[23]:


# make this bucket publicly readable. We will also need to make each blob in the bucket publicly readable
bucket.Acl().put(ACL='public-read')


# In[27]:


# upload a new object into the bucket
# s3.Bucket(BUCKET).upload_file("/Users/qmr/Desktop/cmu_semester1/cloud/experiments.csv", "dump/file")
body = open('/Users/qmr/Desktop/cmu_semester1/cloud/experiments.csv', 'rb')


# In[28]:


o = s3.Object('mingruo', 'test').put(Body=body )


# In[29]:


s3.Object('mingruo', 'test').Acl().put(ACL='public-read')


# In[30]:


dyndb = boto3.resource('dynamodb',
 region_name='us-west-2',
 aws_access_key_id='AKIA5SUXCFMO2QNUR3XT',
 aws_secret_access_key='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'
)


# In[31]:


try:
 table = dyndb.create_table(
 TableName='DataTable',
 KeySchema=[
 {
 'AttributeName': 'Id',
 'KeyType': 'RANGE'
 },
 {
 'AttributeName': 'Temp',
 'KeyType': 'HASH'
 },
 {
 'AttributeName': 'Conductivity',
 'KeyType': 'HASH'
 },
 {
 'AttributeName': 'Concentration',
 'KeyType': 'HASH'
 },
 {
 'AttributeName': 'URL',
 'KeyType': 'HASH'
 }
 ],
 AttributeDefinitions=[
 {
 'AttributeName': 'PartitionKey',
 'AttributeType': 'S'
 },
 {
 'AttributeName': 'RowKey',
 'AttributeType': 'S'
 },
 ],
 ProvisionedThroughput={
 'ReadCapacityUnits': 5,
 'WriteCapacityUnits': 5
 }
 )
except Exception as e:
 print (e)
 #if there is an exception, the table may already exist. if so...
 table = dyndb.Table("DataTable")


# In[32]:


table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')


# In[ ]:


print(table.item_count)


# In[11]:


import csv


# In[12]:


with open('c:\users\farag\documents\experiments.csv', 'rb') as csvfile:
 csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
 for item in csvf:
 print item
 body = open('c:\users\farag\documents\datafiles\\'+item[3], 'rb')
 s3.Object('datacont-name', item[3]).put(Body=body )
 md = s3.Object('datacont-name', item[3]).Acl().put(ACL='public-read')

 url = " https://s3-us-west-2.amazonaws.com/datacont-name/"+item[3]
 metadata_item = {'PartitionKey': item[0], 'RowKey': item[1],
 'description' : item[4], 'date' : item[2], 'url':url}
 try:
 table.put_item(Item=metadata_item)
 except:
 print "item may already be there or another failure"
['experiment1', '1', '3/15/2002', 'exp1', 'this is the comment']
['experiment1', '2', '3/15/2002', 'exp2', 'this is the comment2']
['experiment2', '3', '3/16/2002', 'exp3', 'this is the comment3']
['experiment3', '4', '3/16/2002', 'exp4', 'this is the comment233']


# In[13]:


response = table.get_item(
 Key={
 'PartitionKey': 'experiment3',
 'RowKey': '4'
 }
)
item = response['Item']
print(item)
# {u'url': u' https://s3-us-west-2.amazonaws.com/datacont-name/exp4', u'date':
# u'3/16/2002', u'PartitionKey': u'experiment3', u'description': u'this is the
# comment233', u'RowKey': u'4'}


# In[14]:


response


# In[ ]:




