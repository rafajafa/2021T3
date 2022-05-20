def tax_function(income):
    if income <= 18200:
        tax =  0
    elif income <= 37000:
        tax = (income - 18200) * 0.19
    elif income <= 87000:
        tax = 3572 + (income - 37000) * 0.325
    elif income <= 180000:
        tax = 19822 + (income - 87000) * 0.37
    else:
        tax = 54232 + (income - 180000) * 0.45

    tax = round(tax, 2)
    print(f"The estimated tax on your income is ${tax:,.2f}")

if __name__ == '__main__':
    income = float(input("Enter your income: "))
    tax_function(income)
    
    