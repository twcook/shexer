from dbshx.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from dbshx.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS


class FixedPropChoiceStatementSerializer(BaseStatementSerializer):

    def __init__(self, instantiation_property_str):
        super(FixedPropChoiceStatementSerializer, self).__init__(instantiation_property_str)

    def serialize_statement_with_indent_level(self, a_statement, is_last_statement_of_shape, namespaces_dict):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, namespaces_dict)
        st_target_elements = []
        for a_type in a_statement.st_types:
            st_target_elements.append(self.str_of_target_element(target_element=a_type,
                                                                 st_property=a_statement.st_property,
                                                                 namespaces_dict=namespaces_dict))

        tuples_line_indent.append(FixedPropChoiceStatementSerializer._opening_tuple_line_of_choice())

        tuples_line_indent.append(FixedPropChoiceStatementSerializer.
                                  _statement_in_choice_no_cardinality(st_property,
                                                                      st_target_elements[0]))

        for a_type in st_target_elements[1:]:
            tuples_line_indent.append(FixedPropChoiceStatementSerializer._tuple_of_disjunction())
            tuples_line_indent.append(
                FixedPropChoiceStatementSerializer._statement_in_choice_no_cardinality(st_property,
                                                                                       a_type))

        tuples_line_indent.append(FixedPropChoiceStatementSerializer._tuple_closing_choice(a_statement,
                                                                                           is_last_statement_of_shape))

        for a_comment in a_statement.comments:
            tuples_line_indent.append((a_comment, 4))
        a = 3 + 1

        return tuples_line_indent

    @staticmethod
    def _tuple_closing_choice(a_statement, is_last_statement_of_shape):
        str_res = ")" + SPACES_GAP_BETWEEN_TOKENS + \
                  BaseStatementSerializer.cardinality_representation(a_statement.cardinality) + \
                  BaseStatementSerializer.closure_of_statement(is_last_statement_of_shape)
        str_res += BaseStatementSerializer.adequate_amount_of_final_spaces(str_res) + \
                   BaseStatementSerializer.probability_representation(a_statement.probability)
        return str_res, 1

    @staticmethod
    def _tuple_of_disjunction():
        return "|", 2

    @staticmethod
    def _opening_tuple_line_of_choice():
        return "(", 1

    @staticmethod
    def _statement_in_choice_no_cardinality(st_property, st_type):
        return (st_property + SPACES_GAP_BETWEEN_TOKENS + st_type, 1)
