import pytest
from nosop_py import NosoPoolPublic

@pytest.fixture
def elements():
    return [
        'v0.59',  # Version
        1,        # IPs Count
        57,       # Max Shares
        36,       # Pool Pay Interval
        '127.0.0' # Reques
    ]

def test_NosoPoolPublic_no_args():
    pp = NosoPoolPublic()

    assert pp.version == ''
    assert pp.ips_count == -1
    assert pp.max_shares == -1
    assert pp.pool_pay_interval == -1
    assert pp.requester_range == ''

def test_NosoPoolPublic_with_args(elements):
    pp = NosoPoolPublic(*elements)

    assert pp.version == 'v0.59'
    assert pp.ips_count == 1
    assert pp.max_shares == 57
    assert pp.pool_pay_interval == 36
    assert pp.requester_range == '127.0.0'
