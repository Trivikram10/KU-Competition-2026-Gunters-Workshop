import streamlit as st
import datetime

st.set_page_config(
    page_title="Gunter's Royal Blacksmith Shop",
    page_icon="⚒️",
    layout="centered"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Alegreya+Sans:wght@400;500;700&display=swap');

    :root {
        --soot: #1B1816;
        --deep: #14110F;
        --anvil: #262120;
        --steel: #3E3733;
        --ember: #E2661F;
        --molten: #F2B84B;
        --parch: #EFE4CF;
        --ash: #A89D8A;
        color-scheme: dark;
    }

    /* ---------- Page ---------- */
    .stApp {
        background:
            radial-gradient(ellipse 80% 38% at 50% -6%, rgba(226,102,31,.26), transparent 70%),
            var(--soot);
        color: var(--parch);
        font-family: 'Alegreya Sans', 'Segoe UI', sans-serif;
        font-size: 1.05rem;
    }
    header[data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }
    [data-testid="stHeaderActionElements"] { display: none; }
    [data-testid="stMainBlockContainer"], .block-container {
        max-width: 960px !important;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--deep); }
    ::-webkit-scrollbar-thumb { background: var(--steel); border-radius: 6px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--ember); }

    /* ---------- Typography ---------- */
    .stApp, .stApp p, .stApp li, .stApp label,
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
        color: var(--parch);
    }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--ash); }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        font-family: 'Cinzel', 'Georgia', serif;
        color: var(--parch);
        letter-spacing: .03em;
    }
    .stApp h1 {
        text-align: center;
        font-size: 2.7rem;
        font-weight: 700;
        padding-bottom: .2rem;
        text-shadow: 0 0 28px rgba(226,102,31,.55);
    }
    .stApp h2 { font-size: 1.6rem; font-weight: 700; }
    .stApp h3 { font-size: 1.25rem; font-weight: 700; }
    .stApp h4 { font-size: 1.05rem; font-weight: 700; color: var(--molten); }
    [data-testid="stWidgetLabel"] p { font-weight: 500; }
    code, .stApp code {
        background: rgba(226,102,31,.16);
        color: var(--molten);
        border-radius: 6px;
        padding: .1rem .4rem;
        font-size: .92em;
    }

    /* Heated-bar dividers */
    hr {
        border: 0 !important;
        height: 2px !important;
        margin: 1.4rem 0 !important;
        background: linear-gradient(90deg, transparent, var(--ember), var(--molten), var(--ember), transparent) !important;
        opacity: .65;
    }

    /* ---------- Portal switch (radio as pills) ---------- */
    [data-testid="stElementContainer"]:has([data-testid="stRadio"]) { width: 100% !important; }
    [data-testid="stRadio"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        width: 100% !important;
        text-align: center;
    }
    [data-testid="stRadio"] > div {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    [data-testid="stRadio"] [data-testid="stWidgetLabel"] { width: 100%; justify-content: center; }
    [data-testid="stRadio"] [data-testid="stWidgetLabel"] p { text-align: center; }
    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: .6rem;
        justify-content: center !important;
        width: 100%;
    }
    [data-testid="stRadio"] label {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-radius: 999px;
        padding: .45rem 1.4rem;
        cursor: pointer;
        transition: border-color .15s, background .15s;
    }
    [data-testid="stRadio"] label:hover { border-color: var(--ember); }
    [data-testid="stRadio"] label > div:first-child { display: none; }
    [data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, var(--ember), #B8480F);
        border-color: var(--molten);
        box-shadow: 0 0 18px rgba(226,102,31,.35);
    }
    [data-testid="stRadio"] label:has(input:checked) p { color: #FFF4E0; font-weight: 700; }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 6px;
        border-bottom: 1px solid var(--steel);
    }
    .stTabs [data-baseweb="tab"] {
        flex-grow: 1 !important;
        text-align: center !important;
        height: 3rem;
        background: transparent;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [data-baseweb="tab"]:hover { background: rgba(226,102,31,.08); }
    .stTabs [data-baseweb="tab"] p {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        color: var(--ash);
        letter-spacing: .02em;
    }
    .stTabs [aria-selected="true"] p { color: var(--molten); }
    .stTabs [data-baseweb="tab-highlight"] { background: var(--ember); height: 3px; }
    .stTabs [data-baseweb="tab-border"] { background: transparent; }

    /* ---------- Cards ---------- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--steel);
        border-left-width: 4px;
        border-left-color: var(--ember);
        border-radius: 12px;
    }
    [data-testid="stForm"] {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-top: 3px solid var(--ember);
        border-radius: 14px;
        padding: 1.5rem 1.6rem;
        box-shadow: 0 10px 30px rgba(0,0,0,.35);
    }
    [data-testid="stMetric"] {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-top: 3px solid var(--ember);
        border-radius: 12px;
        padding: .9rem 1rem;
    }
    [data-testid="stMetricLabel"] p { color: var(--ash); font-weight: 500; }
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        color: var(--molten);
        font-size: 1.6rem;
    }

    /* ---------- Alerts & toasts ---------- */
    [data-testid="stAlert"] {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-left: 4px solid var(--steel);
        border-radius: 12px;
        color: var(--parch);
    }
    [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) { border-left-color: var(--ember); }
    [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) { border-left-color: #6FBF73; }
    [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) { border-left-color: var(--molten); }
    [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) { border-left-color: #E5534B; }
    [data-testid="stAlert"] h3 { color: var(--molten); margin-bottom: .3rem; }
    [data-testid="stToast"] {
        background: var(--anvil);
        border: 1px solid var(--ember);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,.45);
    }

    /* ---------- Inputs ---------- */
    [data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
        background: var(--deep) !important;
        border-color: var(--steel) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within {
        border-color: var(--ember) !important;
        box-shadow: 0 0 0 1px var(--ember);
    }
    input, textarea, [data-baseweb="select"] * { color: var(--parch) !important; }
    input { -webkit-text-fill-color: var(--parch); }
    [data-baseweb="select"] svg { fill: var(--ash); }
    [data-testid="stNumberInput"] button { background: var(--steel); color: var(--parch); }
    [data-testid="stNumberInput"] button:hover { background: var(--ember); }
    div[data-baseweb="popover"] ul, div[data-baseweb="menu"] {
        background: var(--anvil) !important;
        border: 1px solid var(--steel);
        border-radius: 10px;
    }
    div[data-baseweb="popover"] li { color: var(--parch); }
    div[data-baseweb="popover"] li:hover, div[data-baseweb="popover"] li[aria-selected="true"] {
        background: rgba(226,102,31,.22) !important;
    }
    label[data-baseweb="checkbox"] > span:first-child { border-color: var(--steel) !important; background-color: var(--deep) !important; }
    label[data-baseweb="checkbox"]:has(input:checked) > span:first-child {
        background-color: var(--ember) !important;
        border-color: var(--molten) !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, [data-testid="stFormSubmitButton"] > button,
    [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"] {
        background: linear-gradient(135deg, var(--molten), var(--ember));
        border: 1px solid var(--molten);
        border-radius: 10px;
        padding: .5rem 1.2rem;
        box-shadow: 0 4px 14px rgba(226,102,31,.28);
        transition: transform .12s, box-shadow .12s, filter .12s;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(226,102,31,.42);
        border-color: var(--parch);
    }
    .stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: translateY(0); }
    .stButton > button p, [data-testid="stFormSubmitButton"] > button p,
    [data-testid="stBaseButton-secondary"] p, [data-testid="stBaseButton-secondaryFormSubmit"] p {
        color: #1B1816;
        font-family: 'Cinzel', serif;
        font-weight: 700;
    }
    [data-testid="stFormSubmitButton"] > button { width: 100%; padding: .65rem 1.2rem; }

    /* ---------- Sidebar (Gunter's Vault) ---------- */
    [data-testid="stSidebar"] {
        background: var(--deep);
        border-right: 1px solid var(--steel);
    }
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: linear-gradient(160deg, var(--anvil), var(--deep));
        border-top-color: var(--molten);
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"], [data-testid="stSidebar"] [data-testid="stMetricValue"] div {
        font-size: 1.9rem;
    }

    /* ---------- Material progress bars ---------- */
    .stProgress > div > div { background: var(--steel) !important; border-radius: 999px; }
    .stProgress > div > div > div, .stProgress [role="progressbar"] > div {
        background: linear-gradient(90deg, #B8480F, var(--ember), var(--molten)) !important;
        border-radius: 999px;
    }
    </style>
""", unsafe_allow_html=True)

if "orders" not in st.session_state:
    st.session_state.orders = []

if "gold_vault" not in st.session_state:
    st.session_state.gold_vault = 500

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Iron Ingots": 50,
        "Steel Plates": 50,
        "Mithril Ores": 50,
        "Bronze Bars": 50
    }

if "form_key" not in st.session_state:
    st.session_state.form_key = 0

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def get_ordered_queue(orders_list):
    active_orders = [o for o in orders_list if o['status'] != "Completed"]
    express_orders = [o for o in active_orders if o.get('is_express')]
    standard_orders = [o for o in active_orders if not o.get('is_express')]
    
    interleaved = []
    exp_idx = 0
    std_idx = 0
    
    while exp_idx < len(express_orders) or std_idx < len(standard_orders):
        for _ in range(3):
            if exp_idx < len(express_orders):
                interleaved.append(express_orders[exp_idx])
                exp_idx += 1
        if std_idx < len(standard_orders):
            interleaved.append(standard_orders[std_idx])
            std_idx += 1
            
    return interleaved

st.title("Gunter's Royal Blacksmith Shop")
st.divider()

portal_choice = st.radio(
    "Select Portal View:",
    ["Customer", "Gunter's Forge Hub"],
    horizontal=True
)

st.divider()

if portal_choice == "Customer":
    tab_store, tab_queue = st.tabs([
        "🛒 Storefront & Order", 
        "📜 To-Do Queue"
    ])

    with tab_store:
        st.subheader("Select Your Blacksmith Gear")
        st.write("Browse Gunter's legendary catalog using your magical orb.")

        catalog = {
            "Sword": {"base_price": 120, "icon": "🗡️", "desc": "Master-crafted blade balanced for royal guards and adventurers."},
            "Plate Armor": {"base_price": 350, "icon": "🛡️", "desc": "Impenetrable steel plating designed to withstand dragon fire."},
            "Chain Mail": {"base_price": 200, "icon": "⛓️", "desc": "Flexible interlocking rings providing maximum agility in battle."},
            "Cooking Pot": {"base_price": 45, "icon": "🍲", "desc": "Indestructible cast-iron pot for campfires and royal feasts."}
        }

        selected_item = st.selectbox("Choose Equipment:", list(catalog.keys()), key=f"item_{st.session_state.form_key}")
        item_info = catalog[selected_item]
        
        st.info(f"### {item_info['icon']} {selected_item}\n{item_info['desc']}\n\n**Base Price:** {item_info['base_price']} Gold Coins")

        with st.form("order_placement_form"):
            st.markdown("#### ⚙️ Customization & Enhancements")
            
            material = st.selectbox("Select Material Grade:", [
                "Iron (Standard)", 
                "Steel (+50 Gold)", 
                "Mithril (+150 Gold)", 
                "Bronze (-20 Gold)"
            ], key=f"mat_{st.session_state.form_key}")
            
            st.markdown("#### ✨ Magical Rune Engravings")
            rune_enhancement = st.selectbox("Select Rune Enhancement:", [
                "None", 
                "Flame Rune (+25 Gold)", 
                "Frost Rune (+25 Gold)", 
                "Lightning Rune (+35 Gold)"
            ], key=f"rune_{st.session_state.form_key}")

            st.markdown("#### ⚡ Gunter's Express Forge Service")
            express_priority = st.checkbox("Rush Order: Express Forge Priority (+50 Gold)", key=f"express_{st.session_state.form_key}")

            customer_name = st.text_input("Adventurer / Guild Name:", key=f"name_{st.session_state.form_key}")

            material_extra = 0
            if "Steel" in material: material_extra = 50
            elif "Mithril" in material: material_extra = 150
            elif "Bronze" in material: material_extra = -20

            rune_cost = 0
            if "Flame" in rune_enhancement or "Frost" in rune_enhancement: rune_cost = 25
            elif "Lightning" in rune_enhancement: rune_cost = 35

            express_cost = 50 if express_priority else 0

            total_cost = item_info['base_price'] + material_extra + rune_cost + express_cost
            st.write(f"💰 **Total Price:** `{total_cost} Gold Coins`")

            submit_btn = st.form_submit_button("Submit Order to Gunter")

            if submit_btn:
                if not customer_name.strip():
                    st.error("⚠️ Please enter your name before submitting!")
                else:
                    new_id = f"Order {len(st.session_state.orders) + 101}"
                    timestamp = datetime.datetime.now().strftime("%I:%M %p")
                    
                    extra_details = rune_enhancement if rune_enhancement != "None" else "Standard Enhancement"
                    
                    mat_type = material.split(" ")[0]
                    mat_key_map = {
                        "Iron": "Iron Ingots",
                        "Steel": "Steel Plates",
                        "Mithril": "Mithril Ores",
                        "Bronze": "Bronze Bars"
                    }
                    
                    st.session_state.orders.append({
                        "id": new_id,
                        "item": selected_item,
                        "material": mat_type,
                        "material_inventory_key": mat_key_map[mat_type],
                        "extra": extra_details,
                        "is_express": express_priority,
                        "status": "Pending",
                        "time": timestamp,
                        "customer": customer_name,
                        "cost": total_cost,
                        "collected": False,
                        "materials_deducted": False
                    })
                    
                    st.session_state.form_key += 1
                    st.toast(f"🎉 Success, {customer_name}! {new_id} ({selected_item}) submitted!", icon="⚒️")
                    st.balloons()
                    st.rerun()

    with tab_queue:
        st.subheader("📜 To-Do Queue")

        priority_queue = get_ordered_queue(st.session_state.orders)

        if not priority_queue:
            st.info("No active orders in the forge queue right now. Place an order in the Storefront tab to see it here!")
        else:
            for idx, order in enumerate(priority_queue):
                tag = "⚡ EXPRESS" if order.get('is_express') else "📜 STANDARD"
                status_color = {"Pending": "🟡", "Forging": "🔥", "Ready": "🟢"}.get(order['status'], "⚪")
                with st.container(border=True):
                    st.markdown(f"**Priority #{idx + 1} | {order['id']}** ({tag})")
                    st.write(f"👤 **Customer:** {order['customer']}")
                    st.write(f"⚒️ **Equipment:** {order['item']} ({order['material']})")
                    st.write(f"✨ **Engravings / Details:** {order['extra']}")
                    st.write(f"💰 **Total Price:** {order['cost']} Gold")
                    st.write(f"📌 **Status:** {status_color} `{order['status']}`")

else:
    if not st.session_state.authenticated:
        st.subheader("🔒 Gunter's Private Forge Master Portal")
        passcode = st.text_input("Enter Password:", type="password")

        if passcode.strip().lower() == "gunter":
            st.session_state.authenticated = True
            st.toast("🔓 Access Granted! Welcome back, Forge Master Gunter.", icon="⚒️")
            st.rerun()
        elif passcode.strip() != "":
            st.error("⚠️ Access Denied! Invalid Passcode. Please try again.")
    else:
        st.sidebar.markdown("### 🪙 Gunter's Vault")
        st.sidebar.metric("Gold Vault Balance", f"{st.session_state.gold_vault} Gold")
        st.sidebar.caption("Updates dynamically on completed orders & merchant purchases.")
        
        if st.sidebar.button("🔒 Logout of Portal"):
            st.session_state.authenticated = False
            st.rerun()

        tab_manage, tab_completed = st.tabs([
            "📊 Forge Dashboard & Queue", 
            "✅ Completed Orders"
        ])

        with tab_manage:
            st.subheader("📊 Forge Master Dashboard")
            st.write("Manage workflow, update order statuses, deduct raw materials, and monitor shop earnings.")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Orders", len(st.session_state.orders))
            col2.metric("In Forge 🔥", sum(1 for o in st.session_state.orders if o['status'] == "Forging"))
            col3.metric("Ready 🟢", sum(1 for o in st.session_state.orders if o['status'] == "Ready"))
            col4.metric("Gold Vault 🪙", f"{st.session_state.gold_vault}g")

            st.divider()
            st.subheader("🛠️ Active Orders")

            priority_queue = get_ordered_queue(st.session_state.orders)

            if not priority_queue:
                st.info("No pending or active orders to manage right now.")
            else:
                for idx, order in enumerate(priority_queue):
                    tag = "⚡ EXPRESS" if order.get('is_express') else "📜 STANDARD"
                    status_color = {"Pending": "🟡", "Forging": "🔥", "Ready": "🟢"}.get(order['status'], "⚪")
                    
                    with st.container(border=True):
                        st.markdown(f"### **Priority #{idx + 1} | {order['id']}** ({tag})")
                        col_info, col_action = st.columns([2, 1])
                        
                        with col_info:
                            st.write(f"👤 **Customer:** {order['customer']}")
                            st.write(f"⚒️ **Equipment:** {order['item']} ({order['material']})")
                            st.write(f"✨ **Engravings / Details:** {order['extra']}")
                            st.write(f"💰 **Total Price:** {order['cost']} Gold Coins")
                            st.write(f"📌 **Current Status:** {status_color} `{order['status']}`")

                        with col_action:
                            st.markdown("#### Update Status")
                            status_index = ["Pending", "Forging", "Ready", "Completed"].index(order['status']) if order['status'] in ["Pending", "Forging", "Ready", "Completed"] else 0
                            new_status = st.selectbox(
                                "Select Status:",
                                ["Pending", "Forging", "Ready", "Completed"],
                                index=status_index,
                                key=f"status_select_{order['id']}"
                            )
                            
                            if st.button("Apply Update", key=f"btn_update_{order['id']}"):
                                required_mat = order['material_inventory_key']
                                
                                if new_status in ["Forging", "Ready", "Completed"] and not order['materials_deducted']:
                                    if st.session_state.inventory[required_mat] < 1:
                                        st.error(f"⚠️ Insufficient {required_mat}! Restock from materials below before forging.")
                                        st.stop()
                                    else:
                                        st.session_state.inventory[required_mat] -= 1
                                        order['materials_deducted'] = True
                                        st.toast(f"⚒️ Used 1 unit of {required_mat} from inventory!", icon="📦")

                                order['status'] = new_status
                                
                                if new_status == "Completed" and not order['collected']:
                                    st.session_state.gold_vault += order['cost']
                                    order['collected'] = True
                                    st.toast(f"💰 Collected {order['cost']} Gold from {order['id']} into Gunter's Vault!", icon="🪙")
                                
                                st.success(f"{order['id']} updated to {new_status}!")
                                st.rerun()

            st.divider()
            st.subheader("📦 Materials")
            st.write("Purchase raw supplies directly using Gold from Gunter's Vault.")

            prices = {
                "Iron Ingots": 20,
                "Steel Plates": 50,
                "Mithril Ores": 100,
                "Bronze Bars": 5
            }

            for mat_name, count in st.session_state.inventory.items():
                st.markdown(f"#### **{mat_name}** ({count} / 50 units remaining)")
                st.progress(min(count / 50.0, 1.0))
                
                unit_cost = prices[mat_name]
                max_purchasable = 50 - count
                
                if max_purchasable <= 0:
                    st.caption("✅ Storage for this material is at full capacity (50/50).")
                else:
                    col_num, col_btn = st.columns([2, 1])
                    with col_num:
                        qty_to_buy = st.number_input(
                            f"Units to buy (Cost: {unit_cost} Gold/unit):",
                            min_value=1,
                            max_value=max_purchasable,
                            value=min(5, max_purchasable),
                            key=f"buy_qty_{mat_name}"
                        )
                    with col_btn:
                        total_purchase_cost = qty_to_buy * unit_cost
                        st.write("")
                        st.write("")
                        if st.button(f"Buy ({total_purchase_cost}g)", key=f"buy_btn_{mat_name}"):
                            if st.session_state.gold_vault < total_purchase_cost:
                                st.error(f"⚠️ Insufficient Gold in Vault! Need {total_purchase_cost} Gold, but only have {st.session_state.gold_vault} Gold.")
                            else:
                                st.session_state.gold_vault -= total_purchase_cost
                                st.session_state.inventory[mat_name] += qty_to_buy
                                st.toast(f"📦 Purchased {qty_to_buy} units of {mat_name} for {total_purchase_cost} Gold!", icon="🛒")
                                st.rerun()
                st.write("---")

        with tab_completed:
            st.subheader("✅ Completed Orders")
            st.write("Successfully forged and delivered orders.")

            completed_orders = [o for o in st.session_state.orders if o['status'] == "Completed"]

            if not completed_orders:
                st.info("No completed orders in the archive yet.")
            else:
                for order in completed_orders:
                    with st.container(border=True):
                        st.markdown(f"**{order['id']}** {'⚡ [EXPRESS]' if order.get('is_express') else ''}")
                        st.write(f"👤 **Customer:** {order['customer']}")
                        st.write(f"⚒️ **Item:** {order['item']} ({order['material']})")
                        st.write(f"✨ **Details:** {order['extra']}")
                        st.write(f"💰 **Revenue Collected:** {order['cost']} Gold")
                        st.write(f"📌 **Status:** ✅ `Completed`")
