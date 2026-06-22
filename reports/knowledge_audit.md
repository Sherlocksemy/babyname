# Knowledge Audit

Overall status: `warning`

## Datasets

| Dataset | Exists | Rows | Status | Warnings | Errors |
| --- | --- | ---: | --- | ---: | ---: |
| compliance_hanzi | True | 8105 | ok | 0 | 0 |
| char_base_info | True | 8105 | ok | 0 | 0 |
| char_semantic | True | 8105 | ok | 0 | 0 |
| kangxi_strokes | True | 8105 | ok | 0 | 0 |
| mandarin_pinyin | True | 8105 | ok | 0 | 0 |
| teochew_pronunciation | True | 30746 | ok | 0 | 0 |
| homophone_blacklist | True | 444 | ok | 0 | 0 |
| shijing | True | 305 | ok | 0 | 0 |
| chuci | True | 65 | ok | 0 | 0 |
| tang_poetry | True | 3000 | ok | 0 | 0 |
| song_ci | True | 3000 | ok | 0 | 0 |
| sishuwujing | True | 36 | ok | 0 | 0 |
| char_frequency | True | 180 | ok | 0 | 0 |
| top_names_blacklist | True | 500 | ok | 0 | 0 |
| bazi_rules | True | 5 | ok | 0 | 0 |
| wuge_rules | True | 3 | ok | 0 | 0 |
| zodiac_taboo | True | 12 | ok | 0 | 0 |

## Checks

### character_joinability
- status: `ok`

### teochew_variants
- status: `ok`

### culture_schema_and_name_candidates
- status: `ok`

### popularity_blacklist
- status: `ok`

### bazi_rules_operability
- status: `warning`
- warning: bazi_rules is mainly rule description; concrete calendar/stem-branch calculation tables are not present

### planned_layers
- status: `warning`
- warning: planned layer directory is missing: 07_surname_layer
- warning: planned layer directory is missing: 08_archetype_layer
- warning: planned layer directory is missing: 09_imagery_layer
- warning: planned layer directory is missing: 10_quality_rules_layer
