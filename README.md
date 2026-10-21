# KU-Competition-2026-CS
Built with Python and Streamlit UI

# Project Overview

This app serves two main purposes:
1. It gives customers a simple way to browse and buy blacksmith gear, customize items with materials and rune engravings, place orders, and track their order status in a live queue.
2. It provides Gunter a private dashboard to track orders, update forging statuses, manage material inventory, buy supplies, and track gold earnings.

The app uses a 3:1 priority queue logic, so for every 3 express orders that come in, there is going to be a regular order to keep it fair for everyone and not leave regular customers waiting forever. 

## Setup Instructions

Access the Live Application
The app is fully deployed on Streamlit Community Cloud and connected to GitHub. You can launch it directly in your web browser:
App URL: https://ku2026.streamlit.app

Alternate Way to access the application
1. Clone this repository

2. Install Streamlit: pip install streamlit

3. Launch the app: python -m streamlit run app.py

## Usage Guide

### Customer View
1. Select "Customer" at the top of the app.
2. In the "Storefront & Order" tab, pick an equipment item (Sword, Plate Armor, Chain Mail, or Cooking Pot).
3. Choose your material grade and rune engraving options. Check the express option if you want to pay extra for rush priority.
4. Type in your name and click "Submit Order to Gunter".
5. Click the "To-Do Queue" tab to view your order's position and current forging status.

### Gunter's View
1. Select "Gunter's Forge Hub" at the top.
2. Enter the passcode: gunter
3. Under "Active Orders", you can view order details and update the status dropdown for any item.
   - Moving an order to Forging, Ready, or Completed uses 1 unit of that item's raw material.
   - Marking an order as Completed collects the order total into Gunter's Gold Vault.
4. Under "Materials", purchase extra raw supplies using the gold in your vault.
5. Click the "Completed Orders" tab to see all finished jobs and past sales.

## Feature List

- Dual-portal view separating customer ordering from shop management by Gunter.
- Passcode-protected dashboard for Gunter to keep secure.
- Pricing calculations are based on base items, material choices, rune engravings, and express fees.
- Custom 3:1 priority queue for express and standard orders.
- Dynamic inventory management that deducts raw materials when orders are forged.
- Supply restock system that allows Gunter to buy materials with the gold that he has in vault.

## Team Contributions

- Trivikram Yellapu: Developed the application interface, storefront logic, custom theme styling, and app deployment to Streamlit Community Cloud.
- Chase Condon: Implemented session management, order logic, and passcode authentication for Gunter's Portal.
- Majd Alkhdr: Built the priority queue sorting algorithm, inventory system, and the gold vault for Gunter.
- Gabe Ledgerwood: Helped with integration, testing, and debugging the app.

# Documentation

AI Usage: AI was used in this project to help with the custom CSS styling. AI was also used in the integration of the dropper game as a website into strealit using HTML. 

# Codebase

app.py is the only file needed to run the application. 
ProjectRequirements.txt is to keep track of requirements for the project and what we need to implement in our code. 
