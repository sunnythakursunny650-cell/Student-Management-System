import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import date

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# DATABASE
# =========================================================

DB_PATH = Path(__file__).parent / "students.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            mobile TEXT,
            gender TEXT,
            date_of_birth TEXT,
            course TEXT NOT NULL,
            attendance REAL DEFAULT 0,
            marks REAL DEFAULT 0,
            grade TEXT,
            status TEXT
        )
    """)

    conn.commit()
    return conn


# =========================================================
# GRADE CALCULATION
# =========================================================

def calculate_grade(marks):

    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


def calculate_status(marks, attendance):

    if marks >= 40 and attendance >= 75:
        return "Pass"
    else:
        return "Fail"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.footer {
    text-align: center;
    padding: 30px;
    margin-top: 50px;
    border-top: 1px solid #ddd;
    color: #666;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎓 Student Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Professional Student Records & Academic Management System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎓 Student Management")

option = st.sidebar.radio(
    "Select Operation",
    [
        "📊 Dashboard",
        "➕ Add Student",
        "👥 All Students",
        "🔍 Search Student",
        "✏️ Update Student",
        "🗑️ Delete Student",
        "🏆 Top Performers",
        "📈 Analytics"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if option == "📊 Dashboard":

    st.header("📊 Dashboard")

    conn = get_connection()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_courses = conn.execute(
        "SELECT COUNT(DISTINCT course) FROM students"
    ).fetchone()[0]

    average_marks = conn.execute(
        "SELECT COALESCE(AVG(marks), 0) FROM students"
    ).fetchone()[0]

    highest_marks = conn.execute(
        "SELECT COALESCE(MAX(marks), 0) FROM students"
    ).fetchone()[0]

    pass_count = conn.execute(
        "SELECT COUNT(*) FROM students WHERE status='Pass'"
    ).fetchone()[0]

    conn.close()

    pass_percentage = (
        (pass_count / total_students) * 100
        if total_students > 0
        else 0
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "📚 Total Courses",
            total_courses
        )

    with col3:
        st.metric(
            "📊 Average Marks",
            f"{average_marks:.2f}"
        )

    with col4:
        st.metric(
            "🏆 Highest Marks",
            f"{highest_marks:.2f}"
        )

    with col5:
        st.metric(
            "✅ Pass %",
            f"{pass_percentage:.1f}%"
        )

    st.divider()

    st.subheader("📋 Recent Student Records")

    conn = get_connection()

    data = conn.execute("""
        SELECT
            student_id,
            name,
            email,
            mobile,
            gender,
            date_of_birth,
            course,
            attendance,
            marks,
            grade,
            status
        FROM students
        ORDER BY student_id DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Student ID",
                "Name",
                "Email",
                "Mobile",
                "Gender",
                "Date of Birth",
                "Course",
                "Attendance %",
                "Marks",
                "Grade",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No student records found. Add your first student."
        )


# =========================================================
# ADD STUDENT
# =========================================================

elif option == "➕ Add Student":

    st.header("➕ Add New Student")

    with st.form("add_student_form"):

        col1, col2 = st.columns(2)

        with col1:

            student_id = st.number_input(
                "Student ID",
                min_value=1,
                step=1
            )

            name = st.text_input(
                "Student Name",
                placeholder="Enter full name"
            )

            email = st.text_input(
                "Email",
                placeholder="student@example.com"
            )

            mobile = st.text_input(
                "Mobile Number",
                placeholder="Enter mobile number"
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            )

        with col2:

            

            course = st.text_input(
                "Course",
                placeholder="Example: Python, BCA, MCA"
            )

            attendance = st.number_input(
                "Attendance (%)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=1.0
            )

            marks = st.number_input(
                "Marks",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0
            )

        submitted = st.form_submit_button(
            "➕ Add Student",
            use_container_width=True
        )

        if submitted:

            name = name.strip()
            email = email.strip()
            mobile = mobile.strip()
            course = course.strip()

            if not name:

                st.error(
                    "Please enter Student Name."
                )

            elif not course:

                st.error(
                    "Please enter Course."
                )

            elif mobile and not mobile.isdigit():

                st.error(
                    "Mobile number should contain digits only."
                )

            else:

                conn = get_connection()

                existing = conn.execute(
                    """
                    SELECT student_id
                    FROM students
                    WHERE student_id=?
                    """,
                    (int(student_id),)
                ).fetchone()

                if existing:

                    st.error(
                        "Student ID already exists ❌"
                    )

                    conn.close()

                else:

                    grade = calculate_grade(marks)

                    status = calculate_status(
                        marks,
                        attendance
                    )

                    conn.execute(
                        """
                        INSERT INTO students (
                            student_id,
                            name,
                            email,
                            mobile,
                            gender,
                            date_of_birth,
                            course,
                            attendance,
                            marks,
                            grade,
                            status
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            int(student_id),
                            name,
                            email,
                            mobile,
                            gender,
                            str(date_of_birth),
                            course,
                            attendance,
                            marks,
                            grade,
                            status
                        )
                    )

                    conn.commit()
                    conn.close()

                    st.success(
                        f"Student {name} added successfully! 🎉"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Marks",
                            f"{marks:.1f}"
                        )

                    with col2:
                        st.metric(
                            "Grade",
                            grade
                        )

                    with col3:
                        st.metric(
                            "Status",
                            status
                        )


# =========================================================
# ALL STUDENTS
# =========================================================

elif option == "👥 All Students":

    st.header("👥 All Students")

    conn = get_connection()

    data = conn.execute("""
        SELECT
            student_id,
            name,
            email,
            mobile,
            gender,
            date_of_birth,
            course,
            attendance,
            marks,
            grade,
            status
        FROM students
        ORDER BY student_id
    """).fetchall()

    conn.close()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Student ID",
                "Name",
                "Email",
                "Mobile",
                "Gender",
                "Date of Birth",
                "Course",
                "Attendance %",
                "Marks",
                "Grade",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            f"Total Students: {len(data)}"
        )

    else:

        st.warning(
            "No student records found."
        )


# =========================================================
# SEARCH STUDENT
# =========================================================

elif option == "🔍 Search Student":

    st.header("🔍 Search Student")

    search_type = st.selectbox(
        "Search By",
        [
            "Student ID",
            "Student Name",
            "Course"
        ]
    )

    search_value = st.text_input(
        "Enter Search Value"
    )

    if st.button(
        "🔍 Search",
        use_container_width=True
    ):

        if not search_value.strip():

            st.error(
                "Please enter a search value."
            )

        else:

            conn = get_connection()

            if search_type == "Student ID":

                try:

                    student_id = int(
                        search_value.strip()
                    )

                    data = conn.execute(
                        """
                        SELECT
                            student_id,
                            name,
                            email,
                            mobile,
                            gender,
                            date_of_birth,
                            course,
                            attendance,
                            marks,
                            grade,
                            status
                        FROM students
                        WHERE student_id=?
                        """,
                        (student_id,)
                    ).fetchall()

                except ValueError:

                    data = []

            elif search_type == "Student Name":

                data = conn.execute(
                    """
                    SELECT
                        student_id,
                        name,
                        email,
                        mobile,
                        gender,
                        date_of_birth,
                        course,
                        attendance,
                        marks,
                        grade,
                        status
                    FROM students
                    WHERE name LIKE ?
                    """,
                    (f"%{search_value.strip()}%",)
                ).fetchall()

            else:

                data = conn.execute(
                    """
                    SELECT
                        student_id,
                        name,
                        email,
                        mobile,
                        gender,
                        date_of_birth,
                        course,
                        attendance,
                        marks,
                        grade,
                        status
                    FROM students
                    WHERE course LIKE ?
                    """,
                    (f"%{search_value.strip()}%",)
                ).fetchall()

            conn.close()

            if data:

                df = pd.DataFrame(
                    data,
                    columns=[
                        "Student ID",
                        "Name",
                        "Email",
                        "Mobile",
                        "Gender",
                        "Date of Birth",
                        "Course",
                        "Attendance %",
                        "Marks",
                        "Grade",
                        "Status"
                    ]
                )

                st.success(
                    f"{len(data)} student record(s) found."
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.error(
                    "No student found ❌"
                )


# =========================================================
# UPDATE STUDENT
# =========================================================

elif option == "✏️ Update Student":

    st.header("✏️ Update Student Details")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    if st.button(
        "🔍 Load Student",
        use_container_width=True
    ):

        conn = get_connection()

        student = conn.execute(
            """
            SELECT
                student_id,
                name,
                email,
                mobile,
                gender,
                date_of_birth,
                course,
                attendance,
                marks
            FROM students
            WHERE student_id=?
            """,
            (int(student_id),)
        ).fetchone()

        conn.close()

        if student:

            st.session_state["edit_student"] = student

        else:

            st.session_state["edit_student"] = None

            st.error(
                "Student not found ❌"
            )

    if "edit_student" in st.session_state:

        student = st.session_state["edit_student"]

        if student:

            st.success(
                f"Student found: {student[1]} ✅"
            )

            with st.form("update_student_form"):

                col1, col2 = st.columns(2)

                with col1:

                    new_name = st.text_input(
                        "Student Name",
                        value=student[1]
                    )

                    new_email = st.text_input(
                        "Email",
                        value=student[2] or ""
                    )

                    new_mobile = st.text_input(
                        "Mobile",
                        value=student[3] or ""
                    )

                    new_gender = st.selectbox(
                        "Gender",
                        ["Male", "Female", "Other"],
                        index=(
                            ["Male", "Female", "Other"].index(
                                student[4]
                            )
                            if student[4] in
                            ["Male", "Female", "Other"]
                            else 0
                        )
                    )

                with col2:

                    new_dob = st.text_input(
                        "Date of Birth",
                        value=student[5] or ""
                    )

                    new_course = st.text_input(
                        "Course",
                        value=student[6]
                    )

                    new_attendance = st.number_input(
                        "Attendance (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(student[7] or 0),
                        step=1.0
                    )

                    new_marks = st.number_input(
                        "Marks",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(student[8] or 0),
                        step=1.0
                    )

                update_button = st.form_submit_button(
                    "💾 Update Student",
                    use_container_width=True
                )

                if update_button:

                    if not new_name.strip():

                        st.error(
                            "Student name cannot be empty."
                        )

                    elif not new_course.strip():

                        st.error(
                            "Course cannot be empty."
                        )

                    elif (
                        new_mobile.strip()
                        and not new_mobile.strip().isdigit()
                    ):

                        st.error(
                            "Mobile number should contain digits only."
                        )

                    else:

                        new_grade = calculate_grade(
                            new_marks
                        )

                        new_status = calculate_status(
                            new_marks,
                            new_attendance
                        )

                        conn = get_connection()

                        conn.execute(
                            """
                            UPDATE students
                            SET
                                name=?,
                                email=?,
                                mobile=?,
                                gender=?,
                                date_of_birth=?,
                                course=?,
                                attendance=?,
                                marks=?,
                                grade=?,
                                status=?
                            WHERE student_id=?
                            """,
                            (
                                new_name.strip(),
                                new_email.strip(),
                                new_mobile.strip(),
                                new_gender,
                                new_dob.strip(),
                                new_course.strip(),
                                new_attendance,
                                new_marks,
                                new_grade,
                                new_status,
                                int(student_id)
                            )
                        )

                        conn.commit()
                        conn.close()

                        st.session_state.pop(
                            "edit_student",
                            None
                        )

                        st.success(
                            "Student updated successfully! ✅"
                        )

                        st.rerun()


# =========================================================
# DELETE STUDENT
# =========================================================

elif option == "🗑️ Delete Student":

    st.header("🗑️ Delete Student")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    st.warning(
        "⚠️ Deleting a student record cannot be undone."
    )

    if st.button(
        "🔍 Check Student",
        use_container_width=True
    ):

        conn = get_connection()

        student = conn.execute(
            """
            SELECT
                student_id,
                name,
                course,
                marks,
                grade,
                status
            FROM students
            WHERE student_id=?
            """,
            (int(student_id),)
        ).fetchone()

        conn.close()

        if student:

            st.session_state[
                "delete_student"
            ] = student

        else:

            st.session_state[
                "delete_student"
            ] = None

            st.error(
                "Student not found ❌"
            )

    if "delete_student" in st.session_state:

        student = st.session_state[
            "delete_student"
        ]

        if student:

            st.warning(
                f"You are about to delete "
                f"{student[1]} (ID: {student[0]})."
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Student ID",
                    student[0]
                )

            with col2:

                st.metric(
                    "Student Name",
                    student[1]
                )

            with col3:

                st.metric(
                    "Marks",
                    f"{student[3]:.1f}"
                )

            confirm = st.checkbox(
                "I confirm that I want to permanently delete this student."
            )

            if confirm:

                if st.button(
                    "🗑️ Permanently Delete Student",
                    use_container_width=True,
                    type="primary"
                ):

                    conn = get_connection()

                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        DELETE FROM students
                        WHERE student_id=?
                        """,
                        (int(student[0]),)
                    )

                    conn.commit()

                    deleted = cursor.rowcount

                    conn.close()

                    if deleted == 1:

                        st.session_state.pop(
                            "delete_student",
                            None
                        )

                        st.success(
                            f"Student {student[0]} deleted successfully! ✅"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Student could not be deleted ❌"
                        )


# =========================================================
# TOP PERFORMERS
# =========================================================

elif option == "🏆 Top Performers":

    st.header("🏆 Top Performing Students")

    conn = get_connection()

    data = conn.execute(
        """
        SELECT
            student_id,
            name,
            course,
            marks,
            grade,
            attendance,
            status
        FROM students
        ORDER BY marks DESC
        LIMIT 5
        """
    ).fetchall()

    conn.close()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Student ID",
                "Name",
                "Course",
                "Marks",
                "Grade",
                "Attendance %",
                "Status"
            ]
        )

        st.subheader("🥇 Top 5 Students")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        top_student = data[0]

        st.success(
            f"🏆 Top Student: {top_student[1]} "
            f"with {top_student[3]:.1f} marks"
        )

    else:

        st.info(
            "No student records available."
        )


# =========================================================
# ANALYTICS
# =========================================================

elif option == "📈 Analytics":

    st.header("📈 Academic Analytics")

    conn = get_connection()

    data = conn.execute(
        """
        SELECT
            student_id,
            name,
            course,
            marks,
            attendance,
            grade,
            status
        FROM students
        """
    ).fetchall()

    conn.close()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Student ID",
                "Name",
                "Course",
                "Marks",
                "Attendance",
                "Grade",
                "Status"
            ]
        )

        # -------------------------------------------------
        # PASS / FAIL
        # -------------------------------------------------

        st.subheader("🎯 Pass / Fail Statistics")

        pass_count = len(
            df[df["Status"] == "Pass"]
        )

        fail_count = len(
            df[df["Status"] == "Fail"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Students",
                len(df)
            )

        with col2:

            st.metric(
                "✅ Passed",
                pass_count
            )

        with col3:

            st.metric(
                "❌ Failed",
                fail_count
            )

        st.divider()

        # -------------------------------------------------
        # GRADE DISTRIBUTION
        # -------------------------------------------------

        st.subheader("🎓 Grade Distribution")

        grade_counts = (
            df["Grade"]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(
            grade_counts
        )

        st.divider()

        # -------------------------------------------------
        # COURSE-WISE AVERAGE
        # -------------------------------------------------

        st.subheader("📚 Course-wise Average Marks")

        course_average = (
            df.groupby("Course")["Marks"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            course_average
        )

        st.divider()

        # -------------------------------------------------
        # MARKS DISTRIBUTION
        # -------------------------------------------------

        st.subheader("📊 Marks Distribution")

        st.line_chart(
            df.sort_values("Marks")[
                ["Marks"]
            ]
        )

        st.divider()

        # -------------------------------------------------
        # ATTENDANCE
        # -------------------------------------------------

        st.subheader("📅 Attendance Overview")

        average_attendance = df[
            "Attendance"
        ].mean()

        low_attendance = len(
            df[df["Attendance"] < 75]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Average Attendance",
                f"{average_attendance:.1f}%"
            )

        with col2:

            st.metric(
                "Students Below 75%",
                low_attendance
            )

    else:

        st.info(
            "No student data available for analytics."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        <h3>🎓 Student Management System</h3>

        <p>
            Python + SQLite + Streamlit
        </p>

        <p>
            Professional Student Records & Academic Management
        </p>

        <p>
            Developed by <b>Sunny Thakur</b> 💫
        </p>

    </div>
    """,
    unsafe_allow_html=True
)