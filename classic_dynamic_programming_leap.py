#=1imports:
import defs#importing the definitions of the functions that will be used in the script
#adjust value or make user input:
#=2inputs:
date1=(2020, 1, 1)#start date
date2=(2025, 1, 1)#end date
#=3logic
r1=defs.final_difference(date1, date2)#number of total days between the two dates, accounting for leap years    
r2=defs.has_leap_between(date1, date2)#boolean indicating whether or not leapage occurs between the two dates
r3=defs.count_leap_years_between(date1, date2)#number of leap years between the two dates
r4=defs.get_leap_years_between(date1, date2)#list of the leap years between the two dates
#=4outputs
print(f"{r1} is the number of days between {date1} and {date2} ", end="")#end with no new line so that if leapage is same line
if r2:
    print(f"leapage does occur between these dates {r3} times at {r4} at Feb 29th each")
whatisleapyear=input("enter 1 to learn about what a leap year is, or ctrl+c to exit")
if whatisleapyear=="1":
    print(defs.explain_leap_effect())