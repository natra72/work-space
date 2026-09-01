import pandas as pd
import numpy as np

df=pd.read_csv(r"C:\Users\natra\Desktop\archive\dirty_cafe_sales.csv")


# المشكلة الاساسي التي واجهتني في هذا الملف هي وجود اكثر من منتج بنفس السعر 
#the main problem I encountered with this file is the presence of more than one product at the same price.

string_data=["Transaction ID","Item","Payment Method","Location"]
df[string_data]=df[string_data].apply(lambda x: x.str.strip()) # A lmbda function for deleting spaces in the mentioned columns
#print(df["Item"].head().apply(lambda x:f"|{x}|")) 

#print(df[(df["Price Per Unit"] == "4.0") & (df["Location"] =="Takeaway")]["Item"].value_counts().idxmax())# Search for the most frequently used product within certain criteria

convert=["Price Per Unit","Quantity","Total Spent",]
df[convert]=df[convert].apply(pd.to_numeric, errors="coerce") # converted the columns to a numeric and assigned the empty values ​​to nan.


df[["Item","Payment Method"]]=df[["Item","Payment Method"]].replace(["ERROR","UNKNOWN"],np.nan) # Convert the missing values ​​in these two columns to NAN
#df["Payment Method"]=df["Payment Method"].replace(["ERROR","UNKNOWN"],np.nan)
#Item_prices={"Coffe":2.0, "Cookie":1.0,"Salad":5.0, "Tea":1.50}
#df["Price Per Unit"]=df["Price Per Unit"].fillna(df["Item"].map(Item_prices))

df.loc[(df["Price Per Unit"] == 4.0) & (df["Item"].isna()),"Item"]="Sandwich" # the most frequently used item based on price.
df.loc[(df["Item"]=="Sandwich")&(df["Price Per Unit"].isna()),"Price Per Unit"]=4.0 #and here's the opposite


Item_prices ={ "Coffee": 2.0 , "Cake" : 3.0 , "Cookie" : 1.0 , "Salad" : 5.0 , "Smoothie" : 4.0 , "Juice" : 3.0 , "Tea" : 1.5 }
df["Price Per Unit"]=df["Price Per Unit"].fillna(df["Item"].map(Item_prices)) # dictionary for filling in empty values ​​in the price column based on products.

# after that: 
calculate_Price=df["Total Spent"]/df["Quantity"] # calculate the missing values ​​in the price column.
df["Price Per Unit"]= df["Price Per Unit"].fillna(calculate_Price)

calculate_Quantity=df["Total Spent"]/df["Price Per Unit"] #calculate the missing values ​​in the quantity column
df["Quantity"]=df["Quantity"].fillna(calculate_Quantity)

calculate_Total_Spent=df["Price Per Unit"]*df["Quantity"] # calculate the missing values ​​in the total spent column.
df["Total Spent"]=df["Total Spent"].fillna(calculate_Total_Spent)

df.loc[(df["Price Per Unit"] == 3.0) &(df["Location"] =="In-store") & (df["Item"].isna()),"Item"]="Juice"
# المنتج الاكثر مبيعا حسب المعطيات المكتوبة في الكود
df.loc[(df["Price Per Unit"] == 3.0) & (df["Location"] =="Takeaway") & (df["Item"].isna()),"Item"]="Cake"
# best selling product, according to the information provided
df.loc[(df["Price Per Unit"]==3.0) & (df["Payment Method"].isin(["Credit Card","Digital Wallet"])) & (df["Item"].isna()),"Item"]="Juice"

df.loc[(df["Price Per Unit"]==3.0) & (df["Payment Method"]=="Cash") & (df["Item"].isna()),"Item"]="Cake"


Item_prices2 ={2.0:"Coffee" , 1.0:"Cookie" , 5.0:"Salad", 1.5:"Tea"} 
df["Item"]=df["Item"].fillna(df["Price Per Unit"].map(Item_prices2))# dictionary for product names based on price

# بقي لدي تقريبا 38 منتج سعره 3 ويوجد فراغات في الاعمدة المتبقية 

Condition=(df["Price Per Unit"]==3.0)&(df["Item"].isna()) 
count=Condition.sum()
df.loc[Condition,"Item"]=np.random.choice(["Cake","Juice"],size=count) # randomly choose between two products that cost three riyals


df.loc[(df["Payment Method"].isna(),"Payment Method")]="Digital Wallet" # the most frequent method of payment
df.loc[(df["Location"].isna(),"Location")]="Takeaway" # the most frequently used method in the location


# هذي الاكواد كتبت لان الاسعار والمنتجات غير معرفة واخذت النتائج على حسب شروط معينة كانت متوفرة في الملف 
# I wrote these codes because the prices and products were not defined. I extracted the results based on specific criteria from the file.
df.loc[[1761,2289],"Price Per Unit"]=4.0
df.loc[[3779],["Item","Price Per Unit"]]=["Salad",5.0]
df.loc[[4152],["Item","Price Per Unit"]]=["Cookie",1.0]
df.loc[[7597],["Item","Price Per Unit"]]=["Juice",3.0]
df.loc[[9819,1761,2289],["Item","Price Per Unit"]]=["Sandwich",4.0]
df.loc[(df["Price Per Unit"] == 4.0) & (df["Item"].isna()),"Item"]="Sandwich"


# هذي الاكواد تحسب الكمية الاكثر تكرارا لكل منتج في الصفوف المفقود فيها الكمية 
# the most requested quantity for each item
df.loc[[236,8021,3224,4257,7029,8465,9869,738,8443,8479,9590,3203,3779,9819],"Quantity"]=5 # the most requested quantities are coffee, salad, and sandwiches
df.loc[[7297],"Quantity"]=3 # The most requested quantity for smoothies Inside.
df.loc[[278,641,8574,7597],"Quantity"]=2 # the most requested quantity of juice.
df.loc[[2796,3401],"Quantity"]=4 # الكمية الاكثر طلبا للكيك والشاي
df.loc[[5841,8732],"Quantity"]=1 # الكمية الاكثر طلبا للكوكيز


calculate_Total_Spent=df["Price Per Unit"]*df["Quantity"] # Calculate the total spent value..
df["Total Spent"]=df["Total Spent"].fillna(calculate_Total_Spent)


# القيم الفارغة في عمود الموقع والتاريخ كثيرة جدا فعطيت بايثون اختيار عشوائي ضمن الموقعين الواردة في الملف وتاريخ ضمن سنة 2023
# fill in the empty values ​​in the Site and Date column by randomly selecting from the two locations listed in the file and the date within 2023.

df["Location"]=df["Location"].replace(["ERROR","UNKNOWN"],np.nan) # حولت قيم الموقع لنان
Condition2=(df["Location"].isna())
count=Condition2.sum()
df.loc[Condition2,"Location"]=np.random.choice(["In-store","Takeaway"],size=count) # تعبئة القيم بشكل عشوائي ضمن هذي القيمتين


date_range=pd.date_range(start="2023-01-01",end="2023-12-31").strftime('%Y-%m-%d') # generate random values ​​for missing dates.
num_nulls=df["Transaction Date"].isna().sum()
if num_nulls>0:
    random_dates=np.random.choice(date_range,size=num_nulls)
    df.loc[df["Transaction Date"].isnull(),"Transaction Date"]=random_dates

# 
#print(df["Price Per Unit"].dtypes) # type of columns
#print(df.head())
#print(df.isna().sum())
#print(df[""].isna().sum()) 
#print(df.shape) # count the number of columns and rows.
#print(df.describe())
#print(df.loc[df["Quantity"].isna()]) # search for empty rows within this column.
#print(df["Location"].value_counts().idxmax()) # the most frequently occurring value within this column
#print(df.duplicated())
#print(df["Item"].unique()) # recall column elements without duplication
df.to_excel("cafesals_cleaned.xlsx",index=False) # the file is saved