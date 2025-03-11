# BestBuy

Create function that will take as input a cart of items and shops where the products can be purchased. 
Function will return a dict with shop name where the specified cart items and quantities 
fave the smallest total cost and the total cost in that shop

```python
cart = {'apple': 10, 'plums': 15, 'bananas': 5}

shop_K = {'apple': 1.2, 'plums': 4, 'bananas': 5.5}
shop_P = {'apple': 1.3, 'plums': 3, 'bananas': 8}
shop_L = {'apple': 1.4, 'plums': 2, 'bananas': 10}

shops = {'pro': shop_P, 'lil': shop_L, 'kau': shop_K}

```
#### Info: 
 - in the cart the value represents the number or units of that item
 - in shop_X the value represents the cost per unit of a specific item

### Considerations:
 - cart can have items that are not in some shops and in this case shop needs to be excluded
 - shops can have large number of items compared to the cart so optimise your for loops
