-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH count_table AS (
    SELECT COUNT(*) AS assignment_graded_count, teacher_id
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
teacher_with_max_graded_assignments AS (
    SELECT teacher_id
    FROM count_table
    WHERE assignment_graded_count = (
        SELECT MAX(assignment_graded_count)
        FROM count_table
    )
)
SELECT COUNT(*)
FROM assignments
WHERE grade = 'A' AND teacher_id = (SELECT teacher_id FROM teacher_with_max_graded_assignments);
