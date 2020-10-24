## Homework 1
### Association Analysis  
#### Dataset1:  
Select from kaggle.com / UCI  

#### Dataset2:  
Use IBM Quest Synthetic Data Generator
* https://sourceforge.net/projects/ibmquestdatagen/  
* Generate different datasets  

#### Implement Apriori Algorithm and apply on these datasets 
* Hash? Tree? (optional)  
* FP-growth  
#### Compare your results

---
### 環境
* macOS: 10.15.7（19H2）
* python: 3.7
* pycharm: 2020.2.3

### 程式檔案
* **main.py**:  
  主程式，放測試集的地方
* **apriori_algorithm.py**:  
  Apriori algorithm
* **FP_Growth.py**:  
  FP_Growth algorithm
  
* **./dataset**:  
  存放測試資料集的資料夾
* **./result**:  
  存放結果的資料夾
  
### 資料集 API
呼叫已整理好的資料集（提供給演算使用）
* deal_lecture_data(chose_type=1)  
  講義中的範例: 
  ```python
  >>> deal_lecture_data()   
  [['a', 'c', 'd'],
   ['b', 'c', 'e'],
   ['a', 'b', 'c', 'e'],
   ['b', 'e']]
   
  >>> deal_lecture_data(2)
  [['11', '33', '44'],
   ['22', '33', '55'],
   ['11', '22', '33', '55'],
   ['22', '55']]                 
  ```
* deal_kaggle_data(filename='./dataset/groceries - groceries.csv')  
  [from kaggle groceries - groceries](https://www.kaggle.com/irfanasrullah/groceries?select=groceries+-+groceries.csv) 共9835筆交易
  ```python
  >>> deal_kaggle_data()
  [['citrus fruit', 'semi-finished bread', 'margarine', 'ready soups'], 
   ['tropical fruit', 'yogurt', 'coffee'], 
   ['whole milk'],
   ...] 
  ``` 
* deal_IBM_data(filename='./dataset/test_data.csv')  
  from IBM Quest Synthetic Data Generator
    ```python
  >>> deal_IBM_data()
  [['118', '266', '364', '427', '628', '673', '868', '904'], 
   ['40', '316', '594', '858', '870', '871', '917'], 
   ['0', '132', '169', '209', '314', '439', '482', '553', '592', '642', '885'], 
   ['73', '128', '188', '319', '374', '432', '456', '511', '705', '707', '756', '767', '825', '894'], 
   ...]
    ```
    
### 測試 API
* class Apriori_test_set:
    * test_from_lecture(chose_type=1, min_support=2)  
      ```python 
      >>> Apriori_test_set.test_from_lecture(min_support=2)
      {('a',): 2, ('c',): 3, ('b',): 3, ('e',): 3, ('a', 'c'): 2, ('b', 'c'): 2, ('b', 'e'): 3, ('c', 'e'): 2, ('b', 'c', 'e'): 2}
      ```
    * test_from_kaggle(min_support=50)  
      ```python
      >>> Apriori_test_set.test_from_kaggle(600)
      {('citrus fruit',): 814, ('tropical fruit',): 1032, ('yogurt',): 1372, ('whole milk',): 2513, ('pip fruit',): 744, ('other vegetables',): 1903, ('rolls/buns',): 1809, ('bottled beer',): 792, ('bottled water',): 1087, ('soda',): 1715, ('fruit/vegetable juice',): 711, ('newspapers',): 785, ('pastry',): 875, ('root vegetables',): 1072, ('canned beer',): 764, ('sausage',): 924, ('brown bread',): 638, ('shopping bags',): 969, ('whipped/sour cream',): 705, ('domestic eggs',): 624, ('other vegetables', 'whole milk'): 736}
      ```
    * test_from_IBMdata(min_support=18)  
      ```python
      >>> Apriori_test_set.test_from_IBMdata(50)
      {('132',): 64, ('553',): 80, ('592',): 58, ('374',): 53, ('432',): 54, ('63',): 53, ('607',): 75, ('442',): 66, ('988',): 55, ('238',): 73, ('471',): 66, ('973',): 63, ('444',): 62, ('902',): 50, ('293',): 55, ('318',): 51, ('87',): 52, ('36',): 66, ('647',): 53, ('405',): 63}      
      ```
    
    
* class FP_Growth_test_set:
    * test_from_lecture(chose_type=1, min_support=2)  
    * test_from_kaggle(min_support=50)  
    * test_from_IBMdata(min_support=18)  
    
### 演算法 API
* Apriori
    * **apriori(transactions, min_support)**  
      transactions: [['str', ...], ['str', 'str' ...], ...]  
      min_support: int
      return: {('item', ...): number, ...}
    * 
    
* FP_Growth  
    *
    *
    
    
### Compare results
    