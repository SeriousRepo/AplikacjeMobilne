from unittest import TestLoader, TextTestRunner, TestSuite

from tests.test_call import CallTestCase
from tests.test_operator import OperatorTestCase
from tests.test_tarrif import TarrifTestCase
from tests.test_user import UserTestCase

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(CallTestCase),
        loader.loadTestsFromTestCase(OperatorTestCase),
        loader.loadTestsFromTestCase(TarrifTestCase),
        loader.loadTestsFromTestCase(UserTestCase),
        ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
