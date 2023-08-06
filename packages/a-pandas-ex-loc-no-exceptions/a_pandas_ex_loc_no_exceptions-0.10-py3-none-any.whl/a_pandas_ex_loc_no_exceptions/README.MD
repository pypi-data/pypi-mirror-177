# Search through all columns of a DataFrame without worrying about Exceptions


```python

$pip install a-pandas-ex-loc-no-exceptions

import re
import pandas as pd
from a_pandas_ex_loc_no_exceptions import pd_add_loc_no_exceptions

pd_add_loc_no_exceptions()

df=pd.read_pickle('f:\\dafasdfaf.pkl')
print(df.d_loc_no_exception('str.contains','youtube',na=False,flags=re.I))
print(df.d_loc_no_exception('__eq__','Non-Data Actions'))
print(df.d_loc_no_exception('__gt__',print)) #wont throw exception


Operators cannot be passed to the function! 
Use dunders like in the examples! 

<	-	__lt__
<=	-	__le__
==	-	__eq__
!=	-	__ne__
>	-	__gt__
>=	-	__ge__
+	-	__add__
+=	-	__iadd__
-	-	__sub__
*	-	__mul__
@	-	__matmul__
/	-	__truediv__
//	-	__floordiv__
%	-	__mod__
**	-	__pow__
<<	-	__lshift__
>>	-	__rshift__
&	-	__and__
^	-	__xor__
|	-	__or__
~   -	__invert__

 
```