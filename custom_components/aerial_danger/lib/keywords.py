"""Keyword templates for the danger detector."""

# Generic danger phrases that refine specific danger types; never used alone.
GENERIC_DANGER = [
    r"(буде|бути) гучно",
    r"в укриття",
    r"перебувайте в укритті",
    r"будьте обережними",
    r"курс(ом)? на",
    r"{area} увага!",
    r"дві стіни",
    r"2 стіни",
    r"від вікон",
    r"вглиб будівель!",
]


# Ballistic-oriented phrases.
BALLISTIC_DANGER = [
    r"🔴🚀",
    r"🟡🚀",
    r"🔴❗️",
    r"балістик",
    r"балістика на {area}",
    r"наближення балістики",
    r"вихід балістики",
    r"вихід бр",
    r"cпуск балістики",
    r"кинджал",
    r"швидкісна ціль",
    r"швидкісна повітряна ціль",
]


# Cruise-missile oriented phrases (including generic "rocket" wording).
CRUISE_DANGER = [
    r"кр на",
    r"кр повз",
    r"кр від",
    r"кр {area}",
    r"група кр",
    r"групи кр",
    r"кр через",
    r"підліт кр",
    r"групи ракет",
    r"крилаті ракети",
    r"крилатих ракет",
    r"крилата ракета",
    r"ракета заходить",
    r"ракети заходять",
    r"ракети на {area}",
    r"ракета на {area}",
    r"{area} ракета",
    r"ракета {area}",
    r"заходить ракета",
    r"{area} ціль!",
    r"{area} цілі!",
    r"ціль на {area}",
    r"ціль швидка на {area}",
    r"спуск {area}",
    r"спуск на {area}",
    r"{area} спуск!",
]


# Drone-oriented phrases.
DRONE_DANGER = [
    r"🟡🛵",
    r"заліт",
    r"бпла",
    r"{area}!",
    r"{area} рух!",
    r"маневри",
    r"шахед на {area}",
    r"\d+х {area}",
]


__all__ = [
    "BALLISTIC_DANGER",
    "CRUISE_DANGER",
    "DRONE_DANGER",
    "GENERIC_DANGER",
]
