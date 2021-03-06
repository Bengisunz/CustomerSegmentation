
# Downloading the file manually
"""

from google.colab import files  #uploading all files
uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(name=fn, length=len(uploaded[fn])))

"""# Reading the File

**Importing Libraries**
---
"""

import pandas as pd # importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import io
import matplotlib.pyplot as plt
#from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import MiniBatchKMeans
from scipy import stats
from sklearn.cluster import KMeans   #importing libraries for the model
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
!pip install -q sklearn
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans  #model implementation
from time import time  # to keep track of the processing time
from sklearn import metrics
from sklearn.metrics import calinski_harabaz_score
from sklearn.cluster import AgglomerativeClustering

newdf=pd.read_csv("newdf200.csv")
#newdf= pd.read_csv(io.StringIO(uploaded['thelastdf.csv'].decode('utf-8')))

newdf = newdf.rename(columns={'OrtalamaSiparişTarihiFarki': 'SonSiparisTarihiFarki', 'OrtalamaSiparişTarihiFarki.1':'OrtalamaSiparişTarihiFarki'})

"""#------------------------------------DATA PROCESSING ----------------------------------

# Removing Outliers

** Numpy Work**
---
"""

newdf_nooutliers =newdf[["cus_no","Quantity Checked Out","Per Session Value","Product Detail Views","Pseudo Bounce Rate for User","Revenue Per Sessions","Cart-to-Detail Rate","Internal Promotion Clicks","Ecommerce Conversion Rate","Avg. Session Duration","% Exit","Unique Pageviews","Number of Sessions per User","Avg. Time on Page","MusteriKayıtYasi","SonSiparisTarihiFarki","OrtalamaSiparişTarihiFarki","IlkSiparisTarihiFarki","SiparisSayisi","SatisAdet","IskontoluKDVli_Tutar_TL","IskontoluKDVsiz_Tutar_TL","Iskonto_tutar","Kampanya_Indirim_Tutari","Maliyet_Fiyati","BrutKar_TL","Recency_Score","Frequency_Score","Monetary_Score","CLV_Degeri","IadeOran","Ortalama_Sepet_Adedi","Ortalama_Sepet_Tutari","Ortalama_Kar","Ortalama_Maliyet","Alisveris_Frekansi_Gun","İskonto_Orani"]]

np_new = newdf_nooutliers.as_matrix()
print(np_new.shape)

"""** With IQR**
---
"""

Q1 = newdf_nooutliers.quantile(0.25)
Q3 = newdf_nooutliers.quantile(0.75)
IQR = Q3 - Q1

df = newdf_nooutliers[~((newdf_nooutliers < (Q1 - 1.5 * IQR)) |(newdf_nooutliers > (Q3 + 1.5 * IQR))).any(axis=1)]
print (df)

df_df=pd.DataFrame(list(df))
print(type(df_df))

"""# RFM Calculation"""

df_rfm_table =df[["cus_no","SonSiparisTarihiFarki","SiparisSayisi","IskontoluKDVli_Tutar_TL"]]
print(df_rfm_table.head())

quantiles = df_rfm_table.quantile(q=[0.20,0.4,0.6,0.8])
quantiles

quantiles.to_dict()

r = []
   
for i in df_rfm_table['SonSiparisTarihiFarki']:
    if i <= 22:
        r.append(5)
    elif i <= 42:
        r.append(4)
    elif i <= 80:
        r.append(3)
    elif i <= 129:
        r.append(2)
    else:
        r.append(1)
    
      
    
df_rfm_table['RECENCY SCORE'] = r

f = []
   
for i in df_rfm_table['SiparisSayisi']:
    if i <= 4:
        f.append(1)
    elif i <= 6:
        f.append(2)
    elif i <= 10:
        f.append(3)
    elif i <= 17:
        f.append(4)
    else:
        f.append(5)
    
      
    
df_rfm_table['FREQUENCY SCORE'] = f

m = []
   
for i in df_rfm_table['IskontoluKDVli_Tutar_TL']:
    if i <= 125.7:
        m.append(1)
    elif i <= 216.5:
        m.append(2)
    elif i <= 352.6:
        m.append(3)
    elif i <= 626.4:
        m.append(4)
    else:
        m.append(5)
    
      
    
df_rfm_table['MONETARY SCORE'] = m

print(df_rfm_table.head())

df_rfm_table=df_rfm_table.drop('SonSiparisTarihiFarki',1)
df_rfm_table=df_rfm_table.drop('SiparisSayisi',1)
df_rfm_table=df_rfm_table.drop('IskontoluKDVli_Tutar_TL',1)

newdf = pd.merge(df, df_rfm_table, on='cus_no', how='inner')

newdf=newdf.drop('Recency_Score',1)
newdf=newdf.drop('Frequency_Score',1)
newdf=newdf.drop('Monetary_Score',1)

newdf.shape

"""#Min-Max Scaling"""

df_scaledfeatures=newdf[["Quantity Checked Out","Per Session Value","Product Detail Views","Pseudo Bounce Rate for User","Revenue Per Sessions","Cart-to-Detail Rate","Internal Promotion Clicks","Ecommerce Conversion Rate","Avg. Session Duration","% Exit","Unique Pageviews","Number of Sessions per User","Avg. Time on Page","MusteriKayıtYasi","SonSiparisTarihiFarki","OrtalamaSiparişTarihiFarki","IlkSiparisTarihiFarki","SiparisSayisi","SatisAdet","IskontoluKDVli_Tutar_TL","IskontoluKDVsiz_Tutar_TL","Iskonto_tutar","Kampanya_Indirim_Tutari","Maliyet_Fiyati","BrutKar_TL","RECENCY SCORE","FREQUENCY SCORE","MONETARY SCORE","CLV_Degeri","IadeOran","Ortalama_Sepet_Adedi","Ortalama_Sepet_Tutari","Ortalama_Kar","Ortalama_Maliyet","Alisveris_Frekansi_Gun","İskonto_Orani"]]

#col_df=newdf[["Quantity Checked Out","Per Session Value","Product Detail Views","Pseudo Bounce Rate for User","Revenue Per Sessions","Cart-to-Detail Rate","Internal Promotion Clicks","Ecommerce Conversion Rate","Avg. Session Duration","% Exit","Unique Pageviews","Number of Sessions per User","Avg. Time on Page","MusteriKayıtYasi","OrtalamaSiparişTarihiFarki","OrtalamaSiparişTarihiFarki","IlkSiparisTarihiFarki","SiparisSayisi","SatisAdet","IskontoluKDVli_Tutar_TL","IskontoluKDVsiz_Tutar_TL","Iskonto_tutar","Kampanya_Indirim_Tutari","Maliyet_Fiyati","BrutKar_TL","RECENCY SCORE","FREQUENCY SCORE","MONETARY SCORE","RFM_Score","CLV_Degeri","IadeOran","Ortalama_Sepet_Adedi","Ortalama_Sepet_Tutari","Ortalama_Kar","Ortalama_Maliyet","Alisveris_Frekansi_Gun","İskonto_Orani"]]

from sklearn import preprocessing

scaler = preprocessing.MinMaxScaler()
np_scaled = scaler.fit_transform(df_scaledfeatures)

columnn=(["Quantity Checked Out","Per Session Value","Product Detail Views","Pseudo Bounce Rate for User","Revenue Per Sessions","Cart-to-Detail Rate","Internal Promotion Clicks","Ecommerce Conversion Rate","Avg. Session Duration","% Exit","Unique Pageviews","Number of Sessions per User","Avg. Time on Page","MusteriKayıtYasi","SonSiparisTarihiFarki","OrtalamaSiparişTarihiFarki","IlkSiparisTarihiFarki","SiparisSayisi","SatisAdet","IskontoluKDVli_Tutar_TL","IskontoluKDVsiz_Tutar_TL","Iskonto_tutar","Kampanya_Indirim_Tutari","Maliyet_Fiyati","BrutKar_TL","RECENCY SCORE","FREQUENCY SCORE","MONETARY SCORE","CLV_Degeri","IadeOran","Ortalama_Sepet_Adedi","Ortalama_Sepet_Tutari","Ortalama_Kar","Ortalama_Maliyet","Alisveris_Frekansi_Gun","İskonto_Orani"])


df_normalized = pd.DataFrame(np_scaled, columns=columnn)

print(df_normalized.head())
print(df_normalized.shape)

#np_scaled.columns = ["Quantity Checked Out","Per Session Value","Product Detail Views","Pseudo Bounce Rate for User","Revenue Per Sessions","Cart-to-Detail Rate","Internal Promotion Clicks","Ecommerce Conversion Rate","Avg. Session Duration","% Exit","Unique Pageviews","Number of Sessions per User","Avg. Time on Page","MusteriKayıtYasi","SonSiparisTarihiFarki","OrtalamaSiparişTarihiFarki","IlkSiparisTarihiFarki","SiparisSayisi","SatisAdet","IskontoluKDVli_Tutar_TL","IskontoluKDVsiz_Tutar_TL","Iskonto_tutar","Kampanya_Indirim_Tutari","Maliyet_Fiyati","BrutKar_TL","RECENCY SCORE","FREQUENCY SCORE","MONETARY SCORE","CLV_Degeri","IadeOran","Ortalama_Sepet_Adedi","Ortalama_Sepet_Tutari","Ortalama_Kar","Ortalama_Maliyet","Alisveris_Frekansi_Gun","İskonto_Orani"]

org_1=pd.read_csv("newdf200.csv")

#newdf = newdf.rename(columns={'OrtalamaSiparişTarihiFarki': 'SonSiparisTarihiFarki', 'OrtalamaSiparişTarihiFarki.1':'OrtalamaSiparişTarihiFarki'})

org_1=org_1.drop('Quantity Checked Out',1)
org_1=org_1.drop('Per Session Value',1)
org_1=org_1.drop('Product Detail Views',1)
org_1=org_1.drop('Pseudo Bounce Rate for User',1)
org_1=org_1.drop('Revenue Per Sessions',1)
org_1=org_1.drop('Cart-to-Detail Rate',1)
org_1=org_1.drop('Internal Promotion Clicks',1)
org_1=org_1.drop('Ecommerce Conversion Rate',1)
org_1=org_1.drop('Avg. Session Duration',1)
org_1=org_1.drop('% Exit',1)
org_1=org_1.drop('Unique Pageviews',1)
org_1=org_1.drop('Number of Sessions per User',1)
org_1=org_1.drop('Avg. Time on Page',1)
org_1=org_1.drop('MusteriKayıtYasi',1)
org_1=org_1.drop('OrtalamaSiparişTarihiFarki',1)
org_1=org_1.drop('IlkSiparisTarihiFarki',1)
org_1=org_1.drop('OrtalamaSiparişTarihiFarki.1',1)
org_1=org_1.drop('SiparisSayisi',1)
org_1=org_1.drop('SatisAdet',1)
org_1=org_1.drop('IskontoluKDVli_Tutar_TL',1)
org_1=org_1.drop('IskontoluKDVsiz_Tutar_TL',1)
org_1=org_1.drop('Iskonto_tutar',1)
org_1=org_1.drop('Kampanya_Indirim_Tutari',1)
org_1=org_1.drop('Maliyet_Fiyati',1)
org_1=org_1.drop('BrutKar_TL',1)
org_1=org_1.drop('Recency_Score',1)
org_1=org_1.drop('Frequency_Score',1)
org_1=org_1.drop('Monetary_Score',1)
org_1=org_1.drop('RFM_Score',1)
org_1=org_1.drop('CLV_Degeri',1)
org_1=org_1.drop('IadeOran',1)
org_1=org_1.drop('Ortalama_Sepet_Adedi',1)
org_1=org_1.drop('Ortalama_Sepet_Tutari',1)
org_1=org_1.drop('Ortalama_Kar',1)
org_1=org_1.drop('Ortalama_Maliyet',1)
org_1=org_1.drop('Alisveris_Frekansi_Gun',1)
org_1=org_1.drop('İskonto_Orani',1)


df_normalized['cus_no']=newdf['cus_no']

org_1= pd.merge(org_1, df_normalized, on='cus_no', how='inner')

print(org_1.shape)

"""#-------------------------------MODEL IMPLEMENTATION-------------------------------

**Principal Component Analysis**
---
"""

print(df_normalized.head(2))

df_normalized=df_normalized.drop('cus_no',1)

from sklearn.decomposition import PCA 

pca=PCA()
pca.fit(df_normalized)
cumsum=np.cumsum(pca.explained_variance_ratio_)
d=np.argmax(cumsum>=0.80)+1

print("The number of variable for PCA", d)

var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4))
plt.plot(var1)
plt.xlim([10,40])
plt.ylim([0.5,0.9])
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')
plt.show()

pca = PCA(n_components=8)
pca.fit(df_normalized)
pca_samples = pca.transform(df_normalized)

ps = pd.DataFrame(pca_samples)
ps.columns = ['PC1','PC2','PC3','PC4','PC5','PC6','PC7','PC8']
ps.head(15)

ps['cus_no']=org_1['cus_no'] #adding customer_no to the dimension reduced dataset

org_df=org_1.copy()

print(org_df.head(2))

#droping reduced features cause we do not need them anymore

org_df=org_df.drop('Quantity Checked Out',1)
org_df=org_df.drop('Per Session Value',1)
org_df=org_df.drop('Product Detail Views',1)
org_df=org_df.drop('Pseudo Bounce Rate for User',1)
org_df=org_df.drop('Revenue Per Sessions',1)
org_df=org_df.drop('Cart-to-Detail Rate',1)
org_df=org_df.drop('Internal Promotion Clicks',1)
org_df=org_df.drop('Ecommerce Conversion Rate',1)
org_df=org_df.drop('Avg. Session Duration',1)
org_df=org_df.drop('% Exit',1)
org_df=org_df.drop('Unique Pageviews',1)
org_df=org_df.drop('Number of Sessions per User',1)
org_df=org_df.drop('Avg. Time on Page',1)
org_df=org_df.drop('MusteriKayıtYasi',1)
org_df=org_df.drop('OrtalamaSiparişTarihiFarki',1)
org_df=org_df.drop('IlkSiparisTarihiFarki',1)
org_df=org_df.drop('SonSiparisTarihiFarki',1)
org_df=org_df.drop('SiparisSayisi',1)
org_df=org_df.drop('SatisAdet',1)
org_df=org_df.drop('IskontoluKDVli_Tutar_TL',1)
org_df=org_df.drop('IskontoluKDVsiz_Tutar_TL',1)
org_df=org_df.drop('Iskonto_tutar',1)
org_df=org_df.drop('Kampanya_Indirim_Tutari',1)
org_df=org_df.drop('Maliyet_Fiyati',1)
org_df=org_df.drop('BrutKar_TL',1)
org_df=org_df.drop('RECENCY SCORE',1)
org_df=org_df.drop('FREQUENCY SCORE',1)
org_df=org_df.drop('MONETARY SCORE',1)
org_df=org_df.drop('CLV_Degeri',1)
org_df=org_df.drop('IadeOran',1)
org_df=org_df.drop('Ortalama_Sepet_Adedi',1)
org_df=org_df.drop('Ortalama_Sepet_Tutari',1)
org_df=org_df.drop('Ortalama_Kar',1)
org_df=org_df.drop('Ortalama_Maliyet',1)
org_df=org_df.drop('Alisveris_Frekansi_Gun',1)
org_df=org_df.drop('İskonto_Orani',1)

"""**Concerating the PCA Components with Category Features **"""

newdf_ps = pd.merge(org_df, ps, on='cus_no', how='inner') #merging pca features and one-hot encoding features

print(newdf_ps.head(2))

"""#K-MEANS CLUSTERING

**Finding the Best k Value with Silhouette Score**
---
"""

newdf_ps=pd.read_csv("newdf_ps.csv")

ps_out_cus=newdf_ps.drop('cus_no',1) #dropping cus_no for k-means

print(ps_out_cus.head(2))

"""```
# for n_cluster in range(2, 20):
    kmeans = KMeans(n_clusters=n_cluster).fit(ps_out_cus)
    label = kmeans.labels_
    sil_coeff = silhouette_score(ps_out_cus, label, metric='euclidean')
    print("For n_clusters={}, The Silhouette Coefficient is {}".format(n_cluster, sil_coeff))
```

**Silhouette Scores of Different K Values in  (Metric:Eudician)**

For n_clusters=2, The Silhouette Coefficient is 0.10027624264849146

For n_clusters=3, The Silhouette Coefficient is 0.09339449243148329

For n_clusters=4, The Silhouette Coefficient is 0.10790112366634444

For n_clusters=5, The Silhouette Coefficient is 0.1254015600377576

For n_clusters=6, The Silhouette Coefficient is 0.14180458393611164

For n_clusters=7, The Silhouette Coefficient is 0.15801995845054995

For n_clusters=8, The Silhouette Coefficient is 0.14468823270707093

For n_clusters=9, The Silhouette Coefficient is 0.15408437256843596

For n_clusters=10, The Silhouette Coefficient is 0.13497267337801314

For n_clusters=11, The Silhouette Coefficient is 0.1269096673809416

For n_clusters=12, The Silhouette Coefficient is 0.12783533559020996

For n_clusters=13, The Silhouette Coefficient is 0.12793948100360347

For n_clusters=14, The Silhouette Coefficient is 0.12859199554261885

For n_clusters=15, The Silhouette Coefficient is 0.12140111967618018

For n_clusters=16, The Silhouette Coefficient is 0.12128354218084411

For n_clusters=17, The Silhouette Coefficient is 0.11516159444638377

For n_clusters=18, The Silhouette Coefficient is 0.11820998594583788

For n_clusters=19, The Silhouette Coefficient is 0.11225849106277139

For n_clusters=20, The Silhouette Coefficient is 0.10991500923379095

For n_clusters=21, The Silhouette Coefficient is 0.11470142195914607

For n_clusters = 22 The average silhouette_score is : 0.27997627797360997



---




**Silhouette Scores of Different K Values in  (Metric:Cosine)**


For n_clusters=2, The Silhouette Coefficient is 0.17207554398521646

For n_clusters=3, The Silhouette Coefficient is 0.1702081301670921

For n_clusters=4, The Silhouette Coefficient is 0.18959259101170017

For n_clusters=5, The Silhouette Coefficient is 0.21491008579448614

For n_clusters=6, The Silhouette Coefficient is 0.23874127763350017

For n_clusters=7, The Silhouette Coefficient is 0.2628105154211806

For n_clusters=8, The Silhouette Coefficient is 0.2388045915965596

For n_clusters=9, The Silhouette Coefficient is 0.21278569610203232

For n_clusters=10, The Silhouette Coefficient is 0.24538950319348327

For n_clusters=11, The Silhouette Coefficient is 0.21356895535887846

For n_clusters=12, The Silhouette Coefficient is 0.21783972580424993

For n_clusters=13, The Silhouette Coefficient is 0.21845350712343065

For n_clusters=14, The Silhouette Coefficient is 0.21788171102896622

For n_clusters=15, The Silhouette Coefficient is 0.21210359186015038

For n_clusters=16, The Silhouette Coefficient is 0.2089227510732205

The highest silhouette score apperances when  K is 7.
"""

sse = {}
for k in range(3, 25):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(ps_out_cus)
    ps_out_cus["clusters"] = kmeans.labels_
    #print(data["clusters"])
    sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
plt.figure()
plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.show()

cluster_range = range( 1, 20 )
cluster_errors = []

for num_clusters in cluster_range:
  clusters = KMeans( num_clusters )
  clusters.fit(ps_out_cus)
  cluster_errors.append( clusters.inertia_ )
 
clusters_df = pd.DataFrame( { "num_clusters":cluster_range, "cluster_errors": cluster_errors } )

plt.figure(figsize=(12,6))
plt.plot( clusters_df.num_clusters, clusters_df.cluster_errors, marker = "o" )

distorsions = []
for k in range(2, 20):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(ps_out_cus)
    distorsions.append(kmeans.inertia_)

fig = plt.figure(figsize=(15, 5))
plt.plot(range(2, 20), distorsions)
plt.grid(True)
plt.title('Elbow curve')

"""**Clustering with K=7**
---

```
# from sklearn import metrics

kmeans = KMeans(init='k-means++',n_clusters=7, n_jobs= -1)
t0 = time()
kmeansoutput=kmeans.fit(ps_out_cus)
t1 = time() - t0
print("K-Means on reduced data:",t1)
df = pd.DataFrame(kmeans.cluster_centers_)
df['count'] = pd.Series(kmeans.labels_).value_counts()  # Number of each clusters
print("Number of elements for each cluster: \t")
print(df['count'])

silhouette_ecludiene= metrics.silhouette_score(ps_out_cus,kmeans.labels_, metric='euclidean', sample_size=ps_out_cus.shape[0])
silhouette_cosine= metrics.silhouette_score(ps_out_cus,kmeans.labels_, metric='cosine', sample_size=ps_out_cus.shape[0])

print(silhouette_ecludiene)
print(silhouette_cosine)
```
"""

n_clusters=7
clusterer = KMeans(n_clusters=n_clusters,random_state=42).fit(ps_out_cus)
centers = clusterer.cluster_centers_
cluster_labels = clusterer.fit_predict(ps_out_cus)

final_pca =newdf_ps.copy()  #unutma burası org olacak
final_pca["cluster"] = cluster_labels

print(final_pca.head(3))

print (final_pca.shape)
#final_nocus = final.drop('cus_no',1)

print(centers)

sns.countplot(x="cluster", data=final_pca)    
plt.xlabel('Clusters')
plt.ylabel('Frequency')
plt.title('Number of Clusters')
plt.show()

col_names = ['PC1','PC2','PC3','PC4','PC5','PC6','PC7','PC8']
LABEL_COLOR_MAP = {0 : 'purple',1 : 'g',2: 'b',3:'m',4:'y',5:'orange',6:'crimson'} #,7:'slategray',8:'aqua'}
label_color = [LABEL_COLOR_MAP[l] for l in cluster_labels]

for i in col_names:
  for j in col_names:
    if i<j:
      print(i+ "-"+j)
      newdf_ps.plot(kind='scatter', x=i, y=j,c=label_color, figsize=(16,8))
      plt.scatter(centers[:, 0], centers[:, 1],   marker="s", s=200, color='r')
      #centers.plot(kind='scatter', x=i, y=j,c=label_color,marker="s", s=169, linewidths=5,color='r', zorder=10, figsize=(16,8))
      plt.xlabel(i)
      plt.ylabel(j)
      plt.title('K-means clustering on the'+" "+i+"-"+j)
      plt.show()

col_names = ['PC1','PC2','PC3','PC4','PC5','PC6','PC7','PC8']
LABEL_COLOR_MAP = {0 : 'purple',1 : 'g',2: 'b',3:'m',4:'y',5:'orange',6:'crimson'} #,7:'slategray',8:'aqua'}
label_color = [LABEL_COLOR_MAP[l] for l in cluster_labels]


for i in col_names:
  for j in col_names:
    if i<j:
      for k in range(0,7):
         x=final_pca.loc[final_pca['cluster'] == k]
         c=LABEL_COLOR_MAP[k]
         x.plot(kind='scatter', x=i, y=j,c=c, figsize=(16,8))
         plt.xlabel(i)
         plt.ylabel(j)
         plt.title('Cluster K-Means '+ i + "-" + j + "& Cluster label: "+str(k))
         plt.show()

final_pca.groupby('cluster', as_index=False).mean()

"""**----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------**

# Feature Agglomeration
"""

from sklearn.cluster import FeatureAgglomeration
agg = FeatureAgglomeration(n_clusters=8, affinity='euclidean')
tx0 = time()
aggoutput=agg.fit(df_normalized,y=None)  
tx1 = time() - tx0
print("K-Means on reduced data:",tx1)
reduced_data = aggoutput.fit_transform(df_normalized,y=None)
print(reduced_data)

fa = pd.DataFrame(reduced_data)
fa.columns = ['F1','F2','F3','F4','F5','F6','F7','F8']
fa.head(2)
print(fa.shape)

#droping reduced features cause we do not need them anymore
org_df=org_1.copy()

org_df=org_df.drop('Quantity Checked Out',1)
org_df=org_df.drop('Per Session Value',1)
org_df=org_df.drop('Product Detail Views',1)
org_df=org_df.drop('Pseudo Bounce Rate for User',1)
org_df=org_df.drop('Revenue Per Sessions',1)
org_df=org_df.drop('Cart-to-Detail Rate',1)
org_df=org_df.drop('Internal Promotion Clicks',1)
org_df=org_df.drop('Ecommerce Conversion Rate',1)
org_df=org_df.drop('Avg. Session Duration',1)
org_df=org_df.drop('% Exit',1)
org_df=org_df.drop('Unique Pageviews',1)
org_df=org_df.drop('Number of Sessions per User',1)
org_df=org_df.drop('Avg. Time on Page',1)
org_df=org_df.drop('MusteriKayıtYasi',1)
org_df=org_df.drop('OrtalamaSiparişTarihiFarki',1)
org_df=org_df.drop('IlkSiparisTarihiFarki',1)
org_df=org_df.drop('SonSiparisTarihiFarki',1)
org_df=org_df.drop('SiparisSayisi',1)
org_df=org_df.drop('SatisAdet',1)
org_df=org_df.drop('IskontoluKDVli_Tutar_TL',1)
org_df=org_df.drop('IskontoluKDVsiz_Tutar_TL',1)
org_df=org_df.drop('Iskonto_tutar',1)
org_df=org_df.drop('Kampanya_Indirim_Tutari',1)
org_df=org_df.drop('Maliyet_Fiyati',1)
org_df=org_df.drop('BrutKar_TL',1)
org_df=org_df.drop('RECENCY SCORE',1)
org_df=org_df.drop('FREQUENCY SCORE',1)
org_df=org_df.drop('MONETARY SCORE',1)
#org_df=org_df.drop('RFM_Score',1)
org_df=org_df.drop('CLV_Degeri',1)
org_df=org_df.drop('IadeOran',1)
org_df=org_df.drop('Ortalama_Sepet_Adedi',1)
org_df=org_df.drop('Ortalama_Sepet_Tutari',1)
org_df=org_df.drop('Ortalama_Kar',1)
org_df=org_df.drop('Ortalama_Maliyet',1)
org_df=org_df.drop('Alisveris_Frekansi_Gun',1)
org_df=org_df.drop('İskonto_Orani',1)

fa['cus_no']=newdf['cus_no']

df_fa = pd.merge(org_df, fa, on='cus_no', how='inner') #merging FEATURES of product category and fa

df_fa=df_fa.drop('cus_no',1)

print(df_fa.shape)

"""# AGGLOMERATIVE CLUSTERING

**Finding the Best k with Silhouette Score**
---

```
# z = []                                      #distance metric is euclidean
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import AgglomerativeClustering


matrix = df_fa.as_matrix()

#cluster = AgglomerativeClustering(n_clusters=8, affinity='euclidean', linkage='ward')
#data=cluster.fit_predict(data)

for n_clusters in range(2,38):
   clustering = AgglomerativeClustering(n_clusters = n_clusters,affinity='euclidean')
   clusters1 = clustering.fit_predict(matrix)
   # clusters = clustering.predict(matrix)
   sil_score = silhouette_score(matrix, clusters1)
   z.append(sil_score)
   print("For n_clusters =", n_clusters, "The average silhouette_score is :", sil_score)

plt.figure(figsize=(12,8))
plt.plot(range(2,38),z)
plt.xlabel('No of Clusters')
plt.ylabel('Silhouette_avg')
plt.title('Silhoutte Score for different clusters with AHC')
```







**Silhouette Scores of Different K Values in  (Metric:Eudician)**

For n_clusters = 2 The average silhouette_score is : 0.13011132018059038

For n_clusters = 3 The average silhouette_score is : 0.16405504835351684

For n_clusters = 4 The average silhouette_score is : 0.20264390138178248

For n_clusters = 5 The average silhouette_score is : 0.23663416499428458

For n_clusters = 6 The average silhouette_score is : 0.26540377517451635

For n_clusters = 7 The average silhouette_score is : 0.20717021684545447

For n_clusters = 8 The average silhouette_score is : 0.22237818853079

For n_clusters = 9 The average silhouette_score is : 0.22650879625263035

For n_clusters = 10 The average silhouette_score is : 0.23348439252628148

For n_clusters = 11 The average silhouette_score is : 0.24585807110595953

For n_clusters = 12 The average silhouette_score is : 0.24625071305069884

For n_clusters = 13 The average silhouette_score is : 0.2388621748545083

For n_clusters = 14 The average silhouette_score is : 0.25040572704673086

For n_clusters = 15 The average silhouette_score is : 0.26015263124113513

For n_clusters = 16 The average silhouette_score is : 0.24950153826796156

For n_clusters = 17 The average silhouette_score is : 0.25733734772473044

For n_clusters = 18 The average silhouette_score is : 0.26361337749319624

For n_clusters = 19 The average silhouette_score is : 0.27188879066067007

For n_clusters = 20 The average silhouette_score is : 0.26499327205243134

For n_clusters = 21 The average silhouette_score is : 0.2728957551246686

For n_clusters = 22 The average silhouette_score is : 0.2799762779736099





---




```
# z = []                     #distance metric is cosine

matrix = df_fa.as_matrix()

for n_clusters in range(2,38):
   clustering = AgglomerativeClustering(n_clusters = n_clusters,affinity='cosine',linkage='complete')
   clusters1 = clustering.fit_predict(matrix)
   # clusters = clustering.predict(matrix)
   sil_score = silhouette_score(matrix, clusters1)
   z.append(sil_score)
   print("For n_clusters =", n_clusters, "The average silhouette_score is :", sil_score)

plt.figure(figsize=(12,8))
plt.plot(range(2,38),z)
plt.xlabel('No of Clusters')
plt.ylabel('Silhouette_avg')
plt.title('Silhoutte Score for different clusters with AHC')
```



**Silhouette Scores of Different K Values in  (Metric:Cosine)**

For n_clusters = 2 The average silhouette_score is : 0.09278121757148973

For n_clusters = 3 The average silhouette_score is : 0.09198853434551706

For n_clusters = 4 The average silhouette_score is : 0.12581527937275627

For n_clusters = 5 The average silhouette_score is : 0.1512424325810709

For n_clusters = 6 The average silhouette_score is : 0.16418505890233873

For n_clusters = 7 The average silhouette_score is : 0.18709606036698617

For n_clusters = 8 The average silhouette_score is : 0.20880134085724567

For n_clusters = 9 The average silhouette_score is : 0.21173277977025404

For n_clusters = 10 The average silhouette_score is : 0.21679260047572774

For n_clusters = 11 The average silhouette_score is : 0.21497016879709072

For n_clusters = 12 The average silhouette_score is : 0.2126606949905361

For n_clusters = 13 The average silhouette_score is : 0.21329994650763776

For n_clusters = 14 The average silhouette_score is : 0.21128334298798354

For n_clusters = 15 The average silhouette_score is : 0.2103188145613723

For n_clusters = 16 The average silhouette_score is : 0.21032342749125033

For n_clusters = 17 The average silhouette_score is : 0.21033740347481658

**Clustering**
---
"""

df_fa=pd.read_csv("df_fa.csv")

print(df_fa.head(1))

#perform_clustering(df_fa)

X=df_fa

clt = AgglomerativeClustering(linkage='average',affinity='euclidean',n_clusters=6)

t0 = time()
model = clt.fit(X)
t1 = time() - t0
labels_ag = clt.labels_

print(labels_ag)
df = pd.DataFrame(X,labels_ag)
df['count'] = pd.Series(labels_ag).value_counts()

print("Runtime for Agglomerative: ",t1)
#print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels_ag))
#print("CH Coefficient: %0.3f" % metrics.calinski_harabaz_score(X,labels_ag))

labels_unique = np.unique(labels_ag)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

print(labels_ag.shape)

#final_ag =org_1.copy()
final_ag =org_1.copy()

final_ag["cluster"] = labels_ag

print (final_ag.shape)
print(final_ag.head(2))
#final_nocus = final.drop('cus_no',1)

sns.countplot(x="cluster", data=final_ag)    
plt.xlabel('Clusters')
plt.ylabel('Frequency')
plt.title('Number of Clusters')
plt.show()

final_ag.groupby('cluster', as_index=False).mean()

f_ag =df_fa.copy()
f_ag["cluster"] = labels_ag
f_ag.groupby('cluster', as_index=False).mean()

col_names = ['F1','F2','F3','F4','F5','F6','F7','F8']


LABEL_COLOR_MAP = {0 : 'purple',1 : 'g',2: 'b',3:'m',4:'y',5:'orange',6:'crimson',7:'slategray',8:'aqua',9:'black'}  
label_color_ag = [LABEL_COLOR_MAP[l] for l in labels_ag]

for i in col_names:
  for j in col_names:
    if i<j:
      print(i+ "-"+j)
      fa.plot(kind='scatter', x=i, y=j,c=label_color_ag, figsize=(16,8))
      plt.xlabel(i)
      plt.ylabel(j)
      plt.title('Cluster K-Means'+i+"-"+j)
      plt.show()

df_fa["cluster"] = labels_ag

col_names = ['F1','F2','F3','F4','F5','F6','F7','F8']
LABEL_COLOR_MAP = {0 : 'purple',1 : 'g',2: 'b',3:'m',4:'y',5:'orange'} #,6:'crimson',7:'slategray',8:'aqua',9:'black'}  
label_color = [LABEL_COLOR_MAP[l] for l in labels_ag]
 

for i in col_names:
  for j in col_names:
    if i<j:
      for k in range(0,6):
         x=df_fa.loc[df_fa['cluster'] == k]
         c=LABEL_COLOR_MAP[k]
         x.plot(kind='scatter', x=i, y=j,c=c, figsize=(16,8))
         plt.xlabel(i)
         plt.ylabel(j)
         plt.title('Agglomerative Clustering '+ i + "-" + j + "& Cluster label: "+str(k))
         plt.show()
