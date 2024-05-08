import random


def random_choice_with_probabilities(probabilities):
    rnd = random.random()
    cumulative_prob = 0
    for item, prob in probabilities.items():
        cumulative_prob += prob
        if rnd < cumulative_prob:
            if item == "15%":
                return "loss_15"
            elif item == "30%":
                return "loss_30"
            elif item == "40%":
                return "loss_40"
            elif item == "60%":
                return "loss_60"
            elif item == "70%":
                return "loss_70"
            elif item == "80%":
                return "loss_80"
            else:
                return item
    return None


probabilities = {
    "15%": 0.15,
    "30%": 0.30,
    "40%": 0.40,
    "60%": 0.60,
    "70%": 0.70,
    "80%": 0.80
}

