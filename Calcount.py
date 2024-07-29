from selenium import webdriver;from selenium.webdriver.common.keys import Keys;from selenium.webdriver.common.by import By;from datetime import date;import time;import csv

def optionsList(): print("\nOptions:\n1) Look up a food's nutritional content\n2) View Macro Summary for today \n3) View a previous day's Macro Summary \n4) Determine Macro Goal \n5) Close program", end='\n\n'); question=int(input('Select option: '));nl();return question
def nl(): print()
def browserStart():print("Macro Tracker V1 Starting...");driver=webdriver.Safari();print('Opening nutrition website...');driver.get('https://www.myfooddiary.com/');return driver

def main():
    print("Welcome to MacroTracker V1!")
    driver=browserStart()
    todaysDate=str(date.today())

    while True: #User selects option here

        #Initializes or opens today's Macro Summary in a separate file
        try:
            with open('MacroLog.csv', 'r') as macroFile:
                csvList=[line.strip().split(',') for line in macroFile]
        except:
            with open('MacroLog.csv', 'w'):
                csvList=[]
        
        userPick=optionsList()
        try:
            if userPick==1: #-----------------------------------------------------------------------------------------------------------------------------------------
                #User searches
                searchBox= driver.find_element(By.NAME, 'q')
                searchBox.send_keys(input('Search foods here: '))
                nl()
                searchBox.send_keys(Keys.RETURN)
                time.sleep(1)
                #User picks item from search
                nutritionElements=driver.find_elements(By.CLASS_NAME, 'lnkFoodDesc')

                i,j= 0,5
                noResult=False
                while noResult==False: #This shows user items in sets of five and goes back to menu if there are no results found.
                    for itemIndex in range(i,j):
                        try:
                            print(f'{itemIndex+1})\t',nutritionElements[itemIndex].text) #A raise needs to happen here incase the user doom scrolls and the list ends
                        except: 
                            if i==0: noResult=True;print('End reached.'); break
                    else:    
                        userMore=input('Would you like to see more items? (y/n): ').lower()
                        try: 
                            if userMore=='y':i+=5; j+=5;nl()
                            elif userMore=='n': break
                            else: raise Exception
                        except: print("Please select either 'y' or 'n'.", end='\n\n')
                if noResult==True: raise Exception('Please try a different search term')
                while True: #This ensures a valid index was selected
                    try:
                        itemPick=int(input("Which item would you like to view the nutrition of?: "))
                        nl()
                        if itemPick <0 or itemPick >(len(nutritionElements)-1): raise ValueError
                        break
                    except ValueError: print('Item was not a valid index within the list. Please pick an integer from the given list.')

                #Lead up to click selected food item for nutrition facts
                item=nutritionElements[itemPick-1]
                idTag= item.get_attribute("id")
                element=driver.find_element(By.ID, idTag)
                driver.execute_script("arguments[0].click();", element)
                time.sleep(1)

                #Nutritional information printed and saved to memory
                calories=driver.find_element(By.XPATH, '//*[@id="nf_cal_hldr"]/div').text
                fat=driver.find_element(By.CLASS_NAME, "GramsFat").text
                carbohydrates=driver.find_element(By.CLASS_NAME, "GramsCarbs").text
                protein=driver.find_element(By.CLASS_NAME, "GramsProtein").text
                print(f'NUTRITION FACTS:\n{calories=}\n{fat=}\n{carbohydrates=}\n{protein=}')

                calories=float(calories)
                fat=float(fat.replace('g',' '))
                carbohydrates=float(carbohydrates.replace('g',' '))
                protein=float(protein.replace('g',' '))

                #Add to summary prompt
                while True:
                    summaryPrompt=input("Would you like to add this to today's Macro Summary? (y/n): ").lower()

                    try: 
                        if summaryPrompt=='y':
                            if len(csvList)==0:csvList.append(['Date','Calories','Fat','Carbohydrates','Protein'])
                            if todaysDate != csvList[-1][0]: #When either list empty or no entries have been made today
                                csvList.append([todaysDate,calories,fat,carbohydrates,protein])
                            else: #When the user tries to log more data for the second+ time in a given day
                                csvList[-1][1]= calories + float(csvList[-1][1])
                                csvList[-1][2]= fat + float(csvList[-1][2])
                                csvList[-1][3]= carbohydrates + float(csvList[-1][3])
                                csvList[-1][4]= protein + float(csvList[-1][4])
                            with open('MacroLog.csv', 'w', newline='') as macroFile: #Will autoclose when done
                                writer=csv.writer(macroFile)
                                for row in csvList:
                                    writer.writerow(row)
                            break 
                        elif summaryPrompt=='n':
                            break
                        else: 
                            raise Exception
                    except Exception as e: print("Please select either 'y' or 'n'.", end='\n\n')

            elif userPick==2: #-----------------------------------------------------------------------------------------------------------------------------------------
                if csvList[-1][0]==todaysDate: print(f"Today's nutritional summary:\nTotal calories:\t\t {csvList[-1][1]}\nTotal fat:\t\t {csvList[-1][2]}g\nTotal carbohydrates:\t {csvList[-1][3]}g\nTotal protein:\t\t {csvList[-1][4]}g")
                else: print('There are no current entries for today.')
            elif userPick==3: #-----------------------------------------------------------------------------------------------------------------------------------------
                userSummaryDate=input('What day would you like to see the Macro Summary from (format: year-month-day): ')
                nl()
                for row in csvList:
                    if row[0]==userSummaryDate:
                        print(f"{userSummaryDate} nutritional summary:\nTotal calories:\t\t {row[1]}\nTotal fat:\t\t {row[2]}g\nTotal carbohydrates:\t {row[3]}g\nTotal protein:\t\t {row[4]}g")

                else: print('Data not found.') #Nobreak
            elif userPick==4: #Use some formulas to do this -----------------------------------------------------------------------------------------------------------------------------------------
                sex=input('Are you male or female? (m/f): ')
                age=int(input('What is your current age?: '))
                weight=float(input('How much do you currently weigh? (in lbs): '))*0.45359237
                height=float(input('What is your height in inches?: '))*2.54
                activity=input('Are you sedentary, lightly, moderately, or very active? (s,l,m,v):  ')
                goal=input('Are you trying to lose, maintain, or gain weight? (l,m,g): ')
                nl()

                try:
                    if sex=='m': bmr=10*weight+6.25*height-5*age+5
                    elif sex=='f': bmr=10*weight+625*height-5*age-161
                    else: raise Exception('Ensure that you select a correct sex value.')

                    if activity=='s': mult=1.2
                    elif activity=='l': mult=1.375
                    elif activity=='m': mult=1.55
                    elif activity=='v': mult=1.725
                    else: raise Exception('Ensure that you select a correct activity value.')

                    if goal=='l': currentGoal=bmr*mult*.8
                    elif goal=='m': currentGoal=bmr*mult+500
                    elif goal=='g': currentGoal=bmr*mult
                    else: raise Exception('Ensure that you select a correct weight goal value.')
                except Exception as e: print(e)

                print(f'Current goal is: \n{currentGoal} calories \n{currentGoal*.4/4}g of carbohydrates\n{currentGoal*.3/4}g of protein\n {currentGoal*.3/9}g of fat')
            elif userPick==5: #-----------------------------------------------------------------------------------------------------------------------------------------
                print('Goodbye.')
                driver.quit()
                break
            else: raise ValueError
        except ValueError: print('Try again with an integer between 1 and 5') #If one enters a wrong input for the menu prompt.
        except: pass #Most likely, this will be a result of noResult==True

main()