def uncertainity_theory():
    print('''
Probability
Uncertainty can be represented as a number of events and the likelihood, or probability, of each of them happening.

Possible Worlds
Every possible situation can be thought of as a world, represented by the lowercase Greek letter omega ω.
Axioms in Probability
•	0 < P(ω) < 1: every value representing probability must range between 0 and 1.
•	Zero is an impossible event, like rolling a standard die and getting a 7.
•	One is an event that is certain to happen, like rolling a standard die and getting a value less than 10.
•	In general, the higher the value, the more likely the event is to happen.
•	The probabilities of every possible event, when summed together, are equal to 1.
Conditional Probability
Conditional probability is the degree of belief in a proposition given some evidence that has already been revealed.
P(a | b), meaning “the probability of event a occurring given that we know event b to have occurred,” or, more succinctly, “the probability of a given b.”
P(a | b) = P(a ^ b)/P(b)
Independence
Independence is the knowledge that the occurrence of one event does not affect the probability of the other event. For example, when rolling two dice, the result of each die is independent from the other.
Bayes’ Rule
Bayes’ rule is commonly used in probability theory to compute conditional probability. In words, Bayes’ rule says that the probability of b given a is equal to the probability of a given b, times the probability of b, divided by the probability of a.
P(b | a) = P(b) * P(a | b) / P(b)

Bayesian Networks
A Bayesian network is a data structure that represents the dependencies among random variables. Bayesian networks have the following properties:

They are directed graphs.
Each node on the graph represent a random variable.
An arrow from X to Y represents that X is a parent of Y. That is, the probability distribution of Y depends on the value of X.

1. 	Bayesian Network
A Bayesian network is a data structure that represents the dependencies among random variables. Bayesian networks have the following properties:
 
They are directed graphs.
Each node on the graph represents a random variable.
Each node X has probability distribution P(X | Parents(X)).
Example: Variables affecting whether we get an appointment on time

Now every node will have a probability distribution table.
Rain pdf
None	Light	Heavy
0.4	     0.2     0.4
 
Maintenance
Rain	Yes	no
None	0.8	0.2
light	0.6	0.4
Heavy	0.2	0.8
 
Train Table
Rain	Main	On time	     Delayed
None	Yes	     0.6	        0.4
None	No	     0.3	        0.7
Light	yes	     0.2	        0.8
Light	No	     0.4	        0.6
Heavy	Yes	     0.9	        0.1
Heavy	No	     0.2	        0.8
 
Appointment
Train	Attend	mIss
On time	0.8	0.2
Delayed	0.7	0.3
 
 
For example, if we want to find the probability of missing the meeting when the train was delayed on a day with no maintenance and heavy rain, or P(heavy, no, delayed, miss), we will compute the following: P(heavy)P(no | heavy)P(delayed | light, no)P(miss | delayed). The value of each of the individual probabilities can be found in the probability distributions above, and then these values are multiplied to produce P(heavy,no, delayed, miss).
2. 	Inference by Enumeration
Inference by enumeration is a process of finding the probability distribution of variable X given observed evidence e and some hidden variables Y.
P(X|e) = α P(X,e) = α  
 
In this equation, X stand for the query variable, e for the observed evidence, y for all the values of the hidden variables, and α normalizes the result such that we end up with probabilities that add up to 1. To explain the equation in words, it is saying that the probability distribution of X given e is equal to a normalized probability distribution of X and e. To get to this distribution, we sum the normalized probability of X, e, and y, where y takes each time a different value of the hidden variables Y.
MAKE GRAPH OF BAYESIAN NETWORK
Ex: P(appointment|light,no)
=alpha[P(appointment,light,no)
=alpha [P(appointment ,light ,no ,on time)+ P(appointment ,light ,no, delayed)]
Comparing with formula Appointment=X(query variable) , light,no=observed evidence and delayed,on time = Y (hidden variables)
 
3. 	Sampling approach
Sampling is one technique of approximate inference. In sampling, each variable is sampled for a value according to its probability distribution.
 
Eg: To generate a distribution using sampling with a die, we can roll the die multiple times and record what value we got each time. Suppose we rolled the die 600 times. We count how many times we got 1, which is supposed to be roughly 100, and then repeat for the rest of the values, 2-6. Then, we divide each count by the total number of rolls. This will generate an approximate distribution of the values of rolling a die: on one hand, it is unlikely that we get the result that each value has a probability of 1/6 of occurring (which is the exact probability), but we will get a value that’s close to it.
 
Example from our Bayesian Network:
If we start with sampling the Rain variable, the value none will be generated with probability of 0.7, the value light will be generated with probability of 0.2, and the value heavy will be generated with probability of 0.1. Suppose that the sampled value we get is none. When we get to the Maintenance variable, we sample it, too, but only from the probability distribution where Rain is equal to none, because this is an already sampled result. We will continue to do so through all the nodes. Now we have one sample, and repeating this process multiple times generates a distribution. Now, if we want to answer a question, such as what is P(Train = on time), we can count the number of samples where the variable Train has the value on time, and divide the result by the total number of samples. This way, we have just generated an approximate probability for P(Train = on time).
 
4. 	Rejection Sampling Approach
For conditional probabilities like P(Train=on time | Rain=heavy), we would have to filter down our data twice.
First to get all the samples where Rain=heavy and then from that filter all the samples in Rain=heavy where Train=on time
So, to remove redundancy, we perform rejection sampling approach.
Since we already have our evidence to be Rain=heavy, we simply fix that value for Rain node and calculate the samples from all the other nodes. And once we have sampled for, say, 10000 times then we can find the number of samples where Train=on time and simply divide that with total number of samples taken.
So in a way we are rejecting all the value of evidence that is not given… in this case we are rejecting Rain=light and Rain=none and only sampling with Rain=heavy.
 
5. 	Likelihood Weighting
 
In Rejection sampling, we discarded the samples that did not match the evidence that we had. This is inefficient. One way to get around this is with likelihood weighting, using the following steps:
 
Start by fixing the values for evidence variables.
Sample the non-evidence variables using conditional probabilities in the Bayesian network.
Weight each sample by its likelihood: the probability of all the evidence occurring.
For example, if we have the observation that the train was on time, we will start sampling as before. We sample a value of Rain given its probability distribution, then Maintenance, but when we get to Train - we always give it the observed value, in our case, on time. Then we proceed and sample Appointment based on its probability distribution given Train = on time. Now that this sample exists, we weight it by the conditional probability of the observed variable given its sampled parents. That is, if we sampled Rain and got light, and then we sampled Maintenance and got yes, then we will weight this sample by P(Train = on time | light, yes).
 
 
6. 	Markov Chain
Markov Model: The Markov assumption is an assumption that the current state depends on only a finite fixed number of previous states.
Example: Predicting weather
In theory, we could use all the data from the past year to predict tomorrow’s weather. However, it is infeasible, both because of the computational power this would require and because there is probably no information about the conditional probability of tomorrow’s weather based on the weather 365 days ago. Using the Markov assumption, we restrict our previous states (e.g., how many previous days we are going to consider when predicting tomorrow’s weather), thereby making the task manageable. This means that we might get a rougher approximation of the probabilities of interest, but this is often good enough for our needs. Moreover, we can use a Markov model based on the information of the one last event (e.g., predicting tomorrow’s weather based on today’s weather).
Markov Chain: A Markov chain is a sequence of random variables where the distribution of each variable follows the Markov assumption. That is, each event in the chain occurs based on the probability of the event before it.
We need a transition model for Markov Chains.
Example: Transition model for tomorrow’s weather given today’s weather.
 	
 	Tomorrow Xt+1
Today
Xt	 	Sunny	Rainy
	Sunny	0.8	0.2
	Rainy	0.4	0.6
 
In this example, the probability of tomorrow being sunny based on today being sunny is 0.8. This is reasonable, because it is more likely than not that a sunny day will follow a sunny day. However, if it is rainy today, the probability of rain tomorrow is 0.7, since rainy days are more likely to follow each other. Using this transition model, it is possible to sample a Markov chain. Start with a day being either rainy or sunny, and then sample the next day based on the probability of it being sunny or rainy given the weather today.
 
Hidden Markov Models: A hidden Markov model is a type of a Markov model for a system with hidden states that generate some observed event. This means that sometimes, the AI has some measurement of the world but no access to the precise state of the world. In these cases, the state of the world is called the hidden state and whatever data the AI has access to are the observations. Here are a few examples for this:
-    	For a robot exploring uncharted territory, the hidden state is its position, and the observation is the data recorded by the robot’s sensors.
-    	In speech recognition, the hidden state is the words that were spoken, and the observation is the audio waveforms.
-    	When measuring user engagement on websites, the hidden state is how engaged the user is, and the observation is the website or app analytics.
Example: Our AI wants to infer the weather (the hidden state), but it only has access to an indoor camera that records how many people brought umbrellas with them. Here is our sensor model (also called emission model) that represents these probabilities:
 
 	Observation Et
State
Xt	 	Umbrella	No Umbrella
	Sunny	 	 
In this model, if it is sunny, it is most probable that people will not bring umbrellas to the building. If it is rainy, then it is very likely that people bring umbrellas to the building. By using the observation of whether people brought an umbrella or not, we can predict with reasonable likelihood what the weather is outside.

Sensor Markov Assumption
The assumption that the evidence variable depends only on the corresponding state. For example, for our models, we assume that whether people bring umbrellas to the office depends only on the weather. This is not necessarily reflective of the complete truth, because, for example, more conscientious, rain-averse people might take an umbrella with them everywhere even when it is sunny, and if we knew everyone’s personalities it would add more data to the model. However, the sensor Markov assumption ignores these data, assuming that only the hidden state affects the observation.
A hidden Markov model can be represented in a Markov chain with two layers. The top layer, variable X, stands for the hidden state. The bottom layer, variable E, stands for the evidence, the observations that we have.
Based on hidden Markov models, multiple tasks can be achieved:
•	Filtering: given observations from start until now, calculate the probability distribution for the current state. For example, given information on when people bring umbrellas form the start of time until today, we generate a probability distribution for whether it is raining today or not.
•	Prediction: given observations from start until now, calculate the probability distribution for a future state.
•	Smoothing: given observations from start until now, calculate the probability distribution for a past state. For example, calculating the probability of rain yesterday given that people brought umbrellas today.
•	Most likely explanation: given observations from start until now, calculate most likely sequence of events.
The most likely explanation task can be used in processes such as voice recognition, where, based on multiple waveforms, the AI infers the most likely sequence of words or syllables that brought to these waveforms.

    ''')

uncertainity_theory()