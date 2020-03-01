# Change Log for Exam Generation Design Guide

## Table of Contents

- [Change Log for Exam Generation Design Guide](#change-log-for-exam-generation-design-guide)
  - [Table of Contents](#table-of-contents)
  - [3/1/2020](#312020)

## 3/1/2020

- Renamed `"choices"` in JSON output to `"options"`
  - `"options"` is recursively defined now to accommodate sub-question(s)
- Added Change Log itself
- Added `"fill_in_blanks"` question type
- Added `<input>` info
- Updated `"answers"` to include `"fill_in_blanks"` question type where it consists of Ruby regex strings
- Added `"hints"` field
- Added `"difficulty"` field, values ranging `[1, 5]` all inclusive
- Updated `JSON Output Example` Section in accommodation of above changes
- Added `run(config : dict, *args, **kwargs)` function signature requirement.
- Some small wording and typo fixes
