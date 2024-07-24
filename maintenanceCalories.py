import sqlite3

def create_table():
    # Connect to SQLite database
    conn = sqlite3.connect('calorie_maintenance.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS calorie_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day INTEGER NOT NULL,
        weight REAL NOT NULL,
        calories INTEGER NOT NULL,
        maintenance_calories REAL
    )
    ''')
    conn.commit()
    conn.close()

def clear_data():
    # Connect to SQLite database
    conn = sqlite3.connect('calorie_maintenance.db')
    c = conn.cursor()
    
    # Clear the table
    c.execute('DELETE FROM calorie_data')
    conn.commit()
    conn.close()
    print("Data has been cleared successfully!")

def calculate_maintenance_calories(last_day, current_day):
    # Calculate the difference in weight and use the formula to find maintenance calories
    delta_weight = current_day[0] - last_day[0]
    calories_consumed = current_day[1]
    maintenance_calories = calories_consumed - (3500 * delta_weight)
    return maintenance_calories

def main():
    create_table()
    
    # Connect to SQLite database
    conn = sqlite3.connect('calorie_maintenance.db')
    c = conn.cursor()
    
    # Check the number of entries
    c.execute('SELECT COUNT(*) FROM calorie_data')
    num_entries = c.fetchone()[0]
    
    if num_entries == 0:
        # Prompt the user for their starting weight
        starting_weight = float(input("Enter your starting weight: "))
        
        # Day 1 (first entry)
        day = 1
        
        # Insert the starting weight into the database
        c.execute('''
        INSERT INTO calorie_data (day, weight, calories, maintenance_calories)
        VALUES (?, ?, ?, NULL)
        ''', (day, starting_weight, 0))
        
        print("Starting weight recorded. Please enter data for the next day.")
    else:
        # Prompt the user for their morning weight
        morning_weight = float(input("Enter your morning weight: "))
        
        # Prompt the user for the calories consumed the day prior
        calories_consumed = int(input("Enter the calories you consumed yesterday: "))
        
        # Next day
        day = num_entries + 1
        
        # Retrieve the most recent entry
        c.execute('''
        SELECT weight, calories, maintenance_calories FROM calorie_data
        ORDER BY day DESC LIMIT 1
        ''')
        last_day = c.fetchone()
        
        maintenance_calories = None
        
        if last_day:
            # Calculate today's maintenance calories based on the last day's data
            maintenance_calories = calculate_maintenance_calories(last_day, (morning_weight, calories_consumed))
        
        # Insert the data into the database
        c.execute('''
        INSERT INTO calorie_data (day, weight, calories, maintenance_calories)
        VALUES (?, ?, ?, ?)
        ''', (day, morning_weight, calories_consumed, maintenance_calories))
        
        # Retrieve all data again including the newly inserted row
        c.execute('''
        SELECT weight, calories FROM calorie_data
        ORDER BY day
        ''')
        all_data = c.fetchall()
        
        if len(all_data) > 1:
            daily_maintenance_calories = []
            
            for i in range(1, len(all_data)):
                last_day = all_data[i-1]
                current_day = all_data[i]
                maintenance_calories = calculate_maintenance_calories(last_day, current_day)
                daily_maintenance_calories.append(maintenance_calories)
            
            avg_maintenance_calories = sum(daily_maintenance_calories) / len(daily_maintenance_calories)
            print(f"Average maintenance calories: {avg_maintenance_calories:.2f} calories")
        else:
            print("Not enough data to calculate average maintenance calories.")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print("Data has been recorded successfully!")

if __name__ == "__main__":
    # Prompt the user for input
    user_input = input("Enter 'r' to record data, 'c' to clear data: ").lower()
    
    if user_input == 'r':
        main()
    elif user_input == 'c':
        clear_data()
    else:
        print("Invalid input. Please enter 'r' to record data or 'c' to clear data.")
