import pygame

def scale_image_by_factor(image, scale_factor):
    if scale_factor == 1:        
        return image
    else:        
        old_width, old_height = image.get_size()      
        new_width = int(old_width * scale_factor)
        new_height = int(old_height * scale_factor)            
        return pygame.transform.scale(image, (new_width, new_height))
