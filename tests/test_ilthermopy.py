'''Unit tests for the ilthermopy package'''

import ilthermopy as ilt


class TestData:
    
    def test_properties(self):
        props = ilt.PropertyList()
        assert props
        assert props.prop2key['Activity']
    
    def test_entries(self):
        df = ilt.GetAllEntries()
        assert len(df) > 54000 # no distinct numbers due to possible updates
    
    def test_compounds(self):
        cmps = ilt.GetSavedCompounds().data
        assert len(cmps) > 4000


class TestSearch:
    
    def test_property_search(self):
        df = ilt.Search(n_compounds=3, prop='Activity', year=2010)
        assert len(df) > 0
    
    def test_retrieving_entry(self):
        df = ilt.Search(n_compounds=3, prop='Activity', year=2010)
        entries = [ilt.GetEntry(idx) for idx in df['id']]
        assert entries[0].components[0]
        assert entries[0].components[0].smiles


