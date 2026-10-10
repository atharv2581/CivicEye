import streamlit as st
from database import get_connection
from ai import analyze_complaint


ADMIN_USERNAME = st.secrets["admin"]["username"]
ADMIN_PASSWORD = st.secrets["admin"]["password"]


st.set_page_config(
    page_title="CivicEye | AI Civic Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main application */
    .stApp {
        background-color: #F5F7FB;
        color: #172033;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5EAF2;
    }

    [data-testid="stSidebar"] * {
        color: #172033;
    }

    /* Header */
    [data-testid="stHeader"] {
        background-color: #F5F7FB;
    }

    /* Headings */
    h1, h2, h3 {
        color: #172033 !important;
        font-weight: 700;
    }

    p, label {
        color: #374151;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
    }

    div[data-testid="stMetricValue"] {
        color: #2563EB;
        font-weight: 700;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #2563EB;
        color: #FFFFFF;
        border: 1px solid #2563EB;
        border-radius: 9px;
        padding: 9px 20px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #1D4ED8;
        border-color: #1D4ED8;
        color: #FFFFFF;
    }

    /* Input fields */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        background-color: transparent !important;
    }

    div[data-baseweb="select"] * {
        color: #111827;
    }

    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 12px;
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 10px;
    }

    /* Dividers */
    hr {
        border-color: #E5EAF2;
    }

    /* Links */
    a {
        color: #2563EB;
    }

    /* Success, warning and error messages */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Form containers */
    [data-testid="stForm"] {
        background-color: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 24px;
    }
</style>
""", unsafe_allow_html=True)

st.title("CivicEye")


page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Report a Problem",
	"Track a Complaint",
        "Admin Dashboard"
    ]
)


# ==================================================
# REPORT A PROBLEM
# ==================================================

if page == "Report a Problem":

    st.header("Report a Civic Problem")

    problem = st.selectbox(
        "What is the problem?",
        [
            "Pothole",
            "Broken Streetlight",
            "Garbage",
            "Other"
        ]
    )

    description = st.text_area(
        "Describe the problem"
    )

    location = st.text_input(
        "Where is the problem?"
    )

    if st.button("Submit Report"):

        if (
            not description.strip()
            or not location.strip()
        ):

            st.warning(
                "Please provide a description and location."
            )

        else:

            with st.spinner(
                "Analyzing your complaint with AI..."
            ):

                try:

                    # AI ANALYSIS

                    ai_result = analyze_complaint(
                        problem,
                        description,
                        location
                    )


                    # DATABASE CONNECTION

                    db = get_connection()

                    cursor = db.cursor()


                    # INSERT REPORT

                    query = """
                        INSERT INTO reports
                        (
                            problem,
                            description,
                            location,
                            category,
                            severity,
                            priority,
                            department,
                            summary,
                            reason
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                    """


                    cursor.execute(
                        query,
                        (
                            problem,
                            description,
                            location,
                            ai_result["category"],
                            ai_result["severity"],
                            ai_result["priority"],
                            ai_result["department"],
                            ai_result["summary"],
                            ai_result["reason"]
                        )
                    )

                    db.commit()

		    # Get the ID of the complaint we just inserted
                    complaint_id = cursor.lastrowid

                    cursor.close()
                    db.close()

                    # SUCCESS
                    st.success(
                    "Your report has been submitted!"
                    )

                    st.info(f"Your Complaint Reference ID: CIV-{complaint_id:06d}")

                    st.write("Save this reference ID to track your complaint later.")

                    # SHOW AI ANALYSIS

                    st.subheader(
                        "AI Analysis"
                    )


                    st.write(
                        "**Category:**",
                        ai_result["category"]
                    )

                    st.write(
                        "**Severity:**",
                        ai_result["severity"]
                    )

                    st.write(
                        "**Priority:**",
                        ai_result["priority"]
                    )

                    st.write(
                        "**Department:**",
                        ai_result["department"]
                    )

                    st.write(
                        "**Summary:**",
                        ai_result["summary"]
                    )

                    st.write(
                        "**Reason:**",
                        ai_result["reason"]
                    )


                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# ==================================================
# ADMIN DASHBOARD
# ==================================================

elif page == "Admin Dashboard":

    st.header("Admin Login")


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            st.session_state.admin_logged_in = True

            st.success(
                "Login successful!"
            )

        else:

            st.error(
                "Incorrect username or password."
            )


    # ==================================================
    # LOGGED IN DASHBOARD
    # ==================================================

    if st.session_state.get(
        "admin_logged_in",
        False
    ):

        st.header(
            "CivicEye Admin Dashboard"
        )


        # ==================================================
        # GET REPORTS
        # ==================================================

        db = get_connection()

        cursor = db.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT
                id,
                problem,
                description,
                location,
                status,
                category,
                severity,
                priority,
                department,
                summary,
                reason,
                admin_notes,
                created_at,
		resolved_at
            FROM reports
            ORDER BY created_at DESC
            """
        )


        reports = cursor.fetchall()


        cursor.close()
        db.close()


        # ==================================================
        # DASHBOARD METRICS
        # ==================================================

        total_reports = len(reports)


        pending_reports = sum(
            1
            for report in reports
            if report["status"] == "Pending"
        )


        in_progress_reports = sum(
            1
            for report in reports
            if report["status"] == "In Progress"
        )


        resolved_reports = sum(
            1
            for report in reports
            if report["status"] == "Resolved"
        )


        urgent_reports = sum(
            1
            for report in reports
            if report["priority"] == "Urgent"
        )


        col1, col2, col3, col4, col5 = st.columns(5)


        col1.metric(
            "Total",
            total_reports
        )


        col2.metric(
            "Pending",
            pending_reports
        )


        col3.metric(
            "In Progress",
            in_progress_reports
        )


        col4.metric(
            "Resolved",
            resolved_reports
        )


        col5.metric(
            "🚨 Urgent",
            urgent_reports
        )

	# ==================================================
        # RESOLUTION TIME ANALYTICS
        # ==================================================


        resolution_hours = []

        for report in reports:
            resolved_at = report.get("resolved_at")
            created_at = report.get("created_at")

            if resolved_at and created_at:
                try:
                    duration = resolved_at - created_at
                    hours = duration.total_seconds() / 3600

                    if hours >= 0:
                        resolution_hours.append(hours)

                except (TypeError, AttributeError):
                    pass

        st.subheader("Resolution Analytics")

        if resolution_hours:
            average_hours = (
                sum(resolution_hours) / len(resolution_hours)
            )

            average_days = average_hours / 24

            metric_col1, metric_col2 = st.columns(2)

            metric_col1.metric(
                "Average Resolution Time",
                f"{average_hours:.1f} hours"
            )

            metric_col2.metric(
                "Complaints With Resolution Data",
                len(resolution_hours)
            )

            st.caption(
                f"Approximately {average_days:.2f} days on average. "
                "Only complaints with valid resolution timestamps "
                "are included."
            )

        else:
            st.info(
                "Resolution-time analytics will appear after "
                "complaints have valid resolution timestamps."
            )

        # ==================================================
        # DEPARTMENT WORKLOAD
        # ==================================================

        st.subheader("Department Workload")

        department_counts = {}

        for report in reports:
            department = report.get("department") or "Unassigned"

            department_counts[department] = (
                department_counts.get(department, 0) + 1
            )

        if department_counts:
            department_data = {
                "Department": list(department_counts.keys()),
                "Complaints": list(department_counts.values())
            }

            st.bar_chart(
                department_data,
                x="Department",
                y="Complaints"
            )
        else:
            st.info("No department data is available yet.")

        # ==================================================
        # PRIORITY DISTRIBUTION
        # ==================================================

        st.subheader("Priority Distribution")

        priority_counts = {}

        for report in reports:
            priority = report.get("priority") or "Unassigned"

            priority_counts[priority] = (
                priority_counts.get(priority, 0) + 1
            )

        if priority_counts:
            priority_data = {
                "Priority": list(priority_counts.keys()),
                "Complaints": list(priority_counts.values())
            }

            st.bar_chart(
                priority_data,
                x="Priority",
                y="Complaints"
            )
        else:
            st.info("No priority data is available yet.")

        st.write("---")


        # ==================================================
        # SEARCH
        # ==================================================

        st.subheader(
            "Find Reports"
        )


        search = st.text_input(
            "Search complaints",
            placeholder=(
                "Search by problem, description "
                "or location..."
            )
        )


        # ==================================================
        # FILTERS
        # ==================================================

        col1, col2, col3 = st.columns(3)


        with col1:

            status_filter = st.selectbox(
                "Status",
                [
                    "All",
                    "Pending",
                    "In Progress",
                    "Resolved"
                ]
            )


        with col2:

            priority_filter = st.selectbox(
                "Priority",
                [
                    "All",
                    "Urgent",
                    "High",
                    "Medium",
                    "Low"
                ]
            )


        with col3:

            department_filter = st.selectbox(
                "Department",
                [
                    "All",
                    "Roads & Infrastructure",
                    "Electrical",
                    "Sanitation",
                    "General"
                ]
            )


        # ==================================================
        # FILTER REPORTS
        # ==================================================

        filtered_reports = []


        for report in reports:

            if (
                status_filter != "All"
                and report["status"] != status_filter
            ):

                continue


            if (
                priority_filter != "All"
                and report["priority"] != priority_filter
            ):

                continue


            if (
                department_filter != "All"
                and report["department"] != department_filter
            ):

                continue


            if search.strip():

                search_text = (
                    str(report["problem"])
                    + " "
                    + str(report["description"])
                    + " "
                    + str(report["location"])
                ).lower()


                if search.lower() not in search_text:

                    continue


            filtered_reports.append(
                report
            )


        st.write(
            f"Showing **{len(filtered_reports)}** "
            f"of **{total_reports}** reports"
        )


        # ==================================================
        # DISPLAY REPORTS
        # ==================================================

        for report in filtered_reports:

            priority = report["priority"]


            if priority == "Urgent":

                priority_icon = "🚨"

            elif priority == "High":

                priority_icon = "🔴"

            elif priority == "Medium":

                priority_icon = "🟠"

            else:

                priority_icon = "🟢"


            with st.expander(
                f"{priority_icon} "
                f"{report['problem']} — "
                f"{priority} Priority"
            ):


                st.write(
                    f"**Report ID:** "
                    f"#{report['id']}"
                )


                st.write(
                    f"**Submitted:** "
                    f"{report['created_at']}"
                )


                st.write(
                    f"**Location:** "
                    f"{report['location']}"
                )


                st.write(
                    f"**Description:** "
                    f"{report['description']}"
                )


                st.write("---")


                # ==================================================
                # AI ANALYSIS
                # ==================================================

                st.subheader(
                    "AI Analysis"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        f"**Category:** "
                        f"{report['category']}"
                    )


                    st.write(
                        f"**Severity:** "
                        f"{report['severity']}"
                    )


                    st.write(
                        f"**Priority:** "
                        f"{report['priority']}"
                    )


                with col2:

                    st.write(
                        f"**Department:** "
                        f"{report['department']}"
                    )


                st.info(
                    f"**AI Summary:** "
                    f"{report['summary']}"
                )


                if report["reason"]:

                    st.write(
                        f"**AI Reason:** "
                        f"{report['reason']}"
                    )

                else:

                    st.write(
                        "**AI Reason:** "
                        "No reason available."
                    )


                st.write("---")


                # ==================================================
                # MANAGE REPORT
                # ==================================================

                st.subheader("Manage Report")

                current_status = report["status"]

                new_status = st.selectbox(
                    "Status",
                    [
                        "Pending",
                        "In Progress",
                        "Resolved"
                    ],
                    index=[
                        "Pending",
                        "In Progress",
                        "Resolved"
                    ].index(current_status),
                    key=f"status_{report['id']}"
                )

                admin_notes = st.text_area(
                    "Admin Notes",
                    value=report["admin_notes"] or "",
                    placeholder="Add notes about this complaint...",
                    key=f"notes_{report['id']}"
                )

                if st.button(
                    "Save Changes",
                    key=f"save_{report['id']}"
                ):
                    db = None
                    cursor = None

                    try:
                        db = get_connection()
                        db.start_transaction()
                        cursor = db.cursor()

                        cursor.execute(
                            """
                            UPDATE reports
                            SET
                                status = %s,
                                admin_notes = %s,
                                resolved_at = CASE
                                    WHEN %s = 'Resolved'
                                         AND %s != 'Resolved'
                                        THEN CURRENT_TIMESTAMP
                                    WHEN %s != 'Resolved'
                                        THEN NULL
                                    ELSE resolved_at
                                END
                            WHERE id = %s
                            """,
                            (
                                new_status,
                                admin_notes,
                                new_status,
                                current_status,
                                new_status,
                                report["id"]
                            )
                        )

                        if new_status != current_status:
                            cursor.execute(
                                """
                                INSERT INTO complaint_history (
                                    complaint_id,
                                    old_status,
                                    new_status
                                )
                                VALUES (%s, %s, %s)
                                """,
                                (
                                    report["id"],
                                    current_status,
                                    new_status
                                )
                            )

                        db.commit()

                        st.success(
                            f"Report #{report['id']} updated!"
                        )

                        st.rerun()

                    except Exception:
                        if db is not None:
                            db.rollback()

                        st.error(
                            "Unable to save changes. "
                            "Please check the database and try again."
                        )

                    finally:
                        if cursor is not None:
                            cursor.close()

                        if db is not None:
                            db.close()

        # ==================================================
        # ANALYTICS
        # ==================================================

        st.write("---")


        st.header(
            "CivicEye Analytics"
        )


        category_counts = {}

        department_counts = {}

        priority_counts = {}


        for report in reports:

            category = report["category"]

            department = report["department"]

            priority = report["priority"]


            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )


            department_counts[department] = (
                department_counts.get(department, 0) + 1
            )


            priority_counts[priority] = (
                priority_counts.get(priority, 0) + 1
            )


        col1, col2 = st.columns(2)


        with col1:

            st.subheader(
                "Reports by Category"
            )

            st.bar_chart(
                category_counts
            )


        with col2:

            st.subheader(
                "Reports by Department"
            )

            st.bar_chart(
                department_counts
            )


        st.subheader(
            "Reports by Priority"
        )


        st.bar_chart(
            priority_counts
        )

# ==========================================================
# TRACK A COMPLAINT
# ==========================================================

if page == "Track a Complaint":

    st.header("Track Your Complaint")

    st.write(
        "Enter the complaint reference ID you received "
        "after submitting your report."
    )

    reference_id = st.text_input(
        "Complaint Reference ID",
        placeholder="Example: CIV-000015"
    )

    if st.button("Track Complaint"):

        reference_id = reference_id.strip().upper()

        if not reference_id.startswith("CIV-"):
            st.error(
                "Invalid reference ID format. "
                "Use a format like CIV-000015."
            )

        else:
            id_part = reference_id[4:]

            if not id_part.isdigit():
                st.error(
                    "Invalid reference ID. "
                    "Please check the ID and try again."
                )

            else:
                complaint_id = int(id_part)

                db = None
                cursor = None

                try:
                    db = get_connection()
                    cursor = db.cursor(dictionary=True)

                    cursor.execute(
                        """
                        SELECT
                            id,
                            problem,
                            status,
                            category,
                            severity,
                            priority,
                            department,
                            summary,
                            created_at
                        FROM reports
                        WHERE id = %s
                        """,
                        (complaint_id,)
                    )

                    complaint = cursor.fetchone()

                    if complaint is None:
                        st.error(
                            "No complaint was found with that "
                            "reference ID. Please check the ID."
                        )

                    else:
                        cursor.execute(
                            """
                            SELECT
                                old_status,
                                new_status,
                                changed_at
                            FROM complaint_history
                            WHERE complaint_id = %s
                            ORDER BY changed_at ASC, history_id ASC
                            """,
                            (complaint_id,)
                        )

                        history = cursor.fetchall()

                        st.success(
                            f"Complaint found: "
                            f"CIV-{complaint['id']:06d}"
                        )

                        st.subheader("Complaint Details")

                        st.write(
                            "**Problem:**",
                            complaint["problem"] or "Not available"
                        )

                        st.write(
                            "**Category:**",
                            complaint["category"] or "Not available"
                        )

                        st.write(
                            "**Department:**",
                            complaint["department"] or "Not assigned"
                        )

                        st.write(
                            "**Priority:**",
                            complaint["priority"] or "Not available"
                        )

                        st.write(
                            "**Severity:**",
                            complaint["severity"] or "Not available"
                        )

                        st.write(
                            "**Submitted:**",
                            complaint["created_at"]
                            or "Not available"
                        )

                        st.subheader("Current Status")

                        status = complaint["status"] or "Pending"

                        if status == "Resolved":
                            st.success("Resolved")

                        elif status == "In Progress":
                            st.info("In Progress")

                        else:
                            st.warning("Pending")

                        st.subheader("Complaint Timeline")

                        st.write(
                            "Follow the status updates recorded "
                            "for your complaint."
                        )

                        st.markdown(
                            f"**Complaint submitted**  \n"
                            f"Status at submission: Pending  \n"
                            f"Time: {complaint['created_at'] or 'Not available'}"
                        )

                        if history:
                            for event in history:
                                st.markdown(
                                    f"**Status changed: "
                                    f"{event['old_status'] or 'Unknown'} "
                                    f"→ {event['new_status']}**  \n"
                                    f"Time: {event['changed_at']}"
                                )
                        else:
                            st.info(
                                "No status changes have been recorded "
                                "yet. Updates will appear here when "
                                "the complaint's status changes."
                            )

                        st.subheader("AI Summary")

                        st.write(
                            complaint["summary"]
                            or "No summary available."
                        )

                except Exception:
                    st.error(
                        "Unable to retrieve the complaint right now. "
                        "Please try again."
                    )

                finally:
                    if cursor is not None:
                        cursor.close()

                    if db is not None:
                        db.close()
