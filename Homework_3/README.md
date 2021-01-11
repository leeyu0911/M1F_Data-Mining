## Link Analysis Practice  

### 程式檔案
* hw3dataset: 資料集
* result: 結果存檔區
* common_func.py: 共同使用到的 function
* HITS.py: HITS 演算法主程式
* PageRank.py: PageRank 演算法主程式
* SimRank.py: SimRank 演算法主程式
* main3.py: 執行以上演算法，並將結果存於 result 資料夾中
* README.md: 此份說明文件

### API
```python
from common_func import *
```
* load_txt(file_name)  
  讀取範例中的資料，轉換成 list 格式  
  file_name: type=`Path`  
  return `[(str, str), ...]`
  
* load_IBM_text(file_name)  
  專門讀取 IBM 資料，轉換成 list 格式  
  file_name: type=`Path`  
  return `[(str, str), ...]`
  
* list_to_adjacent_matrix(load_txt)  
  將讀取進來的資料變成相鄰矩陣，並同時回傳相鄰矩陣 index 對應的元素  
  load_txt: from`load_txt()` or `load_IBM_text()`  
  return `item`: `[str, ...]`相鄰矩陣所對應元素的位置, `am`: `numpy([[int, ...], ...])`相鄰矩陣  
  
```python
import HITS
```
* HITS.hits(am, iters=10000, error=1e-8)  
  am: `numpy.2Darray`相鄰矩陣  
  iters: 疊代次數。iters 和 error 其中一個條件達成演算法即停止  
  error: 當前後兩次計算出的結果誤差(對應項先平方再相減後的和)小於此值後即停止  
  
```python
import PageRank
```
* PageRank.pagerank(am, d=0.15, iters=10000, error=1e-8)  
  am: `numpy.2Darray`相鄰矩陣  
  d: damping factor  
  iters: 疊代次數。iters 和 error 其中一個條件達成演算法即停止  
  error: 當前後兩次計算出的結果誤差(對應項相減後絕對值的和)小於此值後即停止  
  
```python
import SimRank
```
* SimRank.simrank(am, c=0.8)  
  am: `numpy.2Darray`相鄰矩陣  
  c: decay factot  
  
```python
import main3
```
* main(file_name: Path, is_IBM=False, run_sim=True)  
  對一份資料同時跑以上三種演算法，並將結果存在 result 資料夾中  
  file_name: type=`Path`  
  is_IBM: 是否是 IBM 資料集(graph_1~6都是 False)  
  run_sim: 是否要跑 SimRank 演算法

### Find a way (e.g., add/delete some links) to increase hub, authority, and PageRank of Node 1 in first 3 graphs respectively.
這邊我想到的方法是把其他所有 Node 指向 Node 1，並將 Node 1 指向其他的 Node，結果如下:  
* Original:

|         | hub        | authority  | PageRank       |
| ------- | ---------: | ---------: | -------------: |
| graph_1 | 0.2        | 0          | 5.54209455e-18 |
| graph_2 | 0.2        | 0.2        | 0.2            |
| graph_3 | 0.19097222 | 0.19098712 | 0.16666667     |

* increase:

|         | hub        | authority  | PageRank   |
| ------- | ---------: | ---------: | ---------: |
| graph_1 | 0.26966472 | 0.2694944  | 0.38277512 |
| graph_2 | 0.28906618 | 0.28891232 | 0.39506173 |
| graph_3 | 0.28079505 | 0.28074582 | 0.3        |

### Implementation detail
進行不同的演算法之前，我都是先將檔案讀取進來以後，轉成 adjacent matrix 的形式，因此三個演算法在實作方面都是使用二維陣列的方式，
好處是可以不用去管 node 的名稱(如果要查詢原始 node 所對應 adjacent matrix 中的位置，紀錄在`list_to_adjacent_matrix()`回傳的第一個陣列中)，
全部都是用 index 方式在存取，可加速運算及方便表達。
* HITS  
  首先將各個 node 的 authority 分數初始化為 1/n，然後計算第一次的 hub，計算的方式為 adjacent matrix 和 authority 分數作矩陣相乘後再除以自己的 
  normalize(`max(sum(abs(x), axis=0))`)，
  然後存為新的 hub 分數。  
  之後計算 authority，這次是將轉至後的 adjacent matrix 和新的 hub 分數做矩陣相乘後一樣再除以自己的 normalize(`max(sum(abs(x), axis=0))`)。  
  然後不斷的重複以上的操作，不停地疊代。我在設計這個功能時提供了可調整疊代次數及誤差範圍的參數，在設定的疊代次數中，如果誤差範圍
  (兩次的 node 分數對應項相減後的平方總和)小於設定的值也會停止疊代。
  最後返回 hub 和 authority 的分數。
* PageRank  
  首先先將 adjacent matrix 中每個 node 除以該 row 所連結的 node 總數，並初始化每個 node 的 PageRank 分數為 1/n (也可以隨機 0 到 1 之間)。
  然後計算`V(i+1) = (1−α) * M * V(i) + α * V(i)`，其中`V`為每個 node 的 PageRank 分數，`M`為轉至後的 adjacent matrix，
  `α`為 damping factor，在此預設為 0.15。  
  一樣不斷的重複計算該公式。和上個演算法一樣提供了可調整疊代次數及誤差範圍的參數，在設定的疊代次數中，如果誤差範圍
  (兩次的 node 分數對應項相減後的平方總和)小於設定的值也會停止疊代。
* SimRank  
  在實作此演算法時我把它分成兩個部分，一個部分專門計算兩個 node 之間 SimRank 的分數，另一個則是去計算所有 node pair 的 SimRank。
  計算兩個 node 之間 SimRank 的演算法我的實作方式是，如果兩個 node 相等則回傳 1，如果不是的話則將演算法的公式分成前半部分和後半部分處理，
  前半部分計算 `c / (|I(a)| * |I(b)|)` ，`c`為 decay factot，預設為 0.8，`|I(a)|`代表指向 node a 的數量。
  後半部分使用的計算方式為將該 node 所對應到 adjacent matrix 的 column ，然後取得所有值為 1 的 index，
  如果兩個 node 取出的 index 相同則 count += 1。最後再將方程式前半部分和後半部分做相乘。
  後半部其原理就是，計算有多少共同的 node 數同時指向 node a 和 node b。

### Result analysis and discussion
全部的結果都存在 result 資料夾底下，命名規則:`資料集_演算法.txt`  
底下就圖一到圖三做討論
* graph_1  
  圖一為單向連結串列
  ```python
      1    2    3    4    5    6
  1  0.0  1.0  0.0  0.0  0.0  0.0
  2  0.0  0.0  1.0  0.0  0.0  0.0
  3  0.0  0.0  0.0  1.0  0.0  0.0
  4  0.0  0.0  0.0  0.0  1.0  0.0
  5  0.0  0.0  0.0  0.0  0.0  1.0
  6  0.0  0.0  0.0  0.0  0.0  0.0
  ```

  ```python
  HITS iter次數: 3 , error <= 0.0
  Authority:
  [0.  0.2 0.2 0.2 0.2 0.2]
  Hub:
  [0.2 0.2 0.2 0.2 0.2 0. ]
  ```
  可以看出 HITS 演算法在單向串列中，分數都非常的平均，除了第一個和最後一個節點分別在 authority 和 hub 中沒有分數。
  主要原因為第一個節點沒有人指向他，而最後一個節點沒有指向別人。
    
  ```python
  PageRank iter次數: 19 , error <= 2.2649853814246095e-09
  PageRank:
  [5.54209455e-18 6.33646144e-16 3.44465808e-14 1.18408636e-12
   2.88712443e-11 5.30931709e-10]
  ```
  我們知道 PageRank 為一個 Markov 的過程，如果要收斂圖必須是強連通的，而此圖是單向串列，因此不斷地疊代下去值只會越趨近於 0。
  
  ```python
  SimRank:
  [[1. 0. 0. 0. 0. 0.]
   [0. 1. 0. 0. 0. 0.]
   [0. 0. 1. 0. 0. 0.]
   [0. 0. 0. 1. 0. 0.]
   [0. 0. 0. 0. 1. 0.]
   [0. 0. 0. 0. 0. 1.]]
  ```
  因為是單向連結，所以其實可以手動的代入公式去做驗證。可以發現不管是哪一組 pair 都會不斷的遞迴到最初的 node，而只要其中一個
  node 為最初的 node 其值就會為 0，因此全部乘起來就為 0。
* graph_2  
  圖二為單向環
  ```python
       1    2    3    4    5
  1  0.0  1.0  0.0  0.0  0.0
  2  0.0  0.0  1.0  0.0  0.0
  3  0.0  0.0  0.0  1.0  0.0
  4  0.0  0.0  0.0  0.0  1.0
  5  1.0  0.0  0.0  0.0  0.0
  ```
  ```python
  HITS iter次數: 3 , error <= 0.0
  Authority:
  [0.2 0.2 0.2 0.2 0.2]
  Hub:
  [0.2 0.2 0.2 0.2 0.2]
  ```
  因為每個 node 都指向下一個 node，並形成一個環，因此大家的分數都是相同且平均的。
  
  ```python
  PageRank iter次數: 0 , error <= 0.0
  PageRank:
  [0.2 0.2 0.2 0.2 0.2]
  ```
  和 HITS 也是相同的狀況。
  
  ```python
  SimRank:
  [[1. 0. 0. 0. 0.]
   [0. 1. 0. 0. 0.]
   [0. 0. 1. 0. 0.]
   [0. 0. 0. 1. 0.]
   [0. 0. 0. 0. 1.]]
  ```
  其實這部分我有點無法解釋，我覺得按照原公式應該是一個無線遞迴下去的狀況才對，因此我在實作程式時是直接假設初始 node 不同時 SimRank = 0。
  
* graph_3  
  圖三是一個雙向連結串列
  ```python
       1    2    3    4
  1  0.0  1.0  0.0  0.0
  2  1.0  0.0  1.0  0.0
  3  0.0  1.0  0.0  1.0
  4  0.0  0.0  1.0  0.0
  ```
  
  ```python
  HITS iter次數: 10 , error <= 2.325456096530981e-09
  Authority:
  [0.19098712 0.30901288 0.30901288 0.19098712]
  Hub:
  [0.19097222 0.30902778 0.30902778 0.19097222]
  ```
  可以看出在鏈結的中間部分分數較高，因為不管 in link 或是 out link 都是尾端 node 的兩倍，所以以這圖整體而言就是 1/6 2/6 2/6 1/6。
  也因為圖是對稱的，所以 Authority 和 Hub 的分數都是相同的。
  
  ```python
  PageRank iter次數: 14 , error <= 6.012383035880475e-09
  PageRank:
  [0.16666667 0.33333333 0.33333333 0.16666667]
  ```
  PageRank 的結果看起來也是和 HITS 類似的狀況
  ```python
  SimRank:
  [[1. 0. 0. 0.]
   [0. 1. 0. 0.]
   [0. 0. 1. 0.]
   [0. 0. 0. 1.]]
  ```
  這和圖二的狀況有點類似，因為都含有迴圈的部分。但因為互相指向的 node 都是不相關的，所以根據 SimRank 最初的概念，他們的 SimRank 也就非常的低。
  
### Computation performance analysis
我使用的方式是計算一個演算法各跑完六個圖所花的時間及加總，雖然 HITS 和 PageRank 每張圖得疊代次數可能不同，但還是可以觀察出隨著圖越複雜，
PageRank 花費的時間要比 HITS 多，而花最多時間的則是 SimRank 演算法。

|(單位: s) | HITS       | PageRank   | SimRank    |
| ------- | ---------: | ---------: | ---------: |
| graph_1 | 0.00000000 | 0.00000000 | 0.00200081 |
| graph_2 | 0.00100017 | 0.00000000 | 0.00300145 |
| graph_3 | 0.00100040 | 0.00099969 | 0.00099993 |
| graph_4 | 0.00099897 | 0.00000000 | 0.00300026 |
| graph_5 | 0.01300478 | 0.07101583 | 6.67650533 |
| graph_6 | 0.12402606 | 0.38608742 | 58.8322105 |
| SUM     | 0.14003038 | 0.45810294 | 65.5177183 |

以下大約評估各個演算法的時間複雜度
* HITS  
  `O(n^3)`
  主要是使用 n * n 矩陣相乘，在計算上可以使用平行運算去做加速
  
* PageRank  
  `O(n^3)`
  計算上也是使用 n * n 矩陣相乘，不斷的疊代，也可以使用平行運算去做加速
  
* SimRank  
  `O(n^4)`
  內層基本上跑過一次矩陣，然後外層再對矩陣中每個元素跑一次 SimRank，一樣也可以使用平行運算去做加速  
  不過在實作此演算法時，雖然使用相同時間複雜度的寫法，在實際執行時還是有很明顯得時間差異，讓不必要執行的拉到迴圈外面，可以大大減少
  實際執行的時間(舊代碼請查看原始碼中20-23)，舊的方式在跑圖五時需要跑到一個多小時以上，圖六甚至一個晚上都跑不完，
  而改進後的方式不管在執行圖五還是圖六，都可以在大約一分鐘左右或以內就跑完了。
  
### Discussion (what you learned from this project and your comments about this project)
一開始在實做這些演算法的時候其實其實非常的難以理解其背後的真實意涵，大概知道每個演算法的目的就是想要找出一種方式去計算一個集合中各節點的重要性。
而不管是哪種演算法，在查資料的過程中都有發現其某些方面的缺陷(知道其計算的方式，就有辦法利用他的計算方式去提升某個節點的分數)，
並沒有一套完美的演算法可以適用在所有情境下，
通常都是同時搭配好幾套演算去計算或是後續又有其他的 paper 將其改進，然後又接著延續其他的問題。
而在計算上他們都是非常複雜的，實務上資料量都是非常龐大且又是動態的，很難對單獨一個點去計算他的分數是多少。
但不可否認這些演算法在當時甚至一直到現在都還是計算節點重要性非常經典的演算法。

### Questions & Discussion (optional, but recommended)
* #### More limitations about link analysis algorithms
  個人認為要實時的去計算現實中的所有網站是非常困難的，更不用說他的準確性。
* #### Can link analysis algorithms really find the “important” pages from Web?
  演算法中只考慮點和邊，因此增加點和邊的連結數量(如上面的方式，自己指向很多人，很多人指向自己)，極有可能增該該點的分數。
  但在實際中，例如維基百科底下提供非常多的參考連結，我想很少人真的會去點他。
  我想說的意思是，如果只考慮圖的結構，而沒有考量到實際使用者瀏覽網頁的情況，就很難真正找到真正重要的網頁。
* #### What are practical issues when implement these algorithms in a real Web?
  ##### Performance discussion (time cost)
  其實就是網頁每天都瞬息萬變，且數量非常的龐大，且又互相關聯，每跑一次就需花非常多時間了(須不停地疊代)，且還沒跑完可能就又要更新了。
* ####  What do the result say for your actor/movie graph?
  其中某些點的分數在整體看起來算蠻高的感覺，其他大部分都是 0。
* ####  Any new idea about the link analysis algorithm?
  實際使用者的點擊率，乘上網站的權重(例如排名)，做加權，然後除以全部網站的數量。
* ####  What is the effect of “C” parameter in SimRank?
  在遞迴的過程中，C 會不斷的相乘，因此會讓後面的相似性(遞迴數值)越來越小。
* ####  Design a new link-based similarity measurement
  可以同時考慮兩層到三層的遞迴關係，然後在加個權重，相關性可能會更高。