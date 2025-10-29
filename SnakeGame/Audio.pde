import com.pdplusplus.*;

class Audio extends PdAlgorithm {
  // Decibel detection
  Envelope env = new Envelope();
  // Pitch detection
  Sigmund sigmund = new Sigmund();
  // Utility for pitch info
  SigmundPackage sp = new SigmundPackage();

  // Intial values
  double decibels = 0;
  double minDecibels = 100;
  double maxDecibels = 0;
  double minPitch = 100;
  double maxPitch = 0;
  double pitch = 0;
  float speed = 0;
  float angle = 0;
  PVector direction = new PVector(0, 0);

  void runAlgorithm(double in1, double in2) {
    // Mic input
    double input = (in1 + in2) * .5;
    // Measure decibels
    decibels = env.perform(input);
    // Measure pitch
    sp = sigmund.perform(input);
    pitch = sp.pitch;
    // Clip to max and minimum parameters detected
    if (decibels < minDecibels && decibels > 0) {
      minDecibels = decibels;
    }
    if (decibels > maxDecibels) {
      maxDecibels = decibels;
    }
    if (pitch < minPitch && pitch > 0) {
      minPitch = pitch;
    }
    if (pitch > maxPitch) {
      maxPitch = pitch;
    }
    // Set pitch to snake direction and set decibels to snake speed
    if (minDecibels != maxDecibels && minPitch != maxPitch && pitch >= 0) {
      speed = map((float)decibels, (float)minDecibels, (float)maxDecibels, 0, 10);
      angle = map((float)pitch, (float)minPitch, (float)maxPitch, 0, TWO_PI);
    }
    direction.x = cos(angle);
    direction.y = sin(angle);
    outputL = outputR = 0;
  }
  synchronized double getSnakeSpeed() {
    return speed;
  }
  synchronized PVector getSnakeDirection() {
    return direction;
  }
  synchronized void reverseSnakeXDirection() {
    direction.x *= -1;
  }
  synchronized void reverseSnakeYDirection() {
    direction.y *= -1;
  }
  void free() {
    Envelope.free(env);
    Sigmund.free(sigmund);
  }
}
