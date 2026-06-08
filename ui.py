import streamlit as st
import requests

# Configure page layouts and branding
st.set_page_config(
    page_title="Autonomous Agent Switchboard Hub",
    page_icon="🤖",
    layout="wide"
)

BACKEND_URL = "https://agent-switchboard-499706374273.us-central1.run.app"
ADMIN_TOKEN = "switchboard-super-admin-secure-string-2026"

st.title("🤖 Multi-Tenant AI Agent Switchboard Hub")
st.markdown("""
Welcome to the No-Code Agent Orchestrator! This platform allows you to create specialized AI personas 
on the fly, save them to a live cloud database, and automatically route user prompts to the right expert.
""")

st.write("---")

# Split the dashboard into two clean structural columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("🛠️ Phase 1: Create a New Custom Agent")
    st.caption("Define a new behavioral profile. Once saved, the central router automatically learns when to send tasks here.")
    
    with st.form("agent_form", clear_on_submit=True):
        new_agent_name = st.text_input(
            "Agent System Identifier", 
            placeholder="e.g., MARKETING_EXPERT, LEGAL_ADVISOR",
            help="Use letters and underscores only. This becomes the routing key."
        )
        
        system_instruction = st.text_area(
            "System Prompt Persona Instructions",
            placeholder="Describe exactly how this AI should act, its tone, its limits, and its specific expertise...",
            height=150,
            help="The foundational prompt guiding the behavior of your custom agent layer."
        )
        
        submit_btn = st.form_submit_button("🚀 Deploy Agent to Cloud Datastore")
        
        if submit_btn:
            if not new_agent_name or not system_instruction:
                st.error("Please fill out both fields before deploying.")
            else:
                payload = {
                    "agent_name": new_agent_name.strip().upper(),
                    "system_instruction": system_instruction.strip()
                }
                headers = {"X-Admin-Token": ADMIN_TOKEN}
                
                try:
                    response = requests.post(f"{BACKEND_URL}/v1/agents", json=payload, headers=headers)
                    if response.status_code == 200:
                        st.success(f"🎉 Agent '{new_agent_name.upper()}' is now live globally!")
                    else:
                        st.error(f"Backend rejected deployment: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend engine: {e}")

    st.write("---")
    st.header("📋 Current Active Agents Inventory")
    st.caption("These are the custom agents currently stored in your live Cloud Datastore infrastructure.")
    
    if st.button("🔄 Refresh Inventory List"):
        try:
            res = requests.get(f"{BACKEND_URL}/v1/agents")
            if res.status_code == 200:
                agents_data = res.json()
                if not agents_data:
                    st.info("No custom agents found. Use the form above to deploy your first one!")
                for agent in agents_data:
                    with st.expander(f"🤖 {agent.get('agent_name')}"):
                        st.markdown(f"**Instructions:** {agent.get('system_instruction')}")
                        if 'updated_at' in agent:
                            st.caption(f"Last updated: {agent.get('updated_at')}")
            else:
                st.error("Failed to query records from database infrastructure.")
        except Exception as e:
            st.error(f"Connection timeout: {e}")

with col2:
    st.header("🧪 Phase 2: Live Switchboard Playground")
    st.caption("Type an ambiguous prompt below. Watch the dynamic supervisor router figure out which agent should answer.")
    
    tenant_id = st.text_input(
        "Tenant Workspace Context Profile ID", 
        value="enterprise-client-alpha",
        help="Simulates multi-tenant client tracking. Keep as enterprise-client-alpha for default authorization privileges."
    )
    
    user_message = st.text_area(
        "Incoming Evaluation Message Prompt",
        placeholder="e.g., Draft a 3-sentence ad pitch for cargo planes OR check this python code for bugs...",
        height=100
    )
    
    test_btn = st.button("⚡ Execute Intelligent Routing Path")
    
    if test_btn:
        if not user_message:
            st.warning("Please type an input prompt to test.")
        else:
            payload = {
                "tenant_id": tenant_id.strip(),
                "message": user_message.strip()
            }
            
            with st.spinner("Supervisor analyzing intent bounds and executing..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/v1/execute", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        
                        # Call out metrics clearly to users
                        st.metric(label="🎯 Assigned Expert Chosen by Router", value=data.get("routed_to_agent"))
                        
                        st.markdown("### 📝 AI Generation Response Output")
                        st.info(data.get("agent_response"))
                        
                        st.success(f"📊 Metatag logged! Tokens Consumed: {data.get('metering_metrics', {}).get('total_tokens')}")
                    else:
                        st.error(f"Pipeline intercept error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Routing runtime crash: {e}")
