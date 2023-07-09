import efinance as ef 

import pandas as pd
import numpy as np

stockCode = '601318'

def GetRemoteData(stCode):
    df = ef.stock.get_quote_history(stCode)
    print(df)
    np_data= []
    for index,row in df.iterrows():
        st=[row.iloc[2],row.iloc[3],row.iloc[4],row.iloc[5],row.iloc[6],row.iloc[7],row.iloc[8],row[12]]
        np_data.append(st)

    nfdata = np.array(np_data)

    #日期 开盘 结束 最高 最低
    save = pd.DataFrame(nfdata, columns = ['Date','Open','Close', 'High', 'Low','Turnover','TsVolume','ExhcangeRate'])

    print(save)
    csvName = stCode+".a.csv"
    save.to_csv('C:\\Users\\Administrator\\Desktop\\gp\\'+csvName,index=False)

GetRemoteData(stockCode)
