import unittest
from tld_parser import TLDParserTree, InvalidDomain

class TestTLDParserTree(unittest.TestCase):

    def setUp(self):
        self.tld_tree = TLDParserTree()
    
    def test_general_domains(self):
        domain_name, domain_tld = self.tld_tree.s('google.com')
        self.assertEqual(domain_name, 'google')
        self.assertEqual(domain_tld, 'com')

        domain_name, domain_tld = self.tld_tree.s('gardener.gg')
        self.assertEqual(domain_name, 'gardener')
        self.assertEqual(domain_tld, 'gg')

    def test_for_multi_level_tlds(self):
        domain_name, domain_tld = self.tld_tree.s('arjun.in')
        self.assertEqual(domain_name, 'arjun')
        self.assertEqual(domain_tld, 'in')

        domain_name, domain_tld = self.tld_tree.s('smvdu.ac.in')
        self.assertEqual(domain_name, 'smvdu')
        self.assertEqual(domain_tld, 'ac.in')

    def test_invalid_domain(self):
        with self.assertRaises(InvalidDomain):
            domain_name, domain_tld = self.tld_tree.s('fakedomain.faketld')
    
    def test_tlds_with_star(self):
        """
        Tests that the tlds such as *.bd are parsed correctly
        """
        domain_name, domain_tld = self.tld_tree.s('nestle.com.bd')
        self.assertEqual(domain_name, 'nestle')
        self.assertEqual(domain_tld, 'com.bd')

if __name__ == "__main__":
    unittest.main()