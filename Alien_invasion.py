import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullets
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings=Settings()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.screen=pygame.display.set_mode((self.settings.screen_width , self.settings.screen_height))
        pygame.display.set_caption("WELCOME TO ALIEN INVASION")
        self.stats=GameStats(self)
        self.ship=Ship(self)
        self._create_fleet()
        self.bullet= pygame.sprite.Group()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height     
   
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
           # print(len(self.bullets))
            self.screen.fill(self.settings.color_bg)
            self.ship.blitme()
            #self.aliens.blitme()
            #Shows the most recent screen
            pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        #Getting rid of fired bullets
        for bullet in self.bullet.copy():
            if bullet.rect.buttom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
             
        
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()     
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
    def _check_keydown_events(self,event):
        #Respond to key press
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        #Respond to key release
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        new_bullet = Bullets(self)
        self.bullets.add(new_bullet)

    def _create_fleet(self):
        alien=Alien(self)
        alien_width,alien_height= alien.rect.size
        self.aliens.add(alien)
        alien_width , alien_height =alien.rect.size
        available_space_x= self.settings.screen_width - (2* alien_width)
        number_alien_x= available_space_x // (2 * alien_width)
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
             for alien_number in range(number_alien_x):
                self._create_alien(alien_number,row_number) 

    def _create_alien (self,alien_number,row_number):
        alien=Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y +=  self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens (self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit!!")
            self._ship_hit()
        self._check_aliens_buttom()
    
    def _ship_hit(self):
        if self.stats.ships_left>0:
            self.stats.ships_left -=1
            self.aliens.empty()
            self.bullets.empty()
        #Create new fleet
            self._create_fleet()
            self.ship.center_ship()
        # Pause
            sleep(0.5)
        else:
            self.stats.game_active=False

    def _check_aliens_buttom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
        # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        
    def _update_screen(self):
        self.screen.fill(self.settings.color_bg)
        self.aliens.draw(self.screen)
        #self.ship.draw(self.screen)
        self.ship.blitme()
        #self.aliens.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()
        


#if __name__ == '__main__':
 # Make a game instance, and run the game.
ai = AlienInvasion()
ai.run_game()