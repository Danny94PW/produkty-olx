import pandas as pd
import csv


df_actual = pd.read_csv('OLX_actual_hour.csv',names=['ID','Link','Data','Liczba_wyświetleń'])
df_ago = pd.read_csv('OLX_one_hour_ago.csv',names=['ID','Link','Data','Liczba_wyświetleń'])
df = pd.concat([df_actual,df_ago])

# Usuwam pojedyncze wpisy
df = df[df.groupby('ID').ID.transform(len) >1]

# Ten parametr jest zbedny w tej wersji projektu
del df['Data']

# Ciezko odejmowac wartosci miedzy roznymi wierszami, wspomoglem sie stworzeniem kolumny max i min, aby pozniej stworzyc kolumne z ich roznicy
df = df.groupby(['ID','Link']).Liczba_wyświetleń.agg(['max','min'])
df['Liczba_wyświetleń']=df['max']-df['min']

# Usuwam to co dalej niepotrzebne
del df['max']
del df['min']

# Sortuje w celu uzyskania 10 najlepszych wynikow (dla ktorych roznica w przeciagu godziny byla najwieksza)
df = df.sort_values(['Liczba_wyświetleń'],ascending=[False])
df2 = df[0:10]

df2.to_csv('Top_10.csv',header=False)
