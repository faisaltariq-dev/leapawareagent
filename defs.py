def count_days_no_leap(
tuple_start_date: tuple[int,int,int],tuple_end_date: tuple[int,int,int]) -> int:
    month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
    start_year,start_month,start_day=tuple_start_date
    end_year,end_month,end_day=tuple_end_date
    count=0
    while (start_year,start_month,start_day)!=(
        end_year,end_month,end_day):
        start_day+=1
        count+=1
        if start_day>month_days[start_month-1]:
            start_day=1
            start_month+=1
            if start_month>12:
                start_month=1
                start_year+=1
    return count

def is_leap_year(year:int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def count_feb29(tuple_start_year:tuple[int,int,int],tuple_end_year:tuple[int, int, int]) -> int:
    start_year, start_month, start_day = tuple_start_year
    end_year, end_month, end_day = tuple_end_year
    count = 0#loop sum of exceptional feb29ths
    for year in range(start_year, end_year + 1):
        
        if not is_leap_year(year):
            continue
        if year==start_year:
            if (start_month, start_day) > (2, 29):
                continue
        if year==end_year:
            if (end_month, end_day) < (2, 29):
                continue
        count += 1
    return count

def has_leap_between(
    tuple_start_date: tuple[int, int, int],
    tuple_end_date: tuple[int, int, int]
) -> bool:

    return (
        count_feb29(
            tuple_start_date,
            tuple_end_date
        ) > 0
    )

def final_difference(
    tuple_start_date: tuple[int,int,int],
    tuple_end_date: tuple[int,int,int]
) -> int:

    return (
        count_days_no_leap(
            tuple_start_date,
            tuple_end_date
        )
        +
        count_feb29(
            tuple_start_date,
            tuple_end_date
        )
    )

def get_leap_years_between(
    tuple_start_date: tuple[int, int, int],
    tuple_end_date: tuple[int, int, int]
) -> list[int]:

    start_year, _, _ = tuple_start_date
    end_year, _, _ = tuple_end_date

    leap_years = []

    for year in range(start_year, end_year + 1):

        if is_leap_year(year):

            leap_years.append(year)

    return leap_years

def count_leap_years_between(
    tuple_start_date: tuple[int, int, int],
    tuple_end_date: tuple[int, int, int]
) -> int:

    return len(
        get_leap_years_between(
            tuple_start_date,
            tuple_end_date
        )
    )

def explain_leap_effect()->str:
    return """A leap year is a year with an extra day added to February, 
    making it 366 days instead of 365 🌍 This happens because the Earth takes
    slightly more than 365 days to orbit the Sun, so the calendar
    occasionally adds February 29 to stay aligned with the seasons."""

