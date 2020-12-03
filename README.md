# SHINoALICE_records
・スクショした貢献度の画像をimgファイルに渡し実行するだけで貢献度をGoogleスプレッドシートへ自動的に記録します。  
(・Simply pass the screenshot of the contribution to the specified file and automatically fill the value in the spreadsheet.  )  

## Description
SHINoALICE_Colosseum  

対応しているスクリーンショットのサイズは750px x 1334px のみです。  
[.PNG, .jpg, .jpeg] 画像は対応していますが[.png] 画像処理に影響があるので入れないでください。  

(Corresponding image size is (750px x 1334px) )     
(Type to put in folder: [.PNG, .jpg, .jpeg] ok!! not[.png] )  

## Demo Video
https://twitter.com/rem_rem0/status/1028866263018131456?s=20


## Usage
・まずはGoogleスプレッドシートにアクセスする為のサービスアカウントキー(JSON)ファイルを取得!  
　┗━>　<https://qiita.com/akabei/items/0eac37cb852ad476c6b9>  
・pipに入っていないライブラリを全てダウンロード。(python2.7.14で作成されています)  
・必要なフォルダは下記のように構成して下さい。([]があるフォルダは何も入れないよう注意)  


    main / img[このフォルダに画像を入れる]
    	 / imgs  / gray   []
    	         / name   []
    	         / score  []
    	         / sinma  []
    	 / parts / job    [各貢献度表の一部.画像]
    	 / parts / member [ギルドメンバーの名前.画像]
    	 / parts / sinma  [神魔武器.画像]
    	 / recog.py [メインファイル]
    	 / USER.json [サービスアカウントキーのJSONファイル]


・[/parts/member/]にはグレースケール化させたギルドメンバーの名前画像を入れる。  
・[/recog.py]内のスプレッドシート連携部分でJSONファイルやシート名を記入して完了。  

・起動方法  
    $python2 recog.py

## image
<img width="500" alt="スクリーンショット 2018-08-13 14 10 54" src="https://user-images.githubusercontent.com/16487150/101099994-17fd1680-3609-11eb-9b7f-884603a6602f.png">
<img width="500" alt="スクリーンショット 2018-08-08 5 04 32" src="https://user-images.githubusercontent.com/16487150/101100238-7f1acb00-3609-11eb-8f4a-a6be1ca0ed1c.png">
<img width="500" alt="スクリーンショット 2018-08-13 0 18 38" src="https://user-images.githubusercontent.com/16487150/101100354-b4bfb400-3609-11eb-9469-b70123d65820.png">
<img width="416" alt="スクリーンショット 2018-08-13 14 13 16" src="https://user-images.githubusercontent.com/16487150/101100486-ef295100-3609-11eb-866e-261179b9f4ed.png">
<img width="203" alt="スクリーンショット 2018-08-14 14 50 25" src="https://user-images.githubusercontent.com/16487150/101100546-049e7b00-360a-11eb-98ed-2694957fb86e.png">
<img width="200" alt="スクリーンショット 2018-08-14 14 43 29" src="https://user-images.githubusercontent.com/16487150/101100577-16801e00-360a-11eb-864a-1f92fb586225.png">
<img width="204" alt="スクリーンショット 2018-08-14 14 42 20" src="https://user-images.githubusercontent.com/16487150/101100615-2ac41b00-360a-11eb-9c32-7c4e73d1f7c8.png">



## LICENCE
・個人使用なら大丈夫です。  
(・For individual use okay  )  
