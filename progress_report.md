# The Effect of Microtiming on Percussion Learning - Progress Report

#### Name: Ishan Dwivedi
#### Email: id360@cam.ac.uk
#### Supervisors: Dr. Peter Harrison, Dr. Alan Blackwell
#### Director of Studies: Dr. Tim Griffin
#### Overseers: Dr. Frank Stajano, Dr. Ian Wassell
&nbsp;&nbsp;&nbsp;

The overall aim of this project is to produce a piece of software that can give feedback to drummers on their microtiming deviations when trying to replicate another drummer's performance. This has required the development of a backend system that can perform automatic drum transcription and a frontend system that can provide feedback to the user. The backend system is currently being developed in Python and the frontend in React.js.

So far, I have made significant progress in producing an NMF model that achieves automatic drum transcription as required. I have achieved an F-score of 0.82 on the IDMT-SMT Drums dataset. I have also written the outline of a React.js frontend that can provide feedback to the user. I have therefore almost fully completed the core success criteria of the project.

Upon reflection, I underestimated the time needed to work on the frontend of the application. I have made many of the design choices in collaboration with my supervisors and have implemented them in react, but more of the frontend needs to be completed to allow for complete end-to-end interaction with the system. This means writing code that does tasks like making use of the browser microphone API, communcating with the backend API, and updating the UI in response to the user's actions.

As an extension, I have also decided to work on making the analysis feedback to a human participant work in real-time. It would require work on optimization and parallelization of the NMF algorithm. I am also still researching the use of RNNs in drum transcription and will be working on implementing them in the backend system if time allows. It may not be feasible or necessary to compare the RNN to the NMF model for the user study, but it would interesting to see a comparison of performance between the two models for academic reasons.

With regards to the user study, I have identified a few suitable participants and have been in contact with them. I have also identified a suitable venue for the study. I have not yet been able to schedule the study, but I am hoping to do so in the next few weeks.