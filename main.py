import streamlit as st
import src.pages.home
import src.pages.data
import src.pages.missing_vals
import src.pages.dashboard

PAGES = {
    "Home": src.pages.home,
    "Data Snapshot": src.pages.data,
    "Dashboard": src.pages.dashboard,
    "Missing Values": src.pages.missing_vals,
}

def main():
    st.sidebar.title('Menu')
    choice = st.sidebar.radio('Navigate', list(PAGES.keys()))
    PAGES[choice].main()
    st.sidebar.title('About')
    st.sidebar.info(
        '''
        This app was developed by Felix Odete | Data Analyst
        '''
    )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
