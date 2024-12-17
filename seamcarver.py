from picture import Picture
import math
from PIL import Image

class SeamCarver(Picture):
    def energy(self, i: int, j: int) -> float:
        i1 = i - 1
        i2 = i + 1
        j1 = j - 1
        j2 = j + 1

        if i<0 or i>=self.width():
            raise IndexError()
        if j<0 or j>=self.width():
            raise IndexError()

        if i == 0:
            i1 = self.width() - 1
        elif i == self.width() - 1:
            i2 = 0
        if j == 0:
            j1 = self.height() - 1
        elif j == self.height() - 1:
            j2 = 0
        
        gradient_x = ((self[i2, j][0] - self[i1, j][0]) ** 2) + ((self[i2, j][1] - self[i1, j][1]) ** 2) + ((self[i2, j][2] - self[i1, j][2]) ** 2)
        gradient_y = ((self[i, j1][0] - self[i, j2][0]) ** 2) + ((self[i, j1][1] - self[i, j2][1]) ** 2) + ((self[i, j1][2] - self[i, j2][2]) ** 2)

        total = math.sqrt(gradient_x + gradient_y)
        return total

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        width, height = self.width(), self.height()

       
        energy = [[0] * width for _ in range(height)]

        for j in range(height):
            for i in range(width):
                energy[j][i] = self.energy(i, j)

     
        for j in range(1, height):
            for i in range(width):
                left, middle, right = energy[j-1][i-1] if i-1 >= 0 else float('inf'), energy[j-1][i], energy[j-1][i+1] if i+1 < width else float('inf')
                energy[j][i] += min(left, middle, right)

      
        min_energy = min(energy[-1])
        min_energy_index = energy[-1].index(min_energy)

      
        v_seam = [0] * height
        v_seam[-1] = min_energy_index

        for j in range(height - 2, -1, -1):
            i = v_seam[j + 1]
         
            v_seam[j] = i + min((0 if i == 0 else -1), 0, (0 if i == width - 1 else 1), key=lambda offset: energy[j][i + offset])

        return v_seam

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        width, height = self.width(), self.height()

      
        energy = [[0] * width for _ in range(height)]

        
        for j in range(height):
            energy[j][0] = self.energy(0, j)

    
        for i in range(1, width):
            for j in range(height):
               
                neighbourEnergy = [energy[max(j - 1, 0)][i - 1], energy[j][i - 1], energy[min(j + 1, height - 1)][i - 1]]
                energy[j][i] = self.energy(i, j) + min(neighbourEnergy)

       
        min_energy_index = energy.index(min(energy, key=lambda x: x[width - 1]))

     
        h_seam = [0] * width
        h_seam[width - 1] = min_energy_index

        for i in range(width - 2, -1, -1):
            neighbourEnergy = [energy[max(min_energy_index - 1, 0)][i], energy[min_energy_index][i], energy[min(min_energy_index + 1, height - 1)][i]]
            min_energy_index += neighbourEnergy.index(min(neighbourEnergy)) - 1
            h_seam[i] = min_energy_index

        return h_seam

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if self.width() == 1:
            raise SeamError()
        width, height = self.width(), self.height()

        if len(seam) != height:
            raise SeamError()

        for i in range(1, height):
            if abs(seam[i] - seam[i-1]) > 1:
                raise SeamError()

        for j in range(height):
            for i in range(seam[j], width - 1):
                self[i, j] = self[i + 1, j]

        self._width -= 1

        for j in range(height):
            del self[self._width, j]

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        if self.height() == 1:
            raise SeamError()
        width, height = self.width(), self.height()

        if len(seam) != width:
            raise SeamError()

        for i in range(1, width):
            if abs(seam[i] - seam[i-1]) > 1:
                raise SeamError()

        for i in range(width):
            for j in range(seam[i], height - 1):
                self[i, j] = self[i, j + 1]

        self._height -= 1

        for i in range(width):
            del self[i, self._height]

class SeamError(Exception):
    pass