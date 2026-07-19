# Source notes

One section per source. Each entry was checked against a primary or authoritative
listing (publisher page, proceedings, arXiv, or DBLP) during preparation.
Verification date: 2026-07-17. A source appears in references.bib only after the
fields below were confirmed. No source is cited from a remembered title or an
abstract snippet alone.

Coverage map to the required topics:
- Agent and external memory: Graves 2016.
- Episodic and persistent memory: Blundell 2016, Pritzel 2017.
- Navigation and planning with memory: Mirowski 2017, Parisotto 2018, Savinov 2018.
- Reactive navigation, obstacle memory, failure recovery: Lumelsky 1987.
- Loop and cyclic behaviour, local minima and oscillation: Koren 1991.
- Grid-world evaluation: Sutton 2018, Chevalier-Boisvert 2023.
- Reproducibility and reporting in small agent experiments: Henderson 2018.

## lumelsky1987path
- Title: Path-planning strategies for a point mobile automaton moving amidst unknown obstacles of arbitrary shape
- Authors: Vladimir J. Lumelsky, Alexander A. Stepanov
- Year: 1987
- Venue: Algorithmica, volume 2, issue 1, pages 403-430 (peer reviewed)
- DOI: 10.1007/BF01840369
- Exact claim it supports: an agent with only local contact sensing plus memory of
  where it has already encountered obstacles can reach a goal or determine that
  the goal is unreachable. Foundational precedent for storing contact and failure
  information during reactive navigation.
- Where used: Introduction, Related Work.
- Peer reviewed: yes. Manually verified: yes.

## koren1991potential
- Title: Potential field methods and their inherent limitations for mobile robot navigation
- Authors: Yoram Koren, Johann Borenstein
- Year: 1991
- Venue: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pages 1398-1404 (peer reviewed)
- DOI: 10.1109/ROBOT.1991.131810
- Exact claim it supports: reactive local navigation methods are prone to local
  minima and to oscillations, including oscillatory motion in narrow passages.
  Supports the interpretation that the residual failure mode observed here,
  oscillation between valid cells, is a known limitation of local reactive
  policies rather than a failure of memory.
- Where used: Discussion, Limitations, Related Work.
- Peer reviewed: yes. Manually verified: yes.

## sutton2018reinforcement
- Title: Reinforcement Learning: An Introduction, second edition
- Authors: Richard S. Sutton, Andrew G. Barto
- Year: 2018
- Venue: MIT Press (book), ISBN 9780262039246
- DOI: none (book); stable publisher page at mitpress.mit.edu
- Exact claim it supports: grid worlds are a standard, controlled testbed for
  sequential decision-making, and terms such as state, action, and episode are
  standard.
- Where used: Introduction, Methodology.
- Peer reviewed: editorially reviewed book. Manually verified: yes.

## chevalier2023minigrid
- Title: Minigrid & Miniworld: Modular & Customizable Reinforcement Learning Environments for Goal-Oriented Tasks
- Authors: Maxime Chevalier-Boisvert, Bolun Dai, Mark Towers, Rodrigo de Lazcano, Lucas Willems, Salem Lahlou, Suman Pal, Pablo Samuel Castro, Jordan Terry
- Year: 2023
- Venue: Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track (peer reviewed)
- DOI: none assigned by proceedings; arXiv:2306.13831; stable NeurIPS proceedings page
- Exact claim it supports: minimalistic, customizable grid-world environments are
  in wide use for controlled, goal-oriented agent evaluation.
- Where used: Introduction, Related Work.
- Peer reviewed: yes. Manually verified: yes.

## mirowski2017learning
- Title: Learning to Navigate in Complex Environments
- Authors: Piotr Mirowski, Razvan Pascanu, Fabio Viola, Hubert Soyer, Andrew J. Ballard, Andrea Banino, Misha Denil, Ross Goroshin, Laurent Sifre, Koray Kavukcuoglu, Dharshan Kumaran, Raia Hadsell
- Year: 2017
- Venue: International Conference on Learning Representations (ICLR) (peer reviewed)
- DOI: none; arXiv:1611.03673
- Exact claim it supports: navigation agents benefit from auxiliary memory-related
  signals, including a loop-closure prediction task, prior published result.
- Where used: Related Work.
- Peer reviewed: yes (conference). Manually verified: yes.

## parisotto2018neural
- Title: Neural Map: Structured Memory for Deep Reinforcement Learning
- Authors: Emilio Parisotto, Ruslan Salakhutdinov
- Year: 2018
- Venue: International Conference on Learning Representations (ICLR) (peer reviewed)
- DOI: none; arXiv:1702.08360
- Exact claim it supports: earlier deep RL agents often used memory limited to the
  last k frames, and a persistent structured spatial memory improves navigation,
  prior published result.
- Where used: Related Work.
- Peer reviewed: yes (conference). Manually verified: yes.

## savinov2018semi
- Title: Semi-parametric Topological Memory for Navigation
- Authors: Nikolay Savinov, Alexey Dosovitskiy, Vladlen Koltun
- Year: 2018
- Venue: International Conference on Learning Representations (ICLR) (peer reviewed)
- DOI: none; arXiv:1803.00653; DBLP conf/iclr/SavinovDK18
- Exact claim it supports: a memory of visited places, stored as a topological
  graph, supports goal-directed navigation, prior published result. Contrast to
  the state-action failure memory studied here.
- Where used: Related Work, Discussion.
- Peer reviewed: yes (conference). Manually verified: yes.

## blundell2016model
- Title: Model-Free Episodic Control
- Authors: Charles Blundell, Benigno Uria, Alexander Pritzel, Yazhe Li, Avraham Ruderman, Joel Z. Leibo, Jack Rae, Daan Wierstra, Demis Hassabis
- Year: 2016
- Venue: arXiv preprint (not peer reviewed)
- DOI: none; arXiv:1606.04460
- Exact claim it supports: a nonparametric episodic memory of past experience can
  guide action selection, prior reported result. Cited as a preprint.
- Where used: Related Work.
- Peer reviewed: no (preprint, labelled as such). Manually verified: yes.

## pritzel2017neural
- Title: Neural Episodic Control
- Authors: Alexander Pritzel, Benigno Uria, Sriram Srinivasan, Adria Puigdomenech Badia, Oriol Vinyals, Demis Hassabis, Daan Wierstra, Charles Blundell
- Year: 2017
- Venue: Proceedings of the 34th International Conference on Machine Learning (ICML), PMLR volume 70, pages 2827-2836 (peer reviewed)
- DOI: none; PMLR v70/pritzel17a
- Exact claim it supports: an explicit episodic memory buffer can let an agent
  reuse past experience quickly, prior published result.
- Where used: Related Work.
- Peer reviewed: yes. Manually verified: yes.

## graves2016hybrid
- Title: Hybrid computing using a neural network with dynamic external memory
- Authors: Alex Graves, Greg Wayne, Malcolm Reynolds, Tim Harley, Ivo Danihelka, Agnieszka Grabska-Barwinska, Sergio Gomez Colmenarejo, Edward Grefenstette, Tiago Ramalho, John P. Agapiou, Adria Puigdomenech Badia, Karl Moritz Hermann, Yori Zwols, Georg Ostrovski, Adam Cain, Helen King, Christopher Summerfield, Phil Blunsom, Koray Kavukcuoglu, Demis Hassabis
- Year: 2016
- Venue: Nature, volume 538, issue 7626, pages 471-476 (peer reviewed)
- DOI: 10.1038/nature20101
- Exact claim it supports: augmenting a network with a read-write external memory
  lets it store information over long timescales, general motivation for explicit
  memory in agents.
- Where used: Introduction, Related Work.
- Peer reviewed: yes. Manually verified: yes.

## henderson2018deep
- Title: Deep Reinforcement Learning That Matters
- Authors: Peter Henderson, Riashat Islam, Philip Bachman, Joelle Pineau, Doina Precup, David Meger
- Year: 2018
- Venue: Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence (AAAI-18) (peer reviewed)
- DOI: 10.1609/aaai.v32i1.11694; arXiv:1709.06560
- Exact claim it supports: variance and inconsistent reporting make agent results
  hard to interpret, and reproducibility requires fixed conditions and released
  code. Supports the reproducibility practices and the cautious statistical stance
  used here.
- Where used: Methodology, Limitations.
- Peer reviewed: yes. Manually verified: yes.
