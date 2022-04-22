import pandas as pd

questions = [
    "How often should I clean the air filter?",
    "Why is the PTAC so noisy?",
    "How do I remove the front panel?",
    "Why is the fan not working?",
    "Why is there ice forming on my PTAC?"
]

validation_answers = [
    "The air filter should be cleaned once every two weeks",
    "The fan blades may be loose",
    "Pull out at the bottom to release it from the tabs and then lift up",
    "The fan motor may be faulty or there could be debris in the way restricting its movement",
    "Ice can form due to a buildup of dirt and dust within the system"
]

# How often should I clean the air filter?
ans1 = [
    "Twice a year",
    "You should clean the air filter every two weeks, or more often if necessary.",
    "You should clean the air filters at least every 30 days.",
    "You should clean your air filter at least once each month",
]

# Why is the PTAC so noisy?
ans2 = [
    "This is normal, if it makes a gurgling or whooshing noise that means it is working",
    "The unit might not be installed securely and firmly. However, clicking, gurgling, and whooshing noises are normal during operation of the unit.",
    "Clicking, gurgling, and whooshing noises are normal during operation.",
    "Your heat pump may be breaking down, unless it is the winter in which case it is common to be louder in the winter months"
]

# How do I remove the front panel?
ans3 = [
    "Unscrew 4 screws located in each corner of the front of the machine. Then lift the front panel from the bottom up and gently remove.",
    "Pull the front panel out at the bottom to release it from the tabs, then lift it up.",
    "To remove the front panel, pull out the panel at the bottom of the PTAC to release it from the tabs and then lift it up.",
    "Undo the screws securing the front panel on your unit and then gently lift up to remove the panel"
]

# Why is the fan not working?
ans4 = [
    "Make sure that there is nothing restricting the airflow to the fan. Reset the PTAC to a lower or higher temperature setting",
    "The fan motor works according to the operation of the compressor. If the compressor is off, then the fan will be off.",
    "Make sure that curtains, blinds, or furniture are not restricting or blocking unit airflow. Reset the PTAC to a lower or higher temperature setting. Remove and clean filters.",
    "Check your fan motor for damage"
]

# Why is there ice forming on my PTAC?
ans5 = [
    "When the temperature outside is 55 degrees Fahrenheit, frost could form if the PTAC is in cooling mode. You should switch the unit to fan operation until frost melts. Then remove and clean air filters",
    "When the outdoor temperature is below 55 degrees Fahrenheit or below, frost may form on the indoor coil when the unit is in Cooling mode. Switch the unit to FAN operation until the ice or frost melts.",
    "When the outdoor temperature is 55 degrees Fahrenheit or below, frost may form on the indoor coil when unit is in cooling mode. Switch unit to FAN operation until ice or frost melts, then remove and clean filters",
    "Your PTAC unit may have a dirty air filter as that can cause the buildup of ice"
]

df_top5 = pd.DataFrame({"question": questions, "answer": validation_answers})
# print(df_top5)
for idx, col in enumerate(list(zip(ans1, ans2, ans3, ans4, ans5))):
    df_top5["person_" + str(idx+1)] = col
print(df_top5.head())

df_top5.to_csv("top5validation_answers.csv", index=False)
