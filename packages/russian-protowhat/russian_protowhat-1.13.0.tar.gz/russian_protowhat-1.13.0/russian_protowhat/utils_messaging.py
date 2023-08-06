def get_ord(num):
    assert num > 0, "используйте строго положительные числа в get_ord()"
    nums = {
        1: "первый",
        2: "второй",
        3: "третий",
        4: "четвертый",
        5: "пятый",
        6: "шестой",
        7: "седьмой",
        8: "восьмой",
        9: "девятый",
        10: "десятый",
    }
    if num in nums:
        return nums[num]
    else:
        return (
            {1: "{}й", 2: "{}й", 3: "{}й"}.get(
                num if (num < 20) else (num % 10), "{}й"
            )
        ).format(num)


def get_times(num):
    nums = {1: "однажды", 2: "дважды"}
    if num in nums:
        return nums[num]
    else:
        return "%s раз" % get_num(num)


def get_num(num):
    nums = {
        0: "нет",
        1: "один",
        2: "два",
        3: "три",
        4: "четыре",
        5: "пять",
        6: "шесть",
        7: "семь",
        8: "восемь",
    }
    if num in nums:
        return nums[num]
    else:
        return str(num)
