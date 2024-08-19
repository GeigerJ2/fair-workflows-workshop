import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import eigs
import time

np.random.seed(0)
random_matrix = csc_matrix(np.random.rand(100, 100), dtype=float)

A = random_matrix + random_matrix.T * -1j

# Start the timer
def _diagonalize(known_eigenvector=None):
    start_time = time.time()

    eigenvalues, eigenvectors = eigs(A, k=2, which='SM', v0=known_eigenvector, return_eigenvectors=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if known_eigenvector is None:
        np.savetxt('eigenvectors.txt', eigenvectors)
        print(f"Saved eigenvectors to eigenvectors.txt")

    print(f"eigenvalues: {eigenvalues}")
    print(f"Elapsed time: {elapsed_time} seconds")

    return elapsed_time, eigenvectors

eigenvector_file = input("Enter the filename of a previously calculated eigenvector (or press Enter to skip): ")
v0 = np.loadtxt(eigenvector_file, dtype=np.complex128)[:, 0] if eigenvector_file else None
# exit()

elapsed_time_with_v0, eigenvectors = _diagonalize(v0)


