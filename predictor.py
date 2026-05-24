def predict_next(results):

    numbers = [int(x["number"]) for x in results]

    last = numbers[0]

    green = [1,3,7,9]
    red = [2,4,6,8]

    # Simple Pattern Logic
    if last in green:
        next_color = "RED"
    else:
        next_color = "GREEN"

    # Big Small
    if last >= 5:
        next_size = "SMALL"
    else:
        next_size = "BIG"

    return {
        "color": next_color,
        "size": next_size
    }