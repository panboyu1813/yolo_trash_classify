# Litter Classification Model

## Build Site
```
docker compose build
```
```
docker compose up -d
```

本探究旨於改善校園垃圾分類情況，透過操作簡便的AI垃圾識別網站幫助學生養成正確的分類習慣。
我們首先蒐集校園日常垃圾，獲取足量的垃圾樣本圖片以及測資圖片，並將其依垃圾分類放入資料夾中。
繼而使用Python程式進行數據預處理。
再來，我們利用YOLO v11物件偵測模型讀取樣本圖片，訓練出一個能辨別之AI圖像辨識模型（命名為Litter Classification Model，簡稱LCM）。
最後，我們輸入測試資料（簡稱測資），並且得到TOP1 95%的準確率，TOP5 100%的準確率，證明了LCM具備辨識垃圾類別之能力。
我們期望藉由此網站，減少學生因不熟悉分類規則而導致的錯誤，讓資源得以重複利用，永續發展。
