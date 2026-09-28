# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
**Name:** Hanny Payco  
**Corpus:** city_guides

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->
I built a RAG system based on the city_guides documents. The system answers questions about different places and towns in the region and provides information that can be useful when planning a visit. For example, it can answer questions about transportation, attractions, opening hours, accessibility, food, and other practical information. The answers are based on information retrieved from the city guides and include the source document.

## Chunking Strategy

**Chunk size:** Variable — one complete Markdown section (`##`) per chunk. When a document has an introduction, it is included with the first section. Before implementing the strategy, I found that the 84 `##` sections averaged 296 characters, with the longest at 691 characters. The final chunking strategy produced 84 chunks averaging 360 characters, with the longest at 887 characters.

**Overlap:** 0 characters of section content; the parent `#` heading is repeated in each chunk to preserve document context.

When I reviewed the documents, I realized that they have a specific structure, with Markdown headings that in most cases identify the place, town, or topic being discussed. Because of this, I decided not to use a fixed number of characters for the chunk size. Instead, I decided to use a variable size and divide the documents by their Markdown ## sections. I also noticed that some documents have the name of the town as the main # heading, so I decided not to overlap the section content, but to repeat the main heading in each chunk to preserve the document context.

At first, I decided to make the introduction paragraph a separate chunk. However, when I inspected the chunk examples, I realized that the introduction by itself sometimes did not provide enough specific information or identify the places it was referring to. Because of this, I changed the strategy and included the introduction with the first ## section instead.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.
```

Chunk 2  |  source: guide_corry_vale.md#5  |  produced by: chunker.py::split_documents
```
# Corry Vale

## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents
```
# Givens Mill

## Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.
```
Chunk 4  |  source: guide_kestrelford.md#4  |  produced by: chunker.py::split_documents
```
# Kestrelford

## Where to stay

Two inns on the square and a handful of rooms above the pubs. Booking ahead matters between May and September and not at all otherwise. There is no accommodation of any kind within four miles of the town in either direction.
```
Chunk 5  |  source: guide_pellew_sands.md#6  |  produced by: chunker.py::split_documents
```
# Pellew Sands

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```
<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->



## Sample Answer

I kept the top-k at 5 because when I reviewed the retrieved chunks for three of my test questions, the chunks containing the correct information were already included in the five retrieved results. I did not see evidence that changing the number of retrieved chunks was necessary.

I also reviewed the grounding instruction and tested it with one of my questions. The generated answer used only information supported by the retrieved chunks and named the source documents. Because I did not find evidence that the model was adding information outside the retrieved context, I decided to keep the grounding instruction unchanged.

 **Question:** 
 ```
 "Which town has a parking problem in summer?"
  (best distance 0.524, cutoff 0.65)
```
**Answer:**
```
Halden Bay experiences a parking problem in summer during July and August, when it becomes busy enough that the parking problem becomes the defining feature of the visit. 

Source: `guide_halden_bay.md` and `guide_seasons.md`

Sources retrieved: guide_corry_vale.md, guide_halden_bay.md, guide_kestrelford.md, guide_pellew_sands.md, guide_seasons.md

0 model calls this session, 1 served from cache
```
<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->



**My relevance cutoff:**
0.65

I chose a cutoff of 0.65 because the best distances for my in-corpus questions were between 0.3032 and 0.5239, while the out-of-corpus questions were between 0.8350 and 0.9968. I noticed that one of my in-corpus questions had a distance of 0.5239, and when I reviewed the retrieved chunk, it actually contained the answer. Because 0.5239 was relatively close to the original cutoff of 0.6, I decided to increase the cutoff to 0.65. This gives some additional margin for relevant questions while still keeping the cutoff well below the lowest out-of-corpus distance of 0.8350.



| Question | In corpus? | Best distance |
|---|---|---:|
| Before what time I need to go to Kestrelford's bakery to get some food? | Yes | 0.3032 |
| How many rail services are available on Sundays? | Yes | 0.4517 |
| Which town has a parking problem in summer? | Yes | 0.5239 |
| Is there public transportation in Corry Vale? | Yes | 0.3253 |
| What is the main event in Kestrelford on Saturday mornings? | Yes | 0.3922 |
| What is the capital of Mongolia? | No | 0.8463 |
| How do I change the oil in a diesel engine? | No | 0.9032 |
| Who won the 1994 World Cup? | No | 0.9968 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8350 |
| How do I write a for loop in Rust? | No | 0.8365 |

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->



## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
I used AI to help me translate my chunking strategy into Python. I had decided to use the ## Markdown sections
 as the chunk boundaries, repeat the main # heading to preserve context, and use no overlap between the section 
content. AI helped me organize the Python logic in split_documents() to implement this strategy. After running 
the code and inspecting the chunks, I noticed that keeping the introduction as a separate chunk sometimes did 
not provide enough context, so I changed the code to include the introduction with the first ## section.

**2.**
I used AI to help me analyze the relevance cutoff after I got the distances for the five in-corpus and five 
out-of-scope questions. I shared both groups of distances and asked where the cutoff could be placed and what 
could happen if the cutoff was too low or too high. AI helped me understand better that a cutoff that is too 
low could reject a question that the documents can answer, while a cutoff that is too high could allow a 
question that is not supported by the documents. Based on my results, I decided to use 0.65 because my highest 
in-corpus distance was 0.5239 and my lowest out-of-scope distance was 0.8350. I understand that this cutoff 
worked for my test questions, but it may not work perfectly for every future question.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | |
| 2. Every answer names a source | 5 of 5 | 4/5 | 5/5 | 4/5 | |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | |
| 4. Chunks identify the place and contain complete sentences | 5 of 5 | 5/5 | 5/5 | 5/5 | |
| 5. Every factual claim is supported by retrieved chunks | 5 of 5 | 5/5 | 5/5 | 5/5 | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Criterion 1 — Retrieved chunk contains the answer
Question: Which town has a parking problem in summer?

```
#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.5239     guide_halden_bay.md              # Halden Bay    ## When to go  June and September ar...
2   0.5364     guide_kestrelford.md             # Kestrelford    ## Getting around  Everything is wi...
3   0.6006     guide_corry_vale.md              # Corry Vale    ## When to go  May to September. Out...
4   0.6018     guide_pellew_sands.md            # Pellew Sands    ## When to go  June and September ...
5   0.6204     guide_seasons.md                 # When to visit the region    ## Summer, June to Aug...

Gate: best distance 0.524 is under the 0.65 cutoff
Produced by: app.py using store.py::search
```

```
## When to go

June and September are the sweet spot. July and August are busy enough that the parking problem becomes the defining feature of the visit. Winter is dramatic and largely closed. The coastal path is genuinely dangerous in high wind and gets shut.
Produced by: `chunker.py::split_documents`
```

### Criterion 2 — Every answer names a source
 How many rail services are available on Sundays? — run 1
"I do not have enough information to answer your question."
- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`

### Criterion 3 — Gate stops out-of-corpus questions
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.846 | refused |
| How do I change the oil in a diesel engine? | 0.903 | refused |
| Who won the 1994 World Cup? | 0.997 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.835 | refused |
| How do I write a for loop in Rust? | 0.836 | refused |
Produced by `run_eval.py::check_out_of_scope`

### Criterion 4 — Chunks identify the place and contain complete sentences
```
# Corry Vale

Corry Vale is not a town but a valley containing four villages strung along eleven miles of road. Visitors treat it as one destination and locals emphatically do not. The largest village has 900 people and the smallest has 140.

## Getting there

There is no public transport into the valley beyond a school bus that will carry passengers if there is room. Driving from Brightwater takes 35 minutes on a good road as far as the valley mouth and then 20 more on a poor one. Cycling in is a serious undertaking; the road climbs 400 metres in the first four miles.
```
Produced by: `chunker.py::split_documents`

### Criterion 5 — Every factual claim is supported by retrieved chunks

Question: What is the main event in Kestrelford on Saturday mornings? — Run 1

Generated answer:
The main event in Kestrelford on Saturday mornings is the market square, which has run continuously since the 1400s (guide_kestrelford.md and guide_eating.md).

Retrieved supporting chunk:
```
#Kestrelford
## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```
Generated by: `run_eval.py::main`
Retrieval: `store.py::search`


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | The target was at least 4 of 5 questions. The retrieved chunks contained the answer for 4 of 5 questions in all three runs. |
| 2 | Every answer names a source | MISSED | The target was 5 of 5. Run 1 scored 4/5, Run 2 scored 5/5, and Run 3 scored 4/5, so the target did not hold across all three runs. |
| 3 | Gate stops out-of-corpus questions | MET | The target was at least 4 of 5 out-of-corpus questions. The relevance gate refused all 5 out-of-corpus questions. |
| 4 | Chunks identify the place and contain complete sentences | MET | The target was 5 of 5 chunks meeting both requirements. All 5 chunks identified the place and contained complete sentences. |
| 5 | Every factual claim is supported by retrieved chunks | MET | The target was 5 of 5 questions. Every factual claim in the generated answers was supported by the retrieved chunks for all 5 questions in all three runs. |

## Diagnoses

### Criterion 2 — Every answer names a source

**Stage: Generation**

The Sunday rail question was the only question that caused Criterion 2 to miss. The retrieved context was the same in all three runs, but the generated responses were different. In Run 2, the refusal included the source documents, while in Runs 1 and 3, the model responded, "I do not have enough information to answer your question" without naming a source. Because the retrieval results did not change between runs but the source attribution in the generated response did, I traced this miss to the generation stage.

### Additional finding — Sunday rail retrieval

Criterion 1 was MET because its target was at least 4 of 5 questions and the system achieved 4/5 in all three runs. However, the Sunday rail question exposed a retrieval problem. The correct answer, "six on Sundays," is in the railway section of `guide_regional_transport.md`, but the retrieved chunk from that document was from the buses section instead. Therefore, the answer was not present in the retrieved context even though the correct source document appeared in the retrieval results.



<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

I made one change to the grounding instruction in `generate.py` to make the source requirement explicit when the model does not have enough information to answer a question.

Before: "If the documents don't cover the question, say you don't have enough information. Do not guess."
After: "If the documents don't cover the question, say you don't have enough information and name at least one document you checked. Do not guess."


**Why I picked it:**

I picked this change because Criterion 2 missed when the Sunday rail question generated refusals without consistently naming a source. My diagnosis traced this problem to the generation stage, so I made the source requirement explicit for refusal responses.


<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks identify the place and contain complete sentences | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Every factual claim is supported by retrieved chunks | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

Yes. The change improved Criterion 2 from 4/5, 5/5, and 4/5 before the improvement to 5/5 in all three runs after the improvement. In the new run, the Sunday rail question still could not be answered because the answer was not in the retrieved chunks, but all three refusal responses now named the documents that were checked. This changed Criterion 2 from MISSED to MET. The other four criteria kept the same verdicts.



## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

After the improvement, none of my five acceptance criteria are still missed. However, the evaluation showed two issues that I would still like to improve.

The first is the Sunday rail question. The correct answer, "six on Sundays," is in `guide_regional_transport.md`, but the chunk containing that answer was not included in the top five retrieved chunks. The system retrieved a different chunk from the same document instead. If I continued improving the system, I would focus on retrieval and test a change that could help the correct railway chunk rank higher.

The second issue appeared with the Kestrelford market question in the after run. In one of the three runs, the generated answer said "the market" instead of "the market square." Because the scorer expected the phrase "the market square," that run was marked as a failure even though the answer was still supported by the retrieved context. This showed me that the current scorer can be sensitive to small differences in the model's wording.

I stopped here because the improvement for this unit was focused on the Criterion 2 source attribution problem. I made one change based on that diagnosis and reran the full evaluation before making any additional changes.


## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

Knowing what I know now, I would make Criterion 1 stricter. My original target required the retrieved chunks to contain the answer for at least 4 of 5 test questions. The system achieved exactly 4/5 in all three runs, so the criterion was MET. However, the Sunday rail question consistently failed because the chunk containing the correct answer was not retrieved.

If I were writing this criterion again before testing, I would require the retrieved chunks to contain the answer for 5 of 5 questions. This would make the criterion more demanding and would not allow a consistent retrieval problem like the Sunday rail question to still meet the target.