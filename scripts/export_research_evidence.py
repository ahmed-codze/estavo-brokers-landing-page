#!/usr/bin/env python3
# coding: utf-8
"""Export only reviewed aggregate facts and selected public source references."""
import argparse
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('research_root', type=Path, help='Local September 30 expanded research directory')
args=parser.parse_args()
root=Path(__file__).resolve().parent.parent
p=args.research_root
files={'coverage':'combined/coverage.json','archive_summary':'archives/summary.json','developer_summary':'private-primary/summary.json'}
values={k:json.loads((p/name).read_text()) for k,name in files.items()}
c=values['coverage'];a=values['archive_summary'];d=values['developer_summary']
assert c['records']==sum(c['by_category'].values())==2268
assert c['by_channel']['archives']==a['records']==346
assert c['by_channel']['private-primary']==d['observation_count']==1922
assert a['new_verified_archive_snapshots']==sum(a['new_archive_years'].values())==297
assert a['new_archive_price_area_pairs']==251
assert d['repeated_offer_groups']==188 and d['groups_area_type_consistent']==185
assert d['groups_with_view_changes']==37 and d['groups_with_status_changes']==56
assert d['hidden_inventory_rows']==475 and d['sold_inventory_rows']==461
assert c['economic_dates_assigned']==c['training_approved']==0
# Verify reported collection totals against underlying rows, not just summary files.
for channel,expected in c['by_channel'].items():
    rows=[json.loads(line) for line in (p/channel/'observations.jsonl').read_text().splitlines()]
    assert len(rows)==expected,(channel,len(rows),expected)
groups=[json.loads(line) for line in (p/'private-primary/repeated-offer-groups.jsonl').read_text().splitlines()]
assert len(groups)==188
assert sum(g['source_count']>=3 for g in groups)==154
assert sum(g['source_count']==6 for g in groups)==36
archive_rows=[json.loads(line) for line in (p/'archives/observations.jsonl').read_text().splitlines()]
assert len({r['listing_id'] for r in archive_rows if r.get('listing_id')})==212
selected={'redseaway-media-3662','redseaway-media-4147','redseaway-media-4257','redseaway-media-4397','redseaway-media-4459','tiba-golden-2023-05-price-list'}
ledger=[]
for line in (p/'private-primary/sources.jsonl').read_text().splitlines():
    s=json.loads(line)
    if s.get('source_id') in selected:
        ledger.append({'reference':s['source_id'],'url':s['url'],'sha256':s['sha256'],
                       'date_evidence_class':s.get('date_evidence_class'),
                       'meaning':'Source version reference, not a verified transaction or economic price date.'})
assert len(ledger)==6
result={'title':'Estavo Brokers — September 2026 property-price evidence summary', 'publisher':'Estavo Brokers',
        'collection_date':'2026-09-30','published_date':'2026-10-02',
        'scope':'One bounded additional research collection; excludes earlier collections. Counts are records, not unique properties or available inventory.',
        'records':c['records'],'by_category':c['by_category'],'by_channel':c['by_channel'],
        'archive':{'capture_year_counts':a['new_archive_years'],'snapshots':297,'portal_listing_ids':212,'with_explicit_currency':297,'with_usable_area':251,'repeated_listing_groups':74,'repeated_groups_with_changed_asking_price':0},
        'developer':{'observations':1922,'projects':7,'document_evidence_2019_2023':1310,'current_source_observations_2026':612,'recurring_offer_groups':188,'groups_in_at_least_three_versions':154,'groups_in_all_six_versions':36,'groups_area_type_consistent':185,'groups_changed_area':3,'groups_changed_view':37,'groups_changed_status':56,'hidden_inventory_rows':475,'sold_status_inventory_rows':461,'change_flags_overlap':True},
        'calculations':[{'name':'2014 share of archive snapshots','numerator':239,'denominator':297,'percent':round(239/297*100,1)}, {'name':'Archive snapshots with usable price/area/currency','numerator':251,'denominator':297,'percent':round(251/297*100,1)}],
        'limitations':['Not a representative Egyptian market sample or a national price index.','Asking prices and stored offers are not achieved transaction prices.','Physical property identity is unverified.','All economic price dates remain unassigned in the research export.','All training-approval flags remain false.','Source redistribution and model-training rights remain unverified; no source documents or raw rows are redistributed in this release.'],
        'input_integrity':[{'reference':key,'sha256':hashlib.sha256((p/path).read_bytes()).hexdigest()} for key,path in files.items()],
        'public_source_versions':ledger}
target=root/'guides/evidence/september-2026.json';target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Exported verified aggregate evidence; no raw records or contact data.')
