"""Vector architecture diagrams and a typed, curated timeline; no invented measurements."""
from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
import matplotlib.dates as mdates
from datetime import datetime,timezone
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
blue='#315d78';orange='#b87632';gray='#59636b';light='#eef3f6';dark='#263844'
meta=[]
def canvas(h):
 f,a=plt.subplots(figsize=(6.5,h));a.set(xlim=(0,10),ylim=(0,10));a.axis('off');return f,a
def box(a,x,y,w,h,s,kind='normal',fs=9):
 edge=orange if kind=='manual'else blue
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.06,rounding_size=0.08',linewidth=1,edgecolor=edge,facecolor='white'if kind=='manual'else light,linestyle='--'if kind=='manual'else'-'))
 a.text(x+w/2,y+h/2,s,ha='center',va='center',fontsize=fs,color=dark,linespacing=1.35)
def arrow(a,p,q,manual=False,curve=0):
 a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=10,lw=1,color=orange if manual else gray,linestyle='--'if manual else'-',connectionstyle=f'arc3,rad={curve}'))
def save(f,name,description,sources=[]):
 f.savefig(P/'figures'/f'{name}.pdf',bbox_inches='tight',pad_inches=.08)
 f.savefig(P/'figures'/f'{name}.svg',bbox_inches='tight',pad_inches=.08)
 plt.close(f);meta.append({'figure':name,'kind':'architecture_diagram' if name!='dual_timeline'else'curated_typed_timeline','description':description,'sources':[{'path':s,'sha256':hashlib.sha256((ROOT/s).read_bytes()).hexdigest()}for s in sources]})

f,a=canvas(4.2)
box(a,.2,8.2,2.9,1.25,'Platform collectors\nTelegram / selected platforms')
box(a,3.55,8.2,2.9,1.25,'Fixed Source Watch\nAllowlisted web captures')
box(a,6.9,8.2,2.9,1.25,'Local media archive\nFiles + source-post manifest')
box(a,.2,5.65,2.9,1.5,'Legacy information analysis\nNormalize / themes / copies\nGraphs / conditional nulls')
box(a,3.55,5.65,2.9,1.5,'Source ingest bridge\nSource / Artifact / Passage\nSQLite EvidenceLedger')
box(a,6.9,5.65,2.9,1.5,'Separate local video runner\nIndex / audio / frames\nCandidate OCR + ASR')
box(a,.2,2.8,2.9,1.6,'Typed analytical inputs\nClaims / event mentions\nLineage / supplied labels',kind='manual')
box(a,3.55,2.8,2.9,1.6,'Offline case runner\nRetrieval / timelines\nConflict / uncertainty')
box(a,6.9,2.8,2.9,1.6,'Report bundle + gates\nSupplied findings / results\nCitations / hashes / schemas')
box(a,3.55,.4,6.25,1.15,'Run receipts + unresolved queue + versioned outputs\nStructural checks do not establish semantic truth',fs=9)
for p,q,m in [((1.65,8.2),(1.65,7.15),False),((5,8.2),(5,7.15),False),((8.35,8.2),(8.35,7.15),False),((3.1,6.4),(3.55,6.4),True),((1.65,5.65),(1.65,4.4),True),((5,5.65),(5,4.4),False),((8.35,5.65),(8.35,4.4),True),((3.1,3.6),(3.55,3.6),False),((6.45,3.6),(6.9,3.6),True),((5,2.8),(5,1.55),False),((8.35,2.8),(8.35,1.55),False)]:arrow(a,p,q,m)
a.text(.2,.6,'Solid: implemented exchange\nDashed: separate / curated handoff',fontsize=8.5,color=gray)
save(f,'system_architecture','Actual subsystem boundaries; no universal automatic collector-to-finding integration.',['src/analysis/offline_case_runner.py','src/analysis/incident_orchestrator.py','src/analysis/source_ingest_bridge.py','src/analysis/video_pipeline_runner.py'])

f,a=canvas(3.6)
for x,s in [(.25,'Source\nURI / publisher'),(3.65,'Artifact\nCaptured bytes / SHA-256'),(7.05,'Passage\nText / locator')]:box(a,x,7.7,2.7,1.5,s)
arrow(a,(2.95,8.45),(3.65,8.45));arrow(a,(6.35,8.45),(7.05,8.45))
box(a,.25,4.1,2.7,1.7,'Claim / mention\nStatement + scope\nAssertion ≠ event')
box(a,3.65,4.1,2.7,1.7,'Evidence assessment\nRelation + rationale\nAcceptance provenance')
box(a,7.05,4.1,2.7,1.7,'Verification result\nScope + cutoff + state\nRetain unknown/conflict')
arrow(a,(8.4,7.7),(5,5.8));arrow(a,(2.95,4.95),(3.65,4.95));arrow(a,(6.35,4.95),(7.05,4.95))
arrow(a,(8.4,7.7),(1.6,5.8),manual=True,curve=.12)
box(a,.25,.7,4.3,1.65,'Source dependency families\nCopies may share one root\nUnknown linkage ≠ independence',kind='manual')
box(a,5.45,.7,4.3,1.65,'Superseding assessment / finding\nPreserve earlier record; validate references\nNo physical truth inferred from a valid ID')
arrow(a,(2.4,2.35),(5,4.1),manual=True);arrow(a,(8.4,4.1),(7.6,2.35))
a.text(.25,6.6,'Information lineage is supplied or inferred separately from byte identity.',fontsize=8.5,color=gray)
save(f,'evidence_provenance','Record relationships and limits. Findings are report objects, not a ledger kind.',['src/evidence_ledger.py','src/analysis/claim_verification.py','src/analysis/source_lineage.py'])

f,a=canvas(3.0)
box(a,.2,7.45,2.7,1.45,'IncidentSpec + budgets\nOptional collection execution')
box(a,3.65,7.45,2.7,1.45,'Fixed Source Watch\nCapture → bridge → ledger')
box(a,7.1,7.45,2.7,1.45,'Pretyped local inputs\nExplicit files + cutoff',kind='manual')
arrow(a,(2.9,8.17),(3.65,8.17));arrow(a,(8.45,7.45),(8.45,6.1))
box(a,.2,4.5,2.7,1.6,'Structural report gates\nReferences / hashes\nCutoffs / frozen controls')
box(a,3.65,4.5,2.7,1.6,'Offline analytical stages\nRetrieve / organize / summarize\nUnknowns remain explicit')
box(a,7.1,4.5,2.7,1.6,'Report input bundle\nFindings / assessments\nSeparately supplied',kind='manual')
arrow(a,(5,7.45),(5,6.1));arrow(a,(7.1,5.3),(6.35,5.3),manual=True);arrow(a,(3.65,5.3),(2.9,5.3))
box(a,.2,1.0,9.6,1.75,'Demonstrated boundary: scripted / integrated bounded workflow (levels 1–2)\nNo independent end-to-end incident benchmark (levels 3–4 unestablished)\nPassing structural gates does not validate retrieval entailment or physical event truth',fs=9)
arrow(a,(1.55,4.5),(1.55,2.75));arrow(a,(5,4.5),(5,2.75))
save(f,'analysis_workflow','Actual orchestrator/controller behavior and descriptive autonomy scale.',['src/analysis/incident_orchestrator.py','src/analysis/offline_case_runner.py','src/analysis/evaluation_harness.py'])

f,a=canvas(3.0)
for x,s in [(.2,'Local file + manifest\nHash / stat stability'),(3.65,'Probe + strict decode\nTechnical readability only'),(7.1,'Audio + sampled frames\nDerivative checksums')]:box(a,x,7.6,2.7,1.6,s)
arrow(a,(2.9,8.4),(3.65,8.4));arrow(a,(6.35,8.4),(7.1,8.4))
box(a,.2,4.1,2.7,1.7,'Perceptual candidates\npHash / dHash / alignment\nUncalibrated thresholds')
box(a,3.65,4.1,2.7,1.7,'Candidate text\nLocal OCR + ASR\nPreserve original segments')
box(a,7.1,4.1,2.7,1.7,'Correction sidecars\nAlternatives + uncertainty\nNo contextual word invention')
arrow(a,(8.45,7.6),(5,5.8));arrow(a,(8.45,7.6),(1.55,5.8),curve=.12);arrow(a,(6.35,4.95),(7.1,4.95))
box(a,.2,.75,9.6,1.7,'Independent contextual / acoustic / speaker / fact verification remains separate\nHistorical external Gemini pilot: 3 still frames from 1 clip; not integrated continuous video analysis',kind='manual',fs=9)
arrow(a,(1.55,4.1),(1.55,2.45),manual=True);arrow(a,(8.45,4.1),(8.45,2.45),manual=True)
save(f,'multimodal_pipeline','Local stages and unvalidated semantic handoff.',['src/media_pipeline.py','src/analysis/video_local_extract.py','src/analysis/video_text_extract.py','src/analysis/media_fingerprints.py'])

source='reports/event-reconstruction/physical_event_timeline_2026-11-09.json';d=json.loads((ROOT/source).read_text());physical=[e for e in d['events']if e['event_kind']=='physical'];comm=[e for e in d['events']if e['event_kind']=='communication']
fig,axs=plt.subplots(2,1,figsize=(6.5,3.7),sharex=True,gridspec_kw={'height_ratios':[1.1,1]},layout='constrained')
labelsP=['P1 Gathering mention','P2 Clash mention','P3 Arrival / blockade mention','P4 Smoke / flare mention','P5 Resolution mention'];labelsC=['C1 Police statement','C2 Telegram publication','C3 Investigation announcement','C4 Briefing publication','C5 Fire statement']
for i,e in enumerate(physical):
 t=e['event_time'];lo=datetime.fromisoformat(t['earliest_utc'].replace('Z','+00:00'));hi=datetime.fromisoformat(t['latest_utc'].replace('Z','+00:00'));axs[0].plot([lo,hi],[4-i,4-i],lw=5,color=orange,solid_capstyle='butt')
for i,e in enumerate(comm):axs[1].scatter(datetime.fromisoformat(e['publication_time_utc'].replace('Z','+00:00')),4-i,s=23,color=blue)
for ax,labels,title in zip(axs,[labelsP,labelsC],['Supplied physical-event intervals (all unresolved)','Communication publication times (not recording times)']):
 ax.set_yticks(range(5),labels[::-1],fontsize=8.5);ax.set_title(title,loc='left',fontsize=9.5,pad=7);ax.set_ylim(-.6,4.6);ax.grid(axis='x',alpha=.2);ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0)
axs[1].xaxis.set_major_locator(mdates.HourLocator(byhour=[0,12],tz=timezone.utc));axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%d Nov\n%H:%M',tz=timezone.utc));axs[1].set_xlabel('2026, UTC; assigned intervals are not independently validated bounds',fontsize=8.5)
save(fig,'dual_timeline','Direct plot of analyst-supplied intervals/publication times from frozen typed timeline. All10mentions unresolved, no event-truth claim.',[source])
(P/'data/figure_data').mkdir(exist_ok=True)
(P/'data/figure_data/system_figures.json').write_text(json.dumps({'baseline_commit':'f0e9d0d67422b0c286a2cb9e7d4e935a833a9533','figures':meta},indent=2)+'\n')
print('created',len(meta),'vector figures')
