from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(Product , cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == Product.id:
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(Product , cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == Product.id:
            return cart.get(id)
    return 0

@register.filter(name='price_total')
def price_total(Product , cart):
    return Product.product_price * cart_quantity(Product,cart)

@register.filter(name='grand_price_total')
def grand_price_total(cart_Data , cart):
    sum = 0
    for each in cart_Data:
        sum += price_total(each,cart)
    return sum

