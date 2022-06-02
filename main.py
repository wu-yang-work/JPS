# Define class
class Variant():
    # use
    def __init__(self, price=500, description='default description'):
        self.price = price
        self.description = description
        self.values = []

    def __str__(self):
        return 'price: {}, description: {}, values: {}'.format(self.price, self.description, self.values)


variant_list = []
# Create instance with same name iteratively
for i in range(3):
    current_variant = Variant()
    if i == 1:
        current_variant.values.append('hello')
    current_variant.price = i
    current_variant.description = 'description of variant: {}'.format(i)
    variant_list.append(current_variant)

# Test results
for variant in variant_list:
    print(str(variant))
