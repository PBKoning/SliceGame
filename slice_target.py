import pygame

class Slice_Target:

    def __init__(self, canvas) -> None:

        self.canvas=canvas
        self.x_pos = 100
        self.x_speed = 2
        self.y_pos = self.max_y_pos = 600
        self.y_speed = -12
        self.gravity = 0.15
           
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.y_speed += self.gravity

    def draw(self):
        pygame.draw.circle(self.canvas, (150, 150, 150), (self.x_pos, self.y_pos), 30)
