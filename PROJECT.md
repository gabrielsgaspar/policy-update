# PROJECT.md

Last updated: 2026-05-13

## Working title

**From Voice to Policy: Do Digital Parties Learn from Their Supporters? Evidence from Beppe Grillo's Blog and the Five Star Movement**

## One-sentence summary

This project studies whether a new digital party used a party-owned online forum as a genuine organizational learning technology: did citizen feedback in Beppe Grillo's blog comments shape the issue agenda, policy language, campaign program, and parliamentary behavior of the Five Star Movement (M5S), and did that responsiveness change as the movement entered electoral and governing institutions?

## Big question

Digital platforms are often said to democratize politics by lowering the cost of participation, mobilization, and collective action. Yet it is not enough to show that citizens can speak online or that online movements can win elections. The central democratic question is whether online voice changes what parties do.

This project asks a broad question relevant to political economy, comparative politics, party politics, populism, and computational social science:

> **When citizens use a party-owned digital platform to express grievances, priorities, local information, and policy proposals, does the party learn from them?**

The empirical case is Beppe Grillo's blog and the emergence of M5S in Italy. The case is unusually powerful because the blog was not merely a media outlet. It was a central infrastructure for the movement's identity, mobilization, agenda formation, and relationship with supporters. It also spans a dramatic institutional trajectory: from blog-centered activism, to movement, to electoral party, to parliamentary force, to government participant.

## Why this matters

The project speaks to a core tension in modern democracy. Digital technologies may make political organizations more responsive by allowing them to observe citizens at high frequency and low cost. But the same technologies may also help leaders mobilize supporters while filtering, staging, or ignoring feedback. M5S is a paradigmatic case because it combined claims of direct participation with strong leader/platform control.

The paper should therefore not be framed narrowly as a study of Beppe Grillo's blog. It should be framed as a study of **digital representation and organizational learning**.

The broader contribution is to show whether digital parties are:

1. **Learning organizations** that convert online participation into agenda and policy change.
2. **Mobilization machines** that use online participation to recruit, energize, and legitimate supporters without real policy responsiveness.
3. **Selective responders** that learn from supporters only on some issues, at some times, and under some institutional incentives.

Any of these findings would be important. A positive result would document a concrete mechanism through which digital media transforms representation. A null or selective result would reveal the limits of platform-based participation and populist digital democracy.

## Core contribution

The project fills a gap between four major literatures.

### 1. Internet, media, and political economy

The literature shows that media technologies and internet access can change turnout, protest, party entry, polarization, and electoral outcomes. The key Italian anchor is Campante, Durante, and Sobbrio, "Politics 2.0," which studies broadband internet in Italy and argues that the internet initially reduced turnout but later helped new political entrepreneurs convert political exit back into voice. This project studies the next mechanism: **once the digital political entrepreneur exists, does the organization learn from citizen voice?**

### 2. Party responsiveness and representation

The classic responsiveness literature asks whether public opinion and voter priorities shape party behavior and policy. Much of this work observes preferences through polls or election returns and party response through manifestos, roll calls, or policy outputs. This project observes a much more direct and high-frequency information channel: the text that supporters supplied to a party-owned platform.

### 3. Politicians learning from online feedback

Recent work uses social media to study whether politicians follow citizen priorities or learn from likes, retweets, and other online feedback. This project extends that logic from individual politicians on general social media to a party-owned digital infrastructure during party formation and institutionalization.

### 4. Digital parties, populism, and M5S

The M5S literature has rich work on the movement's hybrid organization, online/offline structure, direct democracy claims, Rousseau, and platform politics. But we still lack a large-scale, validated, longitudinal measure of whether supporter text on the movement's core communication infrastructure shaped later agenda and policy. This project builds that measure.

## Main research questions

1. **Agenda learning:** Do issue priorities in blog comments predict subsequent issue attention in Grillo/M5S posts?
2. **Policy learning:** Do concrete proposals in comments later appear in blog posts, M5S programs, parliamentary bills, parliamentary questions, speeches, or local political activity?
3. **Selective responsiveness:** Which kinds of feedback are most likely to be adopted: repeated proposals, locally informed comments, deliberative comments, emotionally intense comments, comments from highly active participants, or comments aligned with the movement's existing identity?
4. **Institutionalization:** Does responsiveness change after key political transitions such as the launch of M5S, local electoral successes, the 2013 parliamentary breakthrough, or the 2018 entry into government?
5. **Supporters versus public:** Is M5S responding to its own online supporter base, to the broader electorate, to the media agenda, or to national events?
6. **Platform governance:** Do moderation, comment visibility, post structure, and platform migrations shape what kind of citizen voice becomes observable and politically usable?

## Main hypotheses

### H1: Agenda learning

Increases in issue attention in comments predict later increases in Grillo/M5S issue attention, conditional on prior party attention, media attention, election timing, and national events.

### H2: Proposal adoption

Concrete policy proposals in comments are more likely to appear later in party outputs when they are repeated by many distinct commenters, contain specific policy instruments, include local information or evidence, and fit M5S's existing identity.

### H3: Selective responsiveness

M5S is expected to be more responsive on issues where its early brand was flexible or supporter-driven, such as anti-corruption, transparency, public services, environmental policy, infrastructure, digital democracy, media criticism, and local governance. It may be less responsive where leaders already had strong prior positions or where supporters were divided.

### H4: Institutionalization

Responsiveness should change as M5S becomes electorally successful. The early blog may serve as a discovery mechanism, while later digital participation may become more plebiscitary, ratifying, or mobilizational.

### H5: Supporter responsiveness rather than voter responsiveness

The blog probably captures engaged supporters and activists, not the median voter. The paper should distinguish responsiveness to online supporters from responsiveness to the general electorate. This distinction is central to the theory.

## Empirical object

The empirical object is a longitudinal text network connecting:

1. **Inputs:** comments on Beppe Grillo's blog and related M5S online spaces.
2. **Intermediary party communication:** subsequent Grillo/M5S posts, calls to action, campaign messages, and platform materials.
3. **Formal political outputs:** electoral programs, parliamentary bills, parliamentary questions, speeches, motions, local programs, and official party documents.
4. **External controls:** national media agenda, Google Trends/search interest, other parties' outputs, elections, major political events, and institutional milestones.

## Scope

### In scope

- Beppe Grillo blog posts and comments, with priority on 2005-2018.
- Il Blog delle Stelle and archived/mirrored comment pages where relevant.
- Wayback Machine captures of Beppe Grillo/M5S domains.
- Official M5S programs, candidate materials, campaign materials, and platform outputs.
- Parliamentary outputs from the Chamber of Deputies and Senate.
- Election results, especially municipality-level outcomes where possible.
- Comparison texts from other Italian parties and from the broader media agenda.
- LLM and ML measurement of issues, proposals, stance, deliberative quality, semantic similarity, and adoption.
- Validation against human-coded labels.
- Reproducible local data architecture and code pipeline.

### Out of scope for the first paper

- A complete normative evaluation of M5S in government.
- Identifying private individuals behind comments.
- Inferring causal effects of individual comments on individual leaders without supporting evidence.
- Private or non-public data collection.
- Full cross-national comparison with Podemos, Pirate Parties, La France Insoumise, or other digital parties. These are promising extensions, not first-paper requirements.
- A general history of Italian populism unless it directly supports the empirical design.

## Periodization

The project should define historical phases before analysis and then test robustness to alternative cutoffs.

Suggested phases:

1. **Blog formation and pre-party activism, 2005-2007.** The blog grows as a counter-information and mobilization space.
2. **V-Day and proto-movement phase, 2007-2009.** Blog-linked mobilization becomes more explicitly political.
3. **Party launch and local expansion, 2009-2012.** M5S becomes an electoral vehicle.
4. **Parliamentary entry, 2013-2017.** M5S becomes a major parliamentary actor.
5. **Government/institutional phase, 2018-2021.** M5S enters government and faces stronger institutional constraints.
6. **Post-Rousseau/reorganization phase, 2021 onward.** Useful for extension, but probably not central to the first paper.

The first paper should prioritize 2005-2018, with a pilot focused on 2005-2013.

## Main outcomes

### 1. Issue attention

For each issue and week/month, measure the share of text in comments, posts, party outputs, and comparison corpora devoted to the issue.

### 2. Semantic responsiveness

Measure whether later party text becomes closer in embedding space to prior comment text, within the same issue and time window.

### 3. Proposal adoption

Extract concrete proposals from comments and test whether semantically similar proposals later appear in party posts, programs, or parliamentary outputs.

### 4. Explicit acknowledgement

Detect cases where Grillo/M5S explicitly references readers, emails, comments, Meetup groups, or supporter proposals.

### 5. Institutional behavior

Link comment/proposal streams to parliamentary questions, bills, motions, amendments, speeches, or local policy documents.

## Empirical strategy

### A. Issue-week panel

Create an issue-by-week panel:

```text
PartyAttention[i,t+k] = beta * CommentAttention[i,t]
                       + controls for prior party attention
                       + media attention
                       + other-party attention
                       + election/event controls
                       + issue fixed effects
                       + time fixed effects
                       + error
```

The key question is whether comment attention predicts future M5S attention after controlling for confounders.

### B. Proposal-level event history

Create a proposal-level dataset where proposals extracted from comments are followed over time. The outcome is whether and when a semantically similar proposal appears in later party outputs.

```text
Adoption[p,t+k] = f(comment support, proposal specificity, local information,
                    deliberative quality, sentiment, novelty, issue alignment,
                    movement phase, media attention)
```

### C. Lead-lag and placebo tests

- Future comments should not predict past posts.
- M5S comment shocks should predict M5S outputs more than outputs by unrelated parties.
- Comment shocks on one issue should not predict unrelated issue outputs.
- Highly archived threads should not drive all results.

### D. Comparison groups

Use three comparison groups:

1. Other Italian parties' programs, websites, and parliamentary outputs.
2. National media and public agenda measures.
3. M5S itself over time, comparing the movement phase to the parliamentary/government phases.

### E. Institutionalization tests

Estimate whether the comment-output relationship changes around major transitions, especially 2009, 2013, and 2018. The 2013 parliamentary entry is likely the cleanest first break.

## ML and LLM measurement strategy

LLMs and ML are central to the project but should be used as measurement tools with validation, not as substitutes for research design.

### Tasks for ML/LLMs

1. **Issue classification:** classify posts and comments into Comparative Agendas Project categories, Manifesto Project categories, and M5S-specific subcategories.
2. **Policy proposal extraction:** identify whether a comment contains a concrete policy proposal and extract the proposal into structured fields.
3. **Stance detection:** classify support/opposition toward issues and policies.
4. **Deliberative quality:** measure whether a comment includes evidence, reasoning, local information, or constructive engagement.
5. **Semantic matching:** link comment proposals to later party outputs using embeddings and retrieval.
6. **Spam and low-quality text detection:** filter automated spam, link farms, duplicate content, and irrelevant comments.
7. **Named-entity and geography extraction:** identify places, institutions, policies, politicians, companies, and local references.

### Example proposal extraction schema

```json
{
  "contains_policy_proposal": true,
  "issue_major": "transportation",
  "issue_subcategory": "high_speed_rail",
  "proposal_summary": "halt or revise the high-speed rail project",
  "policy_instrument": "cancellation_or_moratorium",
  "target_level": "national_government",
  "stance": "opposed",
  "specificity_1_to_5": 4,
  "uses_evidence": true,
  "contains_local_information": true,
  "contains_mobilization_request": false,
  "confidence_0_to_1": 0.86
}
```

### Validation requirements

- Build a human-coded gold standard stratified by year, issue, post popularity, and platform/source.
- Report accuracy, precision, recall, F1, calibration, and confusion matrices.
- Validate separately by historical phase because rhetoric and templates may change over time.
- Use active learning to focus human coding on ambiguous or rare proposal types.
- Benchmark at least one open-weight model for replicability and one stronger model for measurement quality.
- Keep model version, prompt version, temperature, input text, output JSON, and validation status in the database.

## What would make the paper top-tier

The paper needs to do more than describe online participation. It should deliver:

1. **A new dataset** linking citizen input to party communication and formal outputs over time.
2. **A general theory** of digital parties as possible learning organizations.
3. **A credible empirical design** that separates supporter feedback from common shocks and media trends.
4. **Validated text measurement** using ML/LLMs with human audits.
5. **A politically important finding** about whether digital participation changes representation or mainly legitimates leader-driven mobilization.
6. **Reusable methods** for studying feedback-to-policy pipelines in other parties and movements.

## Expected paper structure

1. Introduction: digital voice and the problem of organizational learning.
2. Theory: digital parties as learning organizations versus mobilization machines.
3. Case: Beppe Grillo's blog and the institutionalization of M5S.
4. Data: posts, comments, archived pages, party outputs, parliamentary outputs, controls.
5. Measurement: LLM/ML extraction, validation, issue taxonomy, proposal matching.
6. Empirical design: issue-week panel, proposal-level adoption, comparison groups, institutionalization breaks.
7. Results: agenda learning, proposal adoption, selective responsiveness, institutionalization.
8. Robustness: media controls, other-party placebos, lead-lag tests, archive completeness, alternative taxonomies.
9. Implications: digital representation, party responsiveness, populism, and political economy of the internet.
10. Data/method appendix.

## Must-cite literature anchors

This is the initial must-cite map. It should be expanded into a proper bibliography later.

### Representation and party responsiveness

- Page, Benjamin I., and Robert Y. Shapiro. 1983. "Effects of Public Opinion on Policy." American Political Science Review. https://www.jstor.org/stable/1956018
- Stimson, James A., Michael B. MacKuen, and Robert S. Erikson. 1995. "Dynamic Representation." American Political Science Review.
- Soroka, Stuart, and Christopher Wlezien. Work on thermostatic representation.
- Adams, James, and coauthors. Work on party policy shifts and public opinion.
- Kluver, Heike, and Jae-Jae Spoon. 2016. "Who Responds? Voters, Parties and Issue Attention." British Journal of Political Science. https://www.cambridge.org/core/journals/british-journal-of-political-science/article/who-responds-voters-parties-and-issue-attention/B0FE670EF39AD2275D423F15CF5ABA39

### Internet, media, and political economy

- DellaVigna, Stefano, and Ethan Kaplan. 2007. "The Fox News Effect."
- Falck, Oliver, Robert Gold, and Stephan Heblich. 2014. "E-lections: Voting Behavior and the Internet."
- Campante, Filipe, Ruben Durante, and Francesco Sobbrio. 2018. "Politics 2.0: The Multifaceted Effect of Broadband Internet on Political Participation." Journal of the European Economic Association. https://www.nber.org/papers/w19029
- Durante, Ruben, Paolo Pinotti, and Andrea Tesei. 2019. "The Political Legacy of Entertainment TV."
- Enikolopov, Ruben, Alexey Makarin, and Maria Petrova. 2020. "Social Media and Protest Participation."
- Fujiwara, Thomas, Karsten Muller, and Carlo Schwarz. Work on social media and elections.

### Online feedback and agenda setting

- Barbera, Pablo, Andreu Casas, Jonathan Nagler, Patrick J. Egan, Richard Bonneau, John T. Jost, and Joshua A. Tucker. 2019. "Who Leads? Who Follows? Measuring Issue Attention and Agenda Setting by Legislators and the Mass Public Using Social Media Data." American Political Science Review. https://www.cambridge.org/core/journals/american-political-science-review/article/who-leads-who-follows-measuring-issue-attention-and-agenda-setting-by-legislators-and-the-mass-public-using-social-media-data/D855849CE288A241529E9EC2E4FBD3A8
- Gallego, Aina, Nikolas B. Scholl, and Gael Le Mens. 2024. "How Politicians Learn from Citizens' Feedback: The Case of Gender on Twitter." American Journal of Political Science. https://onlinelibrary.wiley.com/doi/pdf/10.1111/ajps.12772

### M5S, digital parties, and platform politics

- Bordignon, Fabio, and Luigi Ceccarini. 2013. "Five Stars and a Cricket: Beppe Grillo Shakes Italian Politics." South European Society and Politics. https://www.democraziapura.it/wp-content/uploads/2013/09/2013-Bordignon-Ceccarini.pdf
- Mosca, Lorenzo, Cristian Vaccari, and Augusto Valeriani. Work on M5S as an internet-fuelled party.
- Tronconi, Filippo, ed. Work on Beppe Grillo's Five Star Movement.
- Gerbaudo, Paolo. 2019. The Digital Party.
- Deseriis, Marco. Work on Rousseau and direct parliamentarianism.
- Bailo/related Lex Eletti work on platform politics and law-making in M5S. https://onlinelibrary.wiley.com/doi/epdf/10.1111/spsr.12613

### Text as data and LLM measurement

- Grimmer, Justin, and Brandon M. Stewart. 2013. "Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts." Political Analysis. https://www.jstor.org/stable/24572662
- Gentzkow, Matthew, Bryan Kelly, and Matt Taddy. 2019. "Text as Data." Journal of Economic Literature. https://www.aeaweb.org/articles?id=10.1257/jel.20181020
- Manifesto Project / MARPOR methods and corpus. https://manifesto-project.wzb.eu/
- Comparative Agendas Project methods and taxonomy. https://www.comparativeagendas.net/
- Recent work on LLMs for political text classification, scaling, and validation.

## Key risks

### Risk 1: missing or incomplete comments

Old comments may be missing from current pages or unevenly preserved by the Wayback Machine. The project must measure archive completeness and avoid treating missingness as random.

Mitigation: use multiple sources, including current Beppe Grillo pages, Il Blog delle Stelle, Wayback CDX, archived Internet Archive items, and page-level comment-count checks.

### Risk 2: comments follow posts rather than shape them

Because comments are replies to posts, apparent responsiveness may reflect continued attention to an issue already chosen by Grillo.

Mitigation: focus on novel proposals inside comments, use lag structures, control for original post topic, compare within-issue language shifts, and test future/past placebos.

### Risk 3: common shocks

Comments and party posts may both respond to the same media event.

Mitigation: include media agenda controls, Google Trends, other-party outputs, event calendars, and placebo outcomes.

### Risk 4: commenters are not representative voters

Blog commenters are likely activists and supporters.

Mitigation: frame the project as responsiveness to organized digital supporters, then compare to broader public signals.

### Risk 5: LLM measurement error

LLM classifications may be unstable across years, topics, and rhetorical styles.

Mitigation: human-coded validation, active learning, multiple models, prompt/version tracking, and conservative reporting.

## Initial success criteria

The pilot is successful if we can show:

1. A meaningful number of posts and comment threads can be recovered for 2005-2013.
2. Comments have reliable timestamps or at least recoverable ordering and post dates.
3. We can classify issues and extract proposals with acceptable human-validated precision.
4. Comment issue/proposal signals have predictive structure beyond the original post topic.
5. We can link at least some comment-derived proposals to later M5S posts, programs, or parliamentary outputs.

## First-paper claim to aim for

The strongest first paper should aim to adjudicate this claim:

> Digital parties are not merely low-cost mobilizers. They can be low-cost learning organizations, but their responsiveness to online supporters is selective and changes as they institutionalize.

The empirical contribution is to show, using the Beppe Grillo/M5S case, whether the digital voice of supporters was converted into agenda and policy, or whether participation mainly served mobilization and legitimation.
