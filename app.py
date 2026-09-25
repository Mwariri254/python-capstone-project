import streamlit as st

from visitor_checkin_system import (
    check_in_visitor,
    check_out_visitor,
    delete_visitor,
    edit_visitor,
    initialize_database,
    search_visitors,
    view_all_visitors,
    view_todays_visitors,
)


st.set_page_config(
    page_title="Visitor Desk",
    page_icon="V",
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_database()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --ink: #17211b;
        --muted: #65736a;
        --paper: #f6f7f2;
        --panel: #ffffff;
        --line: #dce3da;
        --accent: #ee6c4d;
        --accent-dark: #c95137;
    }

    .stApp { background: var(--paper); color: var(--ink); }
    .block-container { max-width: 1180px; padding-top: 3rem; padding-bottom: 4rem; }
    h1, h2, h3, p, label, div { font-family: 'DM Sans', sans-serif; }
    h1 { letter-spacing: -0.04em; font-size: 3.2rem !important; line-height: 1 !important; }
    h2, h3 { letter-spacing: -0.025em; }
    [data-testid="stMetric"] { background: var(--panel); border: 1px solid var(--line); padding: 1rem 1.2rem; border-radius: 12px; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); font-family: 'Space Mono', monospace; }
    .eyebrow { color: var(--accent-dark); font-family: 'Space Mono', monospace; font-size: .75rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
    .subtitle { color: var(--muted); font-size: 1.05rem; margin-top: -.6rem; margin-bottom: 2rem; }
    .section-label { color: var(--muted); font-family: 'Space Mono', monospace; font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; margin: 1.5rem 0 .6rem; }
    div[data-testid="stForm"] { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 1.25rem; }
    .stButton > button, .stFormSubmitButton > button { border-radius: 8px; font-weight: 700; border: 1px solid var(--ink); min-height: 2.7rem; }
    .stFormSubmitButton > button[kind="primary"] { background: var(--accent); border-color: var(--accent); color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 1.5rem; }
    .stTabs [data-baseweb="tab"] { color: var(--muted); }
    .stTabs [aria-selected="true"] { color: var(--ink); }
    </style>
    """,
    unsafe_allow_html=True,
)


def refresh_data():
    all_visitors = view_all_visitors()
    today_visitors = view_todays_visitors()
    checked_in = int((all_visitors["status"] == "Checked In").sum()) if not all_visitors.empty else 0
    return all_visitors, today_visitors, checked_in


all_visitors, today_visitors, checked_in = refresh_data()

st.markdown('<div class="eyebrow">Front desk / visitor register</div>', unsafe_allow_html=True)
st.title("Visitor Desk")
st.markdown('<p class="subtitle">A calm, searchable log for everyone coming through the door.</p>', unsafe_allow_html=True)

metric_today, metric_inside, metric_total = st.columns(3)
metric_today.metric("Arrivals today", len(today_visitors))
metric_inside.metric("Currently inside", checked_in)
metric_total.metric("Total records", len(all_visitors))

st.markdown('<div class="section-label">New arrival</div>', unsafe_allow_html=True)
with st.form("check_in_form", clear_on_submit=True):
    name_col, company_col = st.columns(2)
    with name_col:
        name = st.text_input("Visitor name", placeholder="e.g. Jordan Lee")
    with company_col:
        company = st.text_input("Company", placeholder="e.g. Northstar Labs")
    phone_col, purpose_col = st.columns(2)
    with phone_col:
        phone = st.text_input("Phone number", placeholder="Optional")
    with purpose_col:
        purpose = st.text_input("Purpose of visit", placeholder="e.g. Project meeting")
    submitted = st.form_submit_button("Check in visitor", type="primary", use_container_width=True)

if submitted:
    if not name.strip() or not company.strip():
        st.warning("Visitor name and company are required.")
    else:
        visitor_id = check_in_visitor(name.strip(), company.strip(), phone.strip(), purpose.strip())
        st.success(f"{name.strip()} is checked in. Visitor ID: {visitor_id}")
        st.rerun()

st.markdown('<div class="section-label">Quick actions</div>', unsafe_allow_html=True)
action_col, search_col = st.columns([1, 2])
with action_col:
    with st.form("check_out_form"):
        checkout_id = st.number_input("Visitor ID to check out", min_value=1, step=1, value=1)
        checkout_submit = st.form_submit_button("Check out visitor", use_container_width=True)
    if checkout_submit:
        if check_out_visitor(int(checkout_id)):
            st.success("Visitor checked out.")
            st.rerun()
        else:
            st.error("Visitor ID not found.")

    with st.form("delete_visitor_form"):
        delete_id = st.number_input("Visitor ID to delete", min_value=1, step=1, value=1)
        confirm_delete = st.checkbox("Confirm permanent deletion")
        delete_submit = st.form_submit_button("Delete visitor", type="primary", use_container_width=True)
    if delete_submit:
        if not confirm_delete:
            st.error("Confirm the deletion before continuing.")
        elif delete_visitor(int(delete_id)):
            st.success("Visitor record deleted.")
            st.rerun()
        else:
            st.error("Visitor ID not found.")

with search_col:
    search_term = st.text_input("Search the register", placeholder="Name, company, phone, or visitor ID")
    records = search_visitors(search_term) if search_term.strip() else all_visitors
    if records.empty:
        st.info("No matching visitors found.")
    else:
        st.dataframe(records, use_container_width=True, hide_index=True)

st.markdown('<div class="section-label">Manage records</div>', unsafe_allow_html=True)
edit_tab, today_tab = st.tabs(["Edit visitor", "Today’s arrivals"])

with edit_tab:
    with st.form("edit_visitor_form"):
        edit_id = st.number_input("Visitor ID to edit", min_value=1, step=1, value=1)
        edit_name, edit_company = st.columns(2)
        with edit_name:
            new_name = st.text_input("New name", placeholder="Leave blank to keep current")
        with edit_company:
            new_company = st.text_input("New company", placeholder="Leave blank to keep current")
        new_phone = st.text_input("New phone", placeholder="Leave blank to keep current")
        new_purpose = st.text_input("New purpose", placeholder="Leave blank to keep current")
        update_submit = st.form_submit_button("Save changes", type="primary")
    if update_submit:
        success = edit_visitor(
            int(edit_id),
            name=new_name.strip() or None,
            company=new_company.strip() or None,
            phone=new_phone.strip() or None,
            purpose=new_purpose.strip() or None,
        )
        if success:
            st.success("Visitor details updated.")
            st.rerun()
        else:
            st.error("Visitor ID not found.")

with today_tab:
    if today_visitors.empty:
        st.info("No visitors have checked in today.")
    else:
        st.dataframe(today_visitors, use_container_width=True, hide_index=True)
