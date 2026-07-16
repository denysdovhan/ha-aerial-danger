"""Keyword templates for the danger detector."""

# Generic danger phrases that refine specific danger types.
GENERIC_DANGER = [
    r"(буде|бути) гучно",
    r"в укриття",
    r"перебувайте в укритті",
    r"будьте обережними",
    r"курс(ом)? на",
    r"{area} увага!?",
    r"дві стіни",
    r"2 стіни",
    r"від вікон",
    r"вглиб будівель!",
    r"{area} увага",
    r"{area}.+увага",
    r"{area} зреагувати",
    r"{area} жахне",
    r"на {area}!?",
    r"далі {area}",
    r"{area}!+",
    r"❗️?{area}!?",
    r"🟡{area}!",
    r"🟡?🚀.*{area}",
    r"🔴?🚀.*{area}",
    r"🔴❗️.*{area}",
    r"вектор.*{area}",
    r"вектор руху на {area}",
]

# Zircon missile phrases shared by ballistic and cruise detection.
_ZIRCON_DANGER = [
    r"^(?:ще |і ще )?циркон(?: є)?[!.]*$",
    r"^\d+ циркони[!.]*$",
    r"^🔴\s*пуск (?:ракети.*)?циркон",
    r"вихід циркон",
    r"^🔴?\s*циркони? з \w+(?:[!.]* у наш бік)?[!.]*$",
    r"циркони заходять в область",
    r"циркон з (?:півдня|півночі) попередньо",
    r"ще з \w+ (?:на )?циркон",
    r"циркон[аиу]? (?:на|над|у напрямку|у бік) {area}",
    r"циркон повз .* на {area}",
    r"циркон[аи]? {area}",
    r"циркони з \w+ на {area}",
    r"також є циркон.*на {area}",
    r"{area} (?:\d+х? )?циркон",
    r"{area} увага (?:по )?циркон",
    r"{area}.*два циркона",
]

# Ballistic-oriented phrases.
BALLISTIC_DANGER = [
    *_ZIRCON_DANGER,
    r"\bбалістик",
    r"\bбр\b",
    r"балістика на {area}",
    r"наближення балістики",
    r"вихід (балістики|бр)",
    r"вихід з бр",
    r"пуск кинджалу",
    r"cпуск балістики",
    r"кинджал",
    r"швидк(існа|а) {area}",
    r"швидк(існа|а) на {area}",
    r"швидк(існа|а) ціль",
    r"швидк(існа|а) повітряна ціль",
    r"швидк(існа|а) у бік {area}",
    r"{area} швидкісна",
    r"{area} є ціл[ьі!]*",
    r"{area} ціл[ьі!]*",
    r"спуск {area}",
    r"спуск на {area}",
    r"{area} спуск!?",
]

# Cruise-missile oriented phrases (including generic "rocket" wording).
CRUISE_DANGER = [
    *_ZIRCON_DANGER,
    r"кр (на|до|повз|від|через)",
    r"\bкр\b",
    r"кр {area}",
    r"груп(а|и) кр",
    r"груп(а|и) крилатих",
    r"підліт кр",
    r"групи ракет",
    r"крилат(і|их|а)? ракет(и|а)?",
    r"крилаті курсом",
    r"калібр",
    r"крилат[а-яії']*",
    r"ракет(а|и) заход(и|я)ть",
    r"ракет(а|и) (на|до) {area}",
    r"заходить ракета",
    r"{area} ракета",
    r"ракета {area}",
    r"🚀.*?{area}.*?,?\s*йде з",
]

# Drone-oriented phrases.
DRONE_DANGER = [
    r"🛵",
    r"🟡🛵",
    r"заліт",
    r"бпла",
    r"{area} рух!",
    r"маневри",
    r"шахед (над|до|на|повз) {area}",
    r"{area} до вас шахед",
    r"\d+х {area}",
    r"\d+х.*{area}",
    r"у бік {area}",
    r"в бік {area}",
    r"курс(ом)? на {area}",
    r"{area} йде",
]

__all__ = [
    "BALLISTIC_DANGER",
    "CRUISE_DANGER",
    "DRONE_DANGER",
    "GENERIC_DANGER",
]
