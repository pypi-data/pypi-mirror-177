# -*- coding: utf-8 -*-
"""
本模块功能：中国股市估值
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#屏蔽所有警告性信息
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
from siat.common import *
from siat.translate import *
from siat.grafix import *
from siat.security_prices import *

#==============================================================================

if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    measure='pb'; method='lyr'; value='value'; statistic='median'

def get_valuation_market_china(start,end,measure='pe',method='lyr',value='value',statistic='median'):
    """
    功能：中国A股市场估值趋势，一段时间内
    measure：默认市盈率'pe'，可选市净率pb
    method：默认滚动'ttm'，可选静态lyr
    value：默认数值'value'，可选分位数quantile
    statistic：默认使用中位数'median'，可选等权重equal-weighted
    """
    
    #检查日期的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(get_valuation_market_china): invalid date period",start,end)
        return None
    
    #检查选项
    measure1=measure.lower(); measurelist=['pe','pb']
    method1=method.lower(); methodlist=['ttm','lyr']
    value1=value.lower(); valuelist=['value','quantile']
    statistic1=statistic.lower(); statisticlist=['median','equal-weighted']
    
    if not (measure1 in measurelist):
        print("  #Error(get_valuation_market_china): invalid measurement",measure)
        print("  Valid measurement:")
        return None
    if not (method1 in methodlist):
        print("  #Error(get_valuation_market_china): invalid method",method)
        print("  Valid method:",methodlist)
        return None    
    if not (value1 in valuelist):
        print("  #Error(get_valuation_market_china): invalid value",value)
        print("  Valid value:",valuelist)
        return None
    if not (statistic1 in statisticlist):
        print("  #Error(get_valuation_market_china): invalid statistic",statistic)
        print("  Valid statistic:",statisticlist)
        return None

    # 构造组合矩阵   
    import pandas as pd
    matrix=pd.DataFrame([
        
        ['pe ttm value median','middlePETTM','市盈率(滚动TTM，全A股中位数)'],
        ['pe ttm value equal-weighted','averagePETTM','市盈率(滚动TTM，全A股等权平均)'],
        ['pe ttm quantile median','quantileInRecent10YearsMiddlePeTtm','市盈率分位数(滚动TTM，全A股中位数，近10年)'],
        ['pe ttm quantile equal-weighted','quantileInRecent10YearsAveragePeTtm','市盈率分位数(滚动TTM，全A股等权平均，近10年)'],
         
        ['pe lyr value median','middlePELYR','市盈率(静态LYR，全A股中位数)'],
        ['pe lyr value equal-weighted','averagePELYR','市盈率(静态LYR，全A股等权平均)'],
        ['pe lyr quantile median','quantileInRecent10YearsMiddlePeLyr','市盈率分位数(静态LYR，全A股中位数，近10年)'],
        ['pe lyr quantile equal-weighted','quantileInRecent10YearsAveragePeLyr','市盈率分位数(静态LYR，全A股等权平均，近10年)'],
         
        ['pb lyr value median','middlePB','市净率(静态LYR，全A股中位数)'],
        ['pb lyr value equal-weighted','equalWeightAveragePB','市净率(静态LYR，全A股等权平均)'],
        ['pb lyr quantile median','quantileInRecent10YearsMiddlePB','市净率分位数(静态LYR，全A股中位数，近10年)'],
        ['pb lyr quantile equal-weighted','quantileInRecent10YearsEqualWeightAveragePB','市净率分位数(静态LYR，全A股等权平均，近10年)'],
        
        ], columns=['combine','field','desc'])

    #查找组合方式对应的字段名称
    combine=measure1+' '+method1+' '+value1+' '+statistic1
    try:
        field=matrix[matrix['combine']==combine]['field'].values[0]
        desc=matrix[matrix['combine']==combine]['desc'].values[0]
    except:
        #未查到组合
        print("  #Error(get_valuation_market_china): parameter combination not available for",combine)
        return None

    import akshare as ak
    
    #获取全A股市场的市盈率
    if measure1 == 'pe':
        try:
            mp = ak.stock_a_ttm_lyr()
        except:
            #akshare版本需要更新
            print("  #Error(get_valuation_market_china): may need to upgrade akshare")
            return None
    
        #截取选定的日期范围
        mp['Date']=mp['date']
        mp.sort_values(by=['Date'],ascending=True,inplace=True)
        mp.set_index(['Date'],inplace=True) 
        mp1=mp[(mp.index >= startpd) & (mp.index <=endpd)]
        
        mp9=mp1[['date',field,'close']]
        mp9['field']=mp9[field]
        mp9['index']=mp9['close']
        mp9['index name']="沪深300指数"
        mp9['measure']=measure1
        mp9['method']=method1
        mp9['value']=value1
        mp9['statistic']=statistic1
        mp9['desc']=desc
    
    
    #获取全A股市场的市净率
    if measure1 == 'pb':
        try:
            mp = ak.stock_a_all_pb()
        except:
            #akshare版本需要更新
            print("  #Error(get_valuation_market_china): may need to upgrade akshare")
            return None
    
        #截取选定的日期范围
        mp['Date']=mp['date']
        mp.sort_values(by=['Date'],ascending=True,inplace=True)
        mp.set_index(['Date'],inplace=True) 
        mp1=mp[(mp.index >= startpd) & (mp.index <=endpd)]
        
        mp9=mp1[['date',field,'close']]
        mp9['field']=mp9[field]
        mp9['index']=mp9['close']
        mp9['index name']="上证综合指数"
        mp9['measure']=measure1
        mp9['method']=method1
        mp9['value']=value1
        mp9['statistic']=statistic1
        mp9['desc']=desc
        
    df=mp9[['date','field','index','index name','measure','method','value','statistic','desc']]
    
    return df    

if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    df=get_valuation_market_china(start,end,measure='pe',method='lyr',value='value',statistic='median')

#==============================================================================
if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    measures=['pb','pe']; methods='lyr'; values='value'; statistics='median'
    
    measures='pe'; methods=['lyr','ttm']; values='value'; statistics='median'


def valuation_market_china(start,end,measures=['pe','pb'], \
                           methods='lyr',values='value',statistics='median', \
                           twinx='auto',loc1='best',loc2='best'):
    """
    功能：比较中国全A股市场的估值指标变化趋势
    ----------
    start: 开始日期
    end: 结束日期
    measures: 估值指标市盈率'pe'或市净率'pb'
    methods: 滚动'ttm/静态取样'lyr'.
    values: 直接采用估值指标数值'value'或分位数'quantile'
    statistics: 采用中位数'median'或等权均值'equal-weighted'

    """
    
    #解析比较的指标，以第一个双指标为准
    found2=False
    parmlist=['measures','methods','values','statistics']
    for v in parmlist:
        
        #如果是一个字符串
        if isinstance(eval(v),str): 
            globals()[v+'1']=eval(v)
            globals()[v+'2']=eval(v)

        #如果是一个列表
        if isinstance(eval(v),list): 
            num = len(eval(v))
            #print("num=",num)
            
            if num == 0:
                print("  #Error(valuation_market_china)：need at least 1 parameter for",eval(v))
                return None,None
            
            if num == 1:
                globals()[v+'1']=eval(v)[0]
                globals()[v+'2']=eval(v)[0]
            
            
            if num >= 2:
                globals()[v+'1']=eval(v)[0]
                globals()[v+'2']=eval(v)[1]
                found2=True
                
    if not found2:
        print("  #Warning(valuation_market_china)：no comparing parameters from either of",parmlist)
        #return None,None
    """            
    print("measures1=",measures1,"measures2=",measures2)
    print("methods1=",methods1,"methods2=",methods2)
    print("values1=",values1,"values2=",values2)
    print("statistics1=",statistics1,"statistics2=",statistics2)
    """
    
    ylabeltxt='估值比率'
    titletxt='中国全A股市场估值的变化趋势'
    
    import datetime
    today = datetime.date.today()
    footnote="数据来源: 乐咕乐股，"+str(today)
    
    #获取指标1
    df1=get_valuation_market_china(start,end,measure=measures1,method=methods1,value=values1,statistic=statistics1)
    if df1 is None:
        print("  #Error(valuation_market_china)：no data available for the combination of",measures1,methods1,values1,statistics1)
        return None,None
    
    ticker1=df1['desc'].values[0]
    colname1='field'
    label1=''
    
    if not found2:  
        plot_line(df1,colname1,ticker1,ylabeltxt,titletxt,footnote, \
                      power=0,loc=loc1, \
                      date_fmt='%Y-%m-%d')
        return df1,None

    #获取指标2
    df2=get_valuation_market_china(start,end,measure=measures2,method=methods2,value=values2,statistic=statistics2)
    if df2 is None:
        print("  #Error(valuation_market_china)：no data available for the combination of",measures2,methods2,values2,statistics2)
        return None,None
    
    ticker2=df2['desc'].values[0]
    colname2='field'
    label2=''
    
    if twinx == 'auto':
        twinx=False
        
        max1=df1[colname1].max()
        max2=df2[colname2].max()
        bili=max1/max2
        if (bili > 2) or (bili < 0.5):
            twinx=True
    
    plot2_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               twinx=twinx,loc1=loc1,loc2=loc2)
    #清除变量
    #"""    
    for v in parmlist:
        del globals()[v+'1'],globals()[v+'2']
    #"""
    
    return df1,df2

if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    measures=['pe','pb']; methods='lyr'; values='value'; statistics='median'
    df1,df2=valuation_market_china(start,end,measures=['pe','pb'],methods='lyr',values='value',statistics='median')

#==============================================================================
# 行业估值：申万宏远行业，韭圈儿
#==============================================================================
if __name__=='__main__':
    top=5
    vtype='PE'
    vsorting='quantile'
    printout=True
    graph=True
    axisamp=3
    px=False
    
def industry_valuation_sw(top=10,vtype='PE',vsorting='quantile', \
                          graph=True,axisamp=1.2,px=False):
    """
    功能：列示申万行业指数估值最高和最低的行业
    vtype: PE, PB, dividend
    vsorting: 分位数绝对值
    """
    
    import akshare as ak
    df = ak.index_value_name_funddb()    
    
    # 筛选申万行业指数
    substr='(申万)'
    df['申万标志']=df['指数名称'].apply(lambda x: substr in x)
    df1=df[df['申万标志']]
    df1['行业代码']=df1['指数代码'].apply(lambda x: x[:6])
    df1['行业名称']=df1['指数名称'].apply(lambda x: x[:x.index(substr)])
    
    #检查估值类型
    typelist=['pe','pb','dividend']
    vtypeu=vtype.lower()
    if not (vtypeu in typelist):
        print("  #Warning(industry_valuation_sw): unsupported valuation type",vtype)
        print("  Supported types:",typelist)
        return None
    
    #检查排序类型
    sortlist=['quantile','value']
    vsortingu=vsorting.lower()
    if not (vsortingu in sortlist):
        print("  #Warning(industry_valuation_sw): unsupported sorting type",vsorting)
        print("  Supported types:",sortlist)
        return None
    
    #排序：高位优先
    if vtypeu == 'pe':
        if vsortingu == 'value':
            df2=df1.sort_values(by='最新PE',ascending=False)
            collist=['行业名称','最新PE','PE分位','最新PB','PB分位','股息率','股息率分位','行业代码']
            colname='最新PE'
        else:
            df2=df1.sort_values(by='PE分位',ascending=False)
            collist=['行业名称','PE分位','最新PE','PB分位','最新PB','股息率','股息率分位','行业代码']
            colname='PE分位'
        
    if vtypeu == 'pb':
        if vsortingu == 'value':
            df2=df1.sort_values(by='最新PB',ascending=False)
            collist=['行业名称','最新PB','PB分位','最新PE','PE分位','股息率','股息率分位','行业代码']
            colname='最新PB'
        else:
            df2=df1.sort_values(by='PB分位',ascending=False)
            collist=['行业名称','PB分位','最新PB','最新PE','PE分位','股息率','股息率分位','行业代码']
            colname='PB分位'
        
    if vtypeu == 'dividend':
        if vsortingu == 'value':
            df2=df1.sort_values(by='股息率',ascending=False)
            collist=['行业名称','股息率','股息率分位','最新PB','PB分位','最新PE','PE分位','行业代码']
            colname='股息率'
        else:
            df2=df1.sort_values(by='股息率分位',ascending=False)
            collist=['行业名称','股息率分位','股息率','最新PB','PB分位','最新PE','PE分位','行业代码']
            colname='股息率分位'
            
    df2.reset_index(drop=True,inplace=True)
    df2.index=df2.index+1
    df3=df2[collist]
    
    if top > 0:
        df4=df3.head(top)
    elif top < 0:
        df4=df3.tail(-top)
    else:
        df4=df3
    df5=df4.set_index('行业名称')
    df5.sort_values(by=colname,ascending=True,inplace=True)

    #绘图
    if graph:
        if top > 0:
            prefix="最高的"
        else:
            prefix="最低的"

        if vsortingu=='quantile':
            suffix="数百分比"
            footnote1="分位数表示历史上比当前便宜的百分比，"
        else:
            suffix="数值"
            footnote1=''
            
        titletxt="估值分析：基于"+colname+suffix+"，"+prefix+str(abs(top))+"个行业"
        
        import datetime
        today = datetime.date.today()
        footnote0="注：申万宏源行业分类，"
        footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
        footnote=footnote0+footnote1+footnote2
        
        if not px:
            fig=plot_barh(df5,colname,titletxt,footnote,axisamp=axisamp)
        else:
            fig=plot_barh2(df5,colname,titletxt,footnote)
        
    return df2

if __name__=='__main__':
    df=industry_valuation_sw(top=10,vtype='PE',vsorting='quantile',axisamp=2.3)
    df=industry_valuation_sw(top=-10,vtype='PE',vsorting='quantile',axisamp=1.2)
    df=industry_valuation_sw(top=10,vtype='PE',vsorting='value',axisamp=1.5)
    df=industry_valuation_sw(top=-10,vtype='PE',vsorting='value',axisamp=1.6)
    
    df=industry_valuation_sw(top=10,vtype='PB',vsorting='quantile',axisamp=2.1)
    df=industry_valuation_sw(top=-10,vtype='PB',vsorting='quantile',axisamp=1.2)
    df=industry_valuation_sw(top=10,vtype='PB',vsorting='value',axisamp=2)
    df=industry_valuation_sw(top=-10,vtype='PB',vsorting='value',axisamp=1.6)
    
    df=industry_valuation_sw(top=10,vtype='dividend',vsorting='quantile',axisamp=32)
    df=industry_valuation_sw(top=-10,vtype='dividend',vsorting='quantile',axisamp=1.2) 
    df=industry_valuation_sw(top=10,vtype='dividend',vsorting='value',axisamp=2)
    df=industry_valuation_sw(top=-10,vtype='dividend',vsorting='value',axisamp=1.3)    
#==============================================================================
#==============================================================================
if __name__=='__main__':
    industry='食品饮料'
    start='2021-1-1'
    end='2022-11-15'
    vtype='PE'
    
    graph=True
    loc='best'
    
def industry_valuation_history_sw(industry,start,end,vtype='PE', \
                                  graph=True,loc='best'):
    """
    功能：绘制一个申万行业的历史估值趋势
    vtype: PE, PB, dividend
    
    """
    #检查日期期间
    result,start1,end1=check_period(start,end)
    if not result:
        print("  #Warning(industry_valuation_history_sw): invalid date period",start,end)
        return None
    
    #检查估值类型
    typelist=['pe','pb','dividend']
    vtypeu=vtype.lower()
    if not (vtypeu in typelist):
        print("  #Warning(industry_valuation_history_sw): unsupported valuation type",vtype)
        print("  Supported types:",typelist)
        return None

    vtypelist=['pe','pb','dividend']
    typelist=['市盈率','市净率','股息率']
    pos=vtypelist.index(vtypeu)
    vtypes=typelist[pos]

    # 获取行业估值历史数据
    import akshare as ak
    sindustry=industry+'(申万)'
    try:
        df = ak.index_value_hist_funddb(symbol=sindustry, indicator=vtypes)  
    except:
        print("  #Warning(industry_valuation_history_sw): industry not found",industry)
        return None

    import pandas as pd
    df['date']=pd.to_datetime(df['日期'])
    df.set_index('date',inplace=True)
    df1=df[[vtypes]]
    
    #筛选期间
    df2=df1[(df1.index >= start1) & (df1.index <= end1)]

    #绘图
    if graph:
        df2['平均值']=df2[vtypes].mean()
        df2['中位数']=df2[vtypes].median()
        
        titletxt="行业估值趋势："+industry+'，'+vtypes   
        
        footnote0="注：申万宏源行业指数，"
        footnote1=''
        import datetime
        today = datetime.date.today()
        footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
        footnote=footnote0+footnote1+footnote2
        
        colname=vtypes
        collabel=vtypes
        ylabeltxt=vtypes
        
        draw_lines(df2,y_label=ylabeltxt,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=titletxt,data_label=False,resample_freq='D')
        
    return df2

if __name__=='__main__':
    df=industry_valuation_history_sw(industry,start,end,vtype='PE')
    df=industry_valuation_history_sw(industry,start,end,vtype='PB')
    df=industry_valuation_history_sw(industry,start,end,vtype='dividend')
    
    df=industry_valuation_history_sw(industry='纺织服饰',start=start,end=end,vtype='PE')
    df=industry_valuation_history_sw(industry='纺织服饰',start=start,end=end,vtype='PB')
    df=industry_valuation_history_sw(industry='纺织服饰',start=start,end=end,vtype='dividend')

#==============================================================================
if __name__=='__main__':
    industries=['食品饮料','纺织服饰']
    start='2021-1-1'
    end='2022-11-15'
    vtypes='PE'
    
    industries='纺织服饰'
    vtypes=['PE','PB']
    
    graph=True
    loc1='lower left'
    loc2='upper right'

def compare_industry_valuation_sw(industries,start,end,vtypes='PE', \
                                  graph=True,loc1='best',loc2='best'):
    """
    功能：比较多个申万行业或者两个指标的历史估值趋势
    条件：若industries为列表且多个，则取vtype的第一个值；
    若industries为字符串或者列表但只有一个，则取vtype的前两个值比较，双轴
    vtypes: PE, PB, dividend
    
    """
    
    #检查日期期间的合理性
    
    
    vtypelist=['pe','pb','dividend']
    typelist=['市盈率','市净率','股息率']

    #检查行业个数：多个行业+单指标
    if isinstance(industries,list) & (len(industries) >= 2):
        
        if isinstance(vtypes,str): 
            vtype=vtypes
        elif isinstance(vtypes,list): 
            vtype=vtypes[0]

        vtypeu=vtype.lower()
        pos=vtypelist.index(vtypeu)
        vtypec=typelist[pos]
        
        import pandas as pd
        df=pd.DataFrame()        
        for i in industries:
            dft=industry_valuation_history_sw(i,start=start,end=end,vtype=vtype,graph=False)
            dft.rename(columns={vtypec:i},inplace=True)
            
            if len(df) == 0:
                df=dft
            else:
                df=pd.merge(df,dft,how='outer',left_index=True,right_index=True)
                
        #绘图
        if graph:
            titletxt="行业估值趋势对比："+vtypec   
            
            footnote0="注：申万宏源行业指数，"
            footnote1=''
            import datetime
            today = datetime.date.today()
            footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
            footnote=footnote0+footnote1+footnote2
            
            ylabeltxt=vtypec
            
            draw_lines(df,y_label=ylabeltxt,x_label=footnote, \
                       axhline_value=0,axhline_label='', \
                       title_txt=titletxt,data_label=False,resample_freq='D')

            return df

    #检查行业个数：一个行业+双指标
    if  ((isinstance(industries,str) | (isinstance(industries,list) & (len(industries) == 1)))) \
        & (isinstance(vtypes,list) & (len(vtypes) >= 2)):
        
        if isinstance(industries,str): 
            industry=industries
        elif isinstance(industries,list): 
            industry=industries[0]
        
        if isinstance(vtypes,str): 
            ivtypelist=[vtypes]
        elif isinstance(vtypes,list): 
            ivtypelist=vtypes[:2]
        
        import pandas as pd
        df=pd.DataFrame()        
        for t in ivtypelist:
            
            dft=industry_valuation_history_sw(industry,start=start,end=end,vtype=t,graph=False)
            
            if len(df) == 0:
                df=dft
            else:
                df=pd.merge(df,dft,how='outer',left_index=True,right_index=True)
                
        #绘图
        if graph:
            titletxt="行业估值趋势对比："+industry   
            
            footnote0="注：申万宏源行业指数，"
            footnote1=''
            import datetime
            today = datetime.date.today()
            footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
            footnote=footnote0+footnote1+footnote2
            
            collist=list(df)
            colname1=label1=collist[0]
            colname2=label2=collist[1]
            
            plot_line2(df,'',colname1,label1, \
                       df,'',colname2,label2, \
                           ylabeltxt='',titletxt=titletxt,footnote=footnote, \
                           twinx=True, \
                           resample_freq='D',loc1=loc1,loc2=loc2, \
                           color1='red',color2='blue')
            
            return df

    #检查行业个数：一个行业+一个指标
    if  ((isinstance(industries,str) | (isinstance(industries,list) & (len(industries) == 1)))) \
        & ((isinstance(vtypes,str) | (isinstance(vtypes,list) & (len(vtypes) == 1)))):

        if isinstance(industries,str): 
            industry=industries
        elif isinstance(industries,list): 
            industry=industries[0]
        
        if isinstance(vtypes,str): 
            ivtype=vtypes
        elif isinstance(vtypes,list): 
            ivtype=vtypes[0]
            
        df=industry_valuation_history_sw(industry,start,end,vtype=ivtype, \
                                          graph=graph,loc=loc1)
        return df
            
if __name__=='__main__':
    df=compare_industry_valuation_sw(industries=['纺织服饰','国防军工','食品饮料'], \
                                     start='2017-1-1',end='2022-11-15', \
                                     vtypes='PE',loc1='lower left',loc2='upper right')

    df=compare_industry_valuation_sw(industries=['纺织服饰'], \
                                     start='2017-1-1',end='2022-11-15', \
                                     vtypes='PE',loc1='lower left',loc2='upper right')

    df=compare_industry_valuation_sw(industries=['纺织服饰'], \
                                     start='2017-1-1',end='2022-11-15', \
                                     vtypes=['PE','PB'],loc1='lower left',loc2='upper right')

#==============================================================================
