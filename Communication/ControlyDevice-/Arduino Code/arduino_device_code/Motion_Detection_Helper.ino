float measure(int trigger, int echoing) {
  long duration, distance;

  digitalWrite(trigger, LOW);
  delayMicroseconds(2);
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);

  duration = pulseIn(echoing, HIGH);
  distance = (duration/2) / 29.1;

  return distance;
}