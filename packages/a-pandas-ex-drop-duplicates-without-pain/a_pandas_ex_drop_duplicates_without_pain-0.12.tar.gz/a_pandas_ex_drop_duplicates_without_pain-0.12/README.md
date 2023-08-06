## Installation

```python
pip install a-pandas-ex-drop-duplicates-without-pain 
```

## Usage

```python
from a_pandas_ex_drop_duplicates_without_pain import pd_add_drop_duplicates_without_pain
pd_add_drop_duplicates_without_pain()
import pandas as pd
df = pd.read_csv("https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_long.csv")
print(f'{df=}')
df_with_duplicates = df[['city', 'country',  'location', 'parameter', 'value','unit']].copy()
print(f'{df_with_duplicates=}')
df_without_duplicates = df_with_duplicates[['city', 'country',  'location', 'parameter', 'value',      'unit']].drop_duplicates().copy()
print(f'{df_without_duplicates=}')
df_with_duplicates['provoke_error'] = [[[1]*10]] * len(df_with_duplicates)
print(f'{df_with_duplicates=}')
df_result1 = None
df_result2 = None
try:
    df_result1=df_with_duplicates.drop_duplicates()
except Exception as Err:
    print(Err)
    df_result2=df_with_duplicates.ds_drop_duplicates_without_pain()
print(f'{df_result1=}')
print(f'{df_result2=}')
df.parameter.ds_drop_duplicates_without_pain()
df=           city country                   date.utc  ... parameter value   unit
0     Antwerpen      BE  2019-06-18 06:00:00+00:00  ...      pm25  18.0  µg/m³
1     Antwerpen      BE  2019-06-17 08:00:00+00:00  ...      pm25   6.5  µg/m³
2     Antwerpen      BE  2019-06-17 07:00:00+00:00  ...      pm25  18.5  µg/m³
3     Antwerpen      BE  2019-06-17 06:00:00+00:00  ...      pm25  16.0  µg/m³
4     Antwerpen      BE  2019-06-17 05:00:00+00:00  ...      pm25   7.5  µg/m³
         ...     ...                        ...  ...       ...   ...    ...
5267     London      GB  2019-04-09 06:00:00+00:00  ...       no2  41.0  µg/m³
5268     London      GB  2019-04-09 05:00:00+00:00  ...       no2  41.0  µg/m³
5269     London      GB  2019-04-09 04:00:00+00:00  ...       no2  41.0  µg/m³
5270     London      GB  2019-04-09 03:00:00+00:00  ...       no2  67.0  µg/m³
5271     London      GB  2019-04-09 02:00:00+00:00  ...       no2  67.0  µg/m³
[5272 rows x 7 columns]
df_with_duplicates=           city country            location parameter  value   unit
0     Antwerpen      BE             BETR801      pm25   18.0  µg/m³
1     Antwerpen      BE             BETR801      pm25    6.5  µg/m³
2     Antwerpen      BE             BETR801      pm25   18.5  µg/m³
3     Antwerpen      BE             BETR801      pm25   16.0  µg/m³
4     Antwerpen      BE             BETR801      pm25    7.5  µg/m³
         ...     ...                 ...       ...    ...    ...
5267     London      GB  London Westminster       no2   41.0  µg/m³
5268     London      GB  London Westminster       no2   41.0  µg/m³
5269     London      GB  London Westminster       no2   41.0  µg/m³
5270     London      GB  London Westminster       no2   67.0  µg/m³
5271     London      GB  London Westminster       no2   67.0  µg/m³
[5272 rows x 6 columns]
df_without_duplicates=           city country            location parameter  value   unit
0     Antwerpen      BE             BETR801      pm25   18.0  µg/m³
1     Antwerpen      BE             BETR801      pm25    6.5  µg/m³
2     Antwerpen      BE             BETR801      pm25   18.5  µg/m³
3     Antwerpen      BE             BETR801      pm25   16.0  µg/m³
4     Antwerpen      BE             BETR801      pm25    7.5  µg/m³
         ...     ...                 ...       ...    ...    ...
5087     London      GB  London Westminster       no2   81.0  µg/m³
5090     London      GB  London Westminster       no2   83.0  µg/m³
5091     London      GB  London Westminster       no2   76.0  µg/m³
5092     London      GB  London Westminster       no2   70.0  µg/m³
5098     London      GB  London Westminster       no2   79.0  µg/m³
[819 rows x 6 columns]
df_with_duplicates=           city country  ...   unit                     provoke_error
0     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
1     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
2     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
3     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
4     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
         ...     ...  ...    ...                               ...
5267     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5268     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5269     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5270     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5271     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
[5272 rows x 7 columns]
unhashable type: 'list'
df_result1=None
df_result2=           city country  ...   unit                     provoke_error
0     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
1     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
2     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
3     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
4     Antwerpen      BE  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
         ...     ...  ...    ...                               ...
5087     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5090     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5091     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5092     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
5098     London      GB  ...  µg/m³  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
[819 rows x 7 columns]
Out[2]: 
0       pm25
1825     no2
Name: parameter, dtype: object

```
