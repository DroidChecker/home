from main import *

class Test2(AndroidCheck):

    
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() and not 
                  d(text="Settings").exists())
    @rule()
    def dataloss2(self):
        d.rotate('l')
        d.rotate('n')
        
        assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() 
# B = Test2()
setting = Setting(apk_path="OmniNotes-6.2.0alpha.apk", timeout=300)


