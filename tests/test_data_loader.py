from app.data_loader import load_transitions

def test_load_transitions():
    df = load_transitions()
    assert not df.empty
