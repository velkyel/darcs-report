# darcs-report

usage:

append

    apply posthook python <path-to>/darcs-report.py email1 [email2, ..]
    apply run-posthook
    pull posthook python <path-to>/darcs-report.py email1 [email2, ..]
    pull run-posthook
    unpull posthook python <path-to>/darcs-report.py email1 [email2, ..]
    unpull run-posthook

into your <repo>/_darcs/prefs/defaults.

tested with darcs version 2.12.0 (release)
