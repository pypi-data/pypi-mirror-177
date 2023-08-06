import itertools
from io import BytesIO
from itertools import product
from typing import Callable, List, Sequence, Any, Dict, Optional

from mrjob.job import MRJob
from approvaltests import verify, verify_all_combinations, Options


# we can compare to other place that pass options to verify
# pass in the options object as an optional parameter
def verify_map_reduce(
    mr_job_under_test: MRJob, test_data: str, *, options: Optional[Options] = None
) -> None:
    storyboard = print_map_reduce_job(mr_job_under_test, test_data)
    # pass into the verify call an options object
    verify(storyboard, options=options)


def print_map_reduce_job(mr_job_under_test: MRJob, test_data: str) -> str:
    storyboard = f"{test_data}\n\nMap reduces to:\n\n"
    mr_job_under_test.sandbox(stdin=BytesIO(test_data.encode("utf-8")))
    with mr_job_under_test.make_runner() as runner:
        runner.run()
        results = mr_job_under_test.parse_output(runner.cat_output())
        for key, value in sorted(results):
            storyboard += f"{key}:{value}\n"
    return storyboard


def verify_templated_map_reduce(
    map_reduction: MRJob,
    input_creator: Callable[[Sequence[Any]], str],
    params: Sequence[Any],
    *,
    options: Optional[Options] = None,
) -> None:
    def map_reducer_creator(*args):
        return map_reduction

    verify_templated_map_reduce_with_customized_job(
        map_reducer_creator, input_creator, params, options=options
    )


def verify_templated_map_reduce_with_customized_job(
    map_reduce_creator: Callable[[Sequence[Any]], MRJob],
    input_creator: Callable[[Sequence[Any]], str],
    params: Sequence[Sequence[Any]],
    *,
    options: Optional[Options] = None,
) -> None:
    inputs = product(*params)
    verify_templated_map_reduce_with_customized_job_with_dictionary_args2(
        lambda i: map_reduce_creator(*i),
        lambda i: input_creator(*i),
        inputs,
        options=options,
    )


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def verify_templated_map_reduce_with_customized_job_with_dictionary_args(
    map_reduce_creator: Callable[[Dict[str, Any]], MRJob],
    input_creator: Callable[[Dict[str, Any]], str],
    params: Dict[str, Sequence[Any]],
    *,
    options: Optional[Options] = None,
) -> None:
    inputs = product_dict(**params)
    verify_templated_map_reduce_with_customized_job_with_dictionary_args2(
        map_reduce_creator, input_creator, inputs, options=options
    )


def verify_templated_map_reduce_with_customized_job_with_dictionary_args2(
    map_reduce_creator: Callable[[Any], MRJob],
    input_creator: Callable[[Any], str],
    inputs: Dict[str, Any],
    *,
    options: Optional[Options] = None,
) -> None:
    storyboard = ""
    for input in inputs:
        storyboard += f"===================\n\n{input} =>\n"
        data = input_creator(input)
        map_reduction = map_reduce_creator(input)

        storyboard += f"{print_map_reduce_job(map_reduction, data)}\n"
    verify(storyboard, options=options)
