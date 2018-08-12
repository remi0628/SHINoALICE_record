# -*- coding: utf-8 -*-
# python2.7.14
import os
import re
import copy
import time
import sys
import glob
import pytesseract
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image, ImageDraw
import numpy as np
import cv2

# [a]:味方貢献度リスト [b]:敵貢献度リスト
result_a   = [''] * 5
result_b   = [''] * 5
im_recog_a = [''] * 5
im_recog_b = [''] * 5
im_recog_m = [''] * 5
name_a     = [''] * 5
# 最終的なリスト変数
member_a   = [''] * 5
top_a = [''] * 2
top_b = [''] * 2
sbk_1 = [''] * 3
sbk_2 = [''] * 3
in_a  = [''] * 5
in_b  = [''] * 5
kf_a  = [''] * 5
kf_b  = [''] * 5
mk_a  = [''] * 5
mk_b  = [''] * 5
mb_a  = [''] * 5
mb_b  = [''] * 5
tk_a  = [''] * 5
tk_b  = [''] * 5
tb_a  = [''] * 5
tb_b  = [''] * 5
kb_a  = [''] * 5
kb_b  = [''] * 5

# time
t = 0

""" メイン """
def record():
	""" 画像のファイル名を読み込めるように変更 """
	image_name()
	# [.png]画像を処理にかける為
	path = './img/*.png'
	list = glob.glob(path)

	""" グレースケール """
	for i in range(0,9):
		image = list[i]
		t = 150
		if i == 7:
			t = 80
		if i == 8:
			t = 180
		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		ret, th2 = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
		cv2.imwrite("./imgs/gray/100%d.png" %(i), th2)

	""" 神魔武器読み込み """
	t = 80
	img = cv2.imread('./img/108.png')
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	ret, th2 = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
	cv2.imwrite("./imgs/gray/1009.png", th2)

	url_img = ('./imgs/gray/1009.png')
	img = Image.open(url_img)
	# トリミング
	# 今日の神魔
	im_recog_a[0] = img.crop((254, 405 , 290 , 442))
	im_recog_a[1] = img.crop((288, 405 , 326 , 442))
	im_recog_a[2] = img.crop((323, 405 , 362 , 442))
	im_recog_b[0] = img.crop((254, 879 , 290 , 917))
	im_recog_b[1] = img.crop((289, 879 , 326 , 917))
	im_recog_b[2] = img.crop((323, 879 , 362 , 917))
	# トリミングした画像の保存
	for i in range(0,3):
		im_recog_a[i].save('./imgs/sinma/1%d.png' % (i), quality = 95)
		im_recog_b[i].save('./imgs/sinma/2%d.png' % (i), quality = 95)
	# 神魔画像判定
	path2 = './imgs/sinma/*.png'
	list = glob.glob(path2)
	l = 0
	for file in list:
		f = 1
		for i in range(0,8):
			if f == 1:
				img_rgb = cv2.imread(file)
				img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
				template = cv2.imread('./parts/sinma/10%d.png' % (i),0)
				res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
				threshold = 0.8
				loc = np.where( res >= threshold)
				z = 0
				for pt in zip(*loc[::-1]):
					if z == 0:
						# 第一神魔
						if l <= 2:
							sbk_1[l] = i
						# 第二神魔
						if l >= 3:
							sbk_2[l-3] = i
						f = 0
						l = l + 1
					z =+ 1
	print ("Shinma recognition complete!")


	""" TOP & 神魔カウント """
	for x in range(0,2):
		url_img = ('./imgs/gray/100%d.png' %(x+7))
		img = Image.open(url_img)
		# トリミング
		# TOP イノチとコンボ
		if x == 0:
			im_recog_a[0] = img.crop((114, 378 , 295 , 410))
			im_recog_a[1] = img.crop((145, 408 , 250 , 436))
			im_recog_b[0] = img.crop((530, 378 , 682 , 410))
			im_recog_b[1] = img.crop((554, 408 , 660 , 440))
		if x == 1:
			im_recog_a[0] = img.crop((302, 350 , 372 , 380))
			im_recog_a[1] = img.crop((302, 825 , 372 , 855))
			im_recog_b[0] = img.crop((535, 350 , 600 , 380))
			im_recog_b[1] = img.crop((535, 825 , 600 , 855))
		# トリミングした画像の保存
		for i in range(0,2):
			im_recog_a[i].save('imgs/score/3%d.png' % (i), quality = 95)
			im_recog_b[i].save('imgs/score/4%d.png' % (i), quality = 95)
		# 画像から数字を認識
		for i in range(0,2):
			result_a[i] = pytesseract.image_to_string(im_recog_a[i])
			result_b[i] = pytesseract.image_to_string(im_recog_b[i])

		""" 表示 [deepcopy]関数で各リストへ値を保存 """
		if x == 0:
			print ("-------------- TOP -----------")
			top_a = copy.deepcopy(result_a)
			top_b = copy.deepcopy(result_b)
			prin_top(top_a,top_b)
		if x == 1:
			print ("----------- 神魔カウント-------")
			prin_sinma(sbk_1,sbk_2)
			sin_a = copy.deepcopy(result_a)
			sin_b = copy.deepcopy(result_b)
			prin_sin(sin_a,sin_b)


	""" スプレッドシートに記録 [イノチ、コンボ、神魔武器、神魔カウント] """
	for top in range(1,3):
		if top == 1:
			cell_list_a = wks.range('C7:C8')
			cell_list_b = wks.range('D7:D8')
			result_aa = copy.deepcopy(top_a)
			result_bb = copy.deepcopy(top_b)
		if top == 2:
			cell_list_a = wks.range('C5:C6')
			cell_list_b = wks.range('D5:D6')
			result_aa = copy.deepcopy(sin_a)
			result_bb = copy.deepcopy(sin_b)
		# 各項目記録
		i = 0
		for cell in cell_list_a:
		    cell.value = format_result(result_aa[i])
		    i = i + 1
		i = 0
		for cell in cell_list_b:
		    cell.value = format_result(result_bb[i])
		    i = i + 1
		# 各アップデート
		wks.update_cells(cell_list_a)
		wks.update_cells(cell_list_b)


	""" 各貢献度 """
	for x in range(0,7):
		# 画像の読み込み
		url_img = ('./imgs/gray/100%d.png' %(x))
		img = Image.open(url_img)
		# トリミング
		# 味方の貢献度
		im_recog_a[0] = img.crop((160, 280 , 400 , 315))
		im_recog_a[1] = img.crop((160, 400 , 400 , 435))
		im_recog_a[2] = img.crop((160, 520 , 400 , 555))
		im_recog_a[3] = img.crop((160, 640 , 400 , 675))
		im_recog_a[4] = img.crop((160, 760 , 400 , 795))
		# 相手の貢献度
		im_recog_b[0] = img.crop((425, 280 , 660 , 315))
		im_recog_b[1] = img.crop((425, 400 , 660 , 435))
		im_recog_b[2] = img.crop((425, 520 , 660 , 555))
		im_recog_b[3] = img.crop((425, 640 , 660 , 675))
		im_recog_b[4] = img.crop((425, 760 , 660 , 795))
		# 味方の名前
		im_recog_m[0] = img.crop((172, 236 , 408 , 284))
		im_recog_m[1] = img.crop((172, 354 , 408 , 404))
		im_recog_m[2] = img.crop((172, 476 , 408 , 524))
		im_recog_m[3] = img.crop((172, 596 , 408 , 644))
		im_recog_m[4] = img.crop((172, 716 , 408 , 764))
		# トリミングした画像の保存
		for i in range(0,5):
			im_recog_a[i].save('./imgs/score/1%d.png' % (i), quality = 95)
			im_recog_b[i].save('./imgs/score/2%d.png' % (i), quality = 95)
			im_recog_m[i].save('./imgs/name/1%d.png'  % (i), quality = 95)
		# 画像から数字を認識
		for i in range(0,5):
			result_a[i] = pytesseract.image_to_string(im_recog_a[i])
			result_b[i] = pytesseract.image_to_string(im_recog_b[i])
		# 味方の名前を認識
		path2 = './imgs/name/*.png'
		list = glob.glob(path2)
		l = 0
		for file in list:
			f = 1
			for i in range(0,11):
				if f == 1:
					img_rgb = cv2.imread(file)
					img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
					template = cv2.imread('./parts/member/10%d.png' % (i),0)
					res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
					threshold = 0.8
					loc = np.where( res >= threshold)
					z = 0
					for pt in zip(*loc[::-1]):
						if z == 0:
							# その人に対応する番号を記録
							name_a[l] = i
							f = 0
							l = l + 1
						z =+ 1


		""" 表示 [deepcopy]関数で各リストへ値を保存 """
		if x == 0:
			print ("------------ イノチ -----------")
			in_a = copy.deepcopy(result_a)
			in_b = copy.deepcopy(result_b)
			prin(in_a,in_b)
		if x == 1:
			print ("------------- 回復 ------------")
			kf_a = copy.deepcopy(result_a)
			kf_b = copy.deepcopy(result_b)
			prin(kf_a,kf_b)
		if x == 2:
			print ("-------- 味方攻撃力支援 --------")
			mk_a = copy.deepcopy(result_a)
			mk_b = copy.deepcopy(result_b)
			prin(mk_a,mk_b)
		if x == 3:
			print ("-------- 味方防御力支援 --------")
			mb_a = copy.deepcopy(result_a)
			mb_b = copy.deepcopy(result_b)
			prin(mb_a,mb_b)
		if x == 4:
			print ("--------- 敵攻撃力妨害 ---------")
			tk_a = copy.deepcopy(result_a)
			tk_b = copy.deepcopy(result_b)
			prin(tk_a,tk_b)
		if x == 5:
			print ("--------- 敵防御力妨害 ---------")
			tb_a = copy.deepcopy(result_a)
			tb_b = copy.deepcopy(result_b)
			prin(tb_a,tb_b)
		if x == 6:
			print ("------------- コンボ ----------")
			kb_a = copy.deepcopy(result_a)
			kb_b = copy.deepcopy(result_b)
			prin(kb_a,kb_b)
		# 味方の順位表示
		prin_member(name_a, x)


	""" 各貢献度スプレッドシートに記録 """
	for main in range(1,8):
		if main == 1:
			cell_list_a = wks.range('C19:C23')
			cell_list_b = wks.range('E19:E23')
			result_aa = copy.deepcopy(in_a)
			result_bb = copy.deepcopy(in_b)
		if main == 2:
			cell_list_a = wks.range('C25:C29')
			cell_list_b = wks.range('E25:E29')
			result_aa = copy.deepcopy(kf_a)
			result_bb = copy.deepcopy(kf_b)
		if main == 3:
			cell_list_a = wks.range('C31:C35')
			cell_list_b = wks.range('E31:E35')
			result_aa = copy.deepcopy(mk_a)
			result_bb = copy.deepcopy(mk_b)
		if main == 4:
			cell_list_a = wks.range('C37:C41')
			cell_list_b = wks.range('E37:E41')
			result_aa = copy.deepcopy(mb_a)
			result_bb = copy.deepcopy(mb_b)
		if main == 5:
			cell_list_a = wks.range('C43:C47')
			cell_list_b = wks.range('E43:E47')
			result_aa = copy.deepcopy(tk_a)
			result_bb = copy.deepcopy(tk_b)
		if main == 6:
			cell_list_a = wks.range('C49:C53')
			cell_list_b = wks.range('E49:E53')
			result_aa = copy.deepcopy(tb_a)
			result_bb = copy.deepcopy(tb_b)
		if main == 7:
			cell_list_a = wks.range('C55:C59')
			cell_list_b = wks.range('E55:E59')
			result_aa = copy.deepcopy(kb_a)
			result_bb = copy.deepcopy(kb_b)
		# 各貢献度記録
		i = 0
		for cell in cell_list_a:
		    cell.value = format_result(result_aa[i])
		    i = i + 1
		i = 0
		for cell in cell_list_b:
		    cell.value = format_result(result_bb[i])
		    i = i + 1
		# 各貢献度アプッデート
		wks.update_cells(cell_list_a)
		wks.update_cells(cell_list_b)



""" ファイル名変更の際に照らし合わせに使う画像 """
def job(x):
	if x == 0:
		return ('./parts/job/in.png')
	if x == 1:
		return ('./parts/job/kf.png')
	if x == 2:
		return ('./parts/job/mk.png')
	if x == 3:
		return ('./parts/job/mb.png')
	if x == 4:
		return ('./parts/job/tk.png')
	if x == 5:
		return ('./parts/job/tb.png')
	if x == 6:
		return ('./parts/job/kb.png')
	if x == 7:
		return ('./parts/job/top.png')
	if x == 8:
		return ('./parts/job/sinma.png')

""" 画像のファイル名変更 [./img/*.PNG] """
# 画像の入れ替えがあった場合[1],変更無しの場合[0]を返す
def image_name():
	print ("1st step: image file check...")
	# ファイル内に追加された画像があるか確認
	if len(glob.glob('./img/*')) >= 10:
		path  = './img/*.png'
		path2 = './img/*.PNG'
		path3 = './img/'
		i = 0
		# 判定する次の画像[.PNG]が9枚あるか確認
		list = glob.glob(path2)
		if len(list) == 9:
			# 前回使用した画像[.png]が1枚以上あるか確認し削除
			list = glob.glob(path)
			if len(list) >= 1:
				for file in list:
					print file
					os.remove(file)
				print ("[.png] all files deleted.")
			# ファイル名の一括変更 [.PNG, .jpg, .jpeg]
			for m in range(0,3):
				if m == 0:
					path2 = './img/*.PNG'
				if m == 1:
					path2 = './img/*jpg'
				if m == 2:
					path2 = './img/*jpeg'
				list = glob.glob(path2)
				for file in list:
					f = 1
					for i in range(0,9):
						if f == 1:
							img_rgb = cv2.imread(file)
							img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
							template = cv2.imread(job(i),0)
							res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
							threshold = 0.8
							loc = np.where( res >= threshold)
							z = 0
							for pt in zip(*loc[::-1]):
								if z == 0:
									os.rename(file, './img/10' + str(i) + '.png')
									print (file + " is rename " + './img/10' + str(i) + '.png')
									f = 0
								z =+ 1
	  		print ("images name change ok!!")
	  	else:
	  		# ファイル内の画像が9枚以上で新しく判定したい画像が9枚ぴったりなければ[.PNG]画像を全削除
	  		print ("There are not 9 [.PNG] images.")
	  		print ("Because there are not enough images, delete unnecessary images.")
	  		list = glob.glob(path2)
	 		if len(list) >= 1:
	 			print ("delete images...")
				for file in list:
					print file
					os.remove(file)
	# ファイル内9枚以内で名前変更していない画像があれば変更
	if len(glob.glob('./img/*')) < 10:
		# ファイル名の一括変更 [.PNG, .jpg, .jpeg]
		for m in range(0,3):
			if m == 0:
				path2 = './img/*.PNG'
			if m == 1:
				path2 = './img/*jpg'
			if m == 2:
				path2 = './img/*jpeg'
			list = glob.glob(path2)
			for file in list:
				f = 1
				for i in range(0,9):
					if f == 1:
						img_rgb = cv2.imread(file)
						img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
						template = cv2.imread(job(i),0)
						res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
						threshold = 0.8
						loc = np.where( res >= threshold)
						z = 0
						for pt in zip(*loc[::-1]):
							if z == 0:
								os.rename(file, './img/10' + str(i) + '.png')
								print (file + " is rename " + './img/10' + str(i) + '.png')
								f = 0
							z =+ 1
	else:
		print ("Image file, no change.")


""" 貢献度表のクリア """
# [0]:味方貢献度 [1]:敵貢献度 [2]:敵味方ナイトメア
def clear_contribution(x):
	for i in range(0,x):
		if i == 0:
			cell_list = wks.range('C19:C59')
		if i == 1:
			cell_list = wks.range('E19:C59')
		if i == 2:
			cell_list = wks.range('B11:E17')
		for cell in cell_list:
			cell.value = ""
			slp()
		wks.update_cells(cell_list)

# [0]:相手ギルド名 [1]:神魔やイノチ、コンボ [2]:相手の名前 [3]:味方の名前
def clear_name(p):
	for i in range(0,p):
		if i == 0:
			wks.update_cell(4,4, u'')
			slp()
		if i == 1:
			cell_list = wks.range('B5:D8')
			for cell in cell_list:
				cell.value = ""
				slp()
			wks.update_cells(cell_list)
		if i == 2:
			cell_list = wks.range('D19:D59')
			for cell in cell_list:
				cell.value = ""
				slp()
			wks.update_cells(cell_list)
		if i == 3:
			cell_list = wks.range('B19:B59')
			for cell in cell_list:
				cell.value = ""
				slp()
			wks.update_cells(cell_list)



""" 間違えて認識した[.]を[,]に置換 """
def format_result(result):
	text = str(result)
	text = re.sub(r'[.]', ",", text)
	return text

""" API呼び出し10毎に1.5秒sleep """
def slp():
	global t
	t = t + 1
	if t >= 10:
		time.sleep(1.5)
		print ("sleep...")
		t = t - 10

""" cmdに分かり易く表示 """
def prin(x,y):
	for i in range(1,6):
		zyuni  = "%d位:" % i
		mikata = ('{:>10}'.format(format_result(x[i-1])))
		teki   = ('{:>10}'.format(format_result(y[i-1])))
		k      = "   "
		p      = zyuni + mikata + k + teki
		print p

# イノチとコンボ表示
def prin_top(x,y):
	for i in range(1,3):
		if i == 1:
			zyuni  = "イノチ:"
			mikata = ('{:>10}'.format(format_result(x[i-1])))
			teki   = ('{:>10}'.format(format_result(y[i-1])))
			k      = "   "
			p      = zyuni + mikata + k + teki
		if i == 2:
			zyuni  = "コンボ:"
			mikata = ('{:>10}'.format(format_result(x[i-1])))
			teki   = ('{:>10}'.format(format_result(y[i-1])))
			k      = "   "
			p      = zyuni + mikata + k + teki
		print p

# 神魔の表示
def prin_sin(x,y):
	for i in range(1,3):
		zyuni  = "第%d神魔:" % i
		mikata = ('{:>6}'.format(format_result(x[i-1])))
		teki   = ('{:>3}'.format(format_result(y[i-1])))
		k      = " vs "
		p      = zyuni + mikata + k + teki
		print p

""" 神魔、ギルメンの画像判定に必要な部分 """
# 神魔
def prin_sinma(x,y):
	shin1_1 = shinma(x[0])
	shin1_2 = shinma(x[1])
	shin1_3 = shinma(x[2])
	shin2_1 = shinma(y[0])
	shin2_2 = shinma(y[1])
	shin2_3 = shinma(y[2])
	shinma1 = shin1_1 + shin1_2 + shin1_3
	shinma2 = shin2_1 + shin2_2 + shin2_3
	print "第1神魔:" + shinma1
	print "第2神魔:" + shinma2
	wks.update_cell(5,2, shinma1)
	wks.update_cell(6,2, shinma2)

# ギルドメンバー
def prin_member(x, y):
	result = [''] * 5
	member_a[0] = member(x[0])
	member_a[1] = member(x[1])
	member_a[2] = member(x[2])
	member_a[3] = member(x[3])
	member_a[4] = member(x[4])
	member_zyuni = member_a[0] + member_a[1] + member_a[2] + member_a[3] + member_a[4]
	print "味方順位:" + member_zyuni
	# スプレッドシートに記録
	if y == 0:
		cell_list_a = wks.range('B19:B23')
		result = copy.deepcopy(member_a)
	if y == 1:
		cell_list_a = wks.range('B25:B29')
		result = copy.deepcopy(member_a)
	if y == 2:
		cell_list_a = wks.range('B31:B35')
		result = copy.deepcopy(member_a)
	if y == 3:
		cell_list_a = wks.range('B37:B41')
		result = copy.deepcopy(member_a)
	if y == 4:
		cell_list_a = wks.range('B43:B47')
		result = copy.deepcopy(member_a)
	if y == 5:
		cell_list_a = wks.range('B49:B53')
		result = copy.deepcopy(member_a)
	if y == 6:
		cell_list_a = wks.range('B55:B59')
		result = copy.deepcopy(member_a)
	i = 0
	for cell in cell_list_a:
	    cell.value = result[i]
	    i = i + 1
	# 各貢献度アプッデート
	wks.update_cells(cell_list_a)

# 神魔
def shinma(x):
	if x == 0:
		return "楽器"
	if x == 1:
		return "魔書"
	if x == 2:
		return "祈祷"
	if x == 3:
		return "刀"
	if x == 4:
		return "槍"
	if x == 5:
		return "槌"
	if x == 6:
		return "弓"
	if x == 7:
		return "魔具"
# ギルドメンバー
def member(x):
	if x == 0:
		return "ゲスまる氏"
	if x == 1:
		return "ヨリト"
	if x == 2:
		return "96黒"
	if x == 3:
		return "秘書"
	if x == 4:
		return "すぎゅ"
	if x == 5:
		return "ゲスゆんモフ丸"
	if x == 6:
		return "ひつじ"
	if x == 7:
		return "れみ"
	if x == 8:
		return "*＊凛＊*"
	if x == 9:
		return "(ゲωス)ぬぅ氏"
	if x == 10:
		return "げすぅ"



""" メイン """
if __name__ == '__main__':
	"""　Google Sheets連携 """
	scope = ['https://spreadsheets.google.com/feeds',
			 'https://www.googleapis.com/auth/drive']
	# 権限の受け渡し＆認証 [.json]ファイル
	credentials = ServiceAccountCredentials.from_json_keyfile_name('test-5eda83f2e6e5.json', scope)
	gc = gspread.authorize(credentials)
	# 記入したいスプレッドシートの名前を入れる
	wks = gc.open('suge-oukoku').sheet1
	# スプレッドシートに記録の準備合図
	wks.update_cell(1,1, u'SHINoALICE')


	""" 表のクリア """
	# [1]:相手ギルド名 [2]:神魔やイノチ、コンボ [3]:相手の名前 [4]:味方の名前
	#clear_name(4)
	# [1]:味方貢献度 [2]:敵貢献度 [3]:敵味方ナイトメア
	#clear_contribution(3)



	""" 記録 """
	record()

	""" 記録終了 """
	wks.update_cell(1,1, u'')
	
