from . import stag_internal
from . import utility


@utility.return_graph
def sbm(n: int, k: int, p: float, q: float, exact=False):
    """
    Generate a graph from the symmetric stochastic block model.

    Every cluster has the same number of vertices. For large enough values of
    n, this method samples from an approximate stochastic block model by
    default which significantly speeds up the execution time. To sample
    exactly from the stochastic block model, pass the optional 'exact'
    parameter to the method.

    The approximate sampling method has running time O(k^2 + nnz) and the exact
    method has running time O(n^2) where nnz is the number of non-zeros in the
    generated graph's adjacency matrix.

    :param n: - the number of vertices in the graph
    :param k: - the number of clusters; vertices are split evenly between clusters
    :param p: - the probability of including an edge inside a cluster
    :param q: - the probability of including an edge between two clusters
    :param exact: (optional) - whether to use the exact probability distribution
                              or an approximation.
    :return: the randomly generated graph
    """
    return stag_internal.sbm(n, k, p, q, exact)


@utility.return_graph
def erdos_renyi(n: int, p: float, exact=False):
    """
    Generate a graph from the Erdos-Renyi model.

    For large values of n, this method will use an approximate version of the
    random model with running time O(nnz) where nnz is the number of edges in
    the sampled graph.

    If the 'exact' parameter is true, then the true Erdos-Renyi distribution
    will be used, with running time O(n^2).

    :param n: - the number of vertices in the graph
    :param p: - the probability of including each edge
    :param exact: (optional) - whether to sample from the exact model
    :return: the randomly generated graph
    """
    return stag_internal.erdos_renyi(n, p, exact)
