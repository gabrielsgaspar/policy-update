# Identification

## Causal or Descriptive Question

The first-stage question is predictive and associational: do issue priorities and policy proposals in supporter comments predict later M5S communication and formal political outputs, after accounting for prior party attention and external agenda controls?

A stronger causal interpretation is TBD and should not be adopted until timing, missingness, common-shock controls, and placebo tests are validated.

## Estimand

TBD. Candidate estimands include:

- the association between comment issue attention in issue-week `t` and M5S issue attention in later weeks;
- the relative hazard or probability that a comment-derived proposal appears in later M5S text;
- heterogeneity in these relationships by movement phase, issue, proposal specificity, comment repetition, and local information.

## Unit Of Observation

Candidate units:

- issue-week or issue-month;
- proposal-by-time interval;
- post-thread;
- text unit, such as comment, post, paragraph, or parliamentary output segment.

## Treatment / Key Regressor / Variation

Primary regressors are planned to include:

- comment issue attention;
- repeated proposal support by distinct hashed commenters;
- proposal specificity, local information, evidence use, mobilization request, stance, and novelty;
- movement phase indicators and interactions.

## Outcomes

Candidate outcomes:

- subsequent issue attention in Grillo/M5S posts;
- semantic closeness between prior comments/proposals and later party text;
- appearance of semantically similar proposals in posts, programs, or parliamentary outputs;
- explicit acknowledgements of readers, comments, emails, Meetup groups, or supporter proposals;
- M5S parliamentary questions, bills, motions, speeches, or amendments.

## Current Best Design

1. Build a pilot issue-week panel for 2005-2013.
2. Estimate lead-lag models with controls for prior party attention, original post topic, media/public agenda, comparison-party attention, elections, and event-calendar indicators.
3. Build a proposal-level event-history dataset for comment-derived proposals.
4. Test whether proposal features predict later candidate adoption in M5S text.
5. Use future-comment placebos, comparison-party outcomes, unrelated-issue placebos, and archive-completeness restrictions.

## Main Specification

```text
PartyAttention[i,t+k] = beta * CommentAttention[i,t]
                      + controls for prior party attention
                      + media/public agenda controls
                      + comparison-party attention
                      + election/event controls
                      + issue fixed effects
                      + time fixed effects
                      + error
```

Proposal adoption specification: TBD after proposal extraction and candidate-match validation.

## Identifying Assumption

For a causal reading, changes in comment attention or proposal support would need to be conditionally independent of unobserved shocks that also affect later M5S outputs, after controlling for prior party attention, media/public agenda, comparison-party attention, elections, events, and fixed effects. This assumption is strong and currently unproven.

## Threats

- Comments respond to posts rather than shape later posts.
- Common media or political shocks affect comments and party outputs.
- Archive missingness is correlated with issue, popularity, year, or site template.
- Commenter population differs from voters and may shift over time.
- M5S leadership may stage or selectively surface participation.
- LLM labels may vary across periods, templates, or issue categories.
- Proposal matching may generate false positives through generic language.

## Falsification / Placebo Tests

- Future comments should not predict past posts.
- Comment shocks should predict M5S outputs more than unrelated comparison-party outputs.
- Comment shocks on one issue should not predict unrelated issue outputs.
- Results should not be driven only by high-coverage archived threads.
- Results should be robust to excluding original post topic continuation windows.

## Robustness Checks

- Alternative issue taxonomies.
- Alternative lag windows.
- Archive completeness weights and restrictions.
- Separate estimates by movement phase.
- Separate estimates by source type.
- Human-validated proposal matches versus model-only candidate matches.
- Spam/duplicate filter sensitivity.

## Inference

- Clustering: TBD. Candidate levels include issue, week/month, post-thread, and source.
- Weights: TBD. Candidate weights include archive coverage and inverse missingness adjustments.
- Multiple testing: TBD. Needed if estimating many issue-specific or proposal-feature effects.

## Language Discipline

Current paper language should be:

- [ ] descriptive
- [x] predictive
- [x] associational
- [ ] causal

Rationale: the repository has not yet validated recoverability, timing, controls, or placebo tests.
