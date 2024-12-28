import pandas as pd
import subprocess
import math
base='C:\\Users\\user\\git\\py\\data_via_setting_table\\'
file_name=base+'sample'
feas_name=base+'feas\\sample'
vn0_file=base+'Param_sample.csv'
# vnt_file=base+'Param_sample画像プロット用転置.csv'
crd_file=file_name+'_crd.csv'
crd1_file=file_name+'_crd1.csv'
output=file_name+'_feas.csv'
output_s=file_name+'_feas_s.csv'
df=pd.read_csv(vn0_file, header=None)
df=df.drop(df.columns[0], axis=1)
# df.head()
df.iloc[0]=''
df.iloc[0,0], df.iloc[0,1]=0,-90
df.iloc[0,2], df.iloc[0,3]=-35,-0
df.iloc[0,4], df.iloc[0,5]=35,-0
df.iloc[0,6], df.iloc[0,7]=-35,-120
df.iloc[0,8], df.iloc[0,9]=35,-120
df.to_csv(crd_file, index=False, header=False)
with open(output_s, 'w') as file:
    file.write('')
df=pd.read_csv(crd_file, header=None)
p0x, p0y=df.iloc[0,0], df.iloc[0,1]
data_num=len(df)-1
stats_df=pd.DataFrame({'Stat':['id', 'ds_min1', 'ds_min2','ds_min3','ds_min4','ds_min5',
                              'ds_max1','ds_max2','ds_max3','ds_max4','ds_max5','ds_avg',
                              'ang_max1','ang_max2','ang_max3','ang_max4','ang_max5',
                              'ang_diff1','ang_diff2','ang_diff3','ang_diff4','ang_diff5',
                              'ds_ind1', 'ds_ind2', 'ds_ind3', 'ds_ind4', 'ds_ind5',
                              'ds_sum_ind2', 'ds_sum_ind3', 'ds_sum_ind4', 'ds_sum_ind5']}) 
r=0.1
for k in range(1, data_num+1):
    value=str(k)
    ds_list=[]
    angles_list=[]
    n=len(df.columns)//2
    for i in range(1, len(df.columns)//2+1):
        px=df.iloc[k, (i-1)*2]
        py=df.iloc[k, (i-1)*2+1]
        dsx=px-p0x
        dsy=py-p0y
        ds=math.sqrt(dsx**2+dsy**2)
        ds_list.append(ds)
        angle=math.atan2(dsy,dsx)*(180/math.pi)
        angle=(angle+360)%360
        angles_list.append(angle)
    result_df=pd.DataFrame({'Distance':ds_list, 'Angle':angles_list})
    result_df=result_df.sort_values('Distance')
    ds_avg=result_df['Distance'].mean()
    result_df=result_df.sort_values('Angle')
    ds_max=[result_df['Distance'].nlargest(i).iloc[-1] for i in range(1, n+1)]
    ds_min=[result_df['Distance'].nsmallest(i).iloc[-1] for i in range(1, n+1)]
    ang_max=[result_df['Angle'].nlargest(i).iloc[-1] for i in range(1, n+1)]
    ang_diff=[ang_max[i-1]-ang_max[i] for i in range(1,n)]
    ang_diff.append(ang_max[n-1]-ang_max[0]+360)
    ang_diff.sort(reverse=True)
    dsmr1,dsmr2,dsmr3,dsmr4,dsmr5=(ds_min[0]-r)/r,(ds_min[1]-r)/r,(ds_min[2]-r)/r,(ds_min[3]-r)/r,(ds_min[4]-r)/r
    ind1,ind2,ind3,ind4,ind5=math.log10(dsmr1),math.log10(dsmr2),math.log10(dsmr3),math.log10(dsmr4),math.log10(dsmr5)
    inv_ind1,inv_ind2,inv_ind3,inv_ind4,inv_ind5=1.0/ind1, 1.0/ind2, 1.0/ind3, 1.0/ind4, 1.0/ind5
    ind_sum2=1.0/(inv_ind1+inv_ind2)
    ind_sum3=1.0/(inv_ind1+inv_ind2+inv_ind3)
    ind_sum4=1.0/(inv_ind1+inv_ind2+inv_ind3+inv_ind4)
    ind_sum5=1.0/(inv_ind1+inv_ind2+inv_ind3+inv_ind4+inv_ind5)
    stats_df[value]=[value, ds_min[0], ds_min[1],ds_min[2],ds_min[3],ds_min[4],
                     ds_max[0],ds_max[1],ds_max[2],ds_max[3],ds_max[4],ds_avg,
                     ang_max[0],ang_max[1],ang_max[2],ang_max[3],ang_max[4],
                     ang_diff[0],ang_diff[1],ang_diff[2],ang_diff[3],ang_diff[4],
                     ind1,ind2,ind3,ind4,ind5,
                     ind_sum2, ind_sum3, ind_sum4, ind_sum5]
stats_df=stats_df.transpose()
stats_df.to_csv(output_s, mode='a',header=None, index=None)