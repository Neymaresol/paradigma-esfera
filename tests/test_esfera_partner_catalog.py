"""Regression tests for multi-partner catalog, without live outbound traffic."""
import unittest
from esfera_partner_catalog import normalize_offer, approved_catalog

class PartnerCatalogTests(unittest.TestCase):
    def test_valid_authorized_offer(self):
        item = {"partner":"hotmart","affiliate_url":"https://go.hotmart.com/G108129576P","title":"Curso autorizado","external_id":"p1","affiliate_authorized":True,"attribution_verified":True}
        self.assertEqual(normalize_offer(item)["external_id"], "p1")
        self.assertEqual(len(approved_catalog([item,item])), 1)

    def test_fail_closed_without_evidence(self):
        base = {"partner":"shopee","affiliate_url":"https://s.shopee.com.br/example","title":"Produto","external_id":"s1"}
        self.assertIsNone(normalize_offer(base))
        self.assertIsNone(normalize_offer({**base,"affiliate_authorized":True}))

    def test_reject_untrusted_destinations(self):
        base = {"partner":"amazon","title":"Produto","external_id":"a1","affiliate_authorized":True,"attribution_verified":True}
        for url in ("http://amazon.com.br/x","https://amazon.com.br.evil.example/x","https://evil.example/x","https://user:pass@amazon.com.br/x","https://amazon.com.br:8080/x"):
            with self.subTest(url=url):
                self.assertIsNone(normalize_offer({**base,"affiliate_url":url}))

if __name__ == "__main__":
    unittest.main()
