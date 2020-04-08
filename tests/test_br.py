
import pandas as pd
import unittest, math, os, ast, statistics
import pyterrier as pt




class TestBatchRetrieve(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBatchRetrieve, self).__init__(*args, **kwargs)
        if not pt.started():
            pt.init()
        self.here=os.path.dirname(os.path.realpath(__file__))
        

    def test_form_dataframe_with_string(self):
        input="light"
        exp_result = pd.DataFrame([["1", "light"]],columns=['qid','query'])
        result=pt.Utils.form_dataframe(input)
        self.assertTrue(exp_result.equals(result))

    def test_form_dataframe_with_list(self):
        input=["light","mathematical","electronic"]
        exp_result = pd.DataFrame([["1", "light"],["2", "mathematical"],["3", "electronic"]],columns=['qid','query'])
        result=pt.Utils.form_dataframe(input)
        self.assertTrue(exp_result.equals(result))

    def test_form_dataframe_throws_assertion_error(self):
        input=("light","mathematical",25)
        self.assertRaises(AssertionError,pt.Utils.form_dataframe,input)

    def test_form_dataframe_with_tuple(self):
        input=("light","mathematical","electronic")
        exp_result = pd.DataFrame([["1", "light"],["2", "mathematical"],["3", "electronic"]],columns=['qid','query'])
        result=pt.Utils.form_dataframe(input)
        self.assertTrue(exp_result.equals(result))

    # this also tests different index-like inputs, namely:
    # a String index location, an IndexRef, and an Index
    def test_one_term_query_correct_docid_and_score(self):
        JIR = pt.autoclass('org.terrier.querying.IndexRef')
        JIF = pt.autoclass('org.terrier.structures.IndexFactory')

        indexloc = self.here+"/fixtures/index/data.properties"
        jindexref = JIR.of(indexloc)
        jindex = JIF.of(jindexref)
        for indexSrc in (indexloc, jindexref, jindex):
            retr = pt.BatchRetrieve(indexSrc)
            result = retr.transform("light")
            exp_result = pt.Utils.parse_query_result(os.path.dirname(os.path.realpath(__file__))+"/fixtures/light_results")
            for index,row in result.iterrows():
                self.assertEqual(row['docno'], exp_result[index][0])
                self.assertAlmostEqual(row['score'], exp_result[index][1])
        jindex.close()

    def test_two_term_query_correct_qid_docid_score(self):
        JIR = pt.autoclass('org.terrier.querying.IndexRef')
        indexref = JIR.of(self.here+"/fixtures/index/data.properties")
        retr = pt.BatchRetrieve(indexref)
        input=pd.DataFrame([["1", "Stability"],["2", "Generator"]],columns=['qid','query'])
        result = retr.transform(input)
        exp_result = pt.Utils.parse_res_file(os.path.dirname(os.path.realpath(__file__))+"/fixtures/two_queries_result")
        for index,row in result.iterrows():
            self.assertEqual(row['qid'], exp_result[index][0])
            self.assertEqual(row['docno'], exp_result[index][1])
            self.assertAlmostEqual(row['score'], exp_result[index][2])

        input=pd.DataFrame([[1, "Stability"],[2, "Generator"]],columns=['qid','query'])
        result = retr.transform(input)
        exp_result = pt.Utils.parse_res_file(os.path.dirname(os.path.realpath(__file__))+"/fixtures/two_queries_result")
        for index,row in result.iterrows():
            self.assertEqual(str(row['qid']), exp_result[index][0])
            self.assertEqual(row['docno'], exp_result[index][1])
            self.assertAlmostEqual(row['score'], exp_result[index][2])



if __name__ == "__main__":
    unittest.main()
