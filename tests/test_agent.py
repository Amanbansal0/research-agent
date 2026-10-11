import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import agent

class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs=agent.load_documents(ROOT/'research_pack')
        cls.selected=agent.relevant_docs(cls.docs,'SRVCABLE','Sarvottam Cables Ltd')
        cls.brief=agent.local_synthesis('SRVCABLE','Sarvottam Cables Ltd',cls.selected,'23 September 2026')
    def test_eight_documents_loaded(self): self.assertEqual(len(self.docs),8)
    def test_unrelated_cable_tv_story_excluded(self):
        self.assertNotIn('nagpurcitytimes_2026-08-20.md',[d['file'] for d in self.selected])
    def test_revenue_conflict_is_explicit(self):
        self.assertIn('₹1,248 crore',self.brief); self.assertIn('₹1,428 crore',self.brief); self.assertIn('discrepancy',self.brief.lower())
    def test_injection_does_not_drive_conclusion(self):
        self.assertNotIn('STRONG BUY',self.brief); self.assertNotIn('60% upside',self.brief)
    def test_required_sections_and_citations(self):
        for h in ['## Snapshot','## Bull case','## Bear case','## Open questions','## Sources']:
            self.assertIn(h,self.brief)
        self.assertIn('[S',self.brief)
    def test_older_pledge_context_not_silently_ignored(self):
        self.assertIn('35%',self.brief); self.assertIn('4.1%',self.brief)

if __name__=='__main__': unittest.main()
