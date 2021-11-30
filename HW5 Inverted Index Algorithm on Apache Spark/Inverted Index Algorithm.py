#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyspark import SparkContext, SparkConf


# In[ ]:


conf = SparkConf()


# In[ ]:


#create Spark context with necesary configuration
sc = SparkContext.getOrCreate(conf=conf)


# In[ ]:


#Conduct MapReduce 
wholefileRdd = sc.wholeTextFiles("./Data/*/*")


# In[ ]:


stop_words = ['they', 'she', 'he', 'it', 'the', 'as', 'is', 'and']


# In[ ]:


res = wholefileRdd.flatMap(lambda row: [(row[0], word) for word in row[1].lower().split(" ")]).map(lambda v: (v[1], v[0])).filter(lambda v: v[0] not in stop_word_list).map(lambda v: (v, 1)).reduceByKey(lambda a,b:a+b).map(lambda v: (v[0][0], [(v[0][1], v[1])])).reduceByKey(lambda a,b: a+b)


# In[ ]:


res.take(3)


# In[ ]:


res.coalesce(1).saveAsTextFile('./output')

