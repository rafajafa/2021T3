def bmi(weight, height):
    bmi = weight / (height ** 2)
    bmi = round(bmi, 1)
    print(f"Your BMI is {bmi}")

if __name__ == '__main__':
    weight = float(input("What is your weight in kg? "))
    height = float(input("What is your height in m? "))
    bmi(weight, height)