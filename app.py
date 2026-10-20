import streamlit as st
import datetime

st.set_page_config(
    page_title="Gunter's Blacksmith Shop",
    page_icon="⚒️",
    layout="centered"
)

if "orders" not in st.session_state:
    st.session_state.orders = []

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Iron Ingots": 30,
        "Steel Plates": 20,
        "Mithril Ores": 10,
        "Bronze Bars": 25
    }

st.title("⚒️ Gunter's Royal Blacksmith")
st.caption("✨ Official Mobile Storefront & Smart Forge Hub of Mautern Town")
st.divider()

tab_store, tab_queue, tab_manage = st.tabs(["🛒 Storefront & Order", "📜 Live To-Do Queue", "📊 Forge Master Dashboard"])

with tab_store:
    st.subheader("Select Your Blacksmith Gear")
    st.write("Browse Gunter's legendary catalog using your magical orb.")

    catalog = {
        "Sword": {"base_price": 120, "icon": "🗡️", "desc": "Master-crafted blade balanced for royal guards and adventurers."},
        "Plate Armor": {"base_price": 350, "icon": "🛡️", "desc": "Impenetrable steel plating designed to withstand dragon fire."},
        "Chain Mail": {"base_price": 200, "icon": "⛓️", "desc": "Flexible interlocking rings providing maximum agility in battle."},
        "Cooking Pot": {"base_price": 45, "icon": "🍲", "desc": "Indestructible cast-iron pot for campfires and royal feasts."}
    }

    selected_item = st.selectbox("Choose Equipment:", list(catalog.keys()))
    item_info = catalog[selected_item]
    
    st.info(f"### {item_info['icon']} {selected_item}\n{item_info['desc']}\n\n**Base Price:** {item_info['base_price']} Gold Coins")

    with st.form("order_placement_form"):
        st.markdown("#### ⚙️ Customization & Enhancements")
        
        material = st.selectbox("Select Material Grade:", [
            "Iron (Standard)", 
            "Steel (+50 Gold)", 
            "Mithril (+150 Gold)", 
            "Bronze (-20 Gold)"
        ])
        
        st.markdown("#### ✨ Magical Rune Engravings")
        rune_enhancement = st.selectbox("Select Rune Enhancement:", [
            "None", 
            "Flame Rune (+25 Gold)", 
            "Frost Rune (+25 Gold)", 
            "Lightning Rune (+35 Gold)"
        ])

        st.markdown("#### ⚡ Gunter's Express Forge Service")
        express_priority = st.checkbox("Rush Order: Express Forge Priority (+50 Gold)")
        st.caption("Moves your order straight to the top of Gunter's anvil queue.")

        customer_name = st.text_input("Adventurer / Guild Name:")

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

        submit_btn = st.form_submit_button("Submit Order to Gunter's Anvil")

        if submit_btn:
            if not customer_name.strip():
                st.error("⚠️ Please enter your name before submitting!")
            else:
                new_id = f"ORD-{len(st.session_state.orders) + 101}"
                timestamp = datetime.datetime.now().strftime("%I:%M %p")
                
                service_tags = []
                if rune_enhancement != "None":
                    service_tags.append(rune_enhancement)
                if express_priority:
                    service_tags.append("⚡ Express Priority")

                extra_details = ", ".join(service_tags) if service_tags else "Standard Order"
                
                st.session_state.orders.append({
                    "id": new_id,
                    "item": selected_item,
                    "material": material.split(" ")[0],
                    "extra": extra_details,
                    "is_express": express_priority,
                    "status": "Pending",
                    "time": timestamp,
                    "customer": customer_name,
                    "cost": total_cost
                })
                st.success(f"🎉 Success, {customer_name}! Order `{new_id}` ({selected_item}) submitted!")
                st.balloons()

with tab_queue:
    st.subheader("📜 Gunter's Live Forge To-Do List")
    st.write("Express Priority Queue and Standard Queue tracked side-by-side.")

    if not st.session_state.orders:
        st.info("No active orders in the forge queue yet. Place an order in the Storefront tab to see it here!")
    else:
        express_orders = [o for o in st.session_state.orders if o.get('is_express')]
        normal_orders = [o for o in st.session_state.orders if not o.get('is_express')]

        col_exp, col_norm = st.columns(2)

        with col_exp:
            st.markdown("### ⚡ Express Queue")
            if not express_orders:
                st.caption("No express orders.")
            else:
                for idx, order in enumerate(express_orders):
                    status_color = {"Pending": "🟡", "Forging": "🔥", "Ready": "🟢", "Completed": "✅"}.get(order['status'], "⚪")
                    with st.container(border=True):
                        st.markdown(f"**Express #{idx + 1} | {order['id']}**")
                        st.write(f"👤 {order['customer']}")
                        st.write(f"⚒️ {order['item']} ({order['material']})")
                        st.write(f"✨ {order['extra']}")
                        st.write(f"💰 {order['cost']} Gold")
                        st.write(f"📌 {status_color} `{order['status']}`")

        with col_norm:
            st.markdown("### 📜 Standard Queue")
            if not normal_orders:
                st.caption("No standard orders.")
            else:
                for idx, order in enumerate(normal_orders):
                    status_color = {"Pending": "🟡", "Forging": "🔥", "Ready": "🟢", "Completed": "✅"}.get(order['status'], "⚪")
                    with st.container(border=True):
                        st.markdown(f"**Standard #{idx + 1} | {order['id']}**")
                        st.write(f"👤 {order['customer']}")
                        st.write(f"⚒️ {order['item']} ({order['material']})")
                        st.write(f"✨ {order['extra']}")
                        st.write(f"💰 {order['cost']} Gold")
                        st.write(f"📌 {status_color} `{order['status']}`")

with tab_manage:
    st.subheader("📊 Gunter's Forge Master Dashboard")
    st.write("Manage workflow, update order statuses, and monitor supplies.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", len(st.session_state.orders))
    col2.metric("In Forge 🔥", sum(1 for o in st.session_state.orders if o['status'] == "Forging"))
    col3.metric("Ready 🟢", sum(1 for o in st.session_state.orders if o['status'] == "Ready"))

    st.divider()
    st.subheader("🛠️ Update Order Status")

    if not st.session_state.orders:
        st.info("No orders available to update yet.")
    else:
        order_options = {f"{o['id']} - {o['customer']} ({o['item']})": o['id'] for o in st.session_state.orders}
        selected_display = st.selectbox("Select Order:", list(order_options.keys()))
        target_id = order_options[selected_display]

        new_status = st.selectbox("New Status:", ["Pending", "Forging", "Ready", "Completed"])

        if st.button("Apply Update"):
            for o in st.session_state.orders:
                if o['id'] == target_id:
                    o['status'] = new_status
            st.success(f"Order `{target_id}` updated to **{new_status}**!")
            st.rerun()

    st.divider()
    st.subheader("📦 Raw Material Supply")
    for mat_name, count in st.session_state.inventory.items():
        st.write(f"**{mat_name}:** {count} units remaining")
        st.progress(min(count / 50.0, 1.0))

    if st.button("Restock Forge Materials (+20 Units Each)"):
        for mat in st.session_state.inventory:
            st.session_state.inventory[mat] += 20
        st.success("Successfully restocked raw materials!")
        st.rerun()
