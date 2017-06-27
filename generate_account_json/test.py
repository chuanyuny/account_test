#-*- coding:utf-8 -*-
'''0003 账户状态规则集成测试'''
'''具体的账户状态等于时，设为呆账还是正常根据具体情况修改代码'''
'''测试测试'''
import unittest
import itertools
import json
import codecs
import sys
from HTMLTestRunner import HTMLTestRunner
import time

reload(sys)
sys.setdefaultencoding('utf8')

class Countstatus(unittest.TestCase):

	def setUp(self):
		self.dk_status=['等于','不等于']
		self.djk_status=['等于','不等于']
		self.zdjk_status=['等于','不等于']
		self.yu_huo1=['与','或']
		self.yu_huo2=['与','或']
		self.account_status=['贷款账户状态','准贷记卡账户状态','贷记卡账户状态']
		self.eq_or_not=['等于','不等于']

	def read_json(self,path):
		f=open(path,'r')
		b=json.load(f)
		# jsondata=json.dumps(b,ensure_ascii=False,indent=4).encode('utf-8')
		f.close()
		return b

	def dk(self,dic,dk_status):
		if dk_status=='等于':
			dic['truPort']['loans'][0]['loan']['accountType']='dkdkdk'
		elif dk_status=='不等于':
			dic['truPort']['loans'][0]['loan']['accountType']='dkdkdk2'
		return dic


	def djk(self,dic,djk_status):
		if djk_status=='等于':
			dic['truPort']['loanCards'][0]['loanCard']['accountType']='djkdjkdjk'
		elif djk_status=='不等于':
			dic['truPort']['loanCards'][0]['loanCard']['accountType']='djkdjkdjk2'
		return dic

	def zdjk(self,dic,zdjk_status):
		if zdjk_status=='等于':
			dic['truPort']['allowLoanCards'][0]['allowCard']['accountType']='zdjkzdjk'
		elif zdjk_status=='不等于':
			dic['truPort']['allowLoanCards'][0]['allowCard']['accountType']='zdjkzdjk2'
		return dic

	def reset_dict(self,dic):
		dic['truPort']['loans'][0]['loan']['accountType']='正常(销户)'
		dic['truPort']['loanCards'][0]['loanCard']['accountType']='正常'
		dic['truPort']['allowLoanCards'][0]['allowCard']['accountType']='正常(销户)'

	def test_1(self):
		'''针对整个规则修改并产生新的json的所有可能情况'''
		listall=[] #所有可能性的json,共32种可能性，列表的每个元素都是一种可能性,是dict格式。
		b=self.read_json('testdata.json') #b是一个dict
		# loans_account=b['truPort']['loans'][0]['loan']['accountType'] # 贷款
		# loancards_account=b['truPort']['loanCards'][0]['loanCard']['accountType'] #贷记卡
		# allowloadcards_account=b['truPort']['allowLoanCards'][0]['allowCard']['accountType']  #准贷记卡

		templist1=list(itertools.product(self.dk_status,self.yu_huo1,self.djk_status,self.yu_huo2,self.zdjk_status))
		for each in templist1:
			self.reset_dict(b)
			# print each[0],each[1],each[2],each[3],each[4]
			if each[1]=='与' and each[3]=='与':
				dk_dict=self.dk(b,each[0])
				djk_dict=self.djk(dk_dict,each[2])
				zdjk_dict=self.zdjk(djk_dict,each[4])
				listall.append(zdjk_dict)
				print json.dumps(each,ensure_ascii=False,indent=4)
				print zdjk_dict['truPort']['loans'][0]['loan']['accountType']
				print zdjk_dict['truPort']['loanCards'][0]['loanCard']['accountType']
				print zdjk_dict['truPort']['allowLoanCards'][0]['allowCard']['accountType']
				continue
			elif each[1]=='与' and each[3]=='或':
				zdjk_dict=self.zdjk(b,each[4])
				listall.append(zdjk_dict)
				print json.dumps(each,ensure_ascii=False,indent=4)
				print zdjk_dict['truPort']['loans'][0]['loan']['accountType']
				print zdjk_dict['truPort']['loanCards'][0]['loanCard']['accountType']
				print zdjk_dict['truPort']['allowLoanCards'][0]['allowCard']['accountType']
				continue
			elif each[1]=='或' and each[3]=='与':
				dk_dict=self.dk(b,each[0])
				listall.append(dk_dict)
				print json.dumps(each,ensure_ascii=False,indent=4)
				print dk_dict['truPort']['loans'][0]['loan']['accountType']
				print dk_dict['truPort']['loanCards'][0]['loanCard']['accountType']
				print dk_dict['truPort']['allowLoanCards'][0]['allowCard']['accountType']
				continue
			elif each[1]=='或' and each[3]=='或':
				dk_dict=self.dk(b,each[0])
				listall.append(dk_dict)
				print json.dumps(each,ensure_ascii=False,indent=4)
				print dk_dict['truPort']['loans'][0]['loan']['accountType']
				print dk_dict['truPort']['loanCards'][0]['loanCard']['accountType']
				print dk_dict['truPort']['allowLoanCards'][0]['allowCard']['accountType']
				continue
		# print listall[0]
		print '一共有%d种可能性'%len(listall)	
		# print json.dumps(listall[0],ensure_ascii=False,indent=4)

	def test_2(self):
		'''只针对一个条件修改并产生新的json'''
		listeach=[]
		c=self.read_json('testdata.json')
		tempeach=list(itertools.product(self.account_status,self.eq_or_not))
		for each in tempeach:
			self.reset_dict(c)
			if each[0]=='贷款账户状态':
				dict1=self.dk(c,each[1])
				listeach.append(dict1)
				print each[0],each[1]
				print dict1['truPort']['loans'][0]['loan']['accountType']
				continue
			elif each[0]=='准贷记卡账户状态':
				dict2=self.zdjk(c,each[1])
				listeach.append(dict2)
				print each[0],each[1]
				print dict2['truPort']['allowLoanCards'][0]['allowCard']['accountType']
				continue
			elif each[0]=='贷记卡账户状态':
				dict3=self.djk(c,each[1])
				listeach.append(dict3)
				print each[0],each[1]
				print dict3['truPort']['loanCards'][0]['loanCard']['accountType']
				continue
		# print json.dumps(listeach[0],ensure_ascii=False,indent=4)


if __name__=='__main__':
	# unittest.main()
	suite=unittest.TestSuite()
	suite.addTest(Countstatus("test_1"))
	suite.addTest(Countstatus("test_2"))
	# runner=unittest.TextTestRunner()
	# runner.run(suite)
	now=time.strftime("%Y-%m-%d %H_%M_%S")
	filename='./'+now+'result.html'
	fp=open(filename,'wb')
	runner=HTMLTestRunner(stream=fp,title='账户测试报告',description='用例执行情况：')
	runner.run(suite)
	fp.close()
	



