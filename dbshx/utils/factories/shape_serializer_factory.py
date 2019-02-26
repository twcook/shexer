from dbshx.consts import SHEX
from dbshx.io.shex.formater.shex_serializer import ShexSerializer


def get_shape_serializer(output_format, shapes_list, target_file=None, string_return=False, namespaces_dict=None,
                         tolerance_to_keep_similar_rules=0.15, keep_less_specific=True, aceptance_threshold=0.4,
                         instantiation_property=None, discard_useles_constraints_with_positive_closure=True):
    if output_format == SHEX:
        return ShexSerializer(target_file=target_file,
                              shapes_list=shapes_list,
                              aceptance_threshold=aceptance_threshold,
                              namespaces_dict=namespaces_dict,
                              tolerance_to_keep_similar_rules=tolerance_to_keep_similar_rules,
                              keep_less_specific=keep_less_specific,
                              string_return=string_return,
                              instantiation_property_str=instantiation_property,
                              discard_useless_positive_closures=discard_useles_constraints_with_positive_closure)
    else:
        raise ValueError("Currently unsupported format: " + output_format)
