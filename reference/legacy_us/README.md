# Legacy US reference data

These files are the original US tables (CSI MasterFormat, IBC 2021 egress,
ADA / ANSI A117.1). They are **not** used by the UK skills and must not be
cited on a UK project.

They are kept because the eval cases in `evals/` were written against a US
test project (Holabird Academy) and still score against them. When UK eval
cases exist, these files can be deleted.

UK replacements:

| US file | UK replacement |
|---|---|
| `csi_masterformat.yaml` | `../uniclass2015.yaml` |
| `ibc_egress_tables.yaml` | `../ad_b_vol2_means_of_escape.yaml` |
| `ada_requirements.yaml` | `../ad_m_vol2_access.yaml` |
| (none) | `../uk_regulations.yaml` — legislation, Approved Documents, BS 7671, standards, JCT/NEC4 forms |
