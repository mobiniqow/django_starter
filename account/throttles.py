from rest_framework.throttling import UserRateThrottle


class SevenPerMinuteThrottle(UserRateThrottle):
    scope = "auth"


class TwentyPerHourThrottle(UserRateThrottle):
    scope = "twenty_per_hour"


class FiftyPerDay(UserRateThrottle):
    scope = "fifty_per_day"
