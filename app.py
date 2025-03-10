import streamlit as st

def main():
    # Initialize session state variables
    if 'step' not in st.session_state:
        st.session_state.step = 1
        st.session_state.puzzle_solved = False
        st.session_state.choice1 = "Investigate the donut"  # default value
        st.session_state.choice2 = "A Map"  # default value
        st.session_state.choice3 = "Quietly leave the office and head to the nearest taco stand"  # default value

    st.title("Silly Office Adventure")
    st.write("A goofy, interactive story to keep you entertained (especially if you've had a few drinks).")

    # STEP 1
    if st.session_state.step == 1:
        st.write(
            """
            You had a couple of drinks at lunch, and now you're stuck in the office late.
            Time to entertain yourself with some mischief until you can leave...
            """
        )
        st.write(
            """
            You wake up from a half-dazed nap at your desk. Your boss is gone. The lights are flickering.
            There's an eerie silence. In front of you, there's a half-eaten donut and a suspicious cup of coffee.
            """
        )

        # First decision
        st.radio(
            "What do you do first?",
            (
                "Investigate the donut",
                "Take a sip of the coffee",
                "Stand up and stretch",
            ),
            key="choice1",  # this updates st.session_state.choice1
        )

        if st.button("Next"):
            st.session_state.step = 2

    # STEP 2
    elif st.session_state.step == 2:
        # Now, st.session_state.choice1 is guaranteed to exist
        choice1 = st.session_state.choice1

        if choice1 == "Investigate the donut":
            st.write(
                """
                You poke the donut. A stale chunk falls off—gross!
                But there's a tiny note inside: "Meet me by the water cooler". Who left this?
                """
            )
        elif choice1 == "Take a sip of the coffee":
            st.write(
                """
                You take a big gulp. It's cold... and tastes like it has so much sugar, your mouth hurts!
                You feel a sudden burst of energy—perhaps too much?
                """
            )
        else:
            st.write(
                """
                You stand and stretch, cracking your back. Ouch, your foot is asleep!
                As you shake it out, you notice a cryptic note pinned to your cubicle wall...
                """
            )

        st.write("You decide to follow the note's mysterious instructions and head toward the water cooler.")

        if st.button("Continue"):
            st.session_state.step = 3

    # STEP 3
    elif st.session_state.step == 3:
        st.write(
            """
            At the water cooler, you see a sticky note that reads:

            "Need a refill? Answer the riddle:
            **I have cities but no houses, forests but no trees, and water but no fish. What am I?**"
            """
        )
        choice2 = st.radio(
            "Is it:",
            ("A Sponge", "A Map", "A Desert"),
            key="choice2",
        )

        if st.button("Submit Answer"):
            # Check puzzle
            if choice2 == "A Map":
                st.session_state.puzzle_solved = True
            st.session_state.step = 4

    # STEP 4
    elif st.session_state.step == 4:
        puzzle_solved = st.session_state.puzzle_solved
        choice2 = st.session_state.choice2

        if choice2 == "A Sponge":
            st.write(
                """
                **A sponge?** That doesn't even make sense!
                The sticky note dissolves in your hand, leaving you stumped and damp. You lose some dignity.
                """
            )
        elif choice2 == "A Map":
            st.write(
                """
                **Correct!** The note reveals a cryptic QR code. You feel a surge of pride.
                """
            )
        else:  # "A Desert"
            st.write(
                """
                **A desert?** That’s definitely got no water, but it doesn't have cities either. Swing and a miss!
                """
            )

        # Next branching
        if puzzle_solved:
            st.write(
                """
                You scan the QR code, and it leads you to an internal company portal with a hidden
                "secret exit" pass! You realize you can now open the supply closet and slip out the back door.
                """
            )
            choice3 = st.radio(
                "Do you...",
                (
                    "Quietly leave the office and head to the nearest taco stand",
                    "Stick around a bit longer to see if there's more free snacks",
                ),
                key="choice3",
            )

            if st.button("Final Decision"):
                if choice3 == "Quietly leave the office and head to the nearest taco stand":
                    st.write(
                        """
                        **Congratulations!** You slip out undetected and treat yourself to tacos.
                        Freedom and delicious comfort food at last. **You WIN!**
                        """
                    )
                else:
                    st.write(
                        """
                        You linger around, rummaging for more snacks... The cleaning crew finds you
                        asleep hugging a giant box of stale crackers. They call security. Oops!
                        **GAME OVER.**
                        """
                    )
                st.session_state.step = 5
        else:
            st.write(
                """
                Without the secret pass, you can't unlock the supply closet. You're doomed to wander the halls...
                You pace around the corridor and trip over your own shoelaces.
                Security cameras catch everything. **Busted!**
                **GAME OVER.**
                """
            )
            st.session_state.step = 5

    # STEP 5 (END)
    else:
        st.write("Thank you for playing **Silly Office Adventure**!")
        if st.button("Play Again"):
            # Reset session state for a fresh start
            for key in ("step", "puzzle_solved", "choice1", "choice2", "choice3"):
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()
