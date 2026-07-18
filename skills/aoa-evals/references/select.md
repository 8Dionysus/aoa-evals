# Select a central eval

## Required input

Require one bounded proof question, object under evaluation, claim class,
acceptance target, and known evidence or comparison posture. Return
`blocked_missing_input` rather than inventing a missing material field.

## Procedure

1. Classify the disputed inference before searching:

   | Disputed inference | Claim class |
   | --- | --- |
   | one true local check or path signal is widened into an overall outcome | outcome-vs-path separation |
   | executed, skipped, blocked, or inferential checks are reported falsely | verification truthfulness |
   | full scope, verification, and reporting workflow is the question | composite bounded workflow |
   | requested and executed scope differ | scope alignment |
   | tool order, proportionality, omissions, or churn are the question | tool trajectory |
   | a checkpointed inquiry cannot honestly restart | long-horizon restart fidelity |

2. Normalize the claim class and object into three to eight short English terms.
   Start with the literal semantic terms of the chosen class from the table:
   for example, `outcome path separation`, `verification truthfulness`, or
   `scope alignment`. Add only material object terms after them. Do not replace
   the class terms with contextual nouns such as `local`, `validator`, `long`,
   `goal`, or `proof`, and do not use repository or expected bundle names.
3. Run exactly one bounded shortlist:

   ```text
   python <bundle_dir>/scripts/eval_contract_packet.py catalog \
     --query "<claim terms>" --limit 8
   ```

   First decide whether any returned card covers the required object and claim
   class. If so, choose one candidate and then one nearest alternative from
   that candidate's `source_neighbor_hints`; consider a lower-ranked lexical
   card only when the source hints do not cover the competing claim. Scores,
   matched terms, and hints route inspection but never establish fit.
4. Only when the result is `no_match` or lacks the required object class, make
   one fallback call:

   ```text
   python <bundle_dir>/scripts/eval_contract_packet.py catalog
   ```

   Ignore neighbor hints from an inapplicable card until after this fallback.
   Do not issue a second lexical query. Do not scan the eval tree or read
   `EVAL_SELECTION.md` unless chooser drift is itself the task.
5. Fetch the direct owner contracts for the candidate and nearest alternative:

   ```text
   python <bundle_dir>/scripts/eval_contract_packet.py contracts \
     --name <candidate> --name <neighbor>
   ```

   Pass exactly the candidate and one nearest alternative. Use the returned
   source manifest and source sections. Expand a source file only if the packet
   explicitly lacks a material field.
6. Compare object, bounded claim, trigger boundary, maturity, baseline, inputs,
   execution/report contract, blind spots, owner, and proof ceiling. Reject the
   nearest tempting alternative explicitly.
7. Return `exact_fit`, `partial_fit`, or `no_fit`. Do not execute an eval,
   scaffold a new one, change maturity, or mutate an owner surface.

## Claim limit

Selection proves only that one inspected source contract is the strongest
bounded fit among the compared candidates. It does not prove the claim,
execution, report, general agent reliability, or catalog completeness.
