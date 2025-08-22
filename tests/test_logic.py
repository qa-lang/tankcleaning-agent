
import pandas as pd
from app.logic import find_transition

def test_find_transition():
    df = pd.DataFrame({
        'Previous_Cargo': ['Base Oil'],
        'Next_Cargo': ['Jet Fuel'],
        'HM50_Code': ['2M']
    })
    row = find_transition(df, 'Base Oil', 'Jet Fuel')
    assert row['HM50_Code'] == '2M'
