from streamlit.testing.v1 import AppTest

def test_full_flow():
    at = AppTest.from_file("src/main.py").run()
    at.chat_input.input("Hello").run()
    assert "Welcome" in at.markdown[1].value