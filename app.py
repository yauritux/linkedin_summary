from taipy import Gui
from profile_stalker import summarize_linkedin

value="Yauri Attamimi"
summary=""
facts=None

page="""
### Linkedin Profile Stalker
<br/>
<|{value}|input|label="Profile Name"|>
<|button|label=Get Summary|on_action=get_summary_action|>
<br/>
**Summary:**
<br/>
...
<|{summary}|>
<br/>
**Interesting Facts:**
<br/>
...
<|{facts}|>
"""

def get_summary_action(state):    
    profile_summary, _ = summarize_linkedin(state.value)
    if hasattr(profile_summary, "summary") and hasattr(profile_summary, "facts"):
        state.summary = profile_summary.summary
        state.facts = profile_summary.facts

Gui(page=page).run(dark_mode=True)