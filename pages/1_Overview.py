import streamlit as st
import configparser


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] is True:
        config = configparser.ConfigParser()
        config.sections()
        config.read('user_data.stodo')

        if "cmpl" not in st.session_state:
            st.session_state['cmpl'] = []

        for i in st.session_state["tdl"]:
            if i == "":
                st.session_state["tdl"].remove(i)

        for i in st.session_state["tdfl"]:
            if i == "":
                st.session_state["tdfl"].remove(i)

        for i in st.session_state["cmpl"]:
            if i == "":
                st.session_state["cmpl"].remove(i)

        for i in st.session_state["ltcmpl"]:
            if i == "":
                st.session_state["ltcmpl"].remove(i)

        st.set_page_config(
            page_title="this is not called stodo · Overview",
            layout="centered",
            initial_sidebar_state="collapsed",
        )

        if "cmpl" not in st.session_state:
            st.session_state['cmpl'] = []

        complete = []
        complete_ids = []

        st.title('Overview')

        col1, col2, col3 = st.columns(3)

        with col3:
            st.header("Done")
            st.write("Completed tasks")

        with col1:
            st.header("Do now")
            st.write("Priority Tasks")

            for i in st.session_state['tdl']:
                j = i.split("[")
                st.checkbox(j[0], key=i)
                if st.session_state[i] is True:
                    complete.append(j[0])
                    complete_ids.append(i)

        with col2:
            st.header("Do soon")
            st.write("Do at some point")

            for i in st.session_state['tdfl']:
                j = i.split("[")
                st.checkbox(j[0], key=i)
                if st.session_state[i] is True:
                    complete.append(j[0])
                    complete_ids.append(i)

        completed_tasks(complete_ids)

        with col3:
            for i in st.session_state["cmpl"]:
                col3.text(i)
            if len(st.session_state["cmpl"]) > 0:
                delete_tasks = st.button("Delete completed tasks")
                if delete_tasks is True:
                    del st.session_state["cmpl"]
                    st.experimental_rerun()

        update_config()

    else:
        st.error("Log in please")


def update_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.stodo')

    user = st.session_state["user"]

    tdl_to_update = ""
    tdfl_to_update = ""
    cmpl_to_update = ""
    ltcmpl_to_update = ""

    for i in st.session_state['tdl']:
        tdl_to_update += "`" + i

    for i in st.session_state['tdfl']:
        tdfl_to_update += "`" + i

    for i in st.session_state['cmpl']:
        cmpl_to_update += "`" + i

    for i in st.session_state['ltcmpl']:
        ltcmpl_to_update += "`" + i

    config[user]["name"] = st.session_state["user"]
    config[user]['penguin'] = st.session_state["penguin"]
    config[user]["tdl"] = tdl_to_update
    # config.set(user, 'tdl', str(st.session_state["tdl"]))
    config[user]["tdfl"] = tdfl_to_update
    config[user]["cmpl"] = cmpl_to_update
    config[user]["ltcmpl"] = ltcmpl_to_update
    config[user]["num_complete"] = str(st.session_state['num_complete'])

    with open('user_data.stodo', 'w') as configfile:
        config.write(configfile)


def completed_tasks(keys):
    removed_something = False

    for i in keys:
        # add to complete and long term complete list in session_state
        st.session_state["cmpl"].append(i)
        st.session_state["ltcmpl"].append(i)
        st.session_state['num_complete'] += 1

        # remove keys of completed tasks from respective lists in session_state
        if i in st.session_state["tdl"]:
            st.session_state["tdl"].remove(i)
            removed_something = True
        if i in st.session_state["tdfl"]:
            st.session_state["tdfl"].remove(i)
            removed_something = True

        if i in st.session_state:
            del st.session_state[i]
            removed_something = True

    # rerun streamlit to update lists in overview
    if removed_something is True:
        st.experimental_rerun()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
