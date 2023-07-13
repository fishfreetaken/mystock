import pandas as pd
import numpy as np
import math

#csvfilename='601318.a.sub.csv'
#data = pd.read_csv('0939.HK.csv')

class StackReader:
    csvfilename = '002475.a.sub.csv'
    rawdata = pd.DataFrame
    buyTimes = 50       #购买和卖出的次数
    colunmName='Low'
    rowsnums = 0

    stackMoney = 100000
    stacknums = 100000  #购买的票数

    resetMoney = 0

    bonus= 5  #手续费
    def __init__(self,filename,money) -> None:
        self.csvfilename = filename
        self.stackMoney = money
        self.resetMoney = money
        self.rawdata = pd.read_csv(self.csvfilename)
        self.rowsnums = self.rawdata[self.colunmName].size
        #print('init' ,self.rawdata)

    def reset(self):
        #print("stacknum:%f stackmoney:%f" %(self.stacknums,self.stackMoney))
        self.stackMoney = self.resetMoney
        self.stacknums = 0
    
    def get_buy_price(self,i):
        prevalue= self.rawdata['Open'][i] - (self.rawdata['High'][i-1]-self.rawdata['Low'][i-1])/2
        if prevalue < self.rawdata['Low'][i]:
                prevalue = self.rawdata['Close'][i]
        return prevalue

    def get_sale_price(self,i):
        salenum = self.rawdata['Open'][i] + (self.rawdata['High'][i-1]-self.rawdata['Low'][i-1])/2 
        if salenum > self.rawdata['High'][i]:
            salenum =  self.rawdata['Close'][i]
        return salenum
    
    def buy_all(self,price):
        fltnum,tagnum = math.modf(self.stackMoney /(100 * price))
        self.stacknums += tagnum*100
        self.stackMoney = fltnum *100* price
        print("buy all price:%f ft:%f tag:%f tacknum:%f money:%f"%(price,fltnum,tagnum,self.stacknums,self.stackMoney))

    def sale_all(self,price):
        self.stackMoney += self.stacknums * price - (self.stacknums * price/200) 
        self.stacknums  = 0
        

    def Cp(self):
        self.reset()
        preValue =0
        st = np.random.randint(0,self.rowsnums,self.buyTimes)
        st.sort()
        for i in st:
            if i==0 :
                continue
            if preValue == 0:
                preValue= self.get_buy_price(i)
                self.buy_all(preValue)
            if preValue > 0:
                salevalue = self.get_sale_price(i)
                self.sale_all(salevalue)
                preValue=0
        print("premoney:%f last money:%f "%(self.resetMoney,self.stackMoney))
        return self.stackMoney

    def GetFirstValue(self):
        return self.rawdata[self.colunmName].mean()

    def CpGetIter(self):
        cycleNum = 1
        reslist =[]
        for i in range(cycleNum):
            v = self.Cp()
            reslist.append(v)

        sp = np.array(reslist)

        resavg = float(np.average(sp))
        resavgpercent = float(resavg*100/self.GetFirstValue())

        print('new sp ',sp)
        print('avg:%f persent::%2f firstvalue:%f' % (resavg,resavgpercent,self.GetFirstValue()))

    def IterAllgo(self,interval,averageStep):
        preValue = 0
        cnt=0
        mincnt =0 
        bigcnt=0

        preaverage=[]
        for i in range (1,self.rowsnums):
            if len(preaverage) >= averageStep :
                del preaverage[0]
            preaverage.append(self.rawdata['Open'][i-1]  - self.rawdata['Close'][i-1])
            if len(preaverage) < averageStep :
                continue
            
            if preValue ==0:
                atf =np.array(preaverage)
                if atf.mean() <= 0 :
                    continue          
                #print('date:%s atf value:%f'% (data['Date'][0],atf.mean())) 
                preValue = self.get_buy_price(i)
                self.buy_all(preValue)
            elif cnt >= interval :
                saleprivace = self.get_sale_price(i)
                self.sale_all(saleprivace)
                #print('data:%s dif:%f bnusP:%f pValue:%f salePri:%f Open:%f High:%f Low:%f'% (data['Date'][i],saleprivace - preValue,(saleprivace - preValue)*100/data['Open'][i],preValue,saleprivace,data['Open'][i],data['High'][i],data['Low'][i] ))
                if saleprivace - preValue < 0 :
                    mincnt+=1
                else :
                    bigcnt+=1
                preValue = 0
                cnt = 0
            else :
                cnt+=1
        resavgpercent = float(sum*100/self.GetFirstValue())
        print('interval:%d sum:%f imporve:%f mincnt:%d bigcnt:%d'% (interval, sum,resavgpercent,mincnt,bigcnt))


    def StaticInfo(self):
        ratearry=[]
        for idx,raw in self.rawdata.iterrows():
            rate = (raw['Close'] - raw['Open'] )*100/ raw['Open']
            if rate <0 :
                rate = 0 - rate 
            ratearry.append(rate)
        lt= pd.Series(ratearry)
        print('average amplitute :%f fx:%f' % (lt.mean(),lt.var()))
        avermean = lt.mean()
        preValue = 0 
        #假如我超过了平均的增值振幅我就买，超过平均跌幅我就卖
        sum=0
        mincnt=0
        bigcnt=0

        begindate=""
        for i in range (1,self.rowsnums):
            rate = (self.rawdata['Close'][i-1] - self.rawdata['Open'][i-1] )*100/ self.rawdata['Open'][i-1]
            if preValue == 0 and rate > 0 and rate >=  avermean:
                preValue = self.rawdata['Open'][i]
                begindate=self.rawdata['Date'][i]
            if preValue > 0 and rate < 0 and (0-rate) >= avermean: 
                saleprivace = self.rawdata['Open'][i]
                sum += saleprivace - preValue
                if saleprivace - preValue < 0 :
                    mincnt+=1
                else :
                    bigcnt+=1
                print("begin:%s end:%s diff:%f rate:%f  sale:%f prevalue:%f"%(begindate,self.rawdata['Date'][i],saleprivace - preValue, rate,saleprivace,preValue))
                preValue=0
        
        print("sum:%f mincnt:%d bigcnt:%d"%(sum,mincnt,bigcnt))


#for i in range(1,30):
#    IterAllgo(i,7)



st = StackReader('002475.a.sub.csv',10000)
st.CpGetIter()
