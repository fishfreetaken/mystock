import pandas as pd
import numpy as np

#csvfilename='601318.a.sub.csv'
#data = pd.read_csv('0939.HK.csv')


class Reader:
    csvfilename = '002475.a.sub.csv'
    rawdata = pd.DataFrame
    buyTimes = 20       #购买和卖出的次数
    colunmNmae='Low'
    rowsnums = 0

    stackMoney = 100000
    stacknums = 0  #购买的票数

    bonus= 5  #手续费
    def __init__(self,filename,money) -> None:
        self.csvfilename = filename
        self.stackMoney = money
        self.rawdata = pd.read_csv(self.csvfilename)
        self.rowsnums = self.rawdata[self.colunmNmae].size

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
        self.stacknums += self.stackMoney / price
        self.stackMoney = self.stackMoney % price
    def sale_all(self,price):
        self.stackMoney += self.stacknums * price
        self.stackMoney -= (self.stacknums * price)*5 
        self.stacknums  = 0

    def Cp(self):
        sum = 0
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
                preValue=0
                salevalue = self.get_sale_price(i)
                self.sale_all(salevalue)
        return

    def GetFirstValue(self,col):
        return self.rawdata[self.colunmNmae].last()

    def CpGetIter():
        cycleNum = 100
        reslist =[]
        for i in range(cycleNum):
            v = Cp(colunmNmae)
            reslist.append(v)

        sp = np.array(reslist)

        resavg = float(np.average(sp))
        resavgpercent = float(resavg*100/GetFirstValue(colunmNmae))
        print('new sp',sp)

        print('avg:%f persent::%2f firstvalue:%f' % (resavg,resavgpercent,GetFirstValue(colunmNmae)))

def IterAllgo(interval , averageStep):
    si = data['Date'].size
    preValue = 0
    sum =0 
    cnt=0
    mincnt =0 
    bigcnt=0

    preaverage=[]
    for i in range (1,si):
        if len(preaverage) >= averageStep :
            del preaverage[0]
        preaverage.append(data['Open'][i-1]  - data['Close'][i-1])
        if len(preaverage) < averageStep :
            continue
        
        if preValue ==0:
            atf =np.array(preaverage)
            if atf.mean() <= 0 :
                continue          
            #print('date:%s atf value:%f'% (data['Date'][0],atf.mean())) 
            preValue = data['Open'][i] - (data['High'][i-1]-data['Low'][i-1])*2/3
            if preValue < data['Low'][i]:
               preValue = data['Close'][i]
        
        if cnt >= interval and preValue > 0 :
            saleprivace = data['Open'][i] + (data['High'][i-1]-data['Low'][i-1])*2/3 
            if saleprivace > data['High'][i]:
                saleprivace =  data['Close'][i]
                #print('exceed max hight data:%s '% (data['Date'][i]))

            sum += saleprivace - preValue 
            #print('data:%s dif:%f bnusP:%f pValue:%f salePri:%f Open:%f High:%f Low:%f'% (data['Date'][i],saleprivace - preValue,(saleprivace - preValue)*100/data['Open'][i],preValue,saleprivace,data['Open'][i],data['High'][i],data['Low'][i] ))
            if saleprivace - preValue < 0 :
                mincnt+=1
            else :
                bigcnt+=1
            preValue = 0
            cnt = 0
        else :
            cnt+=1
    resavgpercent = float(sum*100/GetFirstValue(colunmNmae))
    print('interval:%d sum:%f imporve:%f mincnt:%d bigcnt:%d'% (interval, sum,resavgpercent,mincnt,bigcnt))

print(data)

def CpValue2PreValue(i):
    preValue = data['Open'][i] - (data['High'][i-1]-data['Low'][i-1])*2/3
    if preValue < data['Low'][i]:
        preValue = data['Close'][i]
    return preValue
def CpValue2SaleValue(i):
    saleprivace = data['Open'][i] + (data['High'][i-1]-data['Low'][i-1])*2/3 
    if saleprivace > data['High'][i]:
        saleprivace =  data['Close'][i]
    return saleprivace

def StaticInfo():
    si = data['Date'].size
    ratearry=[]
    for idx,raw in data.iterrows():
        rate = (raw['Close'] - raw['Open'] )*100/ raw['Open']
        if rate <0 :
            rate = 0 -rate 
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
    for i in range (1,si):
        rate = (data['Close'][i-1] - data['Open'][i-1] )*100/ data['Open'][i-1]
        if preValue == 0 and rate > 0 and rate >=  avermean:
            preValue = data['Open'][i]
            begindate=data['Date'][i]
        if preValue > 0 and rate < 0 and (0-rate) >= avermean: 
            saleprivace = data['Open'][i]
            sum += saleprivace - preValue
            if saleprivace - preValue < 0 :
                mincnt+=1
            else :
                bigcnt+=1
            print("begin:%s end:%s diff:%f rate:%f  sale:%f prevalue:%f"%(begindate,data['Date'][i],saleprivace - preValue, rate,saleprivace,preValue))
            preValue=0
    
    print("sum:%f mincnt:%d bigcnt:%d"%(sum,mincnt,bigcnt))

StaticInfo()
#for i in range(1,30):
#    IterAllgo(i,7)