# NLP-missing-pet-service

This is a frame based approach of a simulation of missing pet service. The program itself is simulate human customer service.

The knowledge base has a set of knowledge it needs to get from the input.

The input of customer will be parsed by TRIPS-web to form a graph.
The parsed graph will perform a tree matching using DFS(Depth first search) with the general graph that is hand crafted by myself.
If the two graphs matches, the information will be extracted into the knowledge base.
Then the program would check any missing information and ask questions to the customer.

In this project, I download the TRIPS api at this URL to parse input.
https://github.com/mrmechko/trips-web

A sample image of the implementation of the program can be seened at the sample.jpg.



