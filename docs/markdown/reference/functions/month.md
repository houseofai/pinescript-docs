### month()

Syntax

```
month(time, timezone) → series int
```

Arguments

time (series int) UNIX time in milliseconds.

timezone (series string) Allows adjusting the returned value to a time zone specified in either UTC/GMT notation (e.g., "UTC-5", "GMT+0530") or as an IANA time zone database name (e.g., "America/New\_York"). Optional. The default is [syminfo.timezone](#var_syminfo.timezone).

Returns

Month (in exchange timezone) for provided UNIX time.

Remarks

UNIX time is the number of milliseconds that have elapsed since 00:00:00 UTC, 1 January 1970.

Note that this function returns the month based on the time of the bar's open. For overnight sessions (e.g. EURUSD, where Monday session starts on Sunday, 17:00 UTC-4) this value can be lower by 1 than the month of the trading day.

See also

[month](#var_month)[time](#fun_time)[year](#fun_year)[dayofmonth](#fun_dayofmonth)[dayofweek](#fun_dayofweek)[hour](#fun_hour)[minute](#fun_minute)[second](#fun_second)
