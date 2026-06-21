import streamlit as st
import pandas as pd
import sqlite3
import datetime
import os

# ─── Page Config ───
st.set_page_config(
    page_title="Welch Plug Pressing Machine Datalogging",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Database ───
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "machine_data.db")

def get_db():
    return sqlite3.connect(DB_PATH)

def get_stations():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in c.fetchall()]
        conn.close()
        return tables
    except:
        return []

def get_latest_record(station):
    try:
        conn = get_db()
        df = pd.read_sql_query(f"SELECT * FROM {station} ORDER BY DATE_TIME DESC LIMIT 1", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def get_counts(station):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {station} WHERE STATUS='PASS'")
        p = c.fetchone()[0]
        c.execute(f"SELECT COUNT(*) FROM {station} WHERE STATUS='FAIL'")
        f = c.fetchone()[0]
        c.execute(f"SELECT COUNT(*) FROM {station}")
        t = c.fetchone()[0]
        conn.close()
        return p, f, t
    except:
        return 0, 0, 0

def search_report(start_date, end_date, station, serial_no):
    try:
        conn = get_db()
        query = f"SELECT * FROM {station} WHERE DATE_TIME >= ? AND DATE_TIME <= ?"
        params = [start_date, end_date]
        if serial_no.strip():
            query += " AND SERIAL_NO LIKE ?"
            params.append(f"%{serial_no.strip()}%")
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()


# ═══════════════════════════════════════════════
#  GLOBAL CSS — matches factory software exactly
# ═══════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {visibility:hidden;}
div[data-testid="stToolbar"] {display:none;}

/* ── Sidebar as vertical tab bar ── */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* ── Tab styling to match factory colors ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    background: linear-gradient(180deg, #FFF0F8 0%, #E8FFE8 100%);
    border: 1px solid #999;
    border-radius: 4px;
    padding: 2px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', 'Times New Roman', serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    border-radius: 4px !important;
}
.stTabs [data-baseweb="tab"]:nth-child(1) { color: #FF8C00 !important; }
.stTabs [data-baseweb="tab"]:nth-child(2) { color: #CC0000 !important; }
.stTabs [data-baseweb="tab"]:nth-child(3) { color: #009900 !important; }
.stTabs [aria-selected="true"] {
    background: white !important;
    border-bottom: 3px solid currentColor !important;
}

/* ── Page background ── */
.stApp {background-color: #E8E8D8 !important;}

/* ── Remove default Streamlit padding ── */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* ── HEADER BANNER ── */
.hdr-banner {
    background: linear-gradient(180deg, #F0F0E0 0%, #E0E0D0 100%);
    border: 2px solid #888;
    border-radius: 3px;
    padding: 6px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 3px;
}
.hdr-logo {
    font-family: 'Inter', serif;
    font-size: 11px;
    font-weight: 800;
    color: #0055AA;
    letter-spacing: 0.5px;
    white-space: nowrap;
    min-width: 120px;
}
.hdr-title {
    font-family: 'Inter', 'Times New Roman', serif;
    font-size: 24px;
    font-weight: 800;
    color: #C000C0;
    text-align: center;
    flex: 1;
    letter-spacing: 0.5px;
}
.hdr-time {
    font-family: 'Inter', monospace;
    font-size: 12px;
    font-weight: 600;
    color: #333;
    white-space: nowrap;
    text-align: right;
    min-width: 180px;
}

/* ── INFO BAR ── */
.info-bar {
    display: flex;
    align-items: stretch;
    border: 1px solid #999;
    border-radius: 2px;
    background: #F0F0E0;
    margin-bottom: 4px;
    overflow: hidden;
}
.info-cell {
    flex: 1;
    text-align: center;
    padding: 3px 6px;
    border-right: 1px solid #bbb;
}
.info-cell:last-child {border-right: none;}
.info-lbl {
    font-family: 'Inter', serif;
    font-size: 11px;
    font-weight: 700;
    color: #333;
}
.info-val {
    font-family: 'Inter', serif;
    font-size: 13px;
    font-weight: 700;
    color: #0000C0;
    background: white;
    border: 1px solid #555;
    padding: 1px 8px;
    display: inline-block;
    margin-top: 1px;
    min-width: 70px;
}
.info-val.orange {color: #FF8C00;}
.exit-btn {
    color: red;
    font-weight: 800;
    font-size: 13px;
    margin-left: 4px;
}

/* ── VERTICAL TAB LABELS (rendered as fixed HTML overlay) ── */
.vtab-strip {
    position: fixed;
    left: 0;
    top: 60px;
    width: 46px;
    height: calc(100vh - 60px);
    display: flex;
    flex-direction: column;
    z-index: 999;
    background: linear-gradient(180deg, #FFF0F8 0%, #F0FFF0 100%);
    border-right: 2px solid #888;
}
.vtab {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    font-family: 'Inter', 'Times New Roman', serif;
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    border-bottom: 1px solid #bbb;
    padding: 8px 2px;
    letter-spacing: 0.5px;
    user-select: none;
    transition: background 0.15s;
}
.vtab:hover {opacity: 0.8;}
.vtab.t-overall {color: #FF8C00; background: #FFF8F0;}
.vtab.t-report  {color: #CC0000; background: #FFF0F0;}
.vtab.t-station {color: #009900; background: #F0FFF0;}
.vtab.active {
    font-size: 14px;
    border-left: 4px solid currentColor;
    background: white !important;
}

/* ── CONTENT AREA ── */
.content-wrap {
    margin-left: 0px;
    min-height: calc(100vh - 110px);
}

/* ── OVERALL STATUS ── */
.os-bg {
    background: linear-gradient(135deg, #E6FFE0 0%, #D0F0D0 100%);
    border: 2px solid #0066AA;
    border-radius: 4px;
    padding: 10px;
}
.stn-panel {
    background: #FAFAF5;
    border: 2px solid #888;
    border-radius: 4px;
    padding: 10px;
}
.stn-title {
    font-family: 'Inter', serif;
    font-size: 17px;
    font-weight: 800;
    color: #0000C0;
    text-align: center;
    border-bottom: 2px solid #0066AA;
    padding-bottom: 6px;
    margin-bottom: 8px;
}
.stn-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
    gap: 8px;
}
.stn-lbl {
    font-family: 'Inter', serif;
    font-weight: 700;
    font-size: 12px;
    color: #333;
}
.stn-val {
    font-family: 'Inter', monospace;
    font-weight: 700;
    font-size: 13px;
    background: white;
    border: 1px solid #555;
    padding: 2px 10px;
    text-align: center;
    min-width: 60px;
}
.badge-running {
    background: #00CC00;
    color: white;
    font-weight: 800;
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 3px;
}
.badge-idle {
    background: #999;
    color: white;
    font-weight: 800;
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 3px;
}
.badge-online {
    background: #FFD700;
    color: #333;
    font-weight: 800;
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 3px;
}
.stn-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #0088FF;
    color: white;
    font-weight: 800;
    font-size: 14px;
    border: 2px solid #0055AA;
}

/* ── DIGITAL INPUTS / COUNTS BOXES ── */
.di-cnt-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-top: 8px;
}
.box-bordered {
    border: 2px solid #333;
    border-radius: 3px;
    padding: 8px;
    background: white;
}
.box-title {
    font-family: 'Inter', serif;
    font-size: 13px;
    font-weight: 800;
    text-align: center;
    border-bottom: 1px solid #ccc;
    padding-bottom: 4px;
    margin-bottom: 6px;
}
.di-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 3px 0;
    font-family: 'Inter', serif;
    font-size: 12px;
    font-weight: 600;
}
.dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid #666;
    display: inline-block;
}
.dot-off {background: #ddd;}
.dot-green {background: #00CC00; border-color: #009900;}
.dot-red {background: #FF0000; border-color: #CC0000;}

.cnt-item {text-align: center; margin: 4px 0;}
.cnt-label {
    font-family: 'Inter', serif;
    font-size: 11px;
    font-weight: 700;
}
.cnt-val {
    font-family: 'Inter', monospace;
    font-size: 22px;
    font-weight: 800;
    padding: 2px 14px;
    border-radius: 3px;
    display: inline-block;
    min-width: 60px;
    border: 2px solid;
}
.cnt-g {background:#00CC00; color:white; border-color:#009900;}
.cnt-r {background:#FF0000; color:white; border-color:#CC0000;}
.cnt-b {background:#0000C0; color:white; border-color:#000099;}

/* ── MINI DATA TABLE (bottom of station panel) ── */
.mini-tbl {
    margin-top: 8px;
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
    font-family: 'Inter', monospace;
}
.mini-tbl th {
    background: #3366FF;
    color: white;
    padding: 3px 4px;
    border: 1px solid #333;
    font-weight: 700;
    text-align: center;
}
.mini-tbl td {
    padding: 3px 4px;
    border: 1px solid #ccc;
    text-align: center;
    background: white;
}

/* ── REPORT SCREEN ── */
.rpt-bg {
    background: white;
    border: 2px solid #888;
    border-radius: 4px;
    padding: 10px;
}
.filter-row {
    display: flex;
    align-items: flex-end;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 10px;
    padding: 8px;
    background: #FAFAF5;
    border: 1px solid #ccc;
    border-radius: 3px;
}
.filter-group {display: flex; flex-direction: column; gap: 2px;}
.filter-lbl {
    font-family: 'Inter', serif;
    font-size: 11px;
    font-weight: 700;
    color: #333;
}

/* ── REPORT DATA TABLE ── */
.rpt-tbl-wrap {
    width: 100%;
    overflow-x: auto;
    overflow-y: auto;
    max-height: calc(100vh - 280px);
    border: 2px solid #333;
    border-radius: 3px;
    background: white;
}
.rpt-tbl {
    border-collapse: collapse;
    width: 100%;
    font-family: 'Inter', 'Arial', sans-serif;
    font-size: 12px;
}
.rpt-tbl thead th {
    background: #00CC00;
    color: white;
    font-weight: 700;
    padding: 6px 8px;
    border: 1px solid #333;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 2;
    white-space: nowrap;
}
.rpt-tbl tbody td {
    padding: 5px 6px;
    border: 1px solid #bbb;
    text-align: center;
    white-space: nowrap;
}
.rpt-tbl tbody tr:first-child td {
    background: #3366FF;
    color: white;
    font-weight: 700;
}
.rpt-tbl tbody tr:nth-child(n+2):nth-child(even) td {
    background: #F5F5F0;
}
.rpt-tbl .pass-cell {color: #009900; font-weight: 700;}
.rpt-tbl .fail-cell {color: #FF0000; font-weight: 700;}

/* ── STATION DATA SCREEN ── */
.std-bg {
    background: linear-gradient(135deg, #E0FFE0 0%, #F0FFF0 100%);
    border: 2px solid #888;
    border-radius: 4px;
    padding: 10px;
}

/* ── RECORD COUNT BADGE ── */
.rec-badge {
    display: inline-block;
    background: #00CC00;
    color: white;
    font-family: 'Inter', monospace;
    font-size: 13px;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 10px;
    margin-bottom: 6px;
}

/* ── EMPTY TABLE ROWS (to match screenshot grid) ── */
.empty-rows {
    width: 100%;
    border-collapse: collapse;
}
.empty-rows td {
    border: 1px solid #ddd;
    height: 22px;
    background: white;
}
</style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  HEADER BANNER
# ═══════════════════════════════════════════════
now_str = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
st.markdown(f'<div class="hdr-banner"><div class="hdr-logo">⚙️ ASHOK LEYLAND</div><div class="hdr-title">WELCH PLUG PRESSING MACHINE DATALOGGING</div><div class="hdr-time">{now_str}</div></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  INFO BAR + EXIT BUTTON
# ═══════════════════════════════════════════════
bar_col, exit_col = st.columns([14, 1])
with bar_col:
    st.markdown("""<div class="info-bar">
<div class="info-cell"><div class="info-lbl">Model Name</div><div class="info-val">6 CYL</div></div>
<div class="info-cell"><div class="info-lbl">Customer Name</div><div class="info-val">ASHOK LEYLAND</div></div>
<div class="info-cell"><div class="info-lbl">Assy Name</div><div class="info-val">Welch Plug</div></div>
<div class="info-cell"><div class="info-lbl">Unit</div><div class="info-val">Shop 6</div></div>
<div class="info-cell"><div class="info-lbl">Shift</div><div class="info-val orange">B</div></div>
</div>""", unsafe_allow_html=True)
with exit_col:
    st.markdown("""<style>
    div[data-testid="stVerticalBlock"] button[kind="secondary"][data-testid="stBaseButton-secondary"] p {
        /* fallback */
    }
    </style>""", unsafe_allow_html=True)
    if st.button("❌\nExit", key="exit_btn"):
        st.session_state.app_exited = True
        st.rerun()

# Handle exit
if st.session_state.get("app_exited", False):
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:center; height:60vh; flex-direction:column;">
        <div style="font-size:48px;">👋</div>
        <h2 style="color:#555; font-family:Inter,sans-serif;">Application Closed</h2>
        <p style="color:#888;">You can close this browser tab now.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════
#  HELPER: build a station panel HTML
# ═══════════════════════════════════════════════
def build_station_html(name, stn_num, serial, status, is_running, pass_c, fail_c, total, cols_preview, first_row):
    badge = '<span class="badge-running">RUNNING</span>' if is_running else '<span class="badge-idle">IDLE</span>'
    auto_dot = "dot-green" if is_running else "dot-off"
    pass_dot = "dot-green" if (status == "PASS") else "dot-off"
    fail_dot = "dot-red" if (status == "FAIL") else "dot-off"
    th_html = "".join(f'<th>{c}</th>' for c in cols_preview[:5])
    tr_html = ""
    empty = "".join(f'<tr>{"<td>&nbsp;</td>" * min(5, len(cols_preview))}</tr>' for _ in range(5))
    return f'<div class="stn-panel"><div class="stn-title">{name}</div><div class="stn-row"><span class="stn-lbl">SERIAL NO</span><span class="stn-val">{serial}</span><span class="stn-lbl">STN</span><span class="stn-num">{stn_num}</span></div><div class="stn-row"><span class="stn-lbl">Status</span>{badge}<span class="stn-lbl">Routing</span><span class="badge-online">ONLINE</span></div><div class="di-cnt-grid"><div class="box-bordered"><div class="box-title">Digital Inputs</div><div class="di-row"><span>Scan Done</span><span class="dot dot-off"></span></div><div class="di-row"><span>Auto Start</span><span class="dot {auto_dot}"></span></div><div class="di-row"><span>PASS</span><span class="dot {pass_dot}"></span></div><div class="di-row"><span>FAIL</span><span class="dot {fail_dot}"></span></div></div><div class="box-bordered"><div class="box-title">Counts</div><div class="cnt-item"><div class="cnt-label">PASS Count</div><div class="cnt-val cnt-g">{pass_c:03d}</div></div><div class="cnt-item"><div class="cnt-label">FAIL Count</div><div class="cnt-val cnt-r">{fail_c:03d}</div></div><div class="cnt-item"><div class="cnt-label">Total</div><div class="cnt-val cnt-b">{total:03d}</div></div></div></div><table class="mini-tbl"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}{empty}</tbody></table></div>'


# ═══════════════════════════════════════════════
#  NAVIGATION — using st.tabs (reliable, always visible)
# ═══════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🟠 Overall Status", "🔴 Report Screen", "🟢 Station Data Screen"])


# ═══════════════════════════════════════════════
#  SCREEN: OVERALL STATUS
# ═══════════════════════════════════════════════
with tab1:
    stations = get_stations()

    st.markdown('<div class="os-bg">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── Station 1 (OP10) ──
    if stations:
        stn = stations[0]
        latest = get_latest_record(stn)
        p, f, t = get_counts(stn)
        serial = latest.iloc[0]['SERIAL_NO'] if not latest.empty else "---"
        status = latest.iloc[0]['STATUS'] if not latest.empty else "---"
        is_run = not latest.empty
        cols_list = list(latest.columns) if not latest.empty else ["SERIAL_NO","MODEL","DATE_TIME","SHIFT"]
        row_dict = dict(latest.iloc[0]) if not latest.empty else {}
        with col1:
            st.markdown(build_station_html(stn.replace("_","-"), 1, serial, status, is_run, p, f, t, cols_list, row_dict), unsafe_allow_html=True)
    else:
        with col1:
            st.markdown(build_station_html("OP10-WELCH-PLUG-PRESS-1", 1, "---", "---", False, 0, 0, 0, ["SERIAL_NO","MODEL","DATE_TIME","SHIFT"], None), unsafe_allow_html=True)

    # ── Station 2 (OP20 — placeholder) ──
    if len(stations) > 1:
        stn2 = stations[1]
        lat2 = get_latest_record(stn2)
        p2, f2, t2 = get_counts(stn2)
        ser2 = lat2.iloc[0]['SERIAL_NO'] if not lat2.empty else "---"
        st2 = lat2.iloc[0]['STATUS'] if not lat2.empty else "---"
        cols2 = list(lat2.columns) if not lat2.empty else []
        row2 = dict(lat2.iloc[0]) if not lat2.empty else {}
        with col2:
            st.markdown(build_station_html(stn2.replace("_","-"), 2, ser2, st2, not lat2.empty, p2, f2, t2, cols2, row2), unsafe_allow_html=True)
    else:
        # Mock OP20 panel
        with col2:
            st.markdown(build_station_html("OP20-WELCH-PLUG-PRESSING-2", 2, "---", "---", False, 0, 0, 0, ["FINAL_POS","FINAL_FORCE","RESULT","FINAL_POS","FINAL_FORCE"], None), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  SCREEN: REPORT SCREEN
# ═══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="rpt-bg">', unsafe_allow_html=True)

    # Initialize session state for search results
    if "report_df" not in st.session_state:
        st.session_state.report_df = None
    if "do_search" not in st.session_state:
        st.session_state.do_search = False

    # ── Filter Bar ──
    f1, f2, f3, f4, f5 = st.columns([1, 1, 1.5, 1.2, 1.2])

    with f1:
        from_date = st.date_input("From", datetime.date(2026, 1, 19))
    with f2:
        to_date = st.date_input("To", datetime.date(2026, 1, 21))
    with f3:
        stations = get_stations()
        station = st.selectbox("Select Station", options=stations if stations else ["No Data"])
    with f4:
        serial_no = st.text_input("Serial No", placeholder="Optional")
    with f5:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🔍 Search\nReport", type="primary", use_container_width=True):
                # Run search immediately when clicked
                if station and station != "No Data":
                    start_str = from_date.strftime("%Y-%m-%d") + " 00:00:00"
                    end_str   = to_date.strftime("%Y-%m-%d")   + " 23:59:59"
                    st.session_state.report_df = search_report(start_str, end_str, station, serial_no if serial_no else "")
                    st.rerun()
        with btn_col2:
            # Save button — downloads CSV with proper filename
            if st.session_state.report_df is not None and not st.session_state.report_df.empty:
                import io
                csv_bytes = st.session_state.report_df.to_csv(index=False).encode("utf-8")
                buffer = io.BytesIO(csv_bytes)
                buffer.seek(0)
                fname = f"report_{station}_{from_date.strftime('%Y%m%d')}.csv"
                st.download_button(
                    label="💾 Save",
                    data=buffer,
                    file_name=fname,
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("💾 Save", disabled=True, use_container_width=True)

    # Show save success message
    if "save_msg" in st.session_state and st.session_state.save_msg:
        st.success(st.session_state.save_msg)
        st.session_state.save_msg = None

    # ── Display results (persisted across reruns) ──
    df = st.session_state.report_df
    if df is not None and not df.empty:
        st.markdown(f'<div class="rec-badge">Found {len(df)} record(s)</div>', unsafe_allow_html=True)

        # Build HTML table
        th = "".join(f"<th>{c}</th>" for c in df.columns)
        rows_html = ""
        for idx, row in df.iterrows():
            cells = ""
            for c in df.columns:
                v = str(row[c])
                cls = ""
                if idx > 0:
                    if v == "PASS": cls = ' class="pass-cell"'
                    elif v == "FAIL": cls = ' class="fail-cell"'
                cells += f"<td{cls}>{v}</td>"
            rows_html += f"<tr>{cells}</tr>"

        # Add empty rows to fill the grid like the screenshot
        n_empty = max(0, 15 - len(df))
        empty_row = "<tr>" + "".join(f'<td>&nbsp;</td>' for _ in df.columns) + "</tr>"
        rows_html += empty_row * n_empty

        st.markdown(f'<div class="rpt-tbl-wrap"><table class="rpt-tbl"><thead><tr>{th}</tr></thead><tbody>{rows_html}</tbody></table></div>', unsafe_allow_html=True)
    elif df is not None and df.empty:
        st.warning("No records found for the selected filters.")
    else:
        # Show empty table grid like the original screenshot
        preview_cols = ["SERIAL_NO","MODEL","DATE_TIME","SHIFT","STATUS","4CYL_FINAL_POS_1"]
        th = "".join(f"<th>{c}</th>" for c in preview_cols)
        empty_row = "<tr>" + "".join('<td>&nbsp;</td>' for _ in preview_cols) + "</tr>"
        st.markdown(f'<div class="rpt-tbl-wrap"><table class="rpt-tbl"><thead><tr>{th}</tr></thead><tbody>{empty_row * 18}</tbody></table></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  SCREEN: STATION DATA SCREEN
# ═══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="std-bg">', unsafe_allow_html=True)

    stations = get_stations()
    if stations:
        sel = st.selectbox("Select Station", stations, key="station_data_select")
        if sel:
            try:
                conn = get_db()
                df = pd.read_sql_query(f"SELECT * FROM {sel} ORDER BY DATE_TIME DESC", conn)
                conn.close()
                if not df.empty:
                    st.markdown(f'<div class="rec-badge">{len(df)} record(s) from {sel}</div>', unsafe_allow_html=True)
                    th = "".join(f"<th>{c}</th>" for c in df.columns)
                    rows = ""
                    for _, row in df.iterrows():
                        cells = ""
                        for c in df.columns:
                            v = str(row[c])
                            cls = ""
                            if v == "PASS": cls = ' class="pass-cell"'
                            elif v == "FAIL": cls = ' class="fail-cell"'
                            cells += f"<td{cls}>{v}</td>"
                        rows += f"<tr>{cells}</tr>"
                    st.markdown(f'<div class="rpt-tbl-wrap"><table class="rpt-tbl"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)
                else:
                    st.info("No data.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("No stations found. Run setup_db.py first.")

    st.markdown('</div>', unsafe_allow_html=True)
