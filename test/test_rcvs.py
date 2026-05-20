import polars as pl
from smithy import smith_set

def test_condorcet():
    df = pl.DataFrame({
                          'A': [1, 1, 2, 1],
                          'B': [2, 2, 1, 2],
                          'C': [3, 3, 3, 3],
                      })
    assert smith_set(df) == ['A']

def test_rockpprscrcycle():
    df = pl.DataFrame({
                             'A': [1, 2, 3],
                             'B': [2, 3, 1],
                             'C': [3, 1, 2],
                         })
    assert smith_set(df) == ['A', 'B', 'C']

def test_abpair():
    df = pl.DataFrame({
        "A": [1, 2, 1, 3],
        "B": [2, 1, 3, 1],
        "C": [3, 3, 2, 2]
        })
    assert smith_set(df) == ['A', 'B']

def test_fourcycle():
    df = pl.DataFrame({
        "A": [1,2,3,4],
        "B": [2,3,4,1],
        "C": [3,4,1,2],
        "D": [4,1,2,3],
    })
    assert smith_set(df) == ['A', 'B', 'C', 'D']
