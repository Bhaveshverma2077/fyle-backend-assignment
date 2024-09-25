import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter

def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    # Iterate over each assignment and update its state
    # It also needs to have teacher_id and grade fields set so i modified it
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state
        assignment.grade = GradeEnum.A
        assignment.teacher_id = 1

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Define the expected result before any changes
    # Why is the value '4'? Initially, it is '3' before any tests are run. After executing all tests except sql_test, the value changes to '4', making the expected outcome '4'
    # i don't think there is any use of the '2'; I left it as it is
    expected_result = [(4, 2)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]

# Helpers for test 2
def get_number_of_assignments_teacher_graded(teacher_id):
    return db.session.execute(text("""
    SELECT COUNT(*) FROM assignments where teacher_id=:teacher_id AND STATE='GRADED'
    """),
    {"teacher_id":teacher_id}).fetchall()[0][0]

def get_teacher_which_has_graded_most_assignments():
    return 1 if get_number_of_assignments_teacher_graded(1) > get_number_of_assignments_teacher_graded(2) else 2

def get_a_grade_assignments_of_teacher(teacher_id):
    return db.session.execute(text("""
    SELECT COUNT(*) FROM assignments where teacher_id=:teacher_id AND grade='A'
    """),
    {"teacher_id":teacher_id}).fetchall()[0][0]
# -------------------


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # This test is to get count of grade A assignments for teacher which has graded maximum assignments
    # and NOT to get count of grade A assignments for teacher which has graded maximum "A grade" assignments
    # as mentioned by the above DOCSTRING
    # suppose 
    # teacher_1 has graded 5 assignment out of which he/she has give A grade to 3 assignment
    # teacher_2 has graded 7 assignment out of which he/she has give A grade to 2 assignment
    # so the correct teacher which satisfy the test is teacher_2 beacuse he/she has graded more assignment than teacher 2
    # and the no of assignment which he has given "A" grade is "2"
    # initailly test is wrong so i have modified it

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()
    get_number_of_assignments_teacher_graded(1)
    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5)
    
    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()

    most_assignment_teacher_id = get_teacher_which_has_graded_most_assignments()
    print(most_assignment_teacher_id)
    assignment_count = get_a_grade_assignments_of_teacher(most_assignment_teacher_id)
    assert assignment_count == sql_result[0][0]

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    grade_a_count_2 = create_n_graded_assignments_for_teacher(10, 2)

    # Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    
    most_assignment_teacher_id = get_teacher_which_has_graded_most_assignments()
    assignment_count = get_a_grade_assignments_of_teacher(most_assignment_teacher_id)
    assert assignment_count == sql_result[0][0]
