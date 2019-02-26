
from dbshx.utils.log import log_to_error
from dbshx.utils.triple_yielders import tune_token, tune_prop, check_if_property_belongs_to_namespace_list


class TsvNtTriplesYielder(object):
    def __init__(self, source_file, namespaces_to_ignore=None):
        self._source_file = source_file
        self._triples_count = 0
        self._error_triples = 0
        self._namespaces_to_ignore = None # TODO
        self._namespaces_to_ignore = namespaces_to_ignore
        self.yield_triples = self._yield_triples_not_excluding_namespaces if namespaces_to_ignore is None\
            else self._yield_triples_excluding_namespaces

    def yield_triples(self):
        self._reset_count()
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                tokens = self._look_for_tokens(a_line.strip())
                if len(tokens) != 3:
                    self._error_triples += 1
                    log_to_error(msg="This line caused error: " + a_line,
                                 source=self._source_file)
                else:
                    try:
                        yield (tune_token(tokens[0]), tune_prop(tokens[1]), tune_token(tokens[2], allow_untyped_numbers=True))
                        self._triples_count += 1
                    except ValueError as ve:
                        log_to_error(msg=ve.message + "This line caused error: " + a_line,
                                     source=self._source_file)
                    if self._triples_count % 10000 == 0:
                        print "Reading...", self._triples_count

    def _yield_triples_excluding_namespaces(self):
        self._reset_count()
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                tokens = self._look_for_tokens(a_line.strip())
                if len(tokens) != 3:
                    self._error_triples += 1
                    log_to_error(msg="This line caused error: " + a_line,
                                 source=self._source_file)
                else:
                    try:
                        candidate_triple = (tune_token(tokens[0]),
                                            tune_prop(tokens[1]),
                                            tune_token(tokens[2], allow_untyped_numbers=True))
                        if not check_if_property_belongs_to_namespace_list(str(candidate_triple[1]),
                                                                           namespaces=self._namespaces_to_ignore):
                            yield candidate_triple

                        self._triples_count += 1
                    except ValueError as ve:
                        log_to_error(msg=ve.message + "This line caused error: " + a_line,
                                     source=self._source_file)
                    if self._triples_count % 10000 == 0:
                        print "Reading...", self._triples_count

    def _yield_triples_not_excluding_namespaces(self):
        self._reset_count()
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                tokens = self._look_for_tokens(a_line.strip())
                if len(tokens) != 3:
                    self._error_triples += 1
                    log_to_error(msg="This line caused error: " + a_line,
                                 source=self._source_file)
                else:
                    try:
                        yield (
                        tune_token(tokens[0]), tune_prop(tokens[1]), tune_token(tokens[2], allow_untyped_numbers=True))
                        self._triples_count += 1
                    except ValueError as ve:
                        log_to_error(msg=ve.message + "This line caused error: " + a_line,
                                     source=self._source_file)
                    if self._triples_count % 10000 == 0:
                        print "Reading...", self._triples_count

    def _look_for_tokens(self, str_line):
        return str_line.split("\t")

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_triples

    def _reset_count(self):
        self._error_triples = 0
        self._triples_count = 0

