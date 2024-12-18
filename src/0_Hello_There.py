import streamlit as st
import configparser
import time


def main():

    st.set_page_config(
        page_title="Photogrudo · Hello",
        layout="centered",
        initial_sidebar_state="auto"
    )

    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "sign_in" not in st.session_state:
        st.session_state["sign_in"] = ""

    if "just_changed_name" not in st.session_state:
        st.session_state["just_changed_name"] = False

    # print page title and subheading

    st.title("Photogrudo")
    st.write("photo-gru-doo")

    if st.session_state["logged_in"] is True:
        st.header("Hey!")

        st.write(f"You're logged in as {st.session_state['user']}")
        st.write("Go to the overview page in the sidebar for your to do list. (Press the little arrow to expand the sidebar)")

        name_change()

        with open("Assets/Photogrudo - User Manual.pdf", "rb") as file:
            st.download_button(
                label="📑 Get started by reading the photogrudo user guide",
                data=file,
                file_name="Getting Started with Photogrudo.pdf",
            )

        successful_login()

    else:
        if st.session_state["sign_in"] == "":

            # Create log in page with buttons

            new_user = st.button("👤 Make an account!")
            returning_user = st.button("🔐 Sign in")

            if new_user is True:
                st.session_state["sign_in"] = "new"
                st.experimental_rerun()
            elif returning_user is True:
                st.session_state["sign_in"] = "return"
                st.experimental_rerun()

        # Show page for returning users

        if st.session_state["sign_in"] == "return":
            user = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")

            if user != "":
                login_attempt(user, password)

            if st.button("⏮️ Go back") is True:
                st.session_state["sign_in"] = ""
                st.experimental_rerun()

        # show page for new users
        elif st.session_state["sign_in"] == "new":
            add_user()


def successful_login():
    # Display logout button to show with successful login

    if st.button("🔐 Logout") is True:
        st.session_state["sign_in"] = ""
        st.session_state["logged_in"] = False
        st.experimental_rerun()


def add_user():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.photogrudo')

    user = st.text_input("Make a username for your new account")

    # First time initialisation of session state and config key for new user
    if user != "" and user not in config:
        config.add_section(user)
        config[user]["name"] = user
        config[user]['penguin'] = "Assets/motivation_penguin.gif"
        config[user]["tdl"] = ""
        config[user]["tdfl"] = ""
        config[user]["cmpl"] = ""
        config[user]["ltcmpl"] = ""
        config[user]['num_complete'] = "0"
        config[user]["times_to_complete"] = ""
        config[user]["content_planner"] = ""
        config[user]["was_overdue"] = "0"

        st.session_state["user"] = user
        st.session_state["penguin"] = "Assets/motivation_penguin.gif"
        st.session_state['tdl'] = []
        st.session_state['tdfl'] = []
        st.session_state['cmpl'] = []
        st.session_state['ltcmpl'] = []
        st.session_state['num_complete'] = 0
        st.session_state["times_to_complete"] = []
        st.session_state["content_planner"] = []
        st.session_state["was_overdue"] = 0

        password = st.text_input(f"Set a password for {user}", type="password")
        # display password entry field if username does not exist already and field is not blank

        st.write("Avoid using a password you've used before.")
        set_password = st.button("Save new password")

        if set_password is True and password != "":
            config[user]["password"] = password

            # update config file for new users
            with open('user_data.photogrudo', 'w') as configfile:
                config.write(configfile)
                st.session_state['logged_in'] = True

            st.experimental_rerun()
    elif user in config:  # display error message for username taken
        st.error(
            "Looks like that username is taken! Press the sign in button to log in or choose a different username.")
        retry_new_account = st.button(
            f"⏮️ Alright! I'll try to sign in to {user} or make a new account that isn't called {user}.")
        if retry_new_account:
            st.session_state["sign_in"] = ""
            st.experimental_rerun()

    if st.button("⏮️ Go back") is True:
        st.session_state["sign_in"] = ""
        st.experimental_rerun()


def login_attempt(user, password):
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.photogrudo')

    try:
        # load session state with information from relevant fields in config file

        login = st.button(f"🔓 Log in to {config[user]['name']}")
        if password == config[user]["password"] and login is True:
            st.session_state['logged_in'] = True
            st.session_state["user"] = config[user]["name"]
            st.session_state["penguin"] = config[user]['penguin']
            st.session_state['tdl'] = config[user]["tdl"].split("`")
            st.session_state['tdfl'] = config[user]["tdfl"].split("`")
            st.session_state['cmpl'] = config[user]["cmpl"].split("`")
            st.session_state['ltcmpl'] = config[user]["ltcmpl"].split("`")
            st.session_state['num_complete'] = int(config[user]["num_complete"])
            st.session_state["times_to_complete"] = config[user]["times_to_complete"].split("`")
            st.session_state["content_planner"] = config[user]["content_planner"].split("`")
            st.session_state['was_overdue'] = int(config[user]["was_overdue"])

            # update config file for returning users
            with open('user_data.photogrudo', 'w') as configfile:
                config.write(configfile)

            st.experimental_rerun()
        elif password != config[user]["password"] and password != "" and login is True:
            st.error("Username and password do not match")
            time.sleep(3)
    except KeyError:
        st.error("Looks like that username does not exist. Do you have an account? Check if you've spelled your name wrong.")


def name_change():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.photogrudo')

    with st.expander("Change your username!"):
        user = st.session_state["user"]
        new_name = st.text_input("Type your new username.")

        password = st.text_input(f"Type your password to confirm your name change from {user} to {new_name}",
                                 type="password")
        # display password entry field if username does not exist already and field is not blank

        confirm = st.button("Make the change")

        if confirm is True and password == config[user]["password"] and new_name != "" and new_name not in config:
            config.add_section(new_name)
            config[new_name]["password"] = config[user]["password"]
            config[new_name]["name"] = new_name
            config[new_name]['penguin'] = config[user]["penguin"]
            config[new_name]["tdl"] = config[user]["tdl"]
            config[new_name]["tdfl"] = config[user]["tdfl"]
            config[new_name]["cmpl"] = config[user]["cmpl"]
            config[new_name]["ltcmpl"] = config[user]["ltcmpl"]
            config[new_name]['num_complete'] = config[user]["num_complete"]
            config[new_name]["times_to_complete"] = config[user]["times_to_complete"]
            config[new_name]["content_planner"] = config[user]["content_planner"]
            config[new_name]["was_overdue"] = config[user]["was_overdue"]

            st.session_state["user"] = new_name

            config.remove_section(user)

            # update config file for new users
            with open('user_data.photogrudo', 'w') as configfile:
                config.write(configfile)
                st.session_state["just_changed_name"] = True

            st.experimental_rerun()

        elif new_name in config:  # display error message for username taken
            if not st.session_state["just_changed_name"] is True:
                st.error("Looks like that username is taken! Choose a different username.")
            else:
                st.success("Successfully changed your name")
            st.session_state["just_changed_name"] = False
        elif password != config[user]["password"] and password != "":
            st.error("Double check your password.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()