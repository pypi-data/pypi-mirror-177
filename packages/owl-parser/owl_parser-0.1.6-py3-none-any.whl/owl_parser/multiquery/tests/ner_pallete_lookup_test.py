from baseblock import Enforcer, FileIO

from owl_parser.multiquery.bp import FindOntologyData

absolute_path = FileIO.join_cwd('resources/testing')


class TestFindOntologyData(object):

    def __init__(self,
                 ontology_name: str):
        self.bp = FindOntologyData(
            ontologies=[ontology_name],
            absolute_path=absolute_path)
        assert self.bp

    def ner_pallete_lookup(self):
        """ Given a NER return a Hex Color Code """
        result = self.bp.ner_pallete_lookup('EVENT')
        Enforcer.is_str(result)
        assert result.startswith('#')  # e.g., '#6fcb9f'
        assert len(result) == 7


def runner(ontology_name: str) -> None:
    bp = TestFindOntologyData(ontology_name)
    bp.ner_pallete_lookup()


def test_runner():
    runner('unitest')


def main():
    runner('unitest')


if __name__ == '__main__':
    main()
