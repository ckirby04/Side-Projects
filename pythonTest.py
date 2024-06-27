# Clark Kirby python test 6/22/2024

# Prompt user for yesterday’s caloric intake

# Prompt user for yesterday’s steps, via phone app

# Prompt user for yesterday’s cardio, if applicable 

# Prompt user for morning weight 

# Prompt user for gain/lose/maintain weight 

# Output maintenance calories and recommended calories for bulk/cut

calorieArray     = []
weightArray      = []
deltaWeightArray = [0]

while True:
    calories = input("Input yesterday's total calories(Type '0' when complete) :  ")
    if calories == "0":
        break
    else:
        try:
            calories = int(calories)
        except ValueError:
            print("Please enter a valid integer to complete.")
    
    cardio = input("Input yesterday's cardio, in calories(if none, enter 0) :  ")
    try: 
        cardio = int(cardio)
    except ValueError:
        print("Please enter a valid integer to complete.")
    totalCalories = calories - cardio
    calorieArray.append(totalCalories)
    
    
    weight = int(input("Input today's body weight :  "))
    weightArray.append(weight)

for x in weightArray : 
    deltaWeight = weightArray[x+1] - weightArray[x]
    deltaWeightArray.append(deltaWeight)
    print(deltaWeight)


maint = total - delta 


