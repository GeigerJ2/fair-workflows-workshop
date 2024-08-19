import numpy as np
import argparse

parser = argparse.ArgumentParser(
                    prog='Diagonalization Program',
                    description='Effective diagonlization for sparse matrices')
parser.add_argument('filename', help="Contains matrix")


def jacobi_rotation(A, tol=1e-10, max_iterations=100):
    n = A.shape[0]
    P = np.eye(n)
    iterations = 0
    
    def max_offdiag(A):
        n = A.shape[0]
        max_val = 0.0
        p = 0
        q = 1
        for i in range(n):
            for j in range(i+1, n):
                if abs(A[i, j]) > abs(max_val):
                    max_val = A[i, j]
                    p, q = i, j
        return max_val, p, q
    
    while iterations < max_iterations:
        max_val, p, q = max_offdiag(A)
        
        if abs(max_val) < tol:
            break
        
        theta = 0.5 * np.arctan2(2 * A[p, q], A[p, p] - A[q, q])
        
        # Create the Jacobi rotation matrix
        Ppq = np.eye(n)
        Ppq[p, p] = np.cos(theta)
        Ppq[q, q] = np.cos(theta)
        Ppq[p, q] = -np.sin(theta)
        Ppq[q, p] = np.sin(theta)
        
        # Update the matrix A
        A = Ppq.T @ A @ Ppq
        
        # Accumulate the transformation matrix
        P = P @ Ppq
        
        iterations += 1
    
    return np.diag(A), P



if __name__ == '__main__':
    args = parser.parse_args()
    data = np.load(args.filename)
    eigenvalues, _ = jacobi_rotation(data)
    print("Eigenvalues:", eigenvalues)
