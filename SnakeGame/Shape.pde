import com.pdplusplus.*;
class Shape {
  PVector pos;
  PVector previous_pos;
  float rad;
  Shape(float pos_x, float pos_y, float previous_pos_x, float previous_pos_y) {
    pos = new PVector(pos_x, pos_y);
    previous_pos = new PVector(previous_pos_x, previous_pos_y);
    rad = 30;
  }
  void show(int index, int size) {
    float gradient = map(index, 0, size - 1, 0, 255);
    stroke(gradient, 255, gradient);
    strokeWeight(rad);
    line(pos.x, pos.y, previous_pos.x, previous_pos.y);
  }
  boolean is_snake_in_box(float coord_x, float coord_y, float extent) {
    float upper_bound_x = coord_x + extent;
    float lower_bound_x = coord_x;
    float upper_bound_y = coord_y + extent;
    float lower_bound_y = coord_y;
    boolean x_is_in_bounds = pos.x <= upper_bound_x && pos.x >= lower_bound_x;
    boolean y_is_in_bounds = pos.y <= upper_bound_y && pos.y >= lower_bound_y;
    if (x_is_in_bounds && y_is_in_bounds) {
      return true;
    } else {
      return false;
    }
  }
}
