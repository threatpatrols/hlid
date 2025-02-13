# HLID: a Human Lexicographically (sortable) Identifier

The HLID is a human-readable lexicographically sortable identifier that borrows 
from similar concepts such as -

 * ULID (Universally-Unique, Lexicographically-Sortable Identifier) - https://github.com/ulid/spec
 * UUID7 (Time-ordered UUID with millisecond precision) - https://www.ietf.org/archive/id/draft-peabody-dispatch-new-uuid-format-04.html#name-uuid-version-7

The difference with a HLID is that they are human-readable that generally makes
them easier to work with especially in development stages.   

HLIDs have the following properties -

 * Time sortable
 * Human readable in UTC timezone
 * 10^4 seconds time resolution (tenth of milliseconds)
 * 8 bits of user-data (two hex chars)
 * 48 bits of nonce; optionally derived from a truncated hmac-sha256 (12x hex chars)
 * Can be swapped with UUID-type or ULID-type values

With all good things there are tradeoffs -

 * These values are not cryptographically secure for inputs into to strong 
   crypto routines.
 * HLID can provide at best tenth-of-millisecond time resolution, whereas UUID7
   provides 50 nanosecond resolution.
 * Because the HMAC is truncated, a larger secret value is enforced (128 bits).

For example a HLID value -

```text
    20241105-1108-5200-00ff-8fa646f09a7e
    ^        ^    ^ ^  ^ ^  ^
    |        |    | |  | |  |- 12x hex: nonce-value -or- hmac-value
    |        |    | |  | |- 2x hex: one byte of user-data; 2x hex chars
    |        |    | |+ |- 4x digits: -10^4 seconds; tenth of millisecond
    |        |    |- 2x digits: seconds
    |        |- 4x digits: hours and minutes
    |- 8x digits: year and month and day
    
    All values are zero-padded when required.
```
