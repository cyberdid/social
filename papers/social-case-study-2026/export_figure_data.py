from pathlib import Path
import csv,json,hashlib,collections,datetime,subprocess
root=Path(__file__).resolve().parents[2];paper=root/'papers/social-case-study-2026';out=paper/'supplement';out.mkdir(exist_ok=True)
inputs={}
def rows(path):
 p=root/path;inputs[path]=hashlib.sha256(p.read_bytes()).hexdigest()
 with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def obj(path):
 p=root/path;inputs[path]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def write(name,fields,data):
 with (out/name).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
hours=collections.Counter()
for r in rows('reports/continuation_20261105/timeseries_10min_posts.csv'):
 h=datetime.datetime.fromisoformat(r['bin']).replace(minute=0,second=0,microsecond=0).isoformat();hours[h]+=sum(int(r[k]) for k in ['A','B','C','D','E','U'])
assert sum(hours.values())==1408
write('figure1_hourly_posts.csv',['hour_with_offset','relevant_posts'],[{'hour_with_offset':k,'relevant_posts':v} for k,v in sorted(hours.items())])
n=rows('reports/continuation_20261105/narratives_by_group.csv')
write('figure2_rule_matches.csv',['narrative','posts'],[{k:r[k] for k in ['narrative','posts']} for r in n])
c=obj('reports/evidence-verification/core_claims_verification_2026-11-09.json')['summary']
write('figure3_claim_status.csv',['status','claims'],[{'status':k,'claims':c[k]} for k in ['supported_within_scope','insufficient_evidence','refuted_within_scope']])
hist=collections.Counter(int(r['j0.6_w10']) for r in rows('reports/coordination-null-models-2026-11-08-lsh-audit/temporal_null_draws.csv') if r['model']=='channel_2h_slot_rotation');assert sum(hist.values())==9999
write('figure4_null_histogram.csv',['pairs_within_10min','draw_count'],[{'pairs_within_10min':k,'draw_count':v} for k,v in sorted(hist.items())])
a=obj('reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json');st=a['strata_summary']
fields=['stratum','clips','reference_words','error_words','macro_wer','micro_wer','recorded_quote_safe_flags']
write('figure5_asr_strata.csv',fields,[dict(zip(fields,[k,v['clip_count'],v['total_ref_words'],v['total_err_words'],v['macro_wer'],v['micro_wer'],v['quote_safe_count']])) for k,v in st.items()])
assert sum(x['first_pass_hypothesis']['word_errors']['ref_words'] for x in a['clips'])==415
assert sum(sum(x['first_pass_hypothesis']['word_errors'][k] for k in ['substitutions','deletions','insertions']) for x in a['clips'])==185
assert round(185/415,4)==a['overall_metrics']['micro_wer']
(out/'README.md').write_text('''# Aggregate figure data for the Social preprint

English and Ukrainian PDFs are parallel language editions of one study. This folder contains the machine-readable aggregate values for their five figures. It contains no comment text, account identifiers, personal profiles or raw media.

- Figure 1: observed hourly publication counts in the 1,408-record baseline, with explicit timestamp offset.
- Figure 2: overlapping lexical-rule matches, not validated stance/prevalence.
- Figure 3: 25 curated propositions; support is limited to each proposition's stated scope.
- Figure 4: histogram of 9,999 conditional null draws; observed count 134, mean 42.8680868, central 95% range 32–55; plus-one p=0.0001, Holm p=0.0016. Draws are not independent audience observations.
- Figure 5: discrepancies against supplied reference transcripts. Recorded quote_safe flags are project metadata, not independently audited human approvals.

This is an aggregate inspection supplement. It supports redrawing figures and checking totals, but does not enable independent reconstruction of the private corpus or rerunning all randomizations. Input SHA-256 values identify the repository artifacts used, without asserting their external truth. DOI metadata and corrections are stored in the adjacent audit directory.
''')
manifest={'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_sha256':inputs,'output_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.csv'))},'asr_arithmetic_check':{'reference_words':415,'word_errors':185,'micro_wer':185/415,'scope':'Arithmetic against stored supplied-reference error counts; not acoustic validation.'}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('exported five aggregate tables; ASR arithmetic 185/415 verified')
