# Cayman Islands: law history in git

The law of Cayman Islands as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change; picking a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | The Constitution of the Cayman Islands (Schedule 2 to the Constitution Order 2009) | 1 | As made by the Order of 10 June 2009: preamble, sections 1 to 129 (the Bill of Rights is Part I) |
| `constitution-order-2009/` | The Cayman Islands Constitution Order 2009 (SI 2009/1379): the Order itself | 1 | As made: articles 1 to 9 (citation, commencement, transitional provisions) and Schedule 1 (revocations) |
| `penal-code/` | The Penal Code | 5 | The 2018, 2019, 2022, 2024 and 2026 Revisions (sections 1 to 325 with their lettered sections), each dated from the commencement date the site gives |
| `companies-act/` | The Companies Act | 6 | The 2020, 2021, 2022, 2023, 2025 and 2026 Revisions (sections and schedules), each dated from the commencement date the site gives |
| `contracts-act/` | The Contracts Act (the Contracts Law) | 1 | The 1996 Revision (sections 1 to 17), dated from the gazette supplement of 28 October 1996 that published it |
| `sale-of-goods-act/` | The Sale of Goods Act (the Sale of Goods Law) | 1 | The 1997 Revision (sections 1 to 59), dated from the gazette supplement of 17 March 1997 that published it |
| `criminal-procedure-code/` | The Criminal Procedure Code | 3 | The 2019, 2021 and 2026 Revisions (sections and schedules), each dated from the commencement date the site gives |
| `evidence-act/` | The Evidence Act (the Evidence Law) | 3 | The 2018, 2019 and 2021 Revisions, each dated from the commencement date the site gives |
| `labour-act/` | The Labour Act (the Labour Law) | 2 | The 2011 and 2021 Revisions, each dated from the commencement date the site gives |
| `interpretation-act/` | The Interpretation Act (the Interpretation Law) | 1 | The 1995 Revision (sections 1 to 64), the current revision on the site, dated from its commencement on 20 March 1995 |

**Language.** English, the official language and the language of the source.

**Source.** The Cayman Islands Government's legislation site, https://legislation.gov.ky (Constitution, current: The Cayman Islands Constitution Order 2009, UKSI 1379/2009, PDF with text layer, original version as made), retrieved 29 October 2026.

## Dates

Each commit is dated at noon, America/Cayman. Each revision of the Penal Code, the Companies Act, the Criminal Procedure Code, the Evidence Act, the Labour Act and the Interpretation Act is dated from the commencement date shown on legislation.gov.ky's history table for that revision. The Constitution's one version is dated 10 June 2009, the day the Order was made. The Order came into force on a day the Governor appointed by proclamation, and Part I of the Constitution three years after that; the source gives neither day, so 10 June 2009 is the date of the oldest version available, not the commencement date.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@legislation-gov-ky.invalid`). Both versions are the oldest version available, credited to the publisher, with the Order named in the commit. The committer is always Lexifina.

## Limits

A first build. The Constitution is recorded as made in 2009 only: the Cayman Islands Constitution (Amendment) Orders 2016 (UKSI 780/2016) and 2020 (UKSI 1283/2020) change it and are not replayed here, so this is not the current text. The Penal Code (2018 to 2026) and the Companies Act (2020 to 2026) are recorded revision by revision: each revision is a consolidated text, and a changed section is credited to the revision that carries it, not to the individual amending Act. The Criminal Procedure Code (2019 to 2026), the Evidence Act (2018 to 2021) and the Labour Act (2011 and 2021) are recorded the same way. Earlier revisions (Penal Code 2017 and before, Companies Act 2018 and before, Criminal Procedure Code 2017 and before, Evidence Act 2011 and before, Labour Act 2007 and before) are not included. The Interpretation Act is the 1995 Revision only; its section 63 is kept as printed ("64. 63. No Law ..."). Part headings are mostly left out (a few remain inside the section before them). Footnotes and endnotes, and the table of legislation history, are left out. The Contracts Act (1996 Revision) and the Sale of Goods Act (1997 Revision) are the only versions online and are dated from their gazette supplements because the site gives no commencement date. There is no civil code or commercial code in Cayman law, which is common law: the Contracts Act, the Sale of Goods Act and the Companies Act are the nearest equivalents. The rest of Cayman law (other Acts, regulations) is not included.
