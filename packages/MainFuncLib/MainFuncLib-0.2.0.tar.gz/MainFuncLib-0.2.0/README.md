# MainFuncLib
This library is created for the second homework of MG 8411 Data Engineering and extends the first homework. This library still hides the API key. The code implements also the Keltner bands.  It keeps track in real time of max, min, mean, VOL, FD (fractal dimension) per 6 minute interval.

It does this by calculating the volatility as max – min. Then 100 Keltner bands get formed in the next interval using the mean and the volatility of the previous interval:

Keltner Channel Upper Band = Mean Value + n*0.025*VOL, n from 1 to 100, where Mean Value and VOL are calculated from the previous period of 6 minutes.

Keltner Channel Lower Band = Mean Value – n*0.025*VOL, n from 1 to 100, where Mean Value and VOL are calculated from the previous period of 6 minutes.

The # crosses with the Keltner bands gets counted during the 6 minute interval and then the fractal dimension is calculated as: # cross/VOL

Note that the first 6 minute checkpoint doesn't yield a FD and is set to Null, because there is no previous information yet.

The code also implements a check to see if the provided makes sense and is correct and the comments in the code clarify my implementation of this homework.



### Installation
```
pip install MainFuncLib==0.2.0
```

### Get started
Make sure the latest version of Polygon-api-client is installed. Example of how to use this library in Max's code, delete main() in Max's code and replace with the library:

```Python
from MainFuncLib import mainFunc

vol_AUD_USD =  0 # set to daily volatility
start_mean_AUD_USD = 0 # set to daily mean
vol_GBP_EUR =  0 # set to daily volatility
start_mean_GBP_EUR = 0 # set to daily mean

# Example with 2 currency pairs
currency_pairs = [["AUD","USD",0,0, vol_AUD_USD, start_mean_AUD_USD,0,9999],
                  ["GBP","EUR",0,0, vol_USD_CAD, start_mean_GBP_EUR,0,9999],

mainFunc(currency_pairs)
```