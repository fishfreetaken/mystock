import pandas as pd
import numpy as np

csvfilename='002475.a.sub.csv'
#csvfilename='601318.a.sub.csv'
#data = pd.read_csv('0939.HK.csv')
data = pd.read_csv(csvfilename)
#data.info()
stackNum = 10000    
buyTimes = 20       #购买和卖出的次数
colunmNmae='Low'

def Cp(col):
    sum = 0
    preValue =0 
    si = data[col].size
    
    st = np.random.randint(0,si,buyTimes)
    st.sort()
    for i in st:
        if i==0 :
            continue
        if preValue ==0:
           preValue= data['Open'][i] - (data['High'][i-1]-data['Low'][i-1])/2
           if preValue < data['Low'][i]:
               preValue = data['Close'][i]
        else:
            tpv = data['Open'][i] + (data['High'][i-1]-data['Low'][i-1])/2 
            if tpv > data['High'][i]:
                tpv =  data['Close'][i]
            sum += tpv - preValue 
            preValue = 0
    
    return sum

def GetFirstValue(col):
    return data[col][data['Date'].size-1]

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

    #print("dsaj:%d %f"%(12,1.23))
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
        preaverage.append(data['Open'][i]  - data['Close'][i])
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

for i in range(1,30):
    IterAllgo(i,7)