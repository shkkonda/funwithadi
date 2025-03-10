import streamlit as st

# Initialize the game state if not already set
if "page" not in st.session_state:
    st.session_state["page"] = "start"

def reset_game():
    st.session_state.clear()
    st.session_state["page"] = "start"

# --- Start Page ---
if st.session_state["page"] == "start":
    st.title("Drunken Office Adventure!")
    st.write("You're in the office and a bit too tipsy to handle your usual work.")
    st.write("What do you do?")
    
    choice = st.radio(
        "Choose your action:",
        (
            "Search for snacks in the break room",
            "Try to fix the malfunctioning coffee machine",
            "Chat with a coworker"
        ),
        key="start_choice"
    )
    
    if st.button("Proceed", key="start_proceed"):
        if choice == "Search for snacks in the break room":
            st.session_state["page"] = "snacks"
        elif choice == "Try to fix the malfunctioning coffee machine":
            st.session_state["page"] = "coffee"
        elif choice == "Chat with a coworker":
            st.session_state["page"] = "chat"

# --- Snacks Branch ---
elif st.session_state["page"] == "snacks":
    st.header("The Snack Hunt")
    st.write("You wander into the break room in search of snacks...")
    st.write("You spot a box of donuts and a bag of chips on the counter.")
    
    snack_choice = st.radio(
        "Which one do you pick?",
        ("Donuts", "Chips"),
        key="snacks_choice"
    )
    
    if st.button("Proceed", key="snacks_proceed"):
        if snack_choice == "Donuts":
            st.write("Donuts, yum! The sugary boost makes you feel unstoppable!")
        else:
            st.write("Chips it is! Crunchy and satisfying, though a bit too greasy for your taste.")
        st.session_state["page"] = "end"

# --- Coffee Branch ---
elif st.session_state["page"] == "coffee":
    st.header("The Coffee Machine Challenge")
    st.write("Determined, you approach the temperamental coffee machine.")
    st.write("You press buttons and fiddle with the wires, but nothing seems to work.")
    
    coffee_choice = st.radio(
        "Do you:",
        ("Give it one more try", "Accept defeat and grab a coffee from the vending machine"),
        key="coffee_choice"
    )
    
    if st.button("Proceed", key="coffee_proceed"):
        if coffee_choice == "Give it one more try":
            st.write("Miraculously, with one last twist, the machine sputters to life! Coffee flows like magic!")
        else:
            st.write("Sometimes, it's best to let technology win. You head over to the vending machine and treat yourself to a coffee.")
        st.session_state["page"] = "end"

# --- Chat Branch ---
elif st.session_state["page"] == "chat":
    st.header("Office Chit-Chat")
    st.write("You decide to strike up a conversation with a coworker.")
    st.write("Your coworker raises an eyebrow at your enthusiasm.")
    
    chat_choice = st.radio(
        "Do you:",
        ("Crack a hilarious off-the-cuff joke", "Ask for advice on surviving a hangover"),
        key="chat_choice"
    )
    
    if st.button("Proceed", key="chat_proceed"):
        if chat_choice == "Crack a hilarious off-the-cuff joke":
            st.write("Your joke lands perfectly, and soon you're both laughing like there's no tomorrow!")
        else:
            st.write("Your coworker shares some surprisingly wise hangover tips. Laughter and wisdom mix in the best way!")
        st.session_state["page"] = "end"

# --- End Page ---
elif st.session_state["page"] == "end":
    st.header("=== Thanks for playing the Drunken Office Adventure! ===")
    st.write("Remember: Always drink responsibly and keep the office shenanigans fun!")
    if st.button("Play Again", key="play_again"):
        reset_game()

# Display the current page state (for debugging, optional)
st.sidebar.write("Current page:", st.session_state["page"])
