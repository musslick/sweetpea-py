import glob
import operator as op
import os
import pytest
import re

from sweetpea import fully_cross_block
from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Transition, Window
from sweetpea.sampling_strategies.uniform_combinatoric import UniformCombinatoricSamplingStrategy, UCSolutionEnumerator


color = Factor("color", ["red", "blue"])
text  = Factor("text",  ["red", "blue"])

con_factor_within_trial = Factor("congruent?", [
    DerivedLevel("con", WithinTrial(op.eq, [color, text])),
    DerivedLevel("inc", WithinTrial(op.ne, [color, text]))
])

con_factor_window = Factor("congruent?", [
    DerivedLevel("con", Window(op.eq, [color, text], 1, 1)),
    DerivedLevel("inc", Window(op.ne, [color, text], 1, 1))
])

color_repeats_factor = Factor("repeated color?", [
    DerivedLevel("yes", Transition(lambda colors: colors[0] == colors[1], [color])),
    DerivedLevel("no",  Transition(lambda colors: colors[0] != colors[1], [color]))
])


def test_validate_accepts_basic_factors():
    block = fully_cross_block([color, text],
                              [color, text],
                              [])
    UniformCombinatoricSamplingStrategy._UniformCombinatoricSamplingStrategy__validate(block)


def test_validate_accepts_derived_factors_with_simple_windows():
    block = fully_cross_block([color, text, con_factor_within_trial],
                              [color, text],
                              [])
    UniformCombinatoricSamplingStrategy._UniformCombinatoricSamplingStrategy__validate(block)

    block = fully_cross_block([color, text, con_factor_window],
                              [color, text],
                              [])
    UniformCombinatoricSamplingStrategy._UniformCombinatoricSamplingStrategy__validate(block)


def test_validate_rejects_derived_factors_with_complex_windows():
    block = fully_cross_block([color, text, color_repeats_factor],
                              [color, text],
                              [])
    with pytest.raises(ValueError):
        UniformCombinatoricSamplingStrategy._UniformCombinatoricSamplingStrategy__validate(block)


def test_example_counts():
    # Get all the python examples from the uc-counting-tests directory
    path_to_test_files = os.path.dirname(os.path.abspath(__file__)) + "/uc-counting-tests/*.py"
    files = glob.glob(path_to_test_files)

    failures = []

    for filename in files:
        contents = None
        with open(filename, 'r') as f:
            contents = f.read()
            exec(contents, globals(), locals())

        if 'block' not in vars():
            failures.append("File did not produce a variable named 'block', aborting. file={}".format(filename))
            continue

        matches = re.search('# ASSERT COUNT = (\d+)', contents)
        if matches:
            expected_count = int(matches.groups(0)[0])
            enumerator = UCSolutionEnumerator(vars()['block'])
            if enumerator.solution_count() != expected_count:
                failures.append("Count Mismatch. Actual count: {}, Expected count: {}, File={}"
                    .format(enumerator.solution_count(), expected_count, filename))
        else:
            failures.append("File did not contain an assertion for count, aborting. file={}".format(filename))

    if failures:
        pytest.fail('{} failures occurred in counting tests: {}'.format(len(failures), failures))
