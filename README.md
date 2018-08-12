# SHINoALICE_records
.Simply pass the screenshot of the contribution to the specified file and automatically fill the value in the spreadsheet.  
(・スクショした貢献度の画像をimgファイルに渡し実行するだけで貢献度をGoogleスプレッドシートへ自動的に記録します。)  

## Description
SHINoALICE_Colosseum  

.Corresponding image size is (750px x 1334px)  
.Type to put in folder: [.PNG, .jpg, .jpeg] ok!! not[.png]  

(対応しているスクリーンショットのサイズは750px x 1334px のみです。)  
([.PNG, .jpg, .jpeg] 画像は対応していますが[.png] 画像処理に影響があるので入れないでください。)  

## DEMO


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
'$python2 recog.py'

## LICENCE
.For individual use okay  
(・個人使用ならおk!)  