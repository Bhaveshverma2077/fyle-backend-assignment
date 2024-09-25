If you want to know how to run the app, please go to `INSTRUCTIONS.md`.

This file contains the points I want to mention:

1. The last two principal tests are failing due to some incompatible data, so I added a migration to update the database.

2. The docstring of the second SQL test suggests something different from what the test actually does. I modified the second SQL test and added comments for better clarity.

3. In SQL test 1, only assignment.state is being set, while assignment.grade and assignment.teacher_id are not. This results in an undesirable database state, so I made modifications to it.
