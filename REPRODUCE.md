# How this repository was made (Cayman Islands)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Cayman Islands Legislation, Constitution (current) | <https://legislation.gov.ky/cms/legislation/constitution/current.html> | 2026-10-29 | Official legislation; the PDF carries no licence statement. |
| Cayman Islands Legislation, current Acts by title (Law Revision PDFs) | <https://legislation.gov.ky/cms/legislation/current/by-title.html> | 2026-10-30 | Official legislation; the PDFs carry no licence statement. |
| Cayman Islands Legislation: The Criminal Procedure Code, Law Revisions 2019, 2021, 2026 | <https://legislation.gov.ky/cms/images/LEGISLATION/PRINCIPAL/1975/1975-0013/1975-0013_2026 Revision.pdf> | 2026-10-30 | Official legislation; the PDFs carry no licence statement. |
| Cayman Islands Legislation: The Evidence Act (the Evidence Law), Law Revisions 2018, 2019, 2021 | <https://legislation.gov.ky/cms/images/LEGISLATION/PRINCIPAL/1978/1978-0013/1978-0013_2021 Revision.pdf> | 2026-10-30 | Official legislation; the PDFs carry no licence statement. |
| Cayman Islands Legislation: The Labour Act (the Labour Law), Law Revisions 2011, 2021 | <https://legislation.gov.ky/cms/images/LEGISLATION/PRINCIPAL/1987/1987-0030/1987-0030_2021 Revision.pdf> | 2026-10-30 | Official legislation; the PDFs carry no licence statement. |
| Cayman Islands Legislation: The Interpretation Act (the Interpretation Law), Law Revisions 1995 | <https://legislation.gov.ky/cms/images/LEGISLATION/PRINCIPAL/1963/1963-0017/1963-0017_1995 Revision.pdf> | 2026-10-30 | Official legislation; the PDFs carry no licence statement. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | The Constitution of the Cayman Islands (Schedule 2 to the Cayman Islands Constitution Order 2009) | 1 | 2009-06-10 to 2009-06-10 |
| `constitution-order-2009` | The Cayman Islands Constitution Order 2009: the Order itself (articles 1 to 9 and Schedule 1) | 1 | 2009-06-10 to 2009-06-10 |
| `penal-code` | The Penal Code | 5 | 2018-03-23 to 2026-02-10 |
| `companies-act` | The Companies Act | 6 | 2020-01-09 to 2026-01-29 |
| `contracts-act` | The Contracts Act (the Contracts Law) | 1 | 1996-10-28 to 1996-10-28 |
| `sale-of-goods-act` | The Sale of Goods Act (the Sale of Goods Law) | 1 | 1997-03-17 to 1997-03-17 |
| `criminal-procedure-code` | The Criminal Procedure Code | 3 | 2019-02-14 to 2026-02-03 |
| `evidence-act` | The Evidence Act (the Evidence Law) | 3 | 2018-03-16 to 2021-01-29 |
| `labour-act` | The Labour Act (the Labour Law) | 2 | 2011-11-07 to 2021-02-05 |
| `interpretation-act` | The Interpretation Act (the Interpretation Law) | 1 | 1995-03-20 to 1995-03-20 |

The build made 24 commits:

| Commits | Kind |
| ---: | --- |
| 10 | first version of an act |
| 14 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 23 laws in the record.
- 38 tags.

## Dates

Each commit is dated at noon (America/Cayman) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: The Cayman Islands Constitution Order 2009 came into force on the day the Governor appointed by proclamation (section 1(2)); this first build dates its one version from the day the Order was made, the source's own date. https://legislation.gov.ky/cms/legislation/constitution/current.html?download=55:the-cayman-islands-constitution-order-2009-uksi-1379-2009

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `bf4f2a38077cf50f8285a8e7f7ce06f7219a0172df7752a70b9806655b4d9618` (6022822 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

24 versions of 10 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 24 history commits and 38 tags (history tip `e4ec74197231d8f144360c2bcf83e6b72265450a`).

## Decisions made by hand

- Only the Constitution Order 2009 as made is recorded. The Cayman Islands Constitution (Amendment) Orders 2016 (UKSI 780/2016) and 2020 (UKSI 1283/2020) amend it; they are not replayed in this first build, so the text here is not the current Constitution.
- The version is dated 10 June 2009, the day the Order was made, because the source does not give the appointed day.
- Section headings come from the Order's own contents list; footnotes, page headers and the signature were left out.
- [statutes] The Penal Code: 5 Law Revision(s) from legislation.gov.ky (2018, 2019, 2022, 2024, 2026); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. The 2017 revision and earlier use other layouts and are not included.
- [statutes] The Companies Act: 6 Law Revision(s) from legislation.gov.ky (2020, 2021, 2022, 2023, 2025, 2026); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. Schedules are split into their own units where the schedule heading stands alone on a line; where it does not (for example Schedule 4, 6 and 7), the schedule stays inside the unit before it. Revisions before 2020 use other layouts and are not included.
- [statutes] The Contracts Act (the Contracts Law): 1 Law Revision(s) from legislation.gov.ky (1996); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. The site's history table gives no commencement date for the 1996 Revision, so it is dated from the gazette supplement that published it (28 October 1996). The Act is cited on the site as the Contracts Act; the 1996 text is titled the Contracts Law.
- [statutes] The Sale of Goods Act (the Sale of Goods Law): 1 Law Revision(s) from legislation.gov.ky (1997); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. The site's history table gives no commencement date for the 1997 Revision, so it is dated from the gazette supplement that published it (17 March 1997). The text is titled the Sale of Goods Law.
- [statutes] The Criminal Procedure Code: 3 Law Revision(s) from legislation.gov.ky (2019, 2021, 2026); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. Revisions before 2019 use other layouts and are not included.
- [statutes] The Evidence Act (the Evidence Law): 3 Law Revision(s) from legislation.gov.ky (2018, 2019, 2021); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. Revisions before 2018 are not included. The 2018 and 2019 Revisions are titled the Evidence Law.
- [statutes] The Labour Act (the Labour Law): 2 Law Revision(s) from legislation.gov.ky (2011, 2021); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. Revisions before 2011 are not included. The 2011 Revision is titled the Labour Law.
- [statutes] The Interpretation Act (the Interpretation Law): 1 Law Revision(s) from legislation.gov.ky (1995); each revision is a version dated from the commencement date the site gives, and changed sections are credited to that revision. The 1995 Revision is the current revision on the site, dated from the commencement date the site gives (20 March 1995); the site lists no amending Act against it. The text is titled the Interpretation Law. Section 63 is printed in the source as "64. 63. No Law ..."; it is kept as printed, under its own heading.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
- none
- none
- none
- none
