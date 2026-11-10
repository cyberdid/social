"""Publication experiment: typed synthetic inputs; no expected labels supplied to inference.
Run from repository root. Outputs are private by default and do not overwrite a run.
This is a smoke/reproducibility experiment, not a blind incident benchmark.
"""
from pathlib import Path
import json, tempfile, time, hashlib, resource
from src.analysis.offline_case_runner import run_offline_case

BASELINE='f0e9d0d67422b0c286a2cb9e7d4e935a833a9533'
P=Path(__file__).resolve().parent

def run():
    folder=Path(tempfile.mkdtemp(prefix='social-framework-smoke-'))
    spec=json.loads(Path('tests/fixtures/incident_spec.valid.json').read_text())
    spec['budgets']['max_queries_per_claim']=1
    claims=[{'claim_id':'smoke-claim','statement':'Люди перебували у будівлі.','scope':{'event':'synthetic'}}]
    passages=[{'passage_id':'smoke-p1','source_id':'synthetic-s1','captured_at_utc':'2026-11-01T20:00:00Z','text':'Люди перебували у будівлі.'},
              {'passage_id':'smoke-p2','source_id':'synthetic-s2','captured_at_utc':'2026-11-01T21:00:00Z','text':'Люди не перебували у будівлі.'}]
    mentions=[{'event_mention_id':'smoke-event','event_kind':'physical','predicate':'перебували','actor_entity_ids':['synthetic-people'],'object_entity_ids':[], 'place_id':'synthetic-building','time':None,'publication_time_utc':'2026-11-01T20:00:00Z','evidence_ids':['smoke-p1'],'cannot_link_event_mention_ids':[]}]
    inputs={}
    for name,rows in [('claims',claims),('passages',passages),('event_mentions',mentions)]:
        f=folder/(name+'.jsonl');f.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));inputs[name]=f
    trials=[]; stable=[]
    for index in range(3):
        out=folder/f'run-{index}'
        active_inputs=inputs if index==2 else {k:v for k,v in inputs.items() if k!='event_mentions'}
        start=time.perf_counter();run_offline_case(spec,out,git_commit=BASELINE,inputs=active_inputs,execute=True);elapsed=time.perf_counter()-start
        summary=json.loads((out/'case_summary.json').read_text())
        vr=[json.loads(s) for s in (out/'verification_results.jsonl').read_text().splitlines()]
        candidates=[json.loads(s) for s in (out/'evidence_candidates.jsonl').read_text().splitlines()]
        trials.append({'trial':index,'scenario':'dangling_event_reference_negative_control' if index==2 else 'retrieval_only_no_supplied_report','elapsed_seconds':elapsed,'analysis_status':summary['analysis_status'],'semantic_accuracy':summary['semantic_accuracy'],'stage_status':summary['stage_status'],'claim_statuses':[r['status'] for r in vr], 'accepted_support_assessments':sum(len(r['supporting_evidence_ids']) for r in vr),'candidates':sum(len(r['candidates']) for r in candidates),'report_exists':(out/'report').exists(),'evaluation':json.loads((out/'evaluation.json').read_text())})
        stable.append({'verification':vr,'candidate_ids':[[c.get('passage_id') for c in r['candidates']] for r in candidates]})
    result={'baseline_commit':BASELINE,'kind':'synthetic_typed_input_smoke_not_blind_validation','expected_labels_supplied':False,'network_calls':0,'model_calls':0,'trials':trials,'semantic_projections_repeat_equal':stable[0]==stable[1],'maximum_rss_kib_process':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitation':'No source discovery or raw claim extraction; no accepted assessments; report requires separately supplied report bundle. Physical event time remains unknown. Private temp run files intentionally not distributed.'}
    (P/'data/bounded_workflow_smoke.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
