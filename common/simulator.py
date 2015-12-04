from django.test.runner import DiscoverRunner
from datetime import datetime
import unittest

class Simulator(object):
    """
    Base class for running simulations in an isolated environment
    """
    def __init__(self):
        self._test_runner = _PassiveTestRunner()

    def run(self, simulation):
        self._test_runner.run_single_test(simulation)
        simulation.logger.save(file_format='csv')


class _PassiveTestRunner(DiscoverRunner):
    """
    Custom modification of test runner which does not perform test
    discovery
    """
    def run_single_test(self, test_instance):
        self.run_tests(test_labels=[], extra_tests=[test_instance])

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        """
        Build suite only from instantiated tests in 'extra_tests' list
        """
        suite = self.test_suite()
        for test in extra_tests:
            suite.addTest(test)
        return suite

    def run_suite(self, suite, **kwargs):
        """
        """
        result = self.test_runner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            resultclass=_QuietTestResult,
            stream=_QuietStream()
        ).run(suite)
        print('-' * 70)
        return result

class _QuietStream(object):
    """
    Stream used for simulation runner.
    """
    def write(self, text):
        #text = text.replace('test', 'simulation')
        #print(text, end='')
        pass

    def flush(self):
        pass


class _QuietTestResult(unittest.TextTestResult):
    """
    Test result class which is quit most of the time.
    Used for simulations, we don't want to show dots etc.
    """

    def addSuccess(self, test):
        pass

    def addError(self, test, err):
        pass

    def addFailure(self, test, err):
        pass

    def addSkip(self, test, reason):
        pass

    def addExpectedFailure(self, test, err):
        pass

    def addUnexpectedSuccess(self, test):
        pass