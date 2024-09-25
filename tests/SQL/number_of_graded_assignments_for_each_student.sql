-- Write query to get number of graded assignments for each student:
SELECT Count(*)
FROM assignments
GROUP BY student_id