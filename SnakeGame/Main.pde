// Create initial snake
ArrayList<Shape> snake = new ArrayList<Shape>();

// Setup intial box
float box_x = random(width);
float box_y = random(height);
float box_extent = 220;

// Initial position info
float pos_x = 0;
float pos_y = 0;
float previous_pos_x = 0;
float previous_pos_y = 0;

int score = 0;

// Create pure data audio instance
Audio audio = new Audio();
Pd pd = Pd.getInstance(audio);

// Check if x position outside screen and reverse velocity direction
void checkXBounds() {
  float radius =  snake.get(0).rad;
  if (pos_x < radius) {
    pos_x = radius;
    audio.reverseSnakeXDirection();
  } else if (pos_x > width-radius) {
    pos_x = width-radius;
    audio.reverseSnakeXDirection();
  }
}
// Check if y position outside screen and reverse velocity direction
void checkYBounds() {
  float radius =  snake.get(0).rad;
  if (pos_y < radius) {
    pos_y = radius;
    audio.reverseSnakeYDirection();
  } else if (pos_y > height-radius) {
    pos_y = height-radius;
    audio.reverseSnakeYDirection();
  }
}
// Draw new box if needed and update score
void boxUpdate() {
  // Check if snake is in the box
  boolean snake_in_box = snake.get(0).is_snake_in_box(box_x, box_y, box_extent);
  // Change the color of the box if the snake is in it
  if (snake_in_box == true) {
    box_x = random(width);
    box_y = random(height);
    square(box_x, box_y, box_extent);
    score += 1;
  } else {
  }
}
// Draw the snake
void drawSnake() {
  // Add a new part to the snake with current position coordinates
  while (snake.size() < 20) {
    snake.add(new Shape(pos_x, pos_y, previous_pos_x, previous_pos_y));
  }
  // Draw each part of the snake
  for (int i = 0; i < snake.size(); i++) {
    Shape snake_part = snake.get(i);
    snake_part.show(i, snake.size());
  }
  // Remove the last part of the snake so new part gets added
  snake.remove(0);
}

void setup() {
  pd.start();
  fullScreen();
  background(0, 0, 0);
  colorMode(RGB, 255, 255, 255);
}

void draw() {
  // Re-draw background (canvas)
  background(0);

  // Set previous position coordinates
  previous_pos_x = pos_x;
  previous_pos_y = pos_y;

  drawSnake();

  checkXBounds();
  checkYBounds();

  square(box_x, box_y, box_extent);

  // Update the position with current velocity
  pos_x += audio.getSnakeDirection().x * audio.getSnakeSpeed();
  pos_y += audio.getSnakeDirection().y * audio.getSnakeSpeed();

  boxUpdate();
  textSize(128);
  text(score, width/2, height/2);
}

public void dispose() {
  pd.stop();
  super.dispose();
}
