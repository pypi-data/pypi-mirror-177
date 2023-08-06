This library is submitted as part of homework-1 to hide polygon key access

# Installation
`pip install polygon-api-access-nn2094`

# Getting Started
Below library will be useful to securely access Polygon API. It abstracts the Polygon API key to secure it from getting exposed externally.

### Take care of the dependencies

```python
# dependencies
from polygon_access import Data_Aggregate

# Libraries To import
import math, os

```

### Example:

Below is a driver code example to test out the working

```python

# 4 currency pairs considered for forex exchange
currency_pairs = [["AUD", "USD", [], portfolio("AUD", "USD")],
                  ["EUR", "USD", [], portfolio("EUR", "USD")],
                  ["USD", "INR", [], portfolio("USD", "INR")],
                  ["USD", "PLN", [], portfolio("USD", "PLN")]]

# Driver code
op = Data_Aggregate(os.getcwd(), 'database')

# os.getcwd()
# this line gets the current working directory

```

To print the output after the above function call

```python
print(op.acquire_data_and_write(currency_pairs))

```