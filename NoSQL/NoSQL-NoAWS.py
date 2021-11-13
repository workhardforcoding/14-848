#!/usr/bin/env python
# coding: utf-8

# In[54]:


get_ipython().system('pip install boto3')


# In[55]:


import boto3


# In[56]:


#In the first section, Python will check if you need to install Pscycopg2 library and install it.
import subprocess
import sys

def install(package):
    #if pip doesn't work, try pip3 in the following statement
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("boto3")

import boto3
import csv


# In[57]:


s3 = boto3.resource('s3',
 aws_access_key_id='xxx',
 aws_secret_access_key='xxx')


# In[58]:


try:
 s3.create_bucket(Bucket='mingruoqu1', CreateBucketConfiguration={
 'LocationConstraint': 'us-west-2'})
except Exception as e:
 print (e)


# In[60]:


# make this bucket publicly readable. We will also need to make each blob in the bucket publicly readable
bucket = s3.Bucket('mingruoqu1')
bucket.Acl().put(ACL='public-read')


# In[61]:


# upload a new object into the bucket
# s3.Bucket(BUCKET).upload_file("/Users/qmr/Desktop/cmu_semester1/cloud/experiments.csv", "dump/file")
body = open('/Users/qmr/Desktop/cmu_semester1/cloud/exp1.csv', 'rb')


# In[62]:


o = s3.Object('mingruoqu1', 'test').put(Body=body )


# In[63]:


s3.Object('mingruoqu1', 'test').Acl().put(ACL='public-read')


# In[64]:


dyndb = boto3.resource('dynamodb',
 region_name='us-west-2',
 aws_access_key_id='xxx',
 aws_secret_access_key='xxx'
)


# In[67]:


try:
 table = dyndb.create_table(
 TableName='DataTable1',
 KeySchema=[
 {
 'AttributeName': 'PartitionKey',
 'KeyType': 'HASH'
 },
 {
 'AttributeName': 'RowKey',
 'KeyType': 'RANGE'
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
 table = dyndb.Table("DataTable1")


# In[68]:


table.meta.client.get_waiter('table_exists').wait(TableName='DataTable1')


# In[69]:


print(table.item_count)


# In[70]:


# query
with open('/Users/qmr/Desktop/cmu_semester1/cloud/experiments.csv', 'r') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(csvf)
    for item in csvf:
        print(item)
        body = open('/Users/qmr/Desktop/cmu_semester1/cloud/'+ item[4], 'rb')
        s3.Object('mingruoqu1', item[4]).put(Body=body)
        md = s3.Object('mingruoqu1', item[4]).Acl().put(ACL='public-read')
        url = "https://s3.console.aws.amazon.com/s3/buckets/mingruoqu1?region=us-west-2/"+item[4]
        metadata_item = {'PartitionKey': item[0], 'RowKey': item[1],
                         'Conductivity' : item[2], 'Concentration': item[3], 'url':url}
        try:
            table.put_item(Item=metadata_item)
        except:
            print("item may already be there or another failure")


# In[71]:


#results
response = table.get_item(
    Key={
        'PartitionKey': '1',
        'RowKey': '-1'
    }
)
item = response['Item']


# In[72]:


print(item)


# In[88]:


response2 = table.get_item(
    Key={
        'PartitionKey': '2',
        'RowKey': '-2'
    }
)
item2 = response2['Item']


# In[89]:


print(item2)


# In[90]:


#results
response3 = table.get_item(
    Key={
        'PartitionKey': '3',
        'RowKey': '-2.93'
    }
)
item3 = response3['Item']


# In[91]:


print(item3)


# In[ ]:




