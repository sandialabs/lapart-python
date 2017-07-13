============
Architecture
============
The general layout of the LAPART algorithm includes two fuzzy ARTs, labeled as A and B, that 
are connected by an associator matrix referred to as L. Each of them have an input layer, a recognition 
layer, and a categorization layer. Also, they both have a vigilance parameter rhoA, rhoB respectively. 
The A and B algorithms are connected together by an inference mechanism so that the template 
connections are established during training and then used to provide predictions during testing. 
The flow of the algorithm is shown in the Figure below. During training, the system is able to learn 
through the presentation of input pattern pairs (IA{x1..xn} and IB{y1..yn}) applied to each 
Fuzzy ART network. At the same time, interconnections between classes are formed in the L 
matrix. The interconnections between the A and B Fuzzy ART connect the learned categories and 
allow for predictions to be made in the testing phase when new data becomes available. During 
testing previously unseen data are presented to the A side only. 
Categorization of the input patterns occurs in the A side which connects, through the L matrix, 
to a particular category on the B side. The particular B side category for the input pattern is 
then the prediction for the given A input.

   
.. _fig-lapart2:
.. figure:: figures/lapart2.png
   :scale: 75 %
   :alt: Sample-graphics
   
   LAPART training algorithm flow diagram includes Fuzzy ART A & B and two cases for learning A and B side templates.
   
Fuzzy ART A
-----------
The training process is initiated with the presentation of an input pattern into the Fuzzy 
ART A algorithm. Since no templates exist at the onset of the training the initial input 
becomes the first template on the A-side. Therefore, a new template or class would be created 
using the “New A Class” block shown in the figure above. In this situation, the Fuzzy ART 
B operates as a normal ART algorithm. Since there 
are no B-Side templates, a new template was automatically created and a link between the A 
and B Fuzzy ARTs are established in the L matrix.

The algorithm then starts over with a new input, and repeats until all of the inputs are 
considered. When the new input is presented to all of the existing templates, in the 
“A-Side Search” block, it searched for the top matches as determined by the choice function. 
Then the vigilance test is computed in the “A-Side Resonance” block to determine if 
resonance with an existing template occurs or not. If resonance does not occur then the 
next best template was considered until no choices were left. If a match is not found, 
then the script for Case 1 is implemented. If a match does occur, the script for Case 2 is used.

Case 1
------
The Case 1 code scenario occurs when a new A-side class was created and the Fuzzy ART B is 
allowed to operate as a normal ART algorithm. First, a new A-Side template is created. Then 
the B-Side input pattern is presented to the “B-Side Search” block where the choice function 
is used to discover the best template match. After the best match is found, the system tested 
the match to see if it met the vigilance parameter criteria in the “B-Side Resonance” block. If 
it did not, then a new template is created. If it did, then it updates an existing template. 
After the creation or update of a B-Side template, the inference matrix L was updated to link 
the newly created A-Side template to the B-Side template.

Case 2
------
In the event that resonance occurred in the Fuzzy ART A section of the code then Case 2 is 
implemented. First, the A-side template that resonated with the input pattern is not updated, 
but instead put on hold until further notice. Also, the match function is used to find the 
template that best matched the given input pattern. Then, if the chosen template passed the 
vigilance criteria, where the match function was greater than or equal to the B-side vigilance 
(rhoB), then the given A and B side templates are updated respectively. But, if it does not pass, 
then the system experiences a lateral reset and the initial A-side template is hidden and the 
process is repeated.