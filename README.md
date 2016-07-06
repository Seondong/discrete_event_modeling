### Discrete event modeling practice
* Programmed by using __Python Simpy__ package.
* __IDE__: I used __PyCharm__ to easily play with Python. You can open directory DES as a PyCharm project.
* __Doolgi__ example is also included in DES project.

### Doolgi(Pigeon) example
[비둘기키우기](https://play.google.com/store/apps/details?id=com.Mouse_Duck.DoveGame&hl=ko) is an addictive game which is getting popular(+100k users) in the Android Market. Main objective of this game is collect 36 different types of pigeons. 
![Screenshot](./screenshot/doolgi_screenshot.jpg)

#### Brief introduction of this game
* __Generating pigeon__: A pigeon is generated by putting a meal on the ground, a level of pigeon is decided by the level of your meal. For example if your meal is level 5, a pigeon with level x, x~Uniform(1-5) is generated. Number of total pigeons in the ground can be increased by upgrading utilities.  
* __Game money__
	* __Feathers__: Pigeons are collecting feathers periodically, by upgrading feature collection interval to the max level, collecting interval is shorten to 1.0 seconds. Feather can be used to upgrade utilities or buy additional pigeons. 
		* Available utilities to upgrade: Level of your meal(+1), Decreasing collecting interval(-0.2sec), Total number of available pigeons in the ground(+1), Total number of meals you can possess at once(+1), Meal generating interval(-0.2sec)
		* For each upgrade, you need exponential amount of features
	* __Diamonds__: Diamonds are something similar to cash items, but in this game you don't have to pay cash to get diamonds. By breaking pigeon egg(which occurs in the ground periodically) gives you a diamond with high probability, or you can watch short(15-30sec) ads to get 3 diamonds. Diamond can be used to upgrade additional utilities in the game.
		* Available utilities to upgrade: Automatic merging(a.k.a. Arrow of cupid -1sec, 30sec), Automatic feeding(-1sec, 30sec), DJ Beaver time interval: 10x collecting for 5-6 seconds(-10sec, 200sec), +2 level upgrade(Hamster Magic, +2%, 10%), Moving restriction, Merging restriction
		* These functions are activated by 50 diamonds at first, and additional upgrade needs 60, 70, 80, 90, 100 diamonds. Moving and merging restriction needs 100 diamonds to activate.
* __Merging pigeons__: A pigeon with level n+1 is generated by merging two pigeons with level n. Higher-level pigeon collects more feathers at the same time. 
	* Number of feathers collected by each pigeon, each time: f(1) = 1, f(2) = 2, f(3) = 3, f(n) = f(n-3) + f(n-1), n > 4 


#### Advance thoughts while playing the game
* Usually, f(n+2) ~ 1.465f(n+1) ~ 2.147f(n), so merging two high-level pigeons will result significant decrease of feature collecting rate. Let's consider sequential merging scenario. You might want to make lv.25 pigeon by merging lv.22 + lv.22 + lv.23 + lv.24. Rate of the lv.25 pigeon itself is 12,664/sec, but summation of four pigeons are 22,553/sec. Even if you have to generate three pigeons, randomly-chosen three pigeon's collecting rate is far smaller than the differences.
* So, it is better to retain high level pigeons without merging them. In that case, user will obtain maximum amount of feathers. This equilibrium is maintained by operating automatic merging and feeding with the same interval. Since automatic merging operates with the rule that two lowest level pigeons are merged. 
* By turning on above two automatic features, you can leave the game without controlling much, only thing that you have to do is upgrading utilities.


#### What did I model in this project?
* __Problem definition__: Interesting perspective of this neglect-based mobile game is, use resources as wise as you can. For example, your 120 diamonds can be used to increase 4% probability of +2 level upgrade, or to decrease 1 second merging & feeding interval, or to decrease 20 seconds of beaver time inverval. And I want to make the largest benefit from that long-term decision(it's hard to collect 120 diamonds - take few days). By considering our objective function is the number of feathers collected after the decision, I developed a discrete-event model to simulate different cases. Usually people, who play this game, turn on the phone overnight, I consider 30,000 seconds are enough time to evaluate the outcome.

#### Code description
* trial_doolgi.py
	* class Doolgi: Definition of Doolgi object
		* \_\_init\_\_: initialize Doolgi
		* collect: define collecting behavior
	* generateDoolgi_flowline: SimPy-based event flowline to generate Doolgi regularly.
	* mergeDoolgi_flowline: SimPy-based event flowline to merge Doolgi regularly.
	* initialize_doolgi: initialization condition
	* killDoolgi: remove Doolgi instance
	* mergeDoolgi: merge two Doolgi instance - kill 2 doolgis and generate new one.
* experiment_doolgi.py: Code for experiment
	* playDoolgiGame: Initialize Doolgis and process discrete-event simulation according to parameters
		* Parameter example: [10, 0.12, 30, 200, 4000, 3]
		* Parameter expanation: maxLevel, doubleUpgradeRate, intervalMerge, intervalBeaver, runtime, numExp (from the left)
	* Main: Experiment with 144(=4*6*6) different cases, each case is averaged over 30 different trials. You can easily change input parameters. Final result file is automatically saved as ./doolgi_experiment_result.csv 
		
		```
		maxLevel = [10, 11, 12, 13]
		upgradeRate = [0.10, 0.12, 0.14, 0.16, 0.18, 0.20]
		mergeInterval = [30, 29, 28, 27, 26, 25]
		intervalBeaver, runtime, numExp = 200, 30000, 30
		```

#### To do
* Wait until the experiment ends, and plot graphs - add on this post
* Write interesting blog posts containing upcoming results
* Generate results with more intermediate results - according to each timestep, provide current doolgi status with feathers
* Implement DJ Beaver time
* Get feedback from my friends, Doolgi game users

**Please write an article in 'issue' tab if you have somethings to discuss with me.**

> If it cause any issues such as license, copyright, plagiarism, please let me know, by sending a short e-mail to me (sundong.kim@kaist.ac.kr)