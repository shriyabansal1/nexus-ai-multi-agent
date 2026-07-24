import requests
import streamlit as st

from api_client import client


st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 NEXUS AI")
st.caption("Autonomous Multi-Agent AI System")

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.header("System")

    try:
        status = client.health()

        if status["status"] == "healthy":
            st.success("Backend Online")
        else:
            st.error("Backend Offline")

        st.divider()

        st.markdown("### Models")

        st.write("Planner")
        st.code(status.get("planner_model", "Qwen3"))

        st.write("Workers")
        st.code(status.get("default_model", "Phi-3"))

    except Exception:
        st.error("Cannot connect to FastAPI")

# =====================================================
# Tabs
# =====================================================

chat_tab, upload_tab, history_tab = st.tabs(
    [
        "💬 Chat",
        "📁 Upload",
        "📜 History",
    ]
)

# =====================================================
# CHAT
# =====================================================

with chat_tab:

    goal = st.text_area(
        "Goal",
        height=120,
        placeholder="Explain Transformers...",
    )

    execute = st.button(
        "Execute",
        use_container_width=True,
        disabled=not goal.strip(),
    )

    if execute:

        with st.spinner("Executing Multi-Agent System..."):

            try:

                result = client.execute(goal)

                st.success("Execution Completed")

                st.subheader("Execution ID")
                st.code(result["execution_id"])

                st.subheader("Answer")
                st.write(result.get("answer", "No answer returned."))

                execution = result.get("execution")

                if execution:

                    st.divider()

                    st.subheader("⚙️ Agents Executed")

                    trace = execution.get("trace", {}).get("entries", [])

                    for agent in trace:

                        icon = "✅" if agent.get("status") == "SUCCESS" else "❌"

                        with st.expander(f"{icon} {agent.get('agent')}"):

                            st.write("Task")
                            st.code(str(agent.get("task")))

                            st.write("Status")
                            st.write(agent.get("status"))

                            duration = agent.get("duration")
                            st.write("Duration")
                            st.write(
                                f"{duration:.2f} sec"
                                if duration is not None
                                else "N/A"
                            )

                            st.write("Input")
                            st.code(str(agent.get("input_data")))

                            st.write("Output")
                            st.code(str(agent.get("output_data")))

            except requests.HTTPError as e:

                if e.response is not None:
                    st.error(e.response.text)
                else:
                    st.error(str(e))

            except Exception as e:

                st.exception(e)

# =====================================================
# Upload
# =====================================================

with upload_tab:

    pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
    )

    if pdf:

        if st.button("Upload PDF"):

            with st.spinner("Uploading PDF..."):

                try:

                    result = client.upload_pdf(pdf)

                    st.success(result["message"])

                except requests.HTTPError as e:

                    if e.response is not None:
                        st.error(e.response.text)
                    else:
                        st.error(str(e))

                except Exception as e:

                    st.exception(e)

    st.divider()

    csv = st.file_uploader(
        "Upload CSV",
        type=["csv"],
    )

    if csv:

        if st.button("Upload CSV"):

            with st.spinner("Uploading CSV..."):

                try:

                    result = client.upload_csv(csv)

                    st.success(result["message"])

                except requests.HTTPError as e:

                    if e.response is not None:
                        st.error(e.response.text)
                    else:
                        st.error(str(e))

                except Exception as e:

                    st.exception(e)

    st.divider()

    db = st.file_uploader(
        "Upload SQLite Database",
        type=[
            "db",
            "sqlite",
            "sqlite3",
        ],
    )

    if db:

        if st.button("Upload Database"):

            with st.spinner("Uploading Database..."):

                try:

                    result = client.upload_database(db)

                    st.success(result["message"])

                except requests.HTTPError as e:

                    if e.response is not None:
                        st.error(e.response.text)
                    else:
                        st.error(str(e))

                except Exception as e:

                    st.exception(e)

# =====================================================
# HISTORY
# =====================================================

with history_tab:

    try:

        history = client.history()

        if not history:

            st.info("No executions yet.")

        else:

            for execution_id, execution in history.items():

                with st.expander(execution_id):

                    st.write("### Goal")
                    st.code(execution.get("goal", "N/A"))

                    if execution.get("answer"):
                        st.write("### Answer")
                        st.write(execution["answer"])

                    st.write("### Started")
                    st.write(execution.get("started", "N/A"))

                    st.write("### Finished")
                    st.write(execution.get("finished", "N/A"))

    except requests.HTTPError as e:

        if e.response is not None:
            st.error(e.response.text)
        else:
            st.error(str(e))

    except Exception:

        st.info("History unavailable.")