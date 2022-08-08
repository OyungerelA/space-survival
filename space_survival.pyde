# SPACE SURVIVAL
# by Oyungerel Amarsanaa

# Game Description:
#     > The astronaut at the bottom can be moved with arrow keys (LEFT and RIGHT)
#     > Oxygen bubbles are valuable objects that must be collected 
#     > Meteors are obstacle objects that must be dodged
#     > Powerups reset the game speed back to normal
#     > Game speed will increase as game progresses
#     > Blue oxygen bubbles are worth 1 point
#     > Gold oxygen bubbles are worth 10 points
#     > Game ends if the astronaut is hit by a meteor
#     > The background of the game is chosen randomly out of 4 images


add_library('minim')
import random, os
path = os.getcwd()
player = Minim(this)

# The game was inspired by a mobile game and it's more suitable to play on a narrow screen so the width of our game is relatively short
WIDTH = 350
HEIGHT = 700
NUM_ROWS = 10
NUM_COLS = 5
# List that will hold all game scores; will be later used to determine the high score
score_list = []


# Superclass that oxygen, gold, meteor and powerup classes will inherit from
class Object:
    def __init__(self, row, col, img_name, img_w, img_h):
        self.row = row
        self.col = col
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        # Attribute that will hold the bottom pixel of the object; will be used to check whether the object has hit the astronaut
        self.bp = 0
       
    # Method controlling the falling action of objects
    def fall(self):
        # Objects will fall 0.5 rows at a time unless redefined otherwise; 0.5 is chosen so that the falling action will look smoother
        if self.row <= NUM_ROWS:
            self.row += 0.5
        
        # Calculate the bottom pixel of the object depending on its current row
        self.bp = (self.row + 1) * self.img_h    
    
    def display(self):
        image(self.img, self.col * self.img_w, self.row * self.img_h, self.img_w, self.img_h)
        self.fall()


# Oxygen class
class Oxygen(Object):
    def __init__(self, row, col, img_name, img_w, img_h):
        Object.__init__(self, row, col, img_name, img_w, img_h)


# Gold oxygen class
class Gold(Object):
    def __init__(self, row, col, img_name, img_w, img_h):               
        Object.__init__(self, row, col, img_name, img_w, img_h)

    # Gold oxygen bubbles will fall faster than other objects, 1 row at a time, so that they are more challenging to collect
    def fall(self):
        if self.row <= NUM_ROWS:
            self.row += 1
            
        self.bp = (self.row + 1) * self.img_h    
        

# Meteor class
class Meteor(Object):
    def __init__(self, row, col, img_name, img_w, img_h):
        Object.__init__(self, row, col, img_name, img_w, img_h)


# Powerup class
class Powerup(Object):
    def __init__(self, row, col, img_name, img_w, img_h):
        Object.__init__(self, row, col, img_name, img_w, img_h)
        
    # Powerup objects will fall 0.75 rows at a time so that they are somewhat challenging to collect and so that they don't overlap with other objects
    def fall(self):
        if self.row <= NUM_ROWS:
            self.row += 0.75
            
        self.bp = (self.row + 1) * self.img_h    
    
    
# Astronaut class
class Astronaut:
    def __init__(self, img_name, img_w, img_h):
        # Positioned at the bottom of the board
        self.row = NUM_ROWS - 1
        # The column where the astronaut will be initially placed is chosen randomly
        self.col = random.randint(0, NUM_COLS - 1)
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        # Sprites are used for displaying the astronaut and the default frame is 0
        self.frame = 0
        # Astronaut will face the center/front initially; will be used for sprites
        self.dir = CENTER
        self.alive = True
        self.key_handler = {LEFT:False, RIGHT:False}
        
        self.collect_sound = player.loadFile(path + "/sounds/collect.mp3")
        self.hit_sound = player.loadFile(path + "/sounds/hit.mp3")
        self.powerup_sound = player.loadFile(path + "/sounds/powerup.mp3")
        
    # Method for moving and updating the image of the astronaut based on key presses
    def update(self):
        # Astronaut will be moved one column to the left if LEFT key is pressed and if the move fits within board boundaries
        if self.key_handler[LEFT] == True and self.col - 1 >= 0:
            self.col -= 1
            # Astronaut will face the left direction
            self.dir = LEFT
            
        # Astronaut will be moved one column to the right if RIGHT key is pressed and if the move fits within board boundaries
        elif self.key_handler[RIGHT] == True and self.col + 1 < NUM_COLS:
            self.col += 1      
            # Astronaut will face the right direction
            self.dir = RIGHT
        
        else:
            # The default direction of astronaut is center when no key is pressed or when key is released
            self.dir = CENTER
        
    # Check if astronaut is hit by any objects
    def check_game(self):
    
        self.update()
        
        for o in game.oxygens:
            # Check if the astronaut and oxygen are in the same column
            if o.col == self.col:
                # Check if the oxygen is at the bottom of the board; if both conditions are met, it means the astronaut has collected an oxygen
                if o.bp == HEIGHT:
                    self.collect_sound.rewind()
                    self.collect_sound.play()
                    game.oxygens.remove(o)
                    # Game score and flag score are implemented by 1
                    game.score += 1
                    game.flag_score += 1    
                    
        for g in game.golds:                        
            if g.col == self.col:
                if g.bp == HEIGHT:
                    self.collect_sound.rewind()
                    self.collect_sound.play()
                    game.golds.remove(g)
                    game.score += 10
                    game.flag_score += 10

        for m in game.meteors:
            if m.col == self.col:
                if m.bp == HEIGHT:
                    self.hit_sound.rewind()
                    self.hit_sound.play()
                    game.meteors.remove(m)
                    # The astronaut is no longer alive
                    self.alive = False
            
            # Delete the rest of the meteors that leave the board to prevent lagging
            elif m.row > NUM_ROWS:
                game.meteors.remove(m)
                
        for p in game.powerups: 
            if p.col == self.col:
                if p.bp >= HEIGHT:
                    self.powerup_sound.rewind()
                    self.powerup_sound.play()
                    game.powerups.remove(p)
                    # Flag score is reset to 0 to prevent game speed from increasing right away
                    game.flag_score = 0
                    # Game speed is reset to 0
                    game.speed = 0
                    
            elif p.row > NUM_ROWS:
                game.powerups.remove(s)
                    
        # Game scores will be appended to the score list
        score_list.append(game.score)

    # Display the astronaut sprite depending on arrow keys pressed and released
    def display(self):
        if self.dir == CENTER:
            image(self.img, self.col * self.img_w, self.row * self.img_h, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == RIGHT:
            image(self.img, self.col * self.img_w, self.row * self.img_h, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, (self.frame + 2) * self.img_w, self.img_h) 
        elif self.dir == LEFT:
            image(self.img, self.col * self.img_w, self.row * self.img_h, self.img_w, self.img_h, (self.frame + 2) * self.img_w, 0, (self.frame + 3) * self.img_w, self.img_h)
             
        self.check_game()

    
class Game:
    def __init__(self):
        # Game speed is initially set to 0
        self.speed = 0
        self.score = 0
        # Attribute that is similar to score, but will be reset to 0 when a powerup is collected to leave some time between collecting a powerup and increasing game speed
        self.flag_score = 0
        # UP key is used to start the game and DOWN key is used to read instructions; instructions can only be accessed at the beginning of the game
        self.key_handler = {UP:False, DOWN:False}
        
        # Randomly choosing the background image of the game; 4 different images are available
        self.back_img = loadImage(path + "/images/" + "space" + str(random.randint(1,4)) + ".png")
        
        # The background music of the game; it will start playing right away
        self.music = player.loadFile(path + "/sounds/background_music.mp3")
        self.music.rewind()
        self.music.loop()
        
        # Instantiate the astronaut
        self.astronaut = Astronaut("astronaut.png", 70, 70)

        # Oxygen list that will hold all instantiated oxygens
        self.oxygens = []
        # Instantiate the first oxygen
        self.oxygen = Oxygen(0, random.randint(0, NUM_COLS-1), "oxygen.png", 70, 70)
        self.oxygens.append(self.oxygen)
        
        # Gold oxygen list that will hold all instantiated gold oxygens
        self.golds = []
        self.gold = Gold(0, random.randint(0, NUM_COLS-1), "gold.png", 70, 70)               
        self.golds.append(self.gold)
        
        # Meteor list that will hold all instantiated meteors
        self.meteors = []
        # Meteors images are longer than other object images to create a sense that meteors are falling down faster
        self.meteor = Meteor(0, random.randint(0, NUM_COLS-1), "meteor.png", 70, 100)
        self.meteors.append(self.meteor)
        
        # Powerup list that will hold all instantiated powerups
        self.powerups = [] 
        
        # List that will hold 40 randomly chosen numbers between 25 and 800 that will be used to decide when powerups will be instantiated; a powerup will be instantiated whenever the game score is equal to the random numbers
        self.p_choice = []
        
        # Choosing numbers randomly in 3 separate parts to prevent from numbers being chosen in a cluster
        for i in range(5):
            self.p_choice.append(random.randint(25, 100)) 
        
        for i in range(15):
            self.p_choice.append(random.randint(101, 400))
            
        for i in range(20):
            self.p_choice.append(random.randint(401, 800))
                
    # Method for generating new objects
    def generate(self):
        # Instantiating new oxygens whenever the previous oxygen is at row 3 or below
        if self.oxygen.row >= 3:
            self.oxygen2 = Oxygen(0, random.randint(0, NUM_COLS-1), "oxygen.png", 70, 70)
            self.oxygens.append(self.oxygen2)
            # Assigning the second oxygen to the first to continue the process
            self.oxygen = self.oxygen2
            
        # Instantiating 1 gold oxygen for every 15 regular oxygens and when the previous gold oxygen is below row 7
        if len(self.oxygens)%15 == 0 and self.gold.row > 7:
            self.gold2 = Gold(0, random.randint(0, NUM_COLS-1), "gold.png", 70, 70)             
            self.golds.append(self.gold2)
            self.gold = self.gold2
    
        # Instantiating new meteors whenever the previous meteor is at row 4 or below; less meteors than oxygens will be displayed at a time
        if self.meteor.row >= 4:
            self.meteor2 = Meteor(0, random.randint(0, NUM_COLS-1), "meteor.png", 70, 100)
            self.meteors.append(self.meteor2)
            self.meteor = self.meteor2            
        
        # Instantiating new powerups whenever the game score is equal to a number in the random number list and when the game speed is higher than 0
        if self.score in self.p_choice and self.speed > 0: 
            n = self.score
            self.powerup = Powerup(0, random.randint(0, NUM_COLS-1), "powerup.png", 70, 70)
            self.powerups.append(self.powerup)
            # Remove the number from the list after a powerup has been instantiated to prevent powerups from being instantiated continuously
            self.p_choice.remove(n)

    def display(self):
        image(self.back_img, 0, 0, WIDTH, HEIGHT)  

        self.nameFont = loadFont("Silom-48.vlw")
        textFont(self.nameFont)
        fill (10, 150, 255)
        text("Space", 95, 70)
        text("Survival", 68, 130)
        
        # Displaying the opening background of the game
        if self.key_handler[DOWN] == False:
            fill(255, 255, 255)
            textSize(20)
            text("Press UP to START", 80, 270)
            text("Press DOWN for INSTRUCTIONS", 15, 310)
        
        # The game has begun
        if self.key_handler[UP] == True:
            
            if self.astronaut.alive == False:                
                self.music.pause()
                image(self.back_img, 0, 0, WIDTH, HEIGHT) 
                # Showing the ending text
                self.ending_text()
                return
            
            self.generate()
             
             # Game speed will be incremented whenever the flag score is greater or equal to 15; the flag score will be reset to 0 when a powerup is caught so that the game speed doesn't increase right away
            if self.flag_score >= 15:
                self.speed += 0.003

            image(self.back_img, 0, 0, WIDTH, HEIGHT)        
                                    
            for o in self.oxygens:
                o.display()
        
            for g in self.golds:
                g.display()
    
            for m in self.meteors:
                m.display()    
                
            for p in self.powerups: 
                p.display()   
            
            self.astronaut.display()
    
            # Display the score at the top right corner
            textSize(20)
            fill(255, 255, 255)
            text("Score: " + str(self.score), WIDTH-120, 25)   

        elif self.key_handler[DOWN] == True:
            self.instruction()
    
    # Method containing game instructions
    def instruction(self):
        powerup = Powerup(0, random.randint(0, NUM_COLS-1), "powerup.png", 70, 70)
    
        # Showing the user the different objects present in the game so that it will be easier to understand
        image(self.astronaut.img, 31, 180, 50, 50, 0, 0, 70, 70)  
        image(self.oxygen.img, 91, 180, 50, 50)
        image(self.gold.img, 151, 180, 50, 50)
        image(self.meteor.img, 211, 165, 50, 70)
        image(powerup.img, 271, 180, 50, 50)

        fill(255, 255, 255)
        textSize(15)
        text("You are an astronaut.", 85, 280)  
        text("Collect oxygen bubbles to earn points.", 20, 310)
        text("Gold bubbles are worth ten times", 35, 340)
        text("more than normal bubbles.", 67, 360)
        text("Dodge meteors to survive.", 70, 390) 
        text("Speed of falling objects will increase", 20, 420) 
        text("as you earn more points.", 77, 440)
        text("Powerups will slow down game speed.", 17, 470)
        text("You will die if you get hit by a meteor.", 18, 500) 
        text("Good luck!", 130, 550) 
        
        textSize(25)
        text("Press UP to START", 59, 620)
      
    # Method containing the ending text that will be displayed when game is over
    def ending_text(self):
        textFont(self.nameFont)
        fill (10, 150, 255)
        text("Space", 95, 70)
        text("Survival", 68, 130)
        
        fill(255, 255, 255)
        textSize(25)
        text("Press UP to RESTART", 44, 620)  
        
        textSize(30)
        text("GAME OVER!", 80, 200)
        
        # Dynamically deciding the horizontal position of score and high score that will change depending on the number of digits
        textSize(20)
        if self.score <= 9:
            W = 130
        elif 10 <= self.score <= 99:
            W = 125
        else:
            W = 120
        text("SCORE: " + str(self.score), W, 250)
        text("HIGH SCORE: " + str(max(score_list)), W-30, 280)
      
      
      
game = Game()



def setup():
    size(WIDTH, HEIGHT)
    
def draw():
      if frameCount%(max(1, int(8 - game.speed)))==0 or frameCount==1:
        game.display()
        
def keyPressed():
    global game
    if keyCode == LEFT:
        game.astronaut.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.astronaut.key_handler[RIGHT] = True
    elif keyCode == UP:
        # When the UP key is pressed and when the astronaut is not alive, then a new game will be instantiated and the game will restart
        if game.astronaut.alive == False:
            game = Game()
        game.key_handler[UP] = True
    elif keyCode == DOWN:
        game.key_handler[DOWN] = True
    
def keyReleased():
    if keyCode == LEFT:
        game.astronaut.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.astronaut.key_handler[RIGHT] = False
        
        

        
        
