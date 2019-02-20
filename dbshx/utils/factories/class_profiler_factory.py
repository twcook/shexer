from dbshx.utils.factories.triple_yielders_factory import get_triple_yielder
from dbshx.core.class_profiler import ClassProfiler


def get_class_profiler(target_classes_dict, source_file, list_of_source_files, input_format):
    yielder = get_triple_yielder(source_file=source_file,
                                 list_of_source_files=list_of_source_files,
                                 input_format=input_format)

    return ClassProfiler(triples_yielder=yielder,
                         target_classes_dict=target_classes_dict)
