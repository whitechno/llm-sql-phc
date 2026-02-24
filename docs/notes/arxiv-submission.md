# Submitting to arXiv

**arXiv is not peer-reviewed.** It is a "preprint server," which means it
functions as a digital repository where researchers can share their work
instantly before it undergoes the traditional (and often slow) peer-review
process at a formal journal or conference.

### How it Works

While there isn't a peer-review process, it isn't "wild west" for any random
PDF. arXiv uses a two-step gatekeeping system:
1. **Moderation:** Humans and automated tools check that the submission is
   actually "scientific" and "topical." They look for offensive content,
   plagiarism, or papers that are clearly not academic (e.g., "proofs" of
   complex theorems using high-school algebra).
2. **Endorsement:** New authors usually need to be "endorsed" by an established
   researcher in their field before they can post. If you're at a major
   university, this often happens automatically.

---

### The "Why" Behind arXiv

Researchers use arXiv for several strategic reasons:

* **Speed (The "Early Game"):** Traditional peer review can take 6 months to 2
  years. In fast-moving fields like Artificial Intelligence, a paper can be
  obsolete by the time a journal prints it. arXiv gets it out in 24 hours.
* **Timestamping:** It establishes "priority." By posting to arXiv, you prove
  you had the idea on a specific date, preventing others from "scooping" your
  work while it sits in a reviewer's inbox.
* **Open Access:** Many prestigious journals are behind expensive paywalls.
  arXiv ensures that anyone—from a student in a developing country to an
  independent researcher—can read the work for free.
* **Feedback:** Authors often post "Version 1" to get comments from the global
  community, which they then use to improve the paper before submitting the
  "final" version to a peer-reviewed journal.

### Comparison at a Glance

| Feature             | arXiv (Preprint)              | Traditional Journal             |
|:--------------------|:------------------------------|:--------------------------------|
| **Peer Review**     | No                            | Yes                             |
| **Speed**           | Instant (approx. 1 day)       | Slow (months to years)          |
| **Cost to Read**    | Free                          | Often requires subscription     |
| **Quality Control** | Basic moderation              | Intense scrutiny by experts     |
| **Finality**        | Can be updated (V1, V2, etc.) | Usually the "Version of Record" |

> **Pro Tip:** When you see an arXiv paper, look for a note that says "Accepted
> to [Journal Name]" or "Published in [Conference]." Many authors update their
> arXiv page once the paper has actually passed peer review elsewhere.

Tech Notes
----------
Yes, there is an efficient algorithm for this problem. This is the Maximum
Weight Matching problem, specifically for finding a maximum weight matching in a
general graph. It can be solved efficiently using Edmond's Blossom Algorithm
(also known as the Edmonds-Gallai decomposition), which runs in polynomial time
`O(n³)` or `O(n²m)` depending on the implementation, where `n` is the number of
nodes and `m` is the number of edges.
