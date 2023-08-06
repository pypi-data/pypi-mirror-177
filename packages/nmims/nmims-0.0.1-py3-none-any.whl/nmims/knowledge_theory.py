def knowledge_theory():
    print('''
Knowledge
Knowledge Representation in AI describes the representation of knowledge. Basically, it is a study of how the beliefs, intentions, and judgments of an intelligent agent can be expressed suitably for automated reasoning. 
Implication (→) represents a structure of “if P then Q.” For example, if P: “It is raining” and Q: “I’m indoors”, then P → Q means “If it is raining, then I’m indoors.” In the case of P implies Q (P → Q), P is called the antecedent and Q is called the consequent.
Biconditional (↔) is an implication that goes both directions. You can read it as “if and only if.” P ↔ Q is the same as P → Q and Q → P taken together. For example, if P: “It is raining.” and Q: “I’m indoors,” then P ↔ Q means that “If it is raining, then I’m indoors,” and “if I’m indoors, then it is raining.” This means that we can infer more than we could with a simple implication. If P is false, then Q is also false; if it is not raining, we know that I’m also not indoors.

Model
The model is an assignment of a truth value to every proposition. To reiterate, propositions are statements about the world that can be either true or false. However, knowledge about the world is represented in the truth values of these propositions. The model is the truth-value assignment that provides information about the world.

Knowledge Base (KB)
The knowledge base is a set of sentences known by a knowledge-based agent. This is knowledge that the AI is provided about the world in the form of propositional logic sentences that can be used to make additional inferences about the world.
Entailment (⊨)
If α ⊨ β (α entails β), then in any world where α is true, β is true, too.
For example, if α: “It is a Tuesday in January” and β: “It is a Tuesday,” then we know that α ⊨ β. If it is true that it it a Tuesday in January, we also know that it is a Tuesday. Entailment is different from implication. Implication is a logical connective between two propositions. Entailment, on the other hand, is a relation that means that if all the information in α is true, then all the information in β is true.

Inference
Inference is the process of deriving new sentences from old ones.
For instance, in the Harry Potter example earlier, sentences 4 and 5 were inferred from sentences 1, 2, and 3.
Model Checking algorithm
Is one type of inference algorithm.
 
 
More efficient way of doing model check is by using search technique
1.Initial state : initial state of knowledge. That is knowledge base
2.actions: using logical proposition to perform actions on kb or inference rules.
3.Transitional state : New knowledge base after getting inference from the previous transition state
4.goal state: check statement we are trying to prove
5.path cost:no of steps in proof
·      
To determine if KB ⊨ α (in other words, answering the question: “can we conclude that α is true based on our knowledge base”)
o   Enumerate all possible models.
o   If in every model where KB is true, α is true as well, then KB entails α (KB ⊨ α)
P:it is a Tuesday Q:it is raining R:harry will go for a run
KB: (P ^ ~Q)R  P Q

P	Q	R	KB
 
F	F	F	F
F	F	T	F
F	T	F	F
F	T	T	F
T	F	F	F
T	F	T	T /////// Colored Row
T	T	F	F
T	T	T	F
			
To run the Model Checking algorithm, the following information is needed:
·   	Knowledge Base, which will be used to draw inferences
·   	A query, or the proposition that we are interested in whether it is entailed by the KB
·   	Symbols, a list of all the symbols (or atomic propositions) used (in our case, these are rain, hagrid, and dumbledore)
·   	Model, an assignment of truth and false values to symbols
Add model ckeck from logic.py
 the check_all function works is recursive

Inference Rules
Model Checking is not an efficient algorithm because it has to consider every possible model before giving the answer (a reminder: a query R is true if under all the models (truth assignments) where the KB is true, R is true as well). Inference rules allow us to generate new information based on existing knowledge without considering every possible model.
Inference rules are usually represented using a horizontal bar that separates the top part, the premise, from the bottom part, the conclusion. The premise is whatever knowledge we have, and the conclusion is what knowledge can be generated based on the premise.

De Morgans Law
It is possible to turn an And connective into an Or connective. Consider the following proposition: “It is not true that both Harry and Ron passed the test.” From this, it is possible to conclude that “It is not true that Harry passed the test” Or “It is not true that Ron passed the test.” That is, for the And proposition earlier to be true, at least one of the propositions in the Or propositions must be true.
-(a ^ b) => -a v -b
Similarly, it is possible to conclude the reverse. Consider the proposition “It is not true that Harry or Ron passed the test.” This can be rephrased as “Harry did not pass the test” And “Ron did not pass the test.”
-(a v b) => -a ^ -b

Resolution
Resolution is a powerful inference rule that states that if one of two atomic propositions in an Or proposition is false, the other has to be true. For example, given the proposition “Ron is in the Great Hall” Or “Hermione is in the library”, in addition to the proposition “Ron is not in the Great Hall,” we can conclude that “Hermione is in the library.” More formally, we can define resolution the following way:
	P V Q
        ~P
 ------------------
        Q
Resolution relies on Complementary Literals, two of the same atomic propositions where one is negated and the other is not, such as P and ¬P.
Resolution can be further generalized. Suppose that in addition to the proposition “Ron is in the Great Hall” Or “Hermione is in the library”, we also know that “Ron is not in the Great Hall” Or “Harry is sleeping.” We can infer from this, using resolution, that “Hermione is in the library” Or “Harry is sleeping.”
Complementary literals allow us to generate new sentences through inferences by resolution. Thus, inference algorithms locate complementary literals to generate new knowledge.
A Clause is a disjunction of literals (a propositional symbol or a negation of a propositional symbol, such as P, ¬P). A disjunction consists of propositions that are connected with an Or logical connective (P ∨ Q ∨ R). A conjunction, on the other hand, consists of propositions that are connected with an And logical connective (P ∧ Q ∧ R). Clauses allow us to convert any logical statement into a Conjunctive Normal Form (CNF), which is a conjunction of clauses, for example: (A ∨ B ∨ C) ∧ (D ∨ ¬E) ∧ (F ∨ G).
Steps in Conversion of Propositions to Conjunctive Normal Form
•	Eliminate biconditionals
o	Turn (α ↔ β) into (α → β) ∧ (β → α).
•	Eliminate implications
o	Turn (α → β) into ¬α ∨ β.
•	Move negation inwards until only literals are being negated (and not clauses), using De Morgan’s Laws.
o	Turn ¬(α ∧ β) into ¬α ∨ ¬β
Here’s an example of converting (P ∨ Q) → R to Conjunctive Normal Form:
•	(P ∨ Q) → R
•	¬(P ∨ Q) ∨ R /Eliminate implication
•	(¬P ∧ ¬Q) ∨ R /De Morgan’s Law
•	(¬P ∨ R) ∧ (¬Q ∨ R) /Distributive Law
At this point, we can run an inference algorithm on the conjunctive normal form. Occasionally, through the process of inference by resolution, we might end up in cases where a clause contains the same literal twice. In these cases, a process called factoring is used, where the duplicate literal is removed. For example, (P ∨ Q ∨ S) ∧ (¬P ∨ R ∨ S) allow us to infer by resolution that (Q ∨ S ∨ R ∨ S). The duplicate S can be removed to give us (Q ∨ R ∨ S).
Resolving a literal and its negation, i.e. ¬P and P, gives the empty clause (). The empty clause is always false, and this makes sense because it is impossible that both P and ¬P are true. This fact is used by the resolution algorithm.
•	To determine if KB ⊨ α:
o	Check: is (KB ∧ ¬α) a contradiction?
o	If so, then KB ⊨ α.
o	Otherwise, no entailment.
Proof by contradiction is a tool used often in computer science. If our knowledge base is true, and it contradicts ¬α, it means that ¬α is false, and, therefore, α must be true. More technically, the algorithm would perform the following actions:
•	To determine if KB ⊨ α:
o	Convert (KB ∧ ¬α) to Conjunctive Normal Form.
o	Keep checking to see if we can use resolution to produce a new clause.
o	If we ever produce the empty clause (equivalent to False), congratulations! We have arrived at a contradiction, thus proving that KB ⊨ α.
o	However, if contradiction is not achieved and no more clauses can be inferred, there is no entailment.
Here is an example that illustrates how this algorithm might work:
•	Does (A ∨ B) ∧ (¬B ∨ C) ∧ (¬C) entail A?
•	First, to prove by contradiction, we assume that A is false. Thus, we arrive at (A ∨ B) ∧ (¬B ∨ C) ∧ (¬C) ∧ (¬A).
•	Now, we can start generating new information. Since we know that C is false (¬C), the only way (¬B ∨ C) can be true is if B is false, too. Thus, we can add (¬B) to our KB.
•	Next, since we know (¬B), the only way (A ∨ B) can be true is if A is true. Thus, we can add (A) to our KB.
•	Now our KB has two complementary literals, (A) and (¬A). We resolve them, arriving at the empty set, (). The empty set is false by definition, so we have arrived at a contradiction.

    ''')

knowledge_theory()