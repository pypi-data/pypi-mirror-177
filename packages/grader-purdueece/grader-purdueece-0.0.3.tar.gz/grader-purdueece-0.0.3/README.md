# Module Interface
This grader can load specified tests in a desired loaction that match a specified pattern then run them against source code in another module. The results are collected in CSV format with configurable overrides for each test. Test runs can also change based on a custom submission name (e.g. student name). If grading the submission fails, it will fallback to grading a sepcified template submission directory. It can load a config file that can rename the submission directory to a custom label and can assign weights to individual tests. The help output for the grader is below:

```
usage: grader [-h] [--submission SUBMISSION] [--tests TESTS] [--test-pattern TEST_PATTERN] [--output OUTPUT] [--log LOG] [--config CONFIG] path

positional arguments:
  path                  Path of the module to grade. Defaults to ./

optional arguments:
  -h, --help            show this help message and exit
  --submission SUBMISSION
                        Submission name to grade.
  --tests TESTS         Path of tests to run. Defaults to ./
  --test-pattern TEST_PATTERN
                        Test name pattern to match. Defaults to "test*.py"
  --output OUTPUT       Output file for scores. Defaults to stdout.
  --log LOG             Log file to use. Defaults to stdout.
  --config CONFIG       Config file to use.
```

# Tests Discovery
Tests to run can be located anywhere using a combination of the `--tests` and `--test-pattern` args. By default, they are searched for under the current directory and match the `test*.py` pattern. Tests are discovered using the [`unittest`](https://docs.python.org/3/library/unittest.html) module.

# Grader Config
The grader config can be specified with the `--config` arg. It is a json file that can specify what happens when a certain test runs or when a certain submission is graded. Individual test configs should be under the `"tests"` map and the key should be of the form: `testFunction (test_filename.TestCaseName)`. Inividual submission configs should be under the `"submissions"` map and match the name of the submission. An example format is below:

```json
{
    "tests": {
        "testSimple1 (test_simple.TestSimpleTestCase)": {
            "name": "Simple Test 1",
            "weight": 2
        }
    },
    "submissions": {
        "submission_name": {
            "name": "custom label here"
        }
    }
}
```