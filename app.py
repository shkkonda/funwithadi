import streamlit as st
import random
import time

# Set page config
st.set_page_config(
    page_title="Office Drunk Buddy",
    page_icon="🥴",
    layout="centered"
)

# CSS for some fun styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    .stButton button {
        font-size: 20px;
        border-radius: 12px;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        transform: scale(1.05);
    }
    .game-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: #495057;
    }
    .heading {
        font-size: 30px;
        font-weight: bold;
        margin-top: 30px;
    }
    .score {
        font-size: 24px;
        font-weight: bold;
        color: #495057;
    }
    .result {
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .success {
        background-color: rgba(40, 167, 69, 0.2);
    }
    .danger {
        background-color: rgba(220, 53, 69, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'current_game' not in st.session_state:
    st.session_state.current_game = None
if 'sobriety_level' not in st.session_state:
    st.session_state.sobriety_level = "Tipsy" # Options: "Sober", "Tipsy", "Wobbly", "Office Legend"

# Define sobriety emoji
sobriety_emojis = {
    "Sober": "😊",
    "Tipsy": "🥴",
    "Wobbly": "🥃",
    "Office Legend": "🍻"
}

# Game functions
def reaction_time_game():
    st.markdown("<div class='heading'>Reaction Time Test</div>", unsafe_allow_html=True)
    
    # Instructions
    st.write("Wait for the green button to appear, then click it as fast as you can!")
    
    if "waiting" not in st.session_state:
        st.session_state.waiting = True
        st.session_state.start_time = None
        st.session_state.display_time = None
    
    if st.session_state.waiting:
        wait_col, _ = st.columns([1, 1])
        with wait_col:
            wait_button = st.button("Wait for green...", key="wait_button", disabled=True)
        
        # Randomly decide when to show the green button
        if random.random() < 0.1 or "countdown" in st.session_state:
            st.session_state.waiting = False
            st.session_state.start_time = time.time()
            st.experimental_rerun()
    else:
        click_col, _ = st.columns([1, 1])
        with click_col:
            if st.button("CLICK NOW!", key="click_button"):
                end_time = time.time()
                reaction_time = end_time - st.session_state.start_time
                st.session_state.display_time = reaction_time
                
                # Reset for next round
                st.session_state.waiting = True
                del st.session_state.start_time
                
                # Award points based on reaction time
                if reaction_time < 0.5:
                    points = 10
                    result_class = "success"
                    message = "Amazing reflexes! Are you sure you're drunk? +10 points"
                elif reaction_time < 1.0:
                    points = 5
                    result_class = "success"
                    message = "Pretty good! +5 points"
                else:
                    points = 2
                    result_class = "danger"
                    message = f"Hmm, a bit slow there... but still +2 points for trying!"
                
                st.session_state.points += points
                st.markdown(f"<div class='result {result_class}'>{message}</div>", unsafe_allow_html=True)
                st.markdown(f"Reaction time: {reaction_time:.3f} seconds")
                
                # Update sobriety level based on points
                update_sobriety_level()
                
                st.experimental_rerun()
    
    # Display reaction time from previous round if available
    if "display_time" in st.session_state and st.session_state.display_time is not None:
        st.markdown(f"Last reaction time: {st.session_state.display_time:.3f} seconds")

def memory_game():
    st.markdown("<div class='heading'>Office Memory Game</div>", unsafe_allow_html=True)
    
    if "sequence" not in st.session_state:
        st.session_state.sequence = []
        st.session_state.user_sequence = []
        st.session_state.showing_sequence = False
        st.session_state.game_over = False
    
    office_items = ["📊", "💻", "📱", "📝", "📋", "📌", "☕", "🖨️"]
    
    st.write("Remember the sequence of office items!")
    
    if not st.session_state.showing_sequence and not st.session_state.game_over:
        if st.button("Start New Sequence", key="start_memory"):
            # Generate new sequence
            st.session_state.sequence = [random.choice(office_items) for _ in range(3 + len(st.session_state.sequence)//2)]
            st.session_state.showing_sequence = True
            st.session_state.user_sequence = []
            st.experimental_rerun()
    
    # Show the sequence
    if st.session_state.showing_sequence:
        sequence_display = " ".join(st.session_state.sequence)
        st.markdown(f"<h1 style='text-align: center;'>{sequence_display}</h1>", unsafe_allow_html=True)
        st.write("Memorize this sequence...")
        
        # Use a placeholder to auto-advance
        progress_bar = st.progress(0)
        for i in range(101):
            progress_bar.progress(i)
            time.sleep(0.02)  # Adjust speed based on sequence length
        
        st.session_state.showing_sequence = False
        st.experimental_rerun()
    
    # Let user input their sequence
    if not st.session_state.showing_sequence and not st.session_state.game_over and st.session_state.sequence:
        st.write("Now select the items in the correct order:")
        
        cols = st.columns(4)
        for i, item in enumerate(office_items):
            with cols[i % 4]:
                if st.button(item, key=f"item_{i}"):
                    st.session_state.user_sequence.append(item)
                    if len(st.session_state.user_sequence) == len(st.session_state.sequence):
                        check_sequence()
                    st.experimental_rerun()
        
        current_input = " ".join(st.session_state.user_sequence)
        st.markdown(f"<h3>Your input: {current_input}</h3>", unsafe_allow_html=True)
        
        if st.button("Clear", key="clear_memory"):
            st.session_state.user_sequence = []
            st.experimental_rerun()
    
    if st.session_state.game_over:
        st.markdown("<div class='result danger'>Game Over!</div>", unsafe_allow_html=True)
        correct_sequence = " ".join(st.session_state.sequence)
        user_input = " ".join(st.session_state.user_sequence)
        
        st.markdown(f"<p>Correct sequence: {correct_sequence}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>Your sequence: {user_input}</p>", unsafe_allow_html=True)
        
        score = len(st.session_state.sequence) - 3
        st.session_state.points += score
        st.markdown(f"<p>You remembered {score} items correctly! +{score} points</p>", unsafe_allow_html=True)
        
        if st.button("Play Again", key="memory_again"):
            st.session_state.sequence = []
            st.session_state.user_sequence = []
            st.session_state.game_over = False
            
            # Update sobriety level
            update_sobriety_level()
            st.experimental_rerun()

def check_sequence():
    if st.session_state.user_sequence == st.session_state.sequence:
        # Add new item to sequence
        office_items = ["📊", "💻", "📱", "📝", "📋", "📌", "☕", "🖨️"]
        st.session_state.sequence.append(random.choice(office_items))
        st.session_state.user_sequence = []
        st.session_state.showing_sequence = True
    else:
        st.session_state.game_over = True

def word_scramble():
    st.markdown("<div class='heading'>Office Word Scramble</div>", unsafe_allow_html=True)
    
    office_words = [
        "MEETING", "DEADLINE", "PRINTER", "COFFEE", "LAPTOP", 
        "KEYBOARD", "MONITOR", "PROJECT", "OFFICE", "STAPLER",
        "SCHEDULE", "DOCUMENT", "COWORKER", "PAYCHECK", "CUBICLE"
    ]
    
    if "scrambled_word" not in st.session_state:
        word = random.choice(office_words)
        word_list = list(word)
        random.shuffle(word_list)
        st.session_state.scrambled_word = "".join(word_list)
        st.session_state.correct_word = word
        st.session_state.attempts = 0
        st.session_state.solved = False
    
    st.write(f"Unscramble this office word: **{st.session_state.scrambled_word}**")
    
    # User input
    user_guess = st.text_input("Your guess:", key="word_guess").upper()
    
    if st.button("Submit", key="submit_word"):
        st.session_state.attempts += 1
        
        if user_guess == st.session_state.correct_word:
            st.markdown("<div class='result success'>Correct! You got it!</div>", unsafe_allow_html=True)
            
            # Award points based on attempts
            points = max(1, 10 - st.session_state.attempts)
            st.session_state.points += points
            st.markdown(f"<p>+{points} points!</p>", unsafe_allow_html=True)
            
            st.session_state.solved = True
            
            # Update sobriety level
            update_sobriety_level()
        else:
            st.markdown("<div class='result danger'>Not quite! Try again.</div>", unsafe_allow_html=True)
            
            # Provide a hint after 3 failed attempts
            if st.session_state.attempts >= 3 and not st.session_state.solved:
                correct_word = st.session_state.correct_word
                hint = f"Hint: The word starts with '{correct_word[0]}' and ends with '{correct_word[-1]}'"
                st.info(hint)
    
    if st.session_state.solved:
        if st.button("New Word", key="new_word"):
            # Reset for new word
            word = random.choice([w for w in office_words if w != st.session_state.correct_word])
            word_list = list(word)
            random.shuffle(word_list)
            st.session_state.scrambled_word = "".join(word_list)
            st.session_state.correct_word = word
            st.session_state.attempts = 0
            st.session_state.solved = False
            st.experimental_rerun()

def update_sobriety_level():
    points = st.session_state.points
    
    if points < 10:
        st.session_state.sobriety_level = "Tipsy"
    elif points < 25:
        st.session_state.sobriety_level = "Wobbly"
    elif points < 50:
        st.session_state.sobriety_level = "Office Legend"
    else:
        st.session_state.sobriety_level = "Sober"

# Main app
st.markdown("<div class='game-title'>🥴 Office Drunk Buddy 🥴</div>", unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align: center; margin-bottom: 20px;'>
    <div class='score'>Your Score: {st.session_state.points} points</div>
    <div style='font-size: 20px; margin-top: 10px;'>
        Sobriety Level: {sobriety_emojis[st.session_state.sobriety_level]} {st.session_state.sobriety_level}
    </div>
</div>
""", unsafe_allow_html=True)

# Game selection
if not st.session_state.game_active:
    st.markdown("<div class='heading'>Choose a Game:</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚡ Reaction Test"):
            st.session_state.game_active = True
            st.session_state.current_game = "reaction"
            st.experimental_rerun()
    
    with col2:
        if st.button("🧠 Memory Game"):
            st.session_state.game_active = True
            st.session_state.current_game = "memory"
            st.experimental_rerun()
    
    with col3:
        if st.button("🔤 Word Scramble"):
            st.session_state.game_active = True
            st.session_state.current_game = "word"
            st.experimental_rerun()
    
    st.markdown("""
    <div style='margin-top: 50px; text-align: center; font-size: 18px; color: #6c757d;'>
        <p>Have fun, but remember: Friends don't let friends make poor career decisions! 🚫</p>
        <p>Drink some water and play responsibly! 💧</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Back button
    if st.button("← Back to Game Selection"):
        st.session_state.game_active = False
        st.experimental_rerun()
    
    # Run the selected game
    if st.session_state.current_game == "reaction":
        reaction_time_game()
    elif st.session_state.current_game == "memory":
        memory_game()
    elif st.session_state.current_game == "word":
        word_scramble()

# Add footer
st.markdown("""
<div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background: rgba(255, 255, 255, 0.8);'>
    <p style='font-size: 14px; color: #6c757d;'>
        Remember: This is just a game! Drink water and stay professional. 
        Maybe consider calling a ride home soon? 🚗
    </p>
</div>
""", unsafe_allow_html=True)