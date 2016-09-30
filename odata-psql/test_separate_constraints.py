import os
from separate_constraints import main as separate_constraints

TEST_CASES = (
    (
        'Contactcontactorders_associationSalesOrder.sql',
        'Contactcontactorders_associationSalesOrder-out.sql',
    ),
    (
        'SystemUserSet.sql',
        'SystemUserSet-out.sql',
    ),
)


def test_separate_constraints():
    for name_in, name_out in TEST_CASES:
        fixtures_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'fixtures',
        )
        with open(os.path.join(fixtures_path, name_out), 'r') as out_fh, open(os.path.join(fixtures_path, name_in), 'r') as in_fh:
            out = separate_constraints(in_fh.read())
            expected = out_fh.read().strip()
            assert '\n'.join(out) == expected
