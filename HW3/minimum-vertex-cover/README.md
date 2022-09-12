# Minimum Vertex Cover

In This Problem, We want to investigate the minimum vertex cover problem. Informally, A vertex cover is a subset of vertices that cover all the edges. i.e., for each edge, there exists an endpoint in the vertex cover. A minimum vertex cover is a vertex cover with the least amount of vertices possible.

The Formal definition of the problem is as follows:
A vertex cover V' of an undirected graph G = (V,E) is a subset of V such that for all edge 
<img src="https://render.githubusercontent.com/render/math?math=uv \in E \Rightarrow u \in V' \vee v \in V'">.
The vertex cover with the smallest possible size is called the minimum vertex cover.

Minimum vertex cover is a famous NP-Hard optimization problem. It means that we currently don't have any polynomial-time algorithm for this problem, and we will most likely never have such an algorithm unless P = NP. Therefore it is reasonable to use optimization algorithms like local search to find an approximate but not necessarily perfect answer.

In this question and the next one, you should implement two different local search techniques to solve this problem: Simulated Annealing  and the Genetic Algorithm.
