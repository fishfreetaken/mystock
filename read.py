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
    stacknums = 0   #购买的票数

    const_resetMoney = 0

    bonus= 5  #手续费

    stackcoder=""

    buy_price = 0 #购买成本价

    sale_interval = 0

    sale_inc_percent = 0  # 达到多少涨幅买入
    sale_desc_percent= 0  # 达到多少降幅卖出

    def __init__(self,filename,money,inc_p,desc_p) -> None:
        self.csvfilename = filename
        self.stackcoder = filename.split(',')[0]
        self.sale_inc_percent = inc_p 
        self.sale_desc_percent = desc_p
        if money !=0 :
            self.stackMoney = money
            self.const_resetMoney = money
        
        self.rawdata = pd.read_csv(self.csvfilename)
        self.rowsnums = self.rawdata[self.colunmName].size
        #print('init' ,self.rawdata)


    def getstackcoder(self):
        return self.stackcoder

    def reset(self):
        #print("stacknum:%f stackmoney:%f" %(self.stacknums,self.stackMoney))
        self.stackMoney = self.const_resetMoney
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

    def get_sale_price_from_buy(self,buy_price,i):
        if self.sale_inc_percent == 0 :
            return 0
        targetprice = buy_price*(1+self.sale_inc_percent/100)
        if  self.rawdata['High'][i] > buy_price and self.rawdata['High'][i]  > targetprice :
            return targetprice 
        return 0 

    def can_buy(self,price):
        #策略1 根据历史的值生成一个
        #策略2 根据之前买进的价格进行补充
        return True 

    def can_sel(self,price):
        #简单策略，盈利百分之多少
        return True
    
    def debug_last_info(self):
        res = "last money:%f lastpercent:%f"%(self.stackMoney,self.stackMoney*100/self.const_resetMoney)
        return res
     
    def buy_all(self,price):
        fltnum,tagnum = math.modf(self.stackMoney /(100 * price))
        self.stacknums += tagnum*100
        self.stackMoney = fltnum *100* price
        #print("buy all price:%f resft:%f restag:%f stacknum:%f money:%f"%(price,fltnum,tagnum,self.stacknums,self.stackMoney))

    def sale_all(self,price):
        self.stackMoney += self.stacknums * price - (self.stacknums * price/200) 
        self.stacknums  = 0
        return 0

    def Cp(self):
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
        return self.stackMoney

    def CpGetIter(self):
        cycleNum = 10
        reslist =[]
        for i in range(cycleNum):
            v = self.Cp()
            reslist.append(v)
            print(i,self.debug_last_info())

        sp = np.array(reslist)
        print('resavg:%f new sp ',float(np.average(sp)),sp)


    def CanSale(self,cnt,i):
        return True

    def Salelastday(self):
        lasprice = self.rawdata['Open'].loc(self.rowsnums-1)\
        

    def IterAllgo(self,interval,averageStep,beginday,sawdf1):
        self.sale_interval = interval
        preValue = 0
        cnt=0
        mincnt =0 
        bigcnt=0
        self.reset()

        preaverage=[]
        #给一个随机的开始时间
        for i in range (beginday,self.rowsnums):
            if len(preaverage) >= averageStep :
                del preaverage[0]
            preaverage.append(self.rawdata['Open'][i-1]  - self.rawdata['Close'][i-1])
            if len(preaverage) < averageStep :
                continue
            if preValue == 0:
                atf = np.array(preaverage)
                if atf.mean() <= 0 :
                    continue
                preValue = self.get_buy_price(i)
                self.buy_all(preValue)
                print(preaverage,'date:%s atf value:%f buyprice:%f'% (self.rawdata['Date'][0],atf.mean(),preValue)) 
            else : 
                #进行策略变更，如果涨幅原来的的多少可以卖
                #saleprivace = self.get_sale_price(i)
                saleprivace = self.get_sale_price_from_buy(preValue,i)
                if  saleprivace > 0 :
                    self.sale_all(saleprivace)
                    if saleprivace - preValue < 0 :
                        mincnt+=1
                    else :
                        bigcnt+=1
                    cnt = 0

                    print('stackmoney:%f data:%s dif:%f bnusP:%f pValue:%f salePri:%f Open:%f High:%f Low:%f'% (self.stackMoney,self.rawdata['Date'][i],saleprivace - preValue,(saleprivace - preValue)*100/self.rawdata['Open'][i],preValue,saleprivace,self.rawdata['Open'][i],self.rawdata['High'][i],self.rawdata['Low'][i] ))
                    preValue=0
                else :
                    cnt+=1
        #最后没有卖掉的按照最后一天的开盘价卖掉


        sawdf1.loc[len(sawdf1)] = [str(averageStep),str(interval),str(mincnt),str(bigcnt),round(self.stackMoney,2),round(self.stackMoney*100/self.const_resetMoney,2)]
        return ('averageStep:%d interval:%d mincnt:%d bigcnt:%d res:%s'% (averageStep,interval,mincnt,bigcnt,self.debug_last_info()))


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


def SaveDataFramAsCsv(rawdf,filename):
    prefix='C:\\Users\\Administrator\\Desktop\\gp\\'
    rawdf.to_csv(prefix+filename,index = False)

stackcode = '600036'
#stackcode = '002475'
appendtext = '.a.sub.csv'

def RandbeginTimeTop5(st,interval=10,step=10,beginoffset =1, bSaveFile =False):
    sawdf1 = pd.DataFrame(columns=['Step','Interval','micnt','bigcnt','lastmoney','percent'])
    for i in range(1,step):
        #for j in range(1,interval):
        st.IterAllgo(0,i,beginoffset,sawdf1)
    

    print(sawdf1)
    lastmoney_sort_sawdf = sawdf1.sort_values(by=['lastmoney'],ascending=[False])
    if bSaveFile :
        SaveDataFramAsCsv(sawdf1,st.getstackcoder()+".totalcount."+appendtext)
        SaveDataFramAsCsv(lastmoney_sort_sawdf,st.getstackcoder()+".totalcount.sort."+appendtext)
    
    print('beginoffset',beginoffset,'after sort',lastmoney_sort_sawdf.head(5))


#boffset = np.random.randint(1,30)
st = StackReader(stackcode +appendtext,100000,30,0)
for i in range(4,45):
    RandbeginTimeTop5(st,22,17,i)
    print("========cutlint=========\n")
    break