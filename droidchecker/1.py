from main import *

class Test1(AndroidCheck):


    @initialize()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() and not 
                  d(text="Settings").exists())
    @rule()
    def dataloss1(self):
        d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").click()
        d.rotate('l')
        d.rotate('n')
        
        
        assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() 
# A = Test1()
setting = Setting(apk_path="OmniNotes-6.2.0alpha.apk", timeout=300)



