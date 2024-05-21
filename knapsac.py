import random
import math 

class Knapsack:
    def __init__(self, *args):
       
            self.capacity = args[0]
            self.num_items = args[1]
            self.weights = args[2]
            self.values = args[3]
    
    def is_feasible(self, solution):
        total_weight = sum(self.weights[i] for i in range(self.num_items) if solution[i] == '1')
        return total_weight <= self.capacity
    
    def print_solution(self, solution):
        print(f'Solution: {solution}, Value: {self.eval_solution(solution)}, Feasible: {self.is_feasible(solution)}')
    
    def eval_solution(self, solution):
        return sum(self.values[i] for i in range(self.num_items) if solution[i] == '1')
    
    def brute_force(self):
        best_solution = None
        best_value = 0
        for i in range(2 ** self.num_items):
            solution = bin(i)[2:].zfill(self.num_items)
            if self.is_feasible(solution):
                value = self.eval_solution(solution)
                if value > best_value:
                    best_value = value
                    best_solution = solution
        return best_solution, best_value
    
    def random_solution(self):
        while True:
            solution = ''.join(random.choice('01') for _ in range(self.num_items))
            if self.is_feasible(solution):
                return solution

    def move_1(self, solution, i):
        neighbors = []
        if i == 1:
            # Mouvement (i)
            for j in range(self.num_items):
                neighbor = list(solution)
                neighbor[j] = '1' if solution[j] == '0' else '0'
                neighbor = ''.join(neighbor)
                if self.is_feasible(neighbor):
                    neighbors.append(neighbor)
        elif i == 2:
            # Mouvement (ii)
            for j in range(self.num_items):
                for k in range(j+1, self.num_items):
                    if solution[j] != solution[k]:
                        neighbor = list(solution)
                        neighbor[j], neighbor[k] = neighbor[k], neighbor[j]
                        neighbor = ''.join(neighbor)
                        if self.is_feasible(neighbor):
                            neighbors.append(neighbor)
        elif i == 3:
            # Mouvement (iii)
            A = [idx for idx, bit in enumerate(solution) if bit == '1']
            B = [idx for idx, bit in enumerate(solution) if bit == '0']
            p = random.randint(1, len(A)) if A else 0
            q = random.randint(1, len(B)) if B else 0
            selected_A = random.sample(A, p) if p > 0 else []
            selected_B = random.sample(B, q) if q > 0 else []
            neighbor = list(solution)
            for idx in selected_A:
                neighbor[idx] = '0'
            for idx in selected_B:
                neighbor[idx] = '1'
            neighbor = ''.join(neighbor)
            if self.is_feasible(neighbor):
                neighbors.append(neighbor)
        elif i == 4:
            # Mouvement (iv)
            for j in range(self.num_items):
                for k in range(j + 1, self.num_items):
                    sub = solution[j:k + 1]
                    if sub != sub[::-1]:
                        neighbor = list(solution)
                        neighbor[j:k + 1] = reversed(sub)
                        neighbor = ''.join(neighbor)
                        if self.is_feasible(neighbor):
                            neighbors.append(neighbor)
        return neighbors

    def best_improvement_ls(self):
        solution = self.random_solution()
        best_value = self.eval_solution(solution)
        improving = True
        max_iterations = 1000
        iterations = 0
        
        while improving and iterations < max_iterations:
            improving = False
            best_neighbor = None
            for i in range(1, 5):
                neighbors = self.move_1(solution, i)
                for neighbor in neighbors:
                    value = self.eval_solution(neighbor)
                    if value > best_value:
                        best_value = value
                        best_neighbor = neighbor
                        improving = True
            if best_neighbor:
                solution = best_neighbor
            iterations += 1
        
        return solution, best_value

    def first_improvement_ls(self):
        solution = self.random_solution()
        best_value = self.eval_solution(solution)
        improving = True
        max_iterations = 1000
        iterations = 0
        
        while improving and iterations < max_iterations:
            improving = False
            for i in range(1, 5):
                neighbors = self.move_1(solution, i)
                for neighbor in neighbors:
                    value = self.eval_solution(neighbor)
                    if value > best_value:
                        best_value = value
                        solution = neighbor
                        improving = True
                        break
                if improving:
                    break
            iterations += 1
        
        return solution, best_value

    def full_random(self):
        best_solution = None
        best_value = 0
        for _ in range(10000):
            solution = self.random_solution()
            value = self.eval_solution(solution)
            if value > best_value:
                best_value = value
                best_solution = solution
        return best_solution, best_value

    def homogene_sa(self):
        solution = self.random_solution()
        best_solution = solution
        T = 100.0
        cooling_rate = 0.95
        max_iterations = 1000
        iterations = 0
        
        while T > 1e-3 and iterations < max_iterations:
            neighbors = self.move_1(solution, random.randint(1, 4))
            if not neighbors:
                continue
            neighbor = random.choice(neighbors)
            delta = self.eval_solution(neighbor) - self.eval_solution(solution)
            if delta > 0 or random.uniform(0, 1) < math.exp(delta / T):
                solution = neighbor
            if self.eval_solution(solution) > self.eval_solution(best_solution):
                best_solution = solution
            T *= cooling_rate
            iterations += 1
        
        return best_solution, self.eval_solution(best_solution)

    def no_homogene_sa(self):
        solution = self.random_solution()
        best_solution = solution
        T = 100.0
        max_iterations = 1000
        iterations = 0
        
        while T > 1e-3 and iterations < max_iterations:
            neighbors = self.move_1(solution, random.randint(1, 4))
            if not neighbors:
                continue
            neighbor = random.choice(neighbors)
            delta = self.eval_solution(neighbor) - self.eval_solution(solution)
            if delta > 0 or random.uniform(0, 1) < math.exp(delta / T):
                solution = neighbor
            if self.eval_solution(solution) > self.eval_solution(best_solution):
                best_solution = solution
            T = 1 / (1 + T)
            iterations += 1
        
        return best_solution, self.eval_solution(best_solution)
